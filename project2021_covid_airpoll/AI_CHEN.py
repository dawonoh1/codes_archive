#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import dask as dd
import dask.dataframe as dd


# In[6]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[8]:


df = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\Seoul_Park_202005.csv",  engine = 'python',  encoding="utf_8_sig", sep='|')
df.head()


# In[9]:


df_list = list(df[['M_0009', 'M_1014', 'M_1519', 'M_2024', 'M_2529', 'M_3034', 'M_3539', 'M_4044', 'M_4549', 'M_5054', 'M_5559', 'M_6064', 'M_6569', 'M_7000', 'W_0009', 'W_1014', 'W_1519', 'W_2024', 'W_2529', 'W_3034', 'W_3539', 'W_4044', 'W_4549', 'W_5054', 'W_5559', 'W_6064', 'W_6569', 'W_7000']])


# In[10]:


df["total_visitor"] = df[df_list].sum(axis=1)


# In[11]:


df=df[['ID', 'STD_YM', 'STD_YMD', 'PARK_NAME', 'INFLOW_CD','total_visitor']]


# In[12]:


df.head()


# In[13]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
df.to_csv(path + "skt2020_05_xy.csv", encoding = "CP949", single_file = True )


# In[4]:


df = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\skt2020_xy.csv", engine = 'python', encoding = 'cp949')
df.head()


# In[36]:


dt = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\inflowlist.csv", engine = 'python', encoding = 'cp949') 
dt.head()


# In[37]:


dft = df.merge(dt, left_on='INFLOW_CD',  right_on='INFLOW_CD')


# In[38]:


dft.head()


# In[39]:


dg = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\parklist.csv", engine = 'python', encoding = 'cp949') 
dg.head()


# In[40]:


dftg = dft.merge(dg, left_on='ID',  right_on='ID')
dftg.head()


# In[48]:


del dftg['FID']


# In[44]:


del dftg['Unnamed: 0']


# In[45]:


dftg.head()


# In[47]:


del dftg['PARK_NAME_x']


# In[50]:


del dftg['AREA']


# In[51]:


del dftg['ADDR']


# In[54]:


dftg = dftg[['STD_YMD', 'total_visitor', 'INFLOW_CD', 'lat_x', 'long_x', 'PARK_NAME_y', 'lat_y', 'long_y']]


# In[55]:


dftg.head()


# In[58]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

dftg.to_csv(path + "st_park2020.csv", encoding = "CP949", single_file = True )


# In[ ]:


#################################################################################


# In[ ]:





# In[ ]:





# In[20]:


dt =df[['ID',  'PARK_NAME', 'INFLOW_CD']]
dt = dt. groupby('ID')


# In[57]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   

dt.to_csv(path + "skt2020_xy.csv", encoding = "CP949", single_file = True )

