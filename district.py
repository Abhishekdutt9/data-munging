import pandas as pd
df = pd.read_csv('data/districts.csv') #loading data in the variable df



foo = lambda x: pd.Series([i for i in (x.split(','))]) #function to split after ','

mun = df['municipality_info'].apply(foo)
mun[0] = mun[0].str.extract('(\d+)', expand=False) #remove '[' from the column
mun[3] = mun[3].str.extract('(\d+)', expand=False) #remove ']' from the column
#rename the columns
mun.columns = ['num_municipality_pop_0-499', 'num_municipality_pop_500-1999', 'num_municipality_pop_2000-9999', 'num_municipality_pop_10000+']

unemploy = df['unemployment_rate'].apply(foo)
unemploy[0] = unemploy[0].str.extract('(\d+)', expand=False)#remove '[' from the column
unemploy[1] = unemploy[0].str.extract('(\d+)', expand=False)#remove ']' from the column
unemploy.columns = ['unemployment_rate_95', 'unemployment_rate_96']#rename the columns


crime = df['commited_crimes'].apply(foo)
crime[0] = crime[0].str.extract('(\d+)', expand=False)#remove '[' from the column
crime[1] = crime[0].str.extract('(\d+)', expand=False)#remove ']' from the column
crime.columns = ['commited_crimes_95', 'commited_crimes_96']#rename the columns


con = pd.concat([mun, unemploy,crime], axis=1) #join the subsetted dataframes
df = df.drop(['municipality_info', 'unemployment_rate', 'commited_crimes'], axis=1) #drop the unneeded columns
df = pd.concat([df, con], axis=1) # join to the main dataframe

df.to_csv('district_py.csv', index=False, encoding='utf-8') #convert to csv