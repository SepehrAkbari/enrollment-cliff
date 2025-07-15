library(stats)
library(here)

df <- read.csv("data.csv")

states <- unique(df$state)
n_s <- tapply(df$totalByStateMean, df$state, mean)  # Trial
y_s <- tapply(df$closedByStateMean, df$state, mean)  # Successes (closure)

# Beta(1,1) for each state
# i tried with Beta(2,2) as well
a <- 1
b <- 1
# Uniform prior, E(theta) = 0.5, and non-informative(?).

# posterior parameters for each state
# (im using Beta(y + 1, n - y + 1) from the slides rather than what we discussed yesterday)
a_post <- a + y_s
b_post <- b + n_s - y_s

# posterior means; E(theta|y) = (a + y)/(a + b + n)
post_means <- a_post / (a_post + b_post)

# posterior variance; var(theta|y) = ab/((a + b)^2 (a + b + 1))
post_vars <- (a_post * b_post) / ((a_post + b_post)^2 * (a_post + b_post + 1))

results <- data.frame(trial = n_s, 
                      success = y_s,
                      a_posterior = a_post, 
                      b_posterior = b_post,
                      mean_posterior = round(post_means,8), 
                      variance_posterior = round(post_vars,8))
print(results)