import pymc as pm
import pandas as pd
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import pytensor as pt

df = pd.read_csv('full_data_bhm1.csv', keep_default_na=False, na_values=[''])

years = [i for i in range(2020, 2026)]
states = df['state'].unique()
regions = df['region'].unique()

state_data = []
region_data = []
for year in years:
    for state in states:
        state_df_temp = df[df['state'] == state]
        total = state_df_temp[f'totalByState_{year}'].sum()
        closed = state_df_temp[f'closedByState_{year}'].sum()
        if total > 0:
            state_data.append({'state': state, 'year': year, 'total': total, 'closed': closed})
    for region in regions:
        region_df_temp = df[df['region'] == region]
        total = region_df_temp[f'totalByRegion_{year}'].sum()
        closed = region_df_temp[f'closedByRegion_{year}'].sum()
        if total > 0:
            region_data.append({'region': region, 'year': year, 'total': total, 'closed': closed})

state_df = pd.DataFrame(state_data)
region_df = pd.DataFrame(region_data)

with pt.config.change_flags(exception_verbosity='high'):
    with pm.Model() as model:
        mu_global = pm.Normal('mu_global', mu=0, sigma=10)
        sigma_region = pm.HalfNormal('sigma_region', sigma=5)
        region_effects = pm.Normal('region_effects', mu=0, sigma=sigma_region, shape=len(regions))
        
        region_idx_map = {region: i for i, region in enumerate(regions)}
        state_to_region = dict(zip(df['state'], df['region']))
        state_region_idx = [region_idx_map[state_to_region[state_df.loc[i, 'state']]] for i in range(len(state_df))]
        
        sigma_state = pm.HalfNormal('sigma_state', sigma=5)
        state_effects = pm.Normal('state_effects', mu=region_effects[state_region_idx], sigma=sigma_state, shape=len(state_df))
        
        logit_p = mu_global + state_effects
        p = pm.Deterministic('p', pm.math.sigmoid(logit_p))
        y = pm.Binomial('y', n=state_df['total'], p=p, observed=state_df['closed'])
        
        print("Model defined, starting sampling...")
        trace = pm.sample(8000, tune=2000, target_accept=0.9, return_inferencedata=True, random_seed=42, progressbar=True)
        print("Sampling completed.")

print("Saving trace to NetCDF...")
az.to_netcdf(trace, 'good_bhm_traces/states_8k+_2k_4.nc')
print("Trace saved.")

print("rows with r_hat > 1.01:", (az.rhat(trace) > 1.01).sum())
print("rows with ess < 100:", (az.ess(trace) < 100).sum())
print("rows with ess < 1000:", (az.ess(trace) < 1000).sum())
az.summary(trace)

trace = az.from_netcdf('good_bhm_traces/states_8k+_2k_4.nc')

p_samples = trace.posterior['p'].values  # Shape: (chains, draws, state-years)
state_region_map = [state_to_region[state_df.loc[i, 'state']] for i in range(len(state_df))]
state_year_map = state_df['year'].values

region_year_probs = []
for region in regions:
    for year in years:
        mask = (np.array(state_region_map) == region) & (state_year_map == year)
        if mask.any():
            region_p = p_samples[:, :, mask].mean(axis=2)
            region_year_probs.append({
                'region': region,
                'year': year,
                'mean_probability': region_p.mean(),
                'hdi_2.5%': np.quantile(region_p, 0.025),
                'hdi_97.5%': np.quantile(region_p, 0.975)
            })

region_probs = pd.DataFrame(region_year_probs)

p_samples = trace.posterior['p'].mean(dim=['chain', 'draw'])
state_probs = pd.DataFrame({
    'state': state_df['state'],
    'year': state_df['year'],
    'mean_probability': p_samples,
    'hdi_2.5%': trace.posterior['p'].quantile(0.025, dim=['chain', 'draw']),
    'hdi_97.5%': trace.posterior['p'].quantile(0.975, dim=['chain', 'draw'])
})

region_probs_agg = region_probs.groupby('region').agg({'mean_probability': 'mean', 'hdi_2.5%': 'mean', 'hdi_97.5%': 'mean'}).reset_index()
print(f"aggregated region probabilities:\n\n{region_probs_agg.round(3)}")

state_probs_agg = state_probs.groupby('state').agg({'mean_probability': 'mean', 'hdi_2.5%': 'mean', 'hdi_97.5%': 'mean'}).reset_index()
print(f"aggregated state probabilities:\n\n{state_probs_agg.round(3)}")