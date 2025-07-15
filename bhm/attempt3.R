library(stats)
library(here)

df <- read.csv("data.csv")

n_s <- tapply(df$totalByState_2025, df$state, mean)
y_s <- tapply(rowSums(df[, grep("closedByState_", names(df))], na.rm = TRUE), df$state, sum)
# Justify: n_s takes the 2025 total per state (assuming one row per state). y_s sums closures across years.
# Note: Total y_s should equal 65; if not, data has duplicates—check below.

# Validate total closures
total_closures <- sum(y_s)
if (total_closures != 65) {
  warning(paste("Total closures =", total_closures, "exceeds expected 65. Check for duplicates in df."))
  # Justify: Flags overcounting. User must verify df structure.
}

states <- names(n_s)

a <- 2
b <- 2

a_post <- a + y_s
b_post <- b + n_s - y_s

post_means <- a_post / (a_post + b_post)
post_vars <- (a_post * b_post) / ((a_post + b_post)^2 * (a_post + b_post + 1))

results <- data.frame(trial = n_s,
                      success = y_s,
                      a_posterior = a_post,
                      b_posterior = b_post,
                      mean_posterior = round(post_means, 8),
                      variance_posterior = round(post_vars, 8))
print(results)