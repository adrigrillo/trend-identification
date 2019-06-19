require(dplyr)
require(configr)
require(tibble)

print('Reading .ini\'s.')

setwd('/Users/henrymauranen/PycharmProjects/trend-identification/data/synthetic/')

files <- data.frame(file_name=list.files('./'))
files$SNR <- sapply(files$file_name, function(x) {read.config(paste0('./',x))$noise$signal_to_noise})

ts_list <- sapply(as.character(files$file_name), function(x) {
  print(x)
  conf = read.config(paste0('./',x))
  return(c(name=x,
           function.=conf$trend$function_form,
           SNR=as.numeric(conf$noise$signal_to_noise),
           a=ifelse(is.null(conf$trend$a),0,as.numeric(conf$trend$a)),
           b=ifelse(is.null(conf$trend$b),0,as.numeric(conf$trend$b)),
           c=ifelse(is.null(conf$trend$c),0,as.numeric(conf$trend$c))
           ))
})

ts_list <- data.frame(t(ts_list))
ts_list$name <- gsub('\\.ini','',ts_list$name)

print('Reading results.')

setwd('/Users/henrymauranen/PycharmProjects/trend-identification/results/')

results <- read.csv('trend_estimation_*_12-38-37-161064.csv',row.names=1,header=F)
results <- data.frame(t(results))
colnames(results)[1] <- 'name'

ts_list <- left_join(ts_list, results, by='name')
# Coerce to numerics
ts_list[3:length(ts_list)] <- lapply(ts_list[3:length(ts_list)], as.character)
ts_list[3:length(ts_list)] <- lapply(ts_list[3:length(ts_list)], as.numeric)
# Names to characters
ts_list[1:2] <- lapply(ts_list[1:2], as.character)
colnames(ts_list)[7:12] <- c('EMD_loss','HP_Filter_loss','Splines_loss','Theil_loss','Regression_loss','LOWESS_loss') 

print('Calculating aggregations.')
# -----------

# Losses by pure SNR
SNR_loss <- ts_list %>% 
  select(SNR, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>% 
  group_by(SNR) %>% 
  summarise_all(funs(median))

# Losses by SNR, function_form
function_snr_loss <- ts_list %>% 
  select(function., SNR, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>% 
  group_by(SNR, function.) %>% 
  summarise_all(funs(median))

# Aggregates on effect if a, b, c, grouped by functions
a_loss <- ts_list %>% 
  select(function., a, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>%
  group_by(function.,a) %>%
  summarise_all(funs(median))

b_loss <- ts_list %>% 
  select(function., c, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>%
  group_by(function.,c) %>%
  summarise_all(funs(median))

c_loss <- ts_list %>% 
  select(function., c, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>%
  group_by(function.,c) %>%
  summarise_all(funs(median))

# Function loss
function_loss <- ts_list %>% 
  select(function., EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>%
  group_by(function.) %>%
  summarise_all(funs(median))

# Show best method for each function
best_methods <- data.frame(
  function.=function_loss$function.,
  best=colnames(function_loss)[apply(-function_loss[-1],1,function(x) which(x==max(x)))+1]
)

# Build ranks w.r.t. functions
function_ranks <- data.frame(apply(function_loss[-1], 1, rank))
colnames(function_ranks) <- function_loss$function.
function_ranks <- data.frame(t(function_ranks))

# Ranks w.r.t. SNR
snr_ranks <- data.frame(apply(SNR_loss[-1], 1, rank))
colnames(snr_ranks) <- SNR_loss$SNR
snr_ranks <- data.frame(t(snr_ranks))

# With both
function_snr_ranks <- data.frame(apply(function_snr_loss[c(-1,-2)], 1, rank))
function_snr_ranks <- data.frame(t(function_snr_ranks))
function_snr_ranks$function. <- function_snr_loss$function.
function_snr_ranks$SNR <- function_snr_loss$SNR
function_snr_ranks <- function_snr_ranks %>% select(function., SNR, everything())

# Aggregate/sum/whatever the ranks

# ------------
print('Done!')

