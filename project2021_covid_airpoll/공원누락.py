#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
import os


# In[38]:


path = "E:\\생활인구2020\\extra/" 
list_dir = os.listdir(path)
list_dir


# In[39]:


first_data = pd.read_csv(path + list_dir[0], engine="python", encoding="CP949")
for i in list_dir[1:]:
    try:
        temp_data = pd.read_csv(path + i, engine="python", encoding="CP949")
    except:
        temp_data = pd.read_csv(path + i, engine="python", encoding="utf_8_sig")
    first_data = first_data.append(temp_data)
    print(i)


# In[40]:


first_data 


# In[36]:


first_data [first_data [‘집계구코드’].isin(['1124059010001'])]
first_data 


# In[ ]:





# In[23]:


first_data = first_data.replace(to_replace={'*':'0'}) 

first_data["집계구코드"] = first_data["집계구코드"].astype(str)


# In[ ]:





# In[ ]:





# In[24]:


first_data 


# In[25]:


for i in first_data.columns[6:]:
    first_data[i] = first_data[i].astype(int)
    print("{} complete".format(i))


# In[12]:


first_data


# In[13]:


first_data= first_data.rename({'?"기준일ID"' : '기준일ID'}, axis = 'columns')
first_data


# In[14]:


first_data_analysis = first_data
###

adult_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])
male_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])
female_list = list(first_data_analysis[['여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수', '여자35세부터39세생활인구수', '여자40세부터44세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수', '여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])

first_data_analysis["총성인인구수"] = first_data_analysis[adult_list].sum(axis=1)
first_data_analysis["남성성인인구수"] = first_data_analysis[male_list].sum(axis=1)
first_data_analysis["여성성인인구수"] = first_data_analysis[female_list].sum(axis=1)

###

young_list = list(first_data_analysis[['남자10세부터14세생활인구수', '남자15세부터19세생활인구수','여자10세부터14세생활인구수', '여자15세부터19세생활인구수']])
young_female_list = list(first_data_analysis[['여자10세부터14세생활인구수', '여자15세부터19세생활인구수']])
young_male_list = list(first_data_analysis[['남자10세부터14세생활인구수', '남자15세부터19세생활인구수']])

first_data_analysis["1019인구수"] = first_data_analysis[young_list].sum(axis=1)
first_data_analysis["1019여성인구수"] = first_data_analysis[young_female_list].sum(axis=1)
first_data_analysis["1019남성인구수"] = first_data_analysis[young_male_list].sum(axis=1)

###

young_list = list(first_data_analysis[['남자65세부터69세생활인구수','여자65세부터69세생활인구수']])
young_female_list = list(first_data_analysis[['여자65세부터69세생활인구수']])
young_male_list = list(first_data_analysis[['남자65세부터69세생활인구수']])

first_data_analysis["6569인구수"] = first_data_analysis[young_list].sum(axis=1)
first_data_analysis["6569여성인구수"] = first_data_analysis[young_female_list].sum(axis=1)
first_data_analysis["6569남성인구수"] = first_data_analysis[young_male_list].sum(axis=1)

###

total_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["총성인인구수", "남성성인인구수", "여성성인인구수"], aggfunc=np.sum)
young_pivot = first_data_analysis.pivot_table(index=["집계구코드","기준일ID"], values=["1019인구수","1019여성인구수", "1019남성인구수"], aggfunc=np.sum)
old_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["6569인구수", "6569여성인구수", "6569남성인구수"], aggfunc=np.sum)

###

total_pivot.to_csv(path + "adult.csv", encoding="CP949")
young_pivot.to_csv(path + "minor.csv", encoding="CP949")
old_pivot.to_csv(path + "elderly.csv", encoding="CP949")


# In[ ]:




