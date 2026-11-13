#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import dask.dataframe as dd


# In[5]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[4]:


data = dd.read_csv("G:\\푸어지수\\국토교통부_건축물대장_층별개요(2016년+12월)\\mart_djy_04.csv",sep='|', engine="python", encoding="CP949")


# In[7]:


data


# In[10]:


df_check=data.isna()

check_for_any_nan= data.isna().values.any()


print(df_check)
print("NaN Presence:"+str(check_for_any_nan))
print ("Total Number of NaN values:"+str(total_nan_values))


# In[11]:


check_for_any_nan= data.isna().any().any()
total_nan_values = data.isna().sum().sum()

print(df_check)
print("NaN Presence:"+str(check_for_any_nan))
print ("Total Number of NaN values:"+str(total_nan_values))


# In[ ]:




