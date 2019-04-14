# Simple ITA test to compare the python solution
# install.packages("trendchange")
library(trendchange)

# generate the signal data
x <- 0:99
noise <- rnorm(100)
signal <- x + noise
innovtrend(signal)