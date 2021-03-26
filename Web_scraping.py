pip install requests
from google.colab import auth
auth.authenticate_user()
import gspread
from oauth2client.client import GoogleCredentials
gc = gspread.authorize(GoogleCredentials.get_application_default())
from google.colab import drive
drive.mount('/content/drive')
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
html_text=requests.get('https://www.marksandspencer.in/l/women/all-women-2/').text
soup=BeautifulSoup(html_text,'lxml')
jobs=soup.find_all('div',class_='col-6 col-md-3 gridnumber')
a=[]
for job in jobs:
  brand=job.find('div',class_='pdp-brand').text.replace('\n','')
  dress=job.find('div',class_='pdp-link').text.replace('\n','')
  price1=job.find('div',class_='price').text.replace('\n','')
  
  b=[brand,dress,price1]  
  a.append(b)
df = pd.DataFrame(a)
df.columns=['Brand','Clothing',"Cost"]
df['Dress']=df['Clothing'].apply(lambda x: 1 if (('dress' in x.lower()) or ('jumper' in x.lower())) else 0)
df['Skirt']=df['Clothing'].apply(lambda x: 1 if 'skirt' in x.lower() else 0)
df['Pants']=df['Clothing'].apply(lambda x: 1 if (('trousers' in x.lower()) or ('jeans' in x.lower()) or ('jeggings' in x.lower()) or ('leggings' in x.lower()) or('joggers' in x.lower()) or ('bottoms' in x.lower())) else 0)
df['Shirt']=df['Clothing'].apply(lambda x: 1 if (('shirt' in x.lower()) or ('top' in x.lower()) or ('blouse' in x.lower()) or ('tunic' in x.lower())) else 0)
df['Swimsuit']=df['Clothing'].apply(lambda x:1 if 'swimsuit' in x.lower() else 0)
df['Accessories']=df['Clothing'].apply(lambda x: 0 if (('dress' in x.lower())or ('trousers' in x.lower()) or ('jeans' in x.lower()) or ('jeggings' in x.lower()) 
or ('leggings' in x.lower()) or('joggers' in x.lower()) or ('bottoms' in x.lower()) or ('jumper' in x.lower()) or ('skirt' in x.lower()) or ('shirt' in x.lower())
or ('top' in x.lower()) or ('blouse' in x.lower()) or ('swimsuit' in x.lower()) or ('tunic' in x.lower())) else 1)
df['Marked_Cost']=df['Cost'].copy()
df['Marked_Cost']=df['Marked_Cost'].apply(lambda x:x.replace('₹','-').replace('From','').replace('-','-'))
df['Marked_Cost']=df['Marked_Cost'].apply(lambda x:x.replace('--','-'))
df['Minimum_Cost']=df['Marked_Cost'].apply(lambda x:x.split('-')[1])
df['Maximum_Cost']=df['Marked_Cost'].apply(lambda x:x.split('-')[-1])
df.drop('Marked_Cost', axis=1, inplace=True)
df['Maximum_Cost']=df['Maximum_Cost'].apply(lambda x:x.replace(',',''))
df['Minimum_Cost']=df['Minimum_Cost'].apply(lambda x:x.replace(',',''))
df['Minimum_Cost'] = pd.to_numeric(df['Minimum_Cost'])
df['Maximum_Cost'] = pd.to_numeric(df['Maximum_Cost'])
df['Average_Cost']=(df['Minimum_Cost']+df['Maximum_Cost'])/2
s=df.to_csv('/content/drive/My Drive/f2.csv')
