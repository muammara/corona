#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
import pandas as pd
import numpy as np
from datetime import date, timedelta
import requests
import boto3
import os
#from motionchart.motionchart import MotionChart, MotionChartDemo


# In[2]:


#Getting the daily file if it exists
#url = "https://www.ecdc.europa.eu/sites/default/files/documents/_
#COVID-19-geographic-disbtribution-worldwide-"+ format(Sys.time(), "%Y-%m-%d"), ".xlsx", sep = "")
### 


# In[3]:


#Define all the static entries
url= "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
sheet_name="COVID-19-geographic-disbtributi"
#ouput file
S3_BUCKET_NAME=''


# In[ ]:





# In[4]:


filedate=date.today().strftime('%Y-%m-%d')

# Get the file of today or yesterday
#Test if today's file exists

#Use yesterday's file if today is not uploaded
file_url=url+filedate+".xlsx"
request = requests.get(file_url)
if request.status_code != 200:
  filedate = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
file_url=url+filedate+".xlsx"
coronafilename='CORONA'+filedate+'.xlsx'
urllib.request.urlretrieve(file_url, coronafilename) 
file_url


# In[5]:


df=pd.read_excel(io=coronafilename,sheet_name=sheet_name)


# In[6]:


df['Day']=df['Day'].astype('category')
df['Month']=df['Month'].astype('category')
df['Year']=df['Year'].astype('category')
df['Countries and territories'] =df['Countries and territories'].astype('category')


# In[7]:


df=df.sort_values(by='DateRep',ascending=True)


# In[8]:


df['TotalCases']=0
df['TotalDeath']=0


# In[9]:


df.info()


# In[20]:


df1=pd.DataFrame([])
df2=pd.DataFrame([])
for country in df['Countries and territories'].unique():
    df1=df[df['Countries and territories']==country]
    df1['TotalCases']=df[df['Countries and territories']==country]['Cases'].cumsum()
    df1['TotalDeath']=df[df['Countries and territories']==country]['Deaths'].cumsum()
    
    df2=pd.concat([df2,df1])
    
    #df1=pd.concat(df1, (df[df['Countries and territories']==country]['Cases']))
    #s=df[df['Countries and territories']==country]['Cases'].cumsum()
    #print(s)
    #df[df['Countries and territories']==country]['TotalCases']=s
df2['TotalDeath'].max()


# In[19]:


df2.tail()


# In[21]:


DAILY_FILE='CORONA'+filedate+'.csv'
df2.to_csv(DAILY_FILE)
print(DAILY_FILE)


# In[22]:



#s3 = boto3.resource('s3')
#s3.meta.client.upload_file(DAILY_FILE, S3_BUCKET_NAME,DAILY_FILE)


# In[23]:


f = open("coronafilename", "w")
f.write(DAILY_FILE)
f.close()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




