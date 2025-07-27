import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt

df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

a = 2 # alpha in Beta(alpha, beta)
b = 2 # beta in Beta(alpha, beta)

n_s_state = df.groupby('state')['totalByState_2020'].mean().round(0).astype(int)
y_s_state = df['state'].value_counts()
n_s_region = df.groupby('region')['totalByRegion_2020'].mean().round(0).astype(int)
y_s_region = df['region'].value_counts()

all_states = pd.Index(list(n_s_state.index) + list(y_s_state.index)).unique()
all_regions = pd.Index(list(n_s_region.index) + list(y_s_region.index)).unique()

n_s_state = n_s_state.reindex(all_states)
y_s_state = y_s_state.reindex(all_states)
n_s_region = n_s_region.reindex(all_regions)
y_s_region = y_s_region.reindex(all_regions)

a_post_state = a + y_s_state
b_post_state = b + n_s_state - y_s_state
a_post_region = a + y_s_region
b_post_region = b + n_s_region - y_s_region

post_means_state = a_post_state / (a_post_state + b_post_state)
post_vars_state = (a_post_state * b_post_state) / ((a_post_state + b_post_state)**2 * (a_post_state + b_post_state + 1))
post_means_region = a_post_region / (a_post_region + b_post_region)
post_vars_region = (a_post_region * b_post_region) / ((a_post_region + b_post_region)**2 * (a_post_region + b_post_region + 1))

results_state = pd.DataFrame({
    'n_s': n_s_state,
    'y_s': y_s_state,
    'a_post': a_post_state,
    'b_post': b_post_state,
    'post_mean': post_means_state,
    'post_var': post_vars_state
})
results_region = pd.DataFrame({
    'n_s': n_s_region,
    'y_s': y_s_region,
    'a_post': a_post_region,
    'b_post': b_post_region,
    'post_mean': post_means_region,
    'post_var': post_vars_region
})

print(results_state)
print(results_region)