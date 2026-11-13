#!/usr/bin/env python
# coding: utf-8

# In[6]:


import dask.dataframe as dd
import os


# In[7]:


path = "E:\\생활인구2019\\livingpop2019/" 
list_dir = os.listdir(path)
list_dir


# In[8]:


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


# In[9]:


first_data.head()


# In[10]:


first_data.to_csv("firstdata20191.csv")


# In[9]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[13]:


del first_data['?"기준일ID"']
first_data


# In[ ]:





# In[ ]:





# In[ ]:





# In[16]:


df = dd.read_csv("E:\생활인구2019\livingpop2019\LOCAL_PEOPLE_20190902.csv", engine = 'python', encoding ='CP949')
df


# In[17]:


df1 = dd.read_csv("E:\생활인구2019\livingpop2019\LOCAL_PEOPLE_20190903.csv", engine = 'python', encoding ='CP949')
df1


# In[18]:


df2 = dd.read_csv("E:\생활인구2019\livingpop2019\LOCAL_PEOPLE_20190904.csv", engine = 'python', encoding ='CP949')
df2


# In[19]:


df = df.append(df1)
df = df.append(df2)
df


# In[20]:


df.head()


# In[ ]:




