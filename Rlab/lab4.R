library(tidyverse)

df <- read.csv("ca_drought_data.csv")

str(df)

View(df)

df %>% summarize(distinct = n_distinct(County))

df %>% group_by(County) %>% summarise(Count = n())

df_levels <- df %>% select(County, Date = ValidStart, D0:D4) %>% mutate(Date = as.Date(Date), Drought = D0 + D1 + D2 + D3 + D4)

df_county <- df_levels %>% filter(County == "Santa Clara County")

df_county <- df_county %>% gather(D0:D4, key = "Drought level", value = "Percent of land area")

ggplot(data = df_county) + geom_area(mapping = aes(x = Date, y = `Percent of land area`, fill = `Drought level`))

ggplot(data = df_county) + geom_area(mapping = aes(x = Date, y = `Percent of land area`, fill = `Drought level`)) + scale_fill_brewer(palette = "YlOrRd")