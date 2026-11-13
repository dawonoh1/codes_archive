#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import geopandas as gpd


# In[3]:


import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pandas import Series


# In[4]:


from geopandas import GeoSeries, GeoDataFrame, read_file


# In[5]:


seoul = read_file("E:\\Dropbox\\Dropbox\\geopandas\\seoul", engine = 'python')
type(seoul)


# In[6]:


seoul


# In[7]:


from geopandas.tools import geocode


# In[13]:


data = pd.read_csv("E:\\Dropbox\\Dropbox\\covid\\20210106 회의자료\\서울시 도시공원_분석용 데이터 210106.csv", engine = 'python', encoding = 'CP949')
data


# In[20]:


from geopandas.tools import geocode


# In[22]:


geo = geocode(data['위 치'], provider='nominatim', user_agent='autogis_xx', timeout=4)


# In[ ]:




