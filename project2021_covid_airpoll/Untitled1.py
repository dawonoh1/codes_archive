#!/usr/bin/env python
# coding: utf-8

# In[25]:


import dask.dataframe as dd
import pandas as pd
import os
import numpy as np


# In[38]:


path = "E:\\생활인구2020\\livingpop2020\\notok/" 
list_dir = os.listdir(path)
list_dir


# In[39]:


first_data = dd.read_csv(path + list_dir[0], engine="python", encoding="CP949")
values=[1124080020103, 1124059010001]
first_data = first_data[first_data.집계구코드.isin(values)]

for i in list_dir[2:]:
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


# In[31]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[ ]:


first_data.to_csv(path + "firstdata_2020_test.csv", encoding = "CP949", single_file = True )


# In[ ]:





# In[ ]:





# In[40]:


first_data = first_data.astype(float)


# In[41]:


first_data = first_data.replace(to_replace={'*':'0'}) 

first_data["집계구코드"] = first_data["집계구코드"].astype(str)


# In[43]:


first_data


# In[22]:


first_data= first_data.rename(columns={'?"기준일ID"' : '기준일ID1'})

first_data.head()


# In[ ]:


first_data= first_data.rename(columns={'기준일ID1': '기준일ID'})

first_data.head()


# In[ ]:


for i in first_data.columns[5:]:
    first_data[i] = first_data[i].astype(float)
    print("{} complete".format(i))


# In[ ]:


first_data.head()

