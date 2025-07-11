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
        
        trace = pm.sample(4000, tune=2000, target_accept=0.9, return_inferencedata=True, random_seed=42, progressbar=True)

az.to_netcdf(trace, 'bhm/trace_bhm_4.nc')

trace = az.from_netcdf('bhm/trace_bhm_4.nc')

# Derive region-year probabilities by aggregating state probabilities
p_samples = trace.posterior['p'].values  # Shape: (chains, draws, state-years)
state_region_map = [state_to_region[state_df.loc[i, 'state']] for i in range(len(state_df))]
state_year_map = state_df['year'].values

# Create a mapping to 24 region-year combinations
region_year_probs = []
for region in regions:
    for year in years:
        mask = (np.array(state_region_map) == region) & (state_year_map == year)
        if mask.any():
            region_p = p_samples[:, :, mask].mean(axis=2)  # Average over states in region-year
            region_year_probs.append({
                'region': region,
                'year': year,
                'mean_probability': region_p.mean(),
                'hdi_2.5%': np.quantile(region_p, 0.025),
                'hdi_97.5%': np.quantile(region_p, 0.975)
            })

region_probs = pd.DataFrame(region_year_probs)

# Summary and Plots
print("=== Summary Statistics for States ===")
print(az.summary(trace, var_names=['mu_global', 'p'], hdi_prob=0.95))

az.plot_posterior(trace, var_names=['mu_global', 'p'], hdi_prob=0.95)
plt.title("Posterior Distributions of Global Mean and State Probabilities")
plt.tight_layout()
plt.show()

with model:
    ppc = pm.sample_posterior_predictive(trace, var_names=['y'])
az.plot_ppc(az.from_pymc(ppc), observed_rug=True)
plt.title("Posterior Predictive Check: Observed vs Predicted Closures")
plt.tight_layout()
plt.show()

print("\n=== Table of Derived Region-Year Closure Probabilities ===")
print(region_probs.round(3))

az.plot_forest(trace, var_names=['p'], combined=True, hdi_prob=0.95)
plt.title("Forest Plot of State-Specific Closure Probabilities")
plt.tight_layout()
plt.show()