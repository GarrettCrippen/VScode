#import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
from decimal import Decimal

def create_df():
   url_athletes = 'https://www.espn.com/espn/feature/story/_/id/26113613/espn-world-fame-100-2019'

   #use selenium webdriver because the website load some html using javascript
   browser = webdriver.Firefox()
   browser.get(url_athletes)
   soup = BeautifulSoup(browser.page_source, "html.parser")

   rows = []

   #find player thumbnail using regex
   grid = soup.find('div',{'id':'grid'})
   player_thumbnail = grid.find_all('div',{'id':re.compile('.*-thumb')})
   for player in player_thumbnail:
      name = player['data-id']
      rating = player.find('span',{'class':'rating-value'}).string
      endorsements = player.find('span',{'class':'endorsements-value'}).string
      followers = player.find('span',{'class':'followers-value'}).string
      sport = player.find('span',{'class':'sport'}).string
      country =player.find('span',{'class':'country'}).string
      rows.append([name,rating,endorsements,followers,sport,country])

   #create pandas dataframe from list(rows)
   df=pandas.DataFrame(rows)
   #print(list(df.columns))
   df.rename(columns={0:'name',1:'rating',2:'endorsements',3:'followers',4:'sport',5:'country'},inplace = True)
   #print(list(df.columns))

   #clean data ex. $,m,decimals,append zeros,remove unicode bullet

   # df['endorsements']=df['endorsements'].str[1:].replace('.','')
   # df['endorsements']=df['endorsements'].str.replace('m','000000')

   #$ ensures that m is the end of entry
   df['suffix1']=df['endorsements'].str.extract(r'([mk])+')
   df['endorsements']=(df['endorsements'].str[1:].replace(r'[mk]+$','',regex=True))
   #df['endorsements']=pandas.to_numeric(df['endorsements'])
  

   # df['followers']=df['followers'].str.replace('.','')
   # df['followers']=df['followers'].str.replace('m','000000')

   df['suffix2']=df['followers'].str.extract(r'([mk])+')
   df['followers'].replace(r'[mk]+$','',regex=True,inplace=True)

   df['sport']=df['sport'].str.replace('•','')
   df[df.columns]=df.apply(lambda x: x.str.strip())

   #convert objects to numeric {rating,endorsements,followers}
   df['rating']=pandas.to_numeric(df['rating'],errors='coerce')

   df['endorsements']=pandas.to_numeric(df['endorsements'],errors='coerce')
   df.loc[df['suffix1']=='m','endorsements']=df['endorsements']*10**6
   df.loc[df['suffix1']=='k','endorsements']=df['endorsements']*10**3

   df['followers']=pandas.to_numeric(df['followers'],errors='coerce')
   df.loc[df['suffix2']=='m','followers']=df['followers']*10**6
   df.loc[df['suffix2']=='k','followers']=df['followers']*10**3

   df=df.drop(columns={'suffix1','suffix2'})
   print(df)
   return df