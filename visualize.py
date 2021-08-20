import pandas as pd
from athletes_df import *

df=create_df()
df['total_breaches']=0
df['unique_breaches_by_name']=0
df['name'].replace('-','',regex=True,inplace = True)

f= open('breaches.txt','r')
for line in f.readlines():
    breached_data = line.split(':')
    df.set_index('name')
    df.loc[df['name']==(breached_data[0].strip()),'total_breaches']+=int(breached_data[2].strip())
    df.loc[df['name']==(breached_data[0].strip()),'unique_breaches_by_name']+=1
f.close()
print(df.head(100))