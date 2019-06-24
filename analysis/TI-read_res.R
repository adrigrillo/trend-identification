require(dplyr)
require(configr)
require(tibble)
require(reshape2)
require(ggplot2)

print('Reading .ini\'s.')

setwd('../data/synthetic/')

files <- data.frame(file_name=list.files('./'))

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

setwd('../../results/')

results <- read.csv('trend_estimation___11-18-24-971788.csv',row.names=1,header=F)
results <- data.frame(t(results))
colnames(results)[1] <- 'name'

ts_list <- left_join(ts_list, results, by='name')
# Coerce to numerics
ts_list[3:length(ts_list)] <- lapply(ts_list[3:length(ts_list)], as.character)
ts_list[3:length(ts_list)] <- lapply(ts_list[3:length(ts_list)], as.numeric)
# Names to characters
ts_list[1:2] <- lapply(ts_list[1:2], as.character)
colnames(ts_list)[7:12] <- c('EMD_loss','HP_Filter_loss','Splines_loss','Theil_loss','Regression_loss','LOWESS_loss') 


ts_list <- na.omit(ts_list)

print('Calculating aggregations.')
setwd('../analysis/')
dir.create('./results/', showWarnings=F)
setwd('./results/')
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
write.csv(best_methods, file = "best_methods.csv")

# Build ranks w.r.t. functions
function_ranks <- data.frame(apply(function_loss[-1], 1, rank))
colnames(function_ranks) <- function_loss$function.
function_ranks <- data.frame(t(function_ranks))
write.csv(function_ranks, file = "function_ranks.csv")

# Ranks w.r.t. SNR
snr_ranks <- data.frame(apply(SNR_loss[-1], 1, rank))
colnames(snr_ranks) <- SNR_loss$SNR
snr_ranks <- data.frame(t(snr_ranks))
write.csv(snr_ranks, file = "snr_ranks.csv")

# With both
function_snr_ranks <- data.frame(apply(function_snr_loss[c(-1,-2)], 1, rank))
function_snr_ranks <- data.frame(t(function_snr_ranks))
function_snr_ranks$function. <- function_snr_loss$function.
function_snr_ranks$SNR <- function_snr_loss$SNR
function_snr_ranks <- function_snr_ranks %>% select(function., SNR, everything())
write.csv(function_snr_ranks, file = "function_snr_ranks.csv")

# Aggregate/sum/whatever the ranks


# Plots
## SNR v loss
SNR_summaries <- ts_list %>% 
     select(SNR, EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>% 
     group_by(SNR) %>% 
     summarise_all(funs(median,sd,IQR))

SNR_summaries_melt <- melt(SNR_summaries,id.vars=c('SNR'))

ggplot(SNR_summaries_melt %>% filter(grepl('\\.*median',variable)), aes(x=SNR, y=value, color=variable)) + 
  geom_line() + 
  theme_minimal()
ggsave('./SNR_losses.png')

# Function v loss

function_summaries <- ts_list %>% 
  select(function., EMD_loss, HP_Filter_loss, Splines_loss, Theil_loss, Regression_loss, LOWESS_loss) %>%
  group_by(function.) %>%
  summarise_all(funs(median,sd,IQR))

function_summaries_melt <- melt(function_summaries,id.vars=c('function.'))

function_melt <- ts_list %>%
  select(name, function., contains('loss')) %>%
  melt(id.vars=c('function.','name')) %>%
  group_by(function.,variable)

ggplot(function_melt %>% filter(grepl('synth\\.*', name)) %>% filter(!(abs(value - median(value)) > sd(value))), aes(x=function., y=value, color=variable)) +
  geom_boxplot() +
  theme_minimal() +
  facet_wrap(~function., scales='free')
ggsave('./synthetic_func_loss.png')

ggplot(function_melt %>% filter(!grepl('synth\\.*', name)), aes(x=function., y=value, color=variable)) +
  geom_boxplot() +
  theme_minimal() +
  facet_wrap(~function., scales='free')
ggsave('./pseudoreal_func_loss.png')

coef_melt <- ts_list %>%
  select(name, function., a,b,c, contains('loss')) %>%
  filter(grepl('synth\\.*', name)) %>%
  melt(id.vars=c('function.','a','b','c','name')) %>%
  group_by(function.,name,variable)


dir.create('./abc-losses', showWarnings=F)
setwd('./abc-losses/')

for (var in unique(coef_melt$variable)) {
  print(var)
  plt <- ggplot(coef_melt %>% ungroup() %>% filter(variable == var) %>% select(function.,a,value) %>% group_by(function.,a) %>% summarize_all(funs(median)), aes(x=a, y=value)) +
    geom_line() +
    facet_wrap(~function., scales='free')
  ggsave(paste0('./',var,'_a.png'))
  
  plt <- ggplot(coef_melt %>% ungroup() %>% filter(variable == var, grepl('\\.*b\\.*',function.)) %>% select(function.,b,value) %>% group_by(function.,b) %>% summarize_all(funs(median)), aes(x=b, y=value)) +
    geom_line() +
    facet_wrap(~function., scales='free')
  ggsave(paste0('./',var,'_b.png'))
  
  plt <- ggplot(coef_melt %>% ungroup() %>% filter(variable == var, grepl('\\.*c\\.*',function.)) %>% select(function.,c,value) %>% group_by(function.,c) %>% summarize_all(funs(median)), aes(x=c, y=value)) +
    geom_line() +
    facet_wrap(~function., scales='free')
  ggsave(paste0('./',var,'_c.png'))
}

# ------------
# Trend detection results

setwd('../..')

setwd('../data/synthetic/')

# Reset ts_list.
files <- data.frame(file_name=list.files('./'))

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

setwd('../../results/')

results <- read.csv('trend_detection___16-7-23-536768.csv',row.names=1,header=F)
results <- data.frame(t(results))
colnames(results)[1] <- 'name'

# Reads results columns excluding the name and outputs the first true/false in the tuple
chars <- apply(results[,-1], 2, function(x) { return(unlist(strsplit(gsub('\\(|\\)', '', as.character(x)), ','))) } )
bools <- lapply(chars, as.logical)
bools <- lapply(bools, na.omit)
results[,-1] <- data.frame(bools)

ts_list <- left_join(ts_list, results, by='name')
# Coerce to numerics
ts_list[3:6] <- lapply(ts_list[3:length(ts_list)], as.character)
ts_list[3:6] <- lapply(ts_list[3:length(ts_list)], as.numeric)
# Names to characters
ts_list[1:2] <- lapply(ts_list[1:2], as.character)

ts_list <- na.omit(ts_list)
ts_list$truth <- !grepl('x\\*\\*0',ts_list$function.)

success_rates <- ts_list %>% 
  select(SNR,ITA,MK,Regression,Theil,truth) %>% 
  mutate(ITA_success=ITA == truth,
         MK_success=MK == truth,
         Reg_success=Regression == truth,
         Theil_success=Theil == truth) %>% 
  group_by(SNR) %>% 
  summarize_all(funs(mean)) %>%
  select(SNR,ITA_success,MK_success,Reg_success,Theil_success)

success_rates_melt <- melt(success_rates, id.vars = c('SNR'))

ggplot(success_rates_melt, aes(x=SNR,y=value, color=variable)) +
  geom_line()

pos_rates <- ts_list %>% 
  select(SNR,ITA,MK,Regression,Theil,truth) %>% 
  filter(!truth) %>%
  mutate(ITA_FP=ITA == TRUE & truth == FALSE,
         MK_FP=MK == TRUE & truth == FALSE,
         Reg_FP=Regression == TRUE & truth == FALSE,
         Theil_FP=Theil == TRUE & truth == FALSE) %>% 
  group_by(SNR) %>% 
  summarize_all(funs(mean)) %>%
  select(SNR,ITA_FP,MK_FP,Reg_FP,Theil_FP)

pos_rates_melt <- melt(pos_rates, id.vars = c('SNR'))


neg_rates <- ts_list %>% 
  select(SNR,ITA,MK,Regression,Theil,truth) %>% 
  filter(truth) %>%
  mutate(ITA_FN=ITA == FALSE & truth,
         MK_FN=MK == FALSE & truth,
         Reg_FN=Regression == FALSE & truth,
         Theil_FN=Theil == FALSE & truth) %>% 
  group_by(SNR) %>% 
  summarize_all(funs(mean)) %>%
  select(SNR,ITA_FN,MK_FN,Reg_FN,Theil_FN)

neg_rates_melt <- melt(neg_rates, id.vars = c('SNR'))

ggplot(pos_rates_melt, aes(x=SNR,y=value, color=variable)) +
  geom_line()

ggplot(neg_rates_melt, aes(x=SNR,y=value, color=variable)) +
  geom_line()
# ------------
print('Done!')

