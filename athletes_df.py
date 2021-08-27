#import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
from decimal import Decimal
from requests import get

def create_df():
   url_athletes = 'https://www.espn.com/espn/feature/story/_/id/26113613/espn-world-fame-100-2019'
   url_athletes2 = 'https://opendorse.com/blog/top-100-highest-paid-athlete-endorsers-2019/'


#DF2---------------------------------------------------------------------------------------------------
   #user agent needed to avoid 403 forbidden
   headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
   response = get(url_athletes2,headers=headers)
   soup2 = BeautifulSoup(response.text,'html.parser')

   rows2 = []

   #find player information under article

   article = soup2.find_all('figure',{'class':'wp-block-image'})
   for player2 in article:
      player_thumbnail2=player2.find_next('h3')
      #1. Roger Federer | ATP
      en=player2.find_next('h4')
      t=player2.find_next('p')
      name2=player_thumbnail2.text.split('|')[0].split('.',1)[1].strip()\
      .replace(' ','-').replace('.','-')\
      .replace(',','-').lower()
      sport = player_thumbnail2.text.split('|')[1].strip()
      #2019 Endorsement Earnings: $86,000,000
      endorsements2=(en.text).split('$')[1].replace(',','').strip()
      #Twitter Followers: 12.6M
      twitter = t.text.split(':')[1].strip()
      rows2.append([name2,endorsements2,twitter,sport])
   
   df2=pandas.DataFrame(rows2)
   df2.rename(columns={0:'name',1:'endorsements',2:'followers',3:'sport'},inplace =True)

   df2['sport'].replace('La Liga','Soccer',inplace = True)
   df2['sport'].replace('ATP Tour','Tennis',inplace = True)
   df2['sport'].replace('ATP','Tennis',inplace = True)
   df2['sport'].replace('PGA Tour','Golf',inplace = True)
   df2['sport'].replace('PGA TOUR','Golf',inplace = True)
   df2['sport'].replace('NBA','Basketball',inplace = True)
   df2['sport'].replace('UFC','MMA',inplace = True)
   df2['sport'].replace('Formula 1','Racing',inplace = True)
   df2['sport'].replace('NFL','American Football',inplace = True)
   df2['sport'].replace('MLB','Baseball',inplace = True)
   df2['sport'].replace('Premier League','Soccer',inplace = True)
   df2['sport'].replace('J1 League','Soccer',inplace = True)
   df2['sport'].replace('Indian Premier League','Cricket',inplace = True)
   df2['sport'].replace('Chinese Super League','Soccer',inplace = True)

   df2['followers'].replace('N/A',0,inplace = True)
   df2['suffix2']=df2['followers'].str.extract(r'([MK])+')
   df2['followers'].replace(r'[MK]+$','',regex=True,inplace=True)

   df2['endorsements']=pandas.to_numeric(df2['endorsements'],errors='coerce')
   df2['followers']=pandas.to_numeric(df2['followers'],errors='coerce')
   df2.loc[df2['suffix2']=='M','followers']=df2['followers']*10**6
   df2.loc[df2['suffix2']=='K','followers']=df2['followers']*10**3

   df2.drop(columns={'suffix2'},inplace=True)
   #print(df2['sport'].unique())
  
#DF1---------------------------------------------------------------------------------------------------
   #use selenium webdriver because the website is loading some html using javascript
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


   df3=df2[df2.name.isin(df.name)==False]
   # print(df3)
   # print(df3.shape)
   # print(df.shape)

   df=pandas.concat([df,df3]).reset_index()

   return df
   #return df3.reset_index()