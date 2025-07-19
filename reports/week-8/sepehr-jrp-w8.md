Sepehr Akbari<br>
James Rocco Project '25<br>
Jul 18th, 2025

# Report: Week 8

### Week 7-9 goals (per proposal):

- Additional, unanticipated work of improved modeling
- Completing paper draft.

### **Accomplishments**

This week I focused on finishing up the Bayesian models:

- I first started by using a Monte Carlo method to sample from various distributions, defining effects and priors of the model which were US states. This model used a logit function to compute the likelihood.
- My first iteration was to take a more clear and simpler approach, looking at the data as an experiment. Each trial is a total number of colleges in a state, and the success is the number of colleges that closed. I used a binomial distribution to model this, with no hyper-priors. I then simply computed the posteriors for further analysis.
- This model turned out to be much more effective, so the next step was to add more layers. I sampled alpha and beta variables from a gamma distribution to capture the uncertainty in the model more effectively, and to obtain the probabilities from a $\Beta(\alpha, \beta)$ distribution. That got even better results.
- As the last step, I incorporated even more priors and layers, adding more complexity to the model. I used a $x$ random variable from a normal distribution, with its $\mu$ and $\sigma$ sampled from a normal distribution, and a $\sigma$ sampled from an inverse gamma distribution. To compute $\alpha$ and $\beta$, I used a function $g(n) = e^2$ with an additional scaler $k$ sampled from a half-normal distribution. This final model was able to capture the uncertainty in the data much better, and I was able to compute the posteriors for each state.

I also worked more on the linear discriminant analysis model, using coefficients to explain the model. All this along with other experiments regarding regions will be summed up in a summary paper in the coming week.