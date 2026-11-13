#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dask.dataframe as dd
import pandas as pd
import os


# In[3]:


df1 = pd. read_csv("E:\\생활인구2020\\livingpop2020\\LOCAL_PEOPLE_20200101.csv", engine = 'python', encoding = 'utf_8_sig')
df1


# In[5]:


df2 = pd. read_csv("E:\\생활인구2020\\livingpop2020\\LOCAL_PEOPLE_20200308.csv", engine = 'python', encoding = 'CP949')
df2


# In[ ]:




