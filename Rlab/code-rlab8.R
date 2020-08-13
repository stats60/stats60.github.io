library(NHANES)
library(tidyverse)

# H0: Adults with diabetes will weigh equal to adults without diabetes 

set.seed(12345)
sampleSize <- 200

NHANES_sample <- NHANES %>%
  filter(Age > 17) %>%
  select(Weight,Diabetes) %>%
  drop_na() %>%
  sample_n(200)

summaryDf <- NHANES_sample %>%
  group_by(Diabetes) %>%
  summarise(groupMean = mean(Weight),
            groupSD = sd(Weight),
            sampleSize = n())

summaryDf

ggplot(NHANES_sample,aes(x=Diabetes,y=Weight)) +
  geom_boxplot()

meanDifference = summaryDf$groupMean[1] - summaryDf$groupMean[2]

tStatistic = meanDifference/sqrt(summaryDf$groupSD[1]**2/summaryDf$sampleSize[1] + summaryDf$groupSD[2]**2/summaryDf$sampleSize[2])

tStatistic

# construct CI for the difference of population mean of weight for people with diabetes
# and population mean of weight for people without diabetes

upper <- meanDifference + 1.96 * 
  sqrt(summaryDf$groupSD[1]**2/summaryDf$sampleSize[1] + summaryDf$groupSD[2]**2/summaryDf$sampleSize[2])

lower <- meanDifference - 1.96 * 
  sqrt(summaryDf$groupSD[1]**2/summaryDf$sampleSize[1] + summaryDf$groupSD[2]**2/summaryDf$sampleSize[2])

t_result <- t.test(Weight ~ Diabetes,data=NHANES_sample,alternative='two.sided')
