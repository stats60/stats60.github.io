library(tidyverse)
library(NHANES)
set.seed(12345)

# Null hypothesis: Height of renters is equal to or less than that of home owners
# Alternative hypothesis: Height of renters is greater than that of home owners.

sampleSize <- 200

NHANES_sample <- NHANES %>%
  filter(Age>17) %>%
  select(Height,HomeOwn) %>%
  filter(HomeOwn %in% c('Own','Rent')) %>%
  drop_na() %>%
  sample_n(sampleSize)

ggplot(NHANES_sample,aes(x=HomeOwn,y=Height)) +
  geom_boxplot()

summaryDf <- NHANES_sample %>%
  group_by(HomeOwn) %>%
  summarize(groupMeans = mean(Height),
            sdMeans = sd(Height),
            sampleSize = n())

meanDifference <- summaryDf$groupMeans[2] - summaryDf$groupMeans[1]

tStatistic <- meanDifference/sqrt(summaryDf$sdMeans[1]**2/summaryDf$sampleSize[1] +
                                    summaryDf$sdMeans[2]**2/summaryDf$sampleSize[2] )
tStatistic

ttestResult <- t.test(Height ~ HomeOwn,data=NHANES_sample,
                      alternative = 'less')
ttestResult$statistic

ourPValue <- pt(tStatistic,sampleSize - 2, lower.tail=FALSE)
ourPValue

ttestResult$p.value  