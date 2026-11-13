#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dask.dataframe as dd
import pandas as pd
import os


# In[9]:


path = "E:\\생활인구2020\\livingpop_/" 
list_dir = os.listdir(path)
list_dir


# In[10]:


first_data = dd.read_csv(path + list_dir[0], engine="python", encoding="utf_8_sig")
values=[1124080020103, 1124059010001]
first_data = first_data[first_data.집계구코드.isin(values)]

for i in list_dir[1:]:
    try:
        temp_data = dd.read_csv(path + i, engine="python", encoding="CP949")
        values=[1124080020103, 1124059010001]
        temp_data = temp_data[temp_data.집계구코드.isin(values)]
    except:
        temp_data = dd.read_csv(path + i, engine="python", encoding="utf_8_sig")
        values=[1124080020103, 1124059010001]
        temp_data = temp_data[temp_data.집계구코드.isin(values)]
    first_data = first_data.append(temp_data)
    print(i)


# In[11]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[12]:


first_data = first_data.replace(to_replace={'*':'0'}) 


# In[13]:


first_data.head()


# In[14]:


first_data.to_csv(path + "firstdata2020.csv", encoding = "CP949", single_file = True )


# In[ ]:




