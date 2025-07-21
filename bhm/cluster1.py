import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt

df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

n_s = df.groupby('region')['totalByRegion_2020'].mean().round(0).astype(int)
y_s = df['region'].value_counts()

all_regions = pd.Index(list(n_s.index) + list(y_s.index)).unique()
n_s = n_s.reindex(all_regions)
y_s = y_s.reindex(all_regions)

with pt.config.change_flags(exception_verbosity='high'):
    with pm.Model() as model:
        # mu ~ N(0, 100)
        mu = pm.Normal('mu', mu=0, sigma=10)
        # sigma ~ InverseGamma(0.01, 0.01)
        sigma = pm.InverseGamma('sigma', alpha=0.01, beta=0.01)

        # x_s ~ N(mu, sigma)
        x_s_raw = pm.Normal('x_s_raw', mu=0, sigma=1, shape=len(n_s))
        x_s = pm.Deterministic('x_s', mu + sigma * x_s_raw)

        # a_s ~ exp(x_s)
        a_s = pm.Deterministic('a_s', pm.math.exp(x_s))
        # b_s ~ exp(x_s * k) where k is:
            # k ~ H(mu, sigma=0.5)
        k = pm.HalfNormal('k', sigma=0.5)
        b_s = pm.Deterministic('b_s', pm.math.exp(x_s * k))

        # p_s ~ Beta(a_s, b_s)
        p_s = pm.Beta('p_s', alpha=a_s, beta=b_s, shape=len(n_s))

        # likelihood ~ Binomial(n_s, p_s)
        y = pm.Binomial('y', n=n_s.values, p=p_s, observed=y_s.values)

        print("sampling multilayer model...")

        trace = pm.sample(4000, tune=2000, target_accept=0.9, return_inferencedata=True, 
                          random_seed=42, progressbar=True, max_treedepth=15)

print("multilayer model convergence: ")
print("rows with r_hat > 1.01:", (az.rhat(trace) > 1.01).sum())
print("rows with ess < 100:", (az.ess(trace) < 100).sum())
print("rows with ess < 1000:", (az.ess(trace) < 1000).sum())
az.to_netcdf(trace, 'traces/trace_multilayer_region.nc')

import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt

df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

n_s = df.groupby('region')['totalByRegion_2020'].mean().round(0).astype(int)
y_s = df['region'].value_counts()

all_regions = pd.Index(list(n_s.index) + list(y_s.index)).unique()
n_s = n_s.reindex(all_regions)
y_s = y_s.reindex(all_regions)

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

        print("sampling simple model...")

        trace = pm.sample(4000, tune=2000, target_accept=0.95, return_inferencedata=True, 
                          random_seed=42, progressbar=True, max_treedepth=15)

print("simple model convergence: ")
print("rows with r_hat > 1.01:", (az.rhat(trace) > 1.01).sum())
print("rows with ess < 100:", (az.ess(trace) < 100).sum())
print("rows with ess < 1000:", (az.ess(trace) < 1000).sum())
az.to_netcdf(trace, 'traces/trace_simple_region.nc')

import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt

df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

n_s = df.groupby('region')['totalByRegion_2020'].mean().round(0).astype(int)
y_s = df['region'].value_counts()

all_regions = pd.Index(list(n_s.index) + list(y_s.index)).unique()
n_s = n_s.reindex(all_regions)
y_s = y_s.reindex(all_regions)

a = 2
b = 2

a_post = a + y_s
b_post = b + n_s - y_s

post_means = a_post / (a_post + b_post)
post_vars = (a_post * b_post) / ((a_post + b_post)**2 * (a_post + b_post + 1))

results = pd.DataFrame({
    'n_s': n_s,
    'y_s': y_s,
    'a_post': a_post,
    'b_post': b_post,
    'post_mean': post_means,
    'post_var': post_vars
})
print(results)