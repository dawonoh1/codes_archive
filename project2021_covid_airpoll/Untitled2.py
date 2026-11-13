#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import geopandas as gpd
import numpy as np


# In[2]:


import fiona; help(fiona.open)


# In[3]:


import matplotlib.pyplot as plt
from shapely.geometry import Point
from pandas import Series


# In[4]:


from geopandas import GeoSeries, GeoDataFrame, read_file


# In[5]:


seoul = read_file("E:\\Dropbox\\Dropbox\\geopandas\\seoul", engine = 'python')
type(seoul)
seoul


# In[ ]:




