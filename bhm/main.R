library(readr)
library(dplyr)
library(tidyr)
library(rstan)
library(loo)

setwd("/Users/sepehrakbari/Projects/enrollment-cliff/bhm")

df <- read.csv('data.csv', na = c(""))

n_s <- df %>%
  group_by(state) %>%
  summarise(mean_total = mean(totalByState_2025, na.rm = TRUE)) %>%
  mutate(mean_total = as.integer(round(mean_total))) %>%
  tibble::deframe()

y_s <- as.integer(table(df$state))
names(y_s) <- names(table(df$state))

all_states <- unique(c(names(n_s), names(y_s)))

n_s_reindexed <- rep(0L, length(all_states))
names(n_s_reindexed) <- all_states
n_s_reindexed[names(n_s)] <- n_s
n_s <- n_s_reindexed

y_s_reindexed <- rep(0L, length(all_states))
names(y_s_reindexed) <- all_states
y_s_reindexed[names(y_s)] <- y_s
y_s <- y_s_reindexed

stan_code <- "
data {
  int<lower=0> N_states;
  array[N_states] int<lower=0> n_s;
  array[N_states] int<lower=0> y_s;
}
parameters {
  real mu;
  real<lower=0> sigma;
  vector[N_states] x_s_raw;
  vector<lower=0, upper=1>[N_states] p_s;
}
transformed parameters {
  vector[N_states] x_s;
  vector<lower=0>[N_states] alpha_s;
  vector<lower=0>[N_states] beta_s;
  real k = 1.0; 

  for (i in 1:N_states) {
    x_s[i] = mu + sigma * x_s_raw[i];
    alpha_s[i] = exp(x_s[i]);
    beta_s[i] = exp(x_s[i] * k);
  }
}
model {
  // mu ~ N(0, 100)
  mu ~ normal(0, 10);
  // sigma ~ InverseGamma(0.01, 0.01)
  sigma ~ inv_gamma(0.01, 0.01);
  // x_s_raw ~ N(0, 1)
  x_s_raw ~ normal(0, 1);

  // p_s ~ Beta(a_s, b_s)
  p_s ~ beta(alpha_s, beta_s);

  // likelihood ~ Binomial(n_s, p_s)
  y_s ~ binomial(n_s, p_s);
}
"

stan_data <- list(
  N_states = length(all_states),
  n_s = n_s,
  y_s = y_s
)

rstan_options(auto_write = TRUE)
options(mc.cores = parallel::detectCores())

model <- stan_model(model_code = stan_code)

fit <- sampling(
  model,
  data = stan_data,
  iter = 4000,
  warmup = 2000,
  chains = 4,
  control = list(adapt_delta = 0.95, max_treedepth = 15),
  seed = 42
)


draws <- rstan::extract(fit, permuted = FALSE)
rhat_values <- apply(draws, 3, Rhat)
ess_values <- apply(draws, 3, ess_bulk)

cat("rows with r_hat > 1.01:", sum(rhat_values > 1.01), "\n")
cat("rows with ess < 100:", sum(ess_values < 100), "\n")
cat("rows with ess < 1000:", sum(ess_values < 1000), "\n")

# Save trace to NetCDF (ArviZ format equivalent)
# dir.create("traces", showWarnings = FALSE)
saveRDS(fit, "traces/trace2.rds")
