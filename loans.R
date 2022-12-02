data <- read.csv("data/loans.csv")#loading data

#importing libraries
library("tidyr")
library("devtools")

#combining columns 6-25
data <- gather(data, "code", "check", 6:25)

#making separate columns for months and stutus
data <- separate(data, code, c("months", "status"))

#removing irrelevant rows
data <- data[data$check=="X", ]

#removing X in front of months
data$months<-gsub("X","",as.character(data$months))

#dropping the check column
data <- data[ -c(8) ]

#changing the data type of date
data$date <- as.Date(data$date) 


  
data$loan_status <- ifelse((data$status == 'A') | (data$status == 'B'),"current", "expired") #making new columns based on status

data$loan_default <- ifelse((data$status == 'B') | (data$status == 'D'),TRUE , FALSE)

data <- subset(data, select = -c(status)) #removing status as its not needed


#converting the modified data to a csv file
write.csv(data, "loans_r.csv", row.names=FALSE)

