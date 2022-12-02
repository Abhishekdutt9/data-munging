import pandas as pd
df = pd.read_csv('data/loans.csv') #loading data in the variable df
df = df.melt(id_vars=["id", "account_id", "date", "amount", "payments"]) #using melt to combine the columns except id, account_id,date,amount,payments
df = df[df['value'] == 'X'] #dropping extra rows
df['months'], df['status'] = df['variable'].str.split('_', 1).str #creating new columns by splitting 'variable'
df = df.drop(['variable', 'value'], axis=1) #dropping variable and value


def status(row):
    if row['status'] == 'A' or row['status'] == 'B':
        val = 'expired'
    else:
        val = 'current'
    return val

def default(row):
    if row['status'] == 'B' or row['status'] == 'D':
        val = True
    elif row['status'] == 'A' or row['status'] == 'C':
        val = False

    return val

df['loan_status'] = df.apply(status, axis=1)

df['loan_default'] = df.apply(default, axis=1)

df= df.drop(['status'], axis=1)



df.to_csv('loans_py.csv', index=False, encoding='utf-8') #convert to csv