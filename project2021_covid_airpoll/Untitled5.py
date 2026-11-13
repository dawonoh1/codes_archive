#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dask.dataframe as dd

import pandas as pd
import numpy as np
import os


# In[10]:


path = "E:\\Dropbox\\Dropbox\\covid\\데이터\\2019년 서울시 공원 데이터/" 
list_dir = os.listdir(path)
list_dir


# In[11]:


first_data = pd.read_csv(path + list_dir[2], engine="python", encoding="utf_8_sig", sep='|')

for i in list_dir[3:]:
    try:
        temp_data = pd.read_csv(path + i, engine="python", encoding="CP949", sep='|')
    except:
        temp_data = pd.read_csv(path + i, engine="python", encoding="utf_8_sig", sep='|')
    first_data = first_data.append(temp_data)
    print(i)


# In[12]:


first_data


# In[13]:


first_data = first_data.replace(to_replace={'*':'0'}) 

first_data[["ID", "STD_YM", "STD_YMD", "PARK_NAME", "INFLOW_CD"]] = first_data[["ID", "STD_YM", "STD_YMD", "PARK_NAME", "INFLOW_CD"]].astype(str)


# In[14]:


for i in first_data.columns[5:]:
    first_data[i] = first_data[i].astype(int)
    print("{} complete".format(i))


# In[15]:


import numpy as np

pivot = first_data.pivot_table(index=["ID", "STD_YM", "STD_YMD", "PARK_NAME"], values=["M_0009", "M_1014", "M_1519", "M_2024", "M_2529",  "M_3034", "M_3539", "M_4044", "M_4549", "M_5054", "M_5559", "M_6064", "M_6569", "M_7000", "W_0009", "W_1014", "W_1519", "W_2024", "W_2529", "W_3034", "W_3539", "W_4044", "W_4549", "W_5054", "W_5559", "W_6064", "W_6569", "W_7000"], aggfunc=np.sum)


# In[16]:


pivot


# In[17]:


pivot.to_csv(path + "skt2019sum.csv", encoding="CP949")


# In[ ]:




