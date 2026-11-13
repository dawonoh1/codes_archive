#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import dask as dd
import dask.dataframe as dd


# In[2]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[10]:


dg = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\inflowlist_coordinate.csv", engine = 'python',  encoding="CP949")
dg.head()


# In[4]:


dt = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\parklist_coordinate.csv", engine = 'python',  encoding="CP949")
dt.head()


# In[8]:


df = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\Seoul_Park_202005.csv",  engine = 'python',  encoding="utf_8_sig", sep='|')
df.head()


# In[11]:


dfg = df.merge(dg, left_on='INFLOW_CD',  right_on='INFLOW_CD')
dfg.head()


# In[29]:


dfgt_t = dfg.merge(dt, left_on='PARK_NAME',  right_on='PARK_NAME')
dfgt_t.head()


# In[30]:


del dfgt_t['STD_YM']
del dfgt_t['ADDR']


# In[31]:


dfgt_t.head()


# In[32]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

dfgt_t.to_csv(path + "lstm_data_2005_total.csv", encoding = "CP949", single_file = True )


# In[28]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
dfgt = dfgt[['coordinate_x', 'coordinate_y']]
dfgt.to_csv(path + "lstm_data_2005.csv", encoding = "CP949", single_file = True )


# In[33]:


dfgt.head()


# In[41]:


gp = dfgt.groupby(pd.qcut(range(dfgt.shape[0]), 5))  # N = 3
d = {f'dfgt{i+1}': x[1] for i, x in enumerate(gp)}
d['dfgt1']


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[20]:


import googlemaps 

API_key = 'YOUR_GOOGLE_API_KEY'   #enter the key you got from Google. I removed mine here

gmaps = googlemaps.Client(key=API_key)


# In[24]:


actual_duration = []


for destination in destinations:
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]  
    result = result/3600
    actual_duration.append(result)
    


#Add the list of coordinates to the main data set

data["duration (Hours)"] = actual_duration


data.head(10)


# In[ ]:





# In[ ]:





# In[ ]:





# In[70]:


data = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\lstm_park2020_05.csv", engine = 'python',  encoding="CP949")
data.head()


# In[71]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
data = data[['Unnamed: 0', 'lat_x',  'long_x', 'PARK_NAME_y', 'lat_y', 'long_y']]
data.to_csv(path + "lstm_data_2005_xy.csv", encoding = "CP949", single_file = True )


# In[64]:


#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []


# In[75]:


for (i1, row1) in data.iterrows():
  print("origin")
  print(row1['Unnamed: 0'])
  LatOrigin = row1['lat_x']
  LongOrigin = row1['long_x']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['Unnamed: 0']
  for (i2, row2) in  df.iterrows():
    print("destination id")
    LatDestination = row2['lat_y']
    LongDestination = row2['long_y']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination, mode='driving')
    result_distance = result["rows"][0]["elements"][0]["distance"]        
    ["value"]
    result_time = result["rows"][0]["elements"][0]["duration"]["value"]
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)


# In[ ]:





# In[ ]:


data = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\sample.csv", engine = 'python',  encoding="CP949")


# In[ ]:





# In[ ]:





# In[ ]:





# In[62]:


API_key = 'YOUR_GOOGLE_API_KEY'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)




origin = data['coordinate_x']
destinations = data['coordinate_y']


actual_distance = []


for destination in destinations:
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]  
    result = result/1000
    actual_distance.append(result)
    


#Add the list of coordinates to the main data set

data["distance (Km)"] = actual_distance


data.head(15)


# In[58]:


my_distance = gmaps.distance_matrix(origin, destinations, mode='driving', language=None, avoid=None, units='metric',
                                        departure_time='2475925955', arrival_time=None,
                                        transit_routing_preference=None)

origin = my_distance['origin_addresses']
dest = my_distance['destination_addresses']
dist = my_distance['rows']


actual_duration = []

dct = {d_adresses:[] for d_adresses in data[['coordinate_x']]}
dct['starts'] = []
for i in range(len(data[['coordinate_y']])):
    result = int(data['rows'][i]['elements'][0]['duration']['value'].split(' ')[0])
    result = result/3600
    actual_duration.append(result)
    

#Add the list of coordinates to the main data set

data["duration (Hours)"] = actual_duration


data.head(10)


# In[ ]:




