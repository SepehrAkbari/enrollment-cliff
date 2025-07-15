import pymc as pm
import pandas as pd
import numpy as np
import arviz as az
import matplotlib.pyplot as plt
import pytensor as pt

df = pd.read_csv('full_data_bhm1.csv', keep_default_na=False, na_values=[''])
region_unemployment_rates = df.groupby('region')['stateUnemploymentRate'].mean()
df['regionUnemploymentRate'] = df['region'].map(region_unemployment_rates).round(1)

years = [i for i in range(2020, 2026)]
states = df['state'].unique()
regions = df['region'].unique()

analysis_df = pd.read_csv('analysis_results.csv')

lda_results = analysis_df[[
    'name', 'lda_reason_component_1', 'lda_reason_component_2',
    'lda_reason_component_3', 'lda_reason_component_4', 
    'lda_reason_component_5', 'lda_reason_component_6'
]].copy()

cluster_results = analysis_df[['name', 'kmeans_cluster']].copy()

lda_results.rename(columns={
    'lda_reason_component_1': 'lda_class_0',
    'lda_reason_component_2': 'lda_class_1',
    'lda_reason_component_3': 'lda_class_2',
    'lda_reason_component_4': 'lda_class_3',
    'lda_reason_component_5': 'lda_class_4',
    'lda_reason_component_6': 'lda_class_5'
}, inplace=True)

cluster_results.rename(columns={'kmeans_cluster': 'cluster_label'}, inplace=True)

lda_results['state'] = df['state']
lda_results['region'] = df['region']
cluster_results['state'] = df['state']
cluster_results['region'] = df['region']

lda_results.drop(columns=['name'], inplace=True)
cluster_results.drop(columns=['name'], inplace=True)

state_data = []
for year in years:
    for state in states:
        state_df_temp = df[df['state'] == state]
        total = state_df_temp[f'totalByState_{year}'].sum()
        closed = state_df_temp[f'closedByState_{year}'].sum()
        if total > 0:
            # endowment_median = state_df_temp['endowmentMedian'].replace(-1, state_df_temp['endowmentMedian'].median())
            lda_row = lda_results[lda_results['state'] == state].iloc[0]
            lda_score = max(lda_row[['lda_class_0', 'lda_class_1', 'lda_class_2']].values)  # Adjust class names
            cluster_label = cluster_results[cluster_results['state'] == state]['cluster_label'].iloc[0]
            state_data.append({
                'state': state,
                'year': year,
                'total': total,
                'closed': closed,
                # 'endowmentMedian': endowment_median.mean(),
                # 'stateBirthRate': state_df_temp['stateBirthRate'].mean(),
                # 'stateUnemploymentRate': state_df_temp['stateUnemploymentRate'].mean(),
                # 'hasReligionAffiliation': state_df_temp['hasReligionAffiliation'].any(),
                # 'locationType': state_df_temp['locationType'].mode()[0],
                'lda_score': lda_score,
                'cluster_label': cluster_label
            })

state_df = pd.DataFrame(state_data)

# location_type_map = {loc: i for i, loc in enumerate(state_df['locationType'].unique())}
# location_type_idx = [location_type_map[loc] for loc in state_df['locationType']]
cluster_map = {cl: i for i, cl in enumerate(sorted(state_df['cluster_label'].unique()))}
cluster_idx = [cluster_map[cl] for cl in state_df['cluster_label']]

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
        
        # Cluster effects
        sigma_cluster = pm.HalfNormal('sigma_cluster', sigma=2)
        cluster_effects = pm.Normal('cluster_effects', mu=0, sigma=sigma_cluster, shape=len(cluster_map))
        
        # Covariate effects
        # beta_endowment = pm.Normal('beta_endowment', mu=0, sigma=5)
        # beta_birth = pm.Normal('beta_birth', mu=0, sigma=5)
        # beta_unemp = pm.Normal('beta_unemp', mu=0, sigma=5)
        # beta_religion = pm.Normal('beta_religion', mu=0, sigma=5)
        sigma_lda = pm.HalfNormal('sigma_lda', sigma=2)
        # sigma_loc = pm.HalfNormal('sigma_loc', sigma=2)
        # location_effects = pm.Normal('location_effects', mu=0, sigma=sigma_loc, shape=len(location_type_map))
        
        logit_p = (mu_global + 
                  region_effects[state_region_idx] + 
                  state_effects + 
                  cluster_effects[cluster_idx] + 
                  # beta_endowment * pm.math.log1pexp(state_df['endowmentMedian']) + 
                  # beta_birth * pm.math.log1pexp(state_df['stateBirthRate'].values) + 
                  # beta_unemp * pm.math.log1pexp(state_df['stateUnemploymentRate'].values) + 
                  # beta_religion * state_df['hasReligionAffiliation'].astype(int).values + 
                  # location_effects[location_type_idx] + 
                  state_df['lda_score'].values * sigma_lda)
        
        p = pm.Deterministic('p', pm.math.sigmoid(logit_p))
        y = pm.Binomial('y', n=state_df['total'], p=p, observed=state_df['closed'])
        
        trace = pm.sample(8000, tune=2000, target_accept=0.9, return_inferencedata=True, random_seed=42, progressbar=True)

az.to_netcdf(trace, 'good_bhm_traces/analysis_8k_2k_4.nc')