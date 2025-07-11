<!-- <style>body {text-align: justify}</style> -->

Sepehr Akbari<br>
James Rocco Project '25<br>
Jul 11th, 2025

# Report: Week 7

### Week 7-9 goals (per proposal):

- Additional, unanticipated work of improved modeling
- Completing paper draft.

### **Accomplishments**

This week, I primarily focused on trying out different ways, improving the Bayesian Hierarchical Model to improve the convergence of the model and the insights we can get from it. Here is a overview of some of the "successful" things I tried:

**Initial Model**: My initial model was built with: (1) defining the global mean and standard deviations of state and region then defining the effects of each as a normal distribution with the global mean and std. (2) I would then compute the logit of the probability for each, (3) calculate the probability using the sigmoid function, and (4) then use a binomial likelihood to model the observed data. I then (5) took random intercepts as sample. There are a lot of issues with this approach, which I did not realize last week, so I started this week by trying to improve the model.

**Convergence**: I explored the PyMC docs a little and started using the `pm.sample()` function to sample which uses a kind of Monte Carlo Markov Chain sampling method. This was a great starting point, as it showed me just how bad my initial model was *haha*! At this point I had $\hat{r}$ values as bad as 8.0, and ESS values as low as 30-50. I started adding parameters to the `pm.sample()`, first increasing `tune`, then gradually increasing `draws` and `chains`. I also added a `target_accept`. I ran into an unexpected problem at this point. I was seeing improvement in the convergence; the steps were signaling the need to raise `draws` and `chains = 4` was already too high, so at some point I was running out of memory. I tried to use toaster, but I was still not able to run the model. I never knew this was a problem with python that allocates memory automatically!

Thanks to the many people having the same problem, I found the solution was to decrease the number of hierarchical levels in the model rather than tuning the parameters. I decided to (1) define the regions' std and effects (2) map its indices (3) define the states and its indices using it (4) define the states' std and effects (5) and compute logit, probability, and likelihood only for the states. I then wrote a block of code to obtain region probabilities as well, since they are dependent variables. and so, the final version of the model was:

```python
with pt.config.change_flags(exception_verbosity='high'):
    with pm.Model() as model:
        # (1)
        mu_global = pm.Normal('mu_global', mu=0, sigma=10)
        sigma_region = pm.HalfNormal('sigma_region', sigma=5)
        region_effects = pm.Normal('region_effects', mu=0, sigma=sigma_region, shape=len(regions))

        # (2)
        region_idx_map = {region: i for i, region in enumerate(regions)}

        # (3)
        state_to_region = dict(zip(df['state'], df['region']))
        state_region_idx = [region_idx_map[state_to_region[state_df.loc[i, 'state']]] for i in range(len(state_df))]

        # (4)
        sigma_state = pm.HalfNormal('sigma_state', sigma=5)
        state_effects = pm.Normal('state_effects', mu=region_effects[state_region_idx], sigma=sigma_state, shape=len(state_df))

        # (5)
        logit_p = mu_global + state_effects
        p = pm.Deterministic('p', pm.math.sigmoid(logit_p))
        y = pm.Binomial('y', n=state_df['total'], p=p, observed=state_df['closed'])

        # sampling
        trace = pm.sample(8000, tune=2000, target_accept=0.9, return_inferencedata=True, random_seed=42, progressbar=True)
```

**Insights from Model**: Insights taken from this was as expected. Overall low probabilities due to small dataset, but comparatively high in states like Wisconsin, as expected. 

**Adding Covariates**: As a next step I added birth rate, unemployment rate, religion affiliation, and location covariates to the model. The insights are also interesting to look at, and I think they can be well used to asses Grawe's claims!

**Utilizing LDA and Clustering**: Next, I tried to add the LDA and clustering results to the model. Right now that I am writing this report, the code is not working, which is probably a trivial issue, which I will fix soon. The idea is to see if I can find more insights based on the closure reasons, and use clusters as kind of a shortcut.