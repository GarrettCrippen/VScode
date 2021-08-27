import json
import requests
import pandas
from athletes_df import *
from time import sleep

def hibp(key_upper,key_lower):
    url = "https://api.pwnedpasswords.com/range"
    response = requests.get(f"{url}/{key_upper}")

    breached=-1
    for hash in response.text.splitlines():
        if key_lower in hash:
            breached=int(hash.split(':')[1])
            print('found')
            break
        
    return breached

f=open('result2.json',)
data = json.load(f)

df=create_df()
df['name']=df['name'].replace('-','',regex=True)
d = {}
for n in df['name']:
    d[n]=None

for entries in data:
    for athletes in data[entries]:
        breached=-1
        print(f'for {athletes[1]} {entries}:{athletes[0]}')
        breached = hibp(entries.upper(),athletes[0].upper())
        try:
            f=open('breaches.txt','a')
        except:
            pass
        if breached !=-1: 
            print('found!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            f.write(f'{athletes[2]}:{athletes[1]}:{breached}\n')
            f.close()
            
        #print(f'athletes[0],{athletes[0]},athletes[1],{athletes[1]},')
