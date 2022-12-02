library("tidyr")
library("devtools")
library("dplyr")
library("ggplot2")

#loading data
data = read.csv('analytical_r.csv')

data <- data %>% 
mutate(card = if_else(credit_cards == 0, FALSE, TRUE))

png("base-visualization.png")

ggplot(data, aes(x=card, y=max_balance, fill=card)) + 
  geom_boxplot()+
  labs(title="Max account balance of accounts with and without a credit card",
       x="Credit Card linked to the account", y = "Max Account Balance")+
  theme_classic()+
  scale_fill_brewer(palette="RdBu")

dev.off()
