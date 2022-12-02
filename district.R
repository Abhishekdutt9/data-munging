data <- read.csv("data/districts.csv")

library("tidyr")
library("devtools")

#making separate columns for municipality population
data <- separate(data, municipality_info, c("num_municipality_pop_0-499", "num_municipality_pop_500-1999","num_municipality_pop_2000-9999","num_municipality_pop_10000+"), sep=',')

#removing [ and ] from the columns below 
data$`num_municipality_pop_0-499`<-gsub('[[:punct:]]',"",as.character(data$`num_municipality_pop_0-499`))
data$`num_municipality_pop_10000+`<-gsub('[[:punct:]]',"",as.character(data$`num_municipality_pop_10000+`))


#making separate columns for unemployment rate
data <- separate(data, unemployment_rate, c("unemployment_rate_95", "unemployment_rate_96"), sep=',')

#removing [ and ] from the columns below 
data$`unemployment_rate_95`<-gsub('\\[',"",as.character(data$`unemployment_rate_95`))
data$`unemployment_rate_96`<-gsub('\\]',"",as.character(data$`unemployment_rate_96`))

#making separate columns for commited crimes
data <- separate(data, commited_crimes, c("commited_crimes_95", "commited_crimes_96"), sep=',')

#removing [ and ] from the columns below 
data$`commited_crimes_95`<-gsub('[[:punct:]]',"",as.character(data$`commited_crimes_95`))
data$`commited_crimes_96`<-gsub('[[:punct:]]',"",as.character(data$`commited_crimes_96`))

#converting the modified data to a csv file

write.csv(data, "district_r.csv", row.names=FALSE)