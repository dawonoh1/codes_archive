#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians


# In[32]:


df = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\lstm_data_2005_xy.csv", engine = 'python',  encoding="CP949")
print(df)


# In[35]:


from geopy import distance

def dist_calc (row):
    start = (row['lat_x' ], row['long_x'])
    stop = (row['lat_y'], row['long_y'])
    return distance.great_circle(start, stop).km
df['distance'] = df.apply (lambda row: dist_calc (row), axis=1)


# In[36]:


df.head()


# In[41]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

df.to_csv(path + "dist.csv", encoding = "CP949")


# In[47]:


import dask as dd
import dask.dataframe as dd

dt = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\lstm_park2020_05.csv", engine = 'python',  encoding="CP949")
dt.tail()



# In[44]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[53]:


df = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\dist.csv", engine = 'python',  encoding="CP949")
df.tail()


# In[54]:


df = df[['Unnamed: 0.1', 'distance']]
df


# In[55]:


dft = df.merge(dt, left_on='Unnamed: 0.1',  right_on='Unnamed: 0')


# In[56]:


dft.head()


# In[60]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

dft.to_csv(path + "dataset.csv", encoding = "CP949", single_file = True )


# In[ ]:




