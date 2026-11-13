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


# In[70]:


df = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\gmaps 1.csv", engine = 'python',  encoding="CP949")
print(df)


# In[9]:


conda activate map_env


# In[19]:


from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent = 'park1')


# In[20]:


from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geocoder.geocode, min_delay_seconds = 1,   return_value_on_exception = None) 
# adding 1 second padding between calls


# In[45]:


coordinate1 = df['longitude']
coordinate1


# In[47]:


coordinate2 = df['latitude']
coordinate2


# In[74]:


df = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\lstm_data_2005.csv", engine = 'python',  encoding="CP949")
print(df)


# In[75]:


coordinate1 = df['coordinate_x'].to_numpy()
coordinate1


# In[76]:


coordinate2 = df['coordinate_y'].to_numpy()


# In[68]:


coordinate1.astype(float)
coordinate2.astype(float)


# In[60]:


coordinate1[0:1]


# In[67]:


from geopy.distance import geodesic
for i in range(1272288):
            newport_ri = coordinate1[0:i]
            cleveland_oh = coordinate2[0:i]
            print(geodesic(newport_ri, cleveland_oh).km)


# In[ ]:


for i in coordinate1[0:]:
    for j in  coordinate2[0:]:


# In[ ]:


for j in coordinate1[0:i]:
    for k in  coordinate2[0:i]:


# In[ ]:





# In[ ]:





# In[ ]:





# In[4]:


import googlemaps 

API_key = 'YOUR_GOOGLE_API_KEY'   #enter the key you got from Google. I removed mine here

gmaps = googlemaps.Client(key=API_key)


# In[17]:


import googlemaps

gmaps = googlemaps.Client(key='YOUR_GOOGLE_API_KEY' )
reverse_geocode_result = gmaps.reverse_geocode((37.54794204380073, 127.07460710236217))
print(reverse_geocode_result)


# In[14]:


#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []


# In[72]:


for (i1, row1) in df.iterrows():
  print("origin")
  print(row1['ID'])
  LatOrigin = row1['latitude']
  LongOrigin = row1['longitude']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['ID']
  for (i2, row2) in  df.iterrows():
    print("destination id")
    print(row2['ID'])
    LatDestination = row2['latitude']
    LongDestination = row2['longitude']
    destination_id = row2['ID']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination)
    result_distance = result["rows"][0]["elements"][0]["duration"]["value"]
    result_time = result["rows"][0]["elements"][0]["duration_in_traffic"]["value"]
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)
    destination_id_list.append(destination_id)


# In[77]:


home_coord = coordinate1
work_coord = coordinate2


# In[80]:


url_home2work = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + home_coord + "&destinations=" + work_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + 'YOUR_GOOGLE_API_KEY'


# In[88]:


import requests
from bs4 import BeautifulSoup

result = requests.get(url_home2work)

bs_obj = BeautifulSoup(result.content, "html.parser")
print(bs_obj)


# In[ ]:


output = pd.DataFrame(distance_list, columns = ['Distance in meter'])
output['duration in seconds'] = time_list
output['origin_id'] = origin_id_list
output['destination_id'] = destination_id_list


# In[ ]:


output_v1 = pd.merge(output, df, how = "left", left_on = "origin_id", right_on = "ID")
output_v2 = pd.merge(output_v1, df, how = "left", left_on = "destination_id", right_on = "ID"
output_v2[['city_x', 'city_y', 'Distance in meter', 'duration in seconds']]
output_v2.to_excel('Coordinates_distancematrix.xlsx')


# In[ ]:





# In[9]:


import pyproj as  pyproj 


# In[4]:


from functools import partial
from pyproj import Proj, transform
proj_4326 = Proj(init="epsg:4326")
proj_3857 = Proj(init="epsg:3857")
transformer = partial(transform, proj_4326, proj_3857)
transformer(12, 12)


# In[13]:


pyproj.datadir.set_data_dir('/opt/miniconda3/envs/development/share/proj')


# In[3]:


import osmnx as ox

gw = ox.graph_from_point((37.571, 126.98), network_type='drive')
ox.plot_graph(gw)


# In[15]:


G = ox.graph_from_point([37.5666791, 126.9782914], network_type='drive')
fig, ax = ox.plot_graph(ox.project_graph(G))


# In[ ]:





# In[ ]:




