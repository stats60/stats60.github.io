#install.packages("NHANES")

library(NHANES)
library(dplyr)

NHANES$isChild <- NHANES$Age<18

NHANES_adult=subset(NHANES,subset=!isChild & Height!='NA')

print(paste('Population height: mean = ',mean(NHANES_adult$Height)))

print(paste('Population height: std deviation = ',sd(NHANES_adult$Height)))

exampleSample = NHANES_adult %>% sample_n(10)

dim(NHANES_adult)

print(paste('Sample height: mean = ',mean(exampleSample$Height)))

print(paste('Sample height: std deviation = ',sd(exampleSample$Height)))

sampSize=100
nsamps=5000

sampMeans=array(NA,nsamps)

for (i in 1:nsamps){
  NHANES_sample=sample_n(NHANES_adult,sampSize)
  sampMeans[i]=mean(NHANES_sample$Height)
}
print(paste('Average sample mean =',mean(sampMeans)))
print(paste('Standard deviation of sample means =',sd(sampMeans)))
print(paste('Estimated standard error based on population SD:',sd(NHANES_adult$Height)/sqrt(sampSize)))
