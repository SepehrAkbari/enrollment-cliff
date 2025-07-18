import pandas as pd
import pymc as pm
import arviz as az
import pytensor as pt

df = pd.read_csv('data.csv', keep_default_na=False, na_values=[''])

n_s = df.groupby('state')['totalByState_2020'].mean().round(0).astype(int)
y_s = df['state'].value_counts()

all_states = pd.Index(list(n_s.index) + list(y_s.index)).unique()
n_s = n_s.reindex(all_states)
y_s = y_s.reindex(all_states)

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