#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import dask as dd
import dask.dataframe as dd


# In[3]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[27]:


df = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\skt2020_05_xy.csv", engine = 'python',  encoding="CP949")
df.head()


# In[37]:


dt = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\inflowlist_coordinate.csv", engine = 'python', encoding = 'cp949') 
dt.head()


# In[29]:


dft = df.merge(dt, left_on='INFLOW_CD',  right_on='INFLOW_CD')
dft.head()


# In[30]:


dg = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\parklist_coordinate.csv", engine = 'python', encoding = 'cp949') 
dg.head()


# In[31]:


dftg = dft.merge(dg, left_on='ID',  right_on='ID')
dftg.head()


# In[32]:


del dftg['Unnamed: 0']
dftg.head()


# In[33]:


del dftg['PARK_NAME_x']
del dftg['ADDR']


# In[35]:


del dftg['STD_YM']
del dftg['FID']


# In[34]:


dftg.head()


# In[36]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

dftg.to_csv(path + "skt2020_05_xy.csv", encoding = "CP949", single_file = True )


# In[24]:


data = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\st_park2020_1.csv", engine = 'python', encoding = 'cp949')
data.head()


# In[25]:


data1 = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\lstm_park2020_05.csv", engine = 'python', encoding = 'cp949')
data1.head()


# In[26]:


data2 = data.merge(data1, left_on='Unnamed: 0',  right_on='Unnamed: 0')
data2.head()


# In[ ]:


del data2[['lat_x', 'long_x', 'lat_y', 'long_y']]


# In[22]:


import googlemaps 


# In[ ]:


API_key = 'YOUR_GOOGLE_API_KEY'   #enter the key you got from Google. I removed mine here

gmaps = googlemaps.Client(key=API_key)



origin = data.coordinates1 #Let's say this is the origin
destinations = data.coordinates2


actual_duration = []


for destination in destinations:
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]  
    result = result/60
    actual_duration.append(result)
    


#Add the list of coordinates to the main data set

data["duration (minutes)"] = actual_duration


data.head(10)


# In[ ]:


API_key = 'YOUR_GOOGLE_API_KEY'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)




origin = data.coordinates1
destinations = data.coordinates2


actual_distance = []


for destination in destinations:
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]  
    result = result/1000
    actual_distance.append(result)
    


#Add the list of coordinates to the main data set

data["distance (Km)"] = actual_distance


data.head(15)


# In[24]:


df = df.astype(str)

data["coordinates1"] = data["lat_x"].map(str) + "," + data["long_x"]       
data["coordinates2"] = data["lat_y"].map(str) + "," + data["long_y"]
data.head()

