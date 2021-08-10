#import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas
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
df.columns=['name','rating','endorsements','followers','sport','country']

#clean data ex. $,m,decimals,append zeros,remove unicode bullet
df['endorsements']=df['endorsements'].str[1:].replace('.','')
df['endorsements']=df['endorsements'].str.replace('m','000000')

df['followers']=df['followers'].str.replace('.','')
df['followers']=df['followers'].str.replace('m','000000')

df['sport']=df['sport'].str.replace('•','')
df[df.columns]=df.apply(lambda x: x.str.strip())

#convert objects to numeric {rating,endorsements,followers}
df['rating']=pandas.to_numeric(df['rating'],errors='coerce')
df['endorsements']=pandas.to_numeric(df['endorsements'],errors='coerce')
df['followers']=pandas.to_numeric(df['followers'],errors='coerce')
#print(type(df['rating'][0]))
print(df)