#!/usr/bin/env python
# coding: utf-8

# In[3]:


import dask.dataframe as dd

import pandas as pd
import numpy as np
import os


# In[4]:


path = "E:\\Dropbox\\Dropbox\\covid\\데이터\\2020년 서울시 공원 데이터/" 
list_dir = os.listdir(path)
list_dir


# In[8]:


first_data = pd.read_csv("E:\\Dropbox\\Dropbox\\covid\\데이터\\2020년 서울시 공원 데이터\\Seoul_Park_202001.csv", engine="python", encoding="utf_8_sig", sep='|')

pivot = first_data.pivot_table(index=["STD_YM", "STD_YMD", "INFLOW_CD" ], values= [ "ID"], aggfunc=np.sum)
pivot


# In[9]:


first_data.groupby(first_data.ID).count()


# In[10]:


pivot.to_csv(path + "pivot1.csv", encoding = "CP949" )


# In[11]:


first_data = dd.read_csv("E:\\Dropbox\\Dropbox\\covid\\데이터\\dfcheck\\2020skt.csv", engine="python", encoding="cp949")
first_data


# In[12]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[13]:


df = first_data.groupby(["STD_YMD", "ID"]).count()
df.head()


# In[14]:


path = "E:\\Dropbox\\Dropbox\\covid\\데이터\\2020년 서울시 공원 데이터/" 

df.to_csv(path + "dfcheck_ID.csv", encoding = "CP949",  single_file = True )


# In[ ]:




