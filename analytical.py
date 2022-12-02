import pandas as pd
loans = pd.read_csv('loans_py.csv') #loading data in the variable loans
accounts = pd.read_csv('data/accounts.csv')
links = pd.read_csv('data/links.csv')
transactions = pd.read_csv('data/transactions.csv')
payment_orders = pd.read_csv('data/payment_orders.csv')
cards = pd.read_csv('data/cards.csv')
districts = pd.read_csv('district_py.csv')


df = accounts #df is the main dataframe that will be outputted, using data from accounts.csv to put in df

df.columns = ['account_id', 'id','open_date','statement_frequency']

df = pd.merge(df, districts[["id", "name"]], how="left", on=["id"]) #left outer join on df and districts
df = df.drop(['id'], axis=1) #drop column id
df = df[['account_id','name','open_date','statement_frequency']] #reorder columns
df.columns = ['account_id', 'district_name','open_date','statement_frequency'] #change names of columns


df = pd.merge(df, links[["account_id", "client_id"]], how="left", on=["account_id"]) #left join
s = df.groupby('account_id').size().rename_axis('account_id').reset_index(name='num_customers') #makes a df called s that has number of customers linked to an account

df = df.drop_duplicates('account_id')

#s.columns = ['account_id', 'num_customers']
df = pd.merge(df, s[["account_id","num_customers"]], how="left", on=["account_id"]) #joining this df created to the main df



cards.columns = ['id','client_id','type','issue_date'] #changing the names of the columns
ccard = pd.merge(links, cards[["client_id",'id']], how="inner", on=["client_id"])  #inner join to link the card info to links.csv
ccard = ccard.groupby('account_id').size().rename_axis('account_id').reset_index(name='credit_cards')# makes a df called ccard that has number of cards linked to an account
df = pd.merge(df, ccard[["account_id",'credit_cards']], how="left", on=["account_id"]) #left join since not all customers have cards
df['credit_cards'] = df['credit_cards'].fillna(0) #replacing the na values with 0


loans.columns = ['id','account_id','date', 'loan_amount', 'loan_payments','loan_term','loan_status', 'loan_default'] #changing names of loans_py.csv for convenience
loans['loan'] = True #making a new column that has true for all customers that have or have had a loan
df = pd.merge(df, loans[["account_id",'loan_amount', 'loan_payments','loan_term','loan_status', 'loan_default','loan']], how="left", on=["account_id"]) # left join since not all accounts have a loan
df["loan"].fillna(False,inplace=True) #false inplace of na

withdrawal = transactions[transactions['type']=='debit'] #data for all withdrawals
withdrawal = withdrawal[['account_id','amount']] #changing col names
max_withdrawal = withdrawal.loc[withdrawal.groupby('account_id')['amount'].idxmax(), :].reset_index() #creating a df which has the max withdrawal for each account_id
max_withdrawal.columns = ['index','account_id','max_withdrawal']#changing names of the created df
min_withdrawal = withdrawal.loc[withdrawal.groupby('account_id')['amount'].idxmin(), :].reset_index()#creating a df which has the min withdrawal for each account_id
min_withdrawal.columns = ['index','account_id','min_withdrawal']#changing names of the created df
df = pd.merge(df,max_withdrawal[['account_id','max_withdrawal']],how="left", on=["account_id"])
df = pd.merge(df,min_withdrawal[['account_id','min_withdrawal']],how="left", on=["account_id"])#left outer join this info

ccpayments = transactions[(transactions['method']=='credit card')] #data for all credit card transactions
ccpayments = ccpayments[ccpayments['type']=='debit']
ccpayments = ccpayments[['account_id']] #we only need account_id to count
ccpayments = ccpayments.groupby('account_id').size().rename_axis('account_id').reset_index(name='cc_payments') #making a new column that stores the number of transactions
df = pd.merge(df, ccpayments[["account_id",'cc_payments']], how="left", on=["account_id"])#left join
df['cc_payments'] = df['cc_payments'].fillna(0) #i dont know if this should be left as NA or 0


bal = transactions[['account_id','balance']] #looking at the balances and account_id only
max_bal = bal.loc[bal.groupby('account_id')['balance'].idxmax(), :].reset_index()  #stores the max balance for every account_id
min_bal = bal.loc[bal.groupby('account_id')['balance'].idxmin(), :].reset_index() #stores the min balance for every account_id
max_bal = max_bal.drop(['index'], axis = 1)#drop index column
min_bal = min_bal.drop(['index'], axis = 1)

tot_bal = pd.concat([max_bal,min_bal], axis = 1, join = "inner") #creates a new df with both max and min balances and account_d
tot_bal.columns = ['account_id','max_balance','drop','min_balance'] #renames
tot_bal = tot_bal.drop(['drop'], axis=1) #drops the extra account_id

df = pd.merge(df, tot_bal[["account_id",'max_balance','min_balance']], how="left", on=["account_id"])#adding this to the main df

del df['client_id'] #extra info not required
df = df[['account_id', 'district_name', 'open_date', 'statement_frequency',
       'num_customers', 'credit_cards', 'loan', 'loan_amount',
       'loan_payments', 'loan_term', 'loan_status', 'loan_default',
       'max_withdrawal', 'min_withdrawal', 'cc_payments', 'max_balance',
       'min_balance']] #changed the order to the required


df.to_csv('analytical_py.csv', index=False, encoding='utf-8') #convert to csv and done yay