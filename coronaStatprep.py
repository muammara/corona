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
import warnings

#from motionchart.motionchart import MotionChart, MotionChartDemo
#Getting the daily file if it exists
#url = "https://www.ecdc.europa.eu/sites/default/files/documents/_COVID-19-geographic-disbtribution-worldwide-"+ format(Sys.time(), "%Y-%m-%d"), ".xlsx", sep = "")
##
#ignore by message
warnings.filterwarnings("ignore")
# In[3]:


#Define all the static entries
url= "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-"
sheet_name="COVID-19-geographic-disbtributi"
#ouput file
S3_BUCKET_NAME=''
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

print("Downloadeng ...\n {} \n ===> {}".format(file_url ,coronafilename))
urllib.request.urlretrieve(file_url, coronafilename) 
df=pd.read_excel(io=coronafilename,sheet_name=sheet_name)
print("formating the frame..")
df['Day']=df['Day'].astype('category')
df['Month']=df['Month'].astype('category')
df['Year']=df['Year'].astype('category')
df['Countries and territories'] =df['Countries and territories'].astype('category')
df=df.sort_values(by='DateRep',ascending=True)

# Addiing a filed for the total cases/death
print ("Aggregating the total cases/death per country")
df['TotalCases']=0
df['TotalDeath']=0
df1=pd.DataFrame([])
df2=pd.DataFrame([])
for country in df['Countries and territories'].unique():
    df1=df[df['Countries and territories']==country]
    df1['TotalCases']=df[df['Countries and territories']==country]['Cases'].cumsum()
    df1['TotalDeath']=df[df['Countries and territories']==country]['Deaths'].cumsum()
    df2=pd.concat([df2,df1])
df2.tail()
DAILY_FILE='CORONA'+filedate+'.csv'
print("Creating a new CSV File for processing, \n {} ==> created ".format(DAILY_FILE))
df2.to_csv(DAILY_FILE)

f = open("coronafilename", "w")
f.write(DAILY_FILE)
f.close()

def savetoS3(s3_buacketname, filename):
  s3 = boto3.resource('s3')
  s3.meta.client.upload_file(DAILY_FILE, S3_BUCKET_NAME,DAILY_FILE)




