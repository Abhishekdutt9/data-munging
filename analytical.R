#importing libraries
library("tidyr")
library("devtools")
library("dplyr")

#loading data
loans = read.csv('loans_r.csv') #loading data in the variable loans
accounts = read.csv('data/accounts.csv')
links = read.csv('data/links.csv')
transactions = read.csv('data/transactions.csv')
payment_orders = read.csv('data/payment_orders.csv')
cards = read.csv('data/cards.csv')
districts = read.csv('district_r.csv')


df = accounts #df will be the main dataframe that I will output

colnames(df) <- c('account_id', 'id','open_date','statement_frequency') 

df <- merge(x=df,y=districts[,c("id","name")],by="id",all.x=TRUE) #left join

df <- subset(df, select = -c(id)) #drop column id

df <- df[,c(1,4,2,3)] # reorder columns
colnames(df) <- c('account_id', 'district_name','open_date','statement_frequency') #rename columns

df <- merge(x=df,y=links[,c("account_id","client_id")],by="account_id",all.x=TRUE) #left join

c_customers <- df %>% count(account_id)  # Applying count to count the num of clients with each account
colnames(c_customers) <- c('account_id', 'num_customers') #rename columns

df <- df[!duplicated(df$account_id),] #removing duplicated account_ids
df <- merge(x=df,y=c_customers[,c("account_id","num_customers")],by="account_id",all.x=TRUE) #left join
df <- subset(df, select = -c(client_id)) #drop client id columns

#cards.csv
colnames(cards) <- c('id','client_id','type','issue_date') #changing the names of the columns

ccard = merge(x=links,y=cards[,c("client_id","id")],by="client_id") #inner join 
c_ccard <- ccard %>% count(account_id) #counts the number of credit cards per account_id
colnames(c_ccard) <- c('account_id','credit_cards')
df <- merge(x=df,y=c_ccard[,c("account_id","credit_cards")],by="account_id",all.x=TRUE)
df <- df %>% mutate(credit_cards = ifelse(is.na(credit_cards), 0, credit_cards)) #replace na with 0

#loans.csv

colnames(loans) <- c('id','account_id','date', 'loan_amount', 'loan_payments','loan_term','loan_status', 'loan_default')
loans$loan = TRUE #make a new column called loans with all values True
df <- merge(x=df,y=loans[,c("account_id",'loan_amount', 'loan_payments',
                            'loan_term','loan_status', 'loan_default','loan')]
                         ,by ="account_id",all.x=TRUE)

df <- df %>% mutate(loan = ifelse(is.na(loan), FALSE, loan)) #replace na with FALSE

#transactions.csv

withdrawal <- transactions[which(transactions$type=='debit'),] #data for all withdrawals
withdrawal <- subset(withdrawal, select = c(account_id,amount)) #only two columns are needed hence subsetting
c_withdrawal_max <- aggregate(amount~account_id, withdrawal,max)#finding max withdrawal of each account_id
c_withdrawal_min <- aggregate(amount~account_id, withdrawal,min)#finding min withdrawal of each account_id
colnames(c_withdrawal_max) <-c("account_id", "max_withdrawal")#changing names of columns
colnames(c_withdrawal_min) <-c("account_id", "min_withdrawal")#changing names of columns
c_withdrawal <- merge(x=c_withdrawal_max,y=c_withdrawal_min
            ,by ="account_id")# inner join 
df<-merge(x=df,y=c_withdrawal,by ="account_id",all.x=TRUE) #joining to main df


ccpayments <- transactions[which(transactions$method=='credit card'),]
ccpayments <- ccpayments[which(ccpayments$type=='debit'),]
ccpayments <- subset(ccpayments, select = c(account_id))
c_ccpayments <- ccpayments %>% count(account_id)
colnames(c_ccpayments) <-c("account_id","cc_payments")
df<-merge(x=df,y=c_ccpayments,by ="account_id",all.x=TRUE) #joining to main df
df <- df %>% mutate(cc_payments = ifelse(is.na(cc_payments), 0, cc_payments))#changing na values to 0

bal <- subset(transactions, select = c(account_id,balance))#subsetting since we only need the two columns
c_bal_max <- aggregate(balance~account_id, bal,max)#storing max balance in the account here
c_bal_min <- aggregate(balance~account_id, bal,min)#storing min balance in the account here
colnames(c_bal_max) <-c("account_id", "max_balance")#changing names of columns
colnames(c_bal_min) <-c("account_id", "min_balance")#changing names of columns
c_bal <- merge(x=c_bal_max,y=c_bal_min,by ="account_id")# inner join 
df<-merge(x=df,y=c_bal,by ="account_id",all.x=TRUE) #left outer joining to main df

df <- df[,c(1,2,3,4,5,6,12,7,8,9,10,11,13,14,15,16,17)] #reorder columns

#converting the modified data to a csv 
write.csv(df, "analytical_r.csv", row.names=FALSE) #done yay
