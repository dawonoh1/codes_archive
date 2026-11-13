#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np


# In[11]:


df1 = pd. read_csv("E:\\Dropbox\\Dropbox\\2차심사\\landuse_0402.csv", engine = 'python', encoding = 'cp949')
df1


# In[23]:


type('코드')


# In[29]:


df1 = pd. read_csv("E:\\Dropbox\\Dropbox\\학회3\\건물\\landuse_1.csv", engine = 'python', encoding = 'cp949')
df1


# In[27]:


df2 = pd. read_csv("E:\\Dropbox\\Dropbox\\학회3\\건물\\bdinpark22.csv", engine = 'python', encoding = 'cp949')
df2


# In[26]:


df2['USE_CD_NEW'] = df['USE_CD_NEW'].astype(str)


# In[30]:


df3 = pd.merge(df1, df2, left_on = '코드', right_on = 'USE_CD_NEW')
df3


# In[31]:


df3 = df3.to_csv("bdinpark2.csv", encoding="CP949")


# In[ ]:




