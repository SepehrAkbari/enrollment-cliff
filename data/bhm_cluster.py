import pymc as pm
import pandas as pd
import numpy as np
import arviz as az
import pytensor

df = pd.read_csv('full_data_bhm1.csv', keep_default_na=False, na_values=[''])

years = [i for i in range(2020, 2026)]
states = df['state'].unique()
regions = df['region'].unique()

state_data = []
region_data = []
for year in years:
    for state in states:
        state_df = df[df['state'] == state]
        total = state_df[f'totalByState_{year}'].sum()
        closed = state_df[f'closedByState_{year}'].sum()
        if total > 0:
            state_data.append({'state': state, 'year': year, 'total': total, 'closed': closed})
    for region in regions:
        region_df = df[df['region'] == region]
        total = region_df[f'totalByRegion_{year}'].sum()
        closed = region_df[f'closedByRegion_{year}'].sum()
        if total > 0:
            region_data.append({'region': region, 'year': year, 'total': total, 'closed': closed})

state_df = pd.DataFrame(state_data)
region_df = pd.DataFrame(region_data)

with pytensor.config.change_flags(exception_verbosity='high'):
    with pm.Model() as model:
        mu_global = pm.Normal('mu_global', mu=0, sigma=10)
        sigma_region = pm.HalfNormal('sigma_region', sigma=5)
        region_effects = pm.Normal('region_effects', mu=0, sigma=sigma_region, shape=len(regions))
        
        region_idx_map = {region: i for i, region in enumerate(regions)}
        
        state_to_region = dict(zip(df['state'], df['region']))
        state_region_idx = [region_idx_map[state_to_region[state_df.loc[i, 'state']]] for i in range(len(state_df))]
        
        sigma_state = pm.HalfNormal('sigma_state', sigma=5)
        state_effects = pm.Normal('state_effects', mu=region_effects[state_region_idx], sigma=sigma_state, shape=len(state_df))
        
        region_year_idx = []
        for i in range(len(region_df)):
            region = region_df.loc[i, 'region']
            year = region_df.loc[i, 'year']
            region_year_idx.append(years.index(year) * len(regions) + region_idx_map[region])
        region_year_idx = np.array(region_year_idx)
        
        logit_p_regions = mu_global + region_effects[region_year_idx]
        logit_p_states = mu_global + state_effects
        
        p_regions = pm.Deterministic('p_regions', pm.math.sigmoid(logit_p_regions))
        p_states = pm.Deterministic('p_states', pm.math.sigmoid(logit_p_states))
        
        y_states = pm.Binomial('y_states', n=state_df['total'], p=p_states, observed=state_df['closed'])
        y_regions = pm.Binomial('y_regions', n=region_df['total'], p=p_regions, observed=region_df['closed'])

        print('sampling...')
        with model:
            trace = pm.sample(200, tune=100, target_accept=0.9, return_inferencedata=True, random_seed=42, progressbar=True)
            print('sampling done')

print('saving trace...')
az.to_netcdf(trace, 'bhm/trace_bhm_3.nc')
# az.summary(trace)