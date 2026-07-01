'''
Two layer bayesian hierarchical model
'''

import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt


df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

n_s_state = df.groupby('state')['totalByState_2020'].mean().round(0).astype(int)
y_s_state = df['state'].value_counts()

n_s_region = df.groupby('region')['totalByRegion_2020'].mean().round(0).astype(int)
y_s_region = df['region'].value_counts()

all_states = pd.Index(list(n_s_state.index) + list(y_s_state.index)).unique()
n_s_state = n_s_state.reindex(all_states)
y_s_state = y_s_state.reindex(all_states)

all_regions = pd.Index(list(n_s_region.index) + list(y_s_region.index)).unique()
n_s_region = n_s_region.reindex(all_regions)
y_s_region = y_s_region.reindex(all_regions)

def runModel(n_s, y_s):
    with pt.config.change_flags(exception_verbosity='high'):
        with pm.Model() as model:
            # alpha ~ Gamma(0.01, 0.01)
            a_s = pm.Gamma('a_s', alpha=0.01, beta=0.01, shape=len(n_s))
            # beta ~ Gamma(0.01, 0.01)
            b_s = pm.Gamma('b_s', alpha=0.01, beta=0.01, shape=len(n_s))

            # p_s ~ Beta(a_s, b_s)
            p_s = pm.Beta('p_s', alpha=a_s, beta=b_s, shape=len(n_s))

            # likelihood ~ Binomial(n_s, p_s)
            y = pm.Binomial('y', n=n_s.values, p=p_s, observed=y_s.values)

            print("sampling model...")

            trace = pm.sample(4000, tune=2000, target_accept=0.95, return_inferencedata=True,
                              random_seed=42, progressbar=True, max_treedepth=15)

    return trace

trace_state = runModel(n_s_state, y_s_state)
trace_region = runModel(n_s_region, y_s_region)

print("simple model convergence: ")
print("rows with r_hat > 1.01:", (az.rhat(trace_state) > 1.01).sum())
print("rows with ess < 100:", (az.ess(trace_state) < 100).sum())
print("rows with ess < 1000:", (az.ess(trace_state) < 1000).sum())
az.to_netcdf(trace_state, 'traces/trace_simple_state.nc')

print("region model convergence: ")
print("rows with r_hat > 1.01:", (az.rhat(trace_region) > 1.01).sum())
print("rows with ess < 100:", (az.ess(trace_region) < 100).sum())
print("rows with ess < 1000:", (az.ess(trace_region) < 1000).sum())
az.to_netcdf(trace_region, 'traces/trace_simple_region.nc')