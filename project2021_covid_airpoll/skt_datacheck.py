#!/usr/bin/env python
# coding: utf-8

# In[42]:


import pandas as pd
import numpy as np
import os


# In[74]:


path = "E:\\Dropbox\\Dropbox\\covid\\데이터\\2020년 서울시 공원 데이터/" 
list_dir = os.listdir(path)
list_dir


# In[75]:


first_data = pd.read_csv(path + list_dir[0], engine="python", encoding="utf_8_sig", sep='|')

for i in list_dir[1:]:
    try:
        temp_data = pd.read_csv(path + i, engine="python", encoding="CP949", sep='|')
    except:
        temp_data = pd.read_csv(path + i, engine="python", encoding="utf_8_sig", sep='|')
    first_data = first_data.append(temp_data)
    print(i)


# In[76]:


first_data.to_csv(path + "2020skt.csv", encoding="CP949")


# In[77]:


df_check=first_data.isna()

check_for_any_nan= first_data.isna().values.any()

print(df_check)
print("NaN Presence:"+str(check_for_any_nan))
print ("Total Number of NaN values:"+str(total_nan_values))


# In[78]:


check_for_any_nan= first_data.isna().any().any()
total_nan_values = first_data.isna().sum().sum()

print(df_check)
print("NaN Presence:"+str(check_for_any_nan))
print ("Total Number of NaN values:"+str(total_nan_values))


# In[ ]:




