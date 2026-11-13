#!/usr/bin/env python
# coding: utf-8

# In[8]:


import dask.dataframe as dd
import pandas as pd
import os
import numpy as np


# In[16]:


first_data = pd.read_csv("E:\\생활인구2020\\livingpop2020\\firstdata_2020.csv", engine = 'python', encoding ='CP949')
first_data.head()


# In[21]:


first_data = first_data.replace(to_replace={'*':'0'}) 

first_data["집계구코드"] = first_data["집계구코드"].astype(str)


# In[22]:


first_data_analysis = first_data
###

adult2034_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수']])
adult2034_male_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수']])
adult2034_female_list = list(first_data_analysis[['여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수']])

first_data_analysis["총2034인구수"] = first_data_analysis[adult2034_list].sum(axis=1)
first_data_analysis["남성2034인구수"] = first_data_analysis[adult2034_male_list].sum(axis=1)
first_data_analysis["여성2034인구수"] = first_data_analysis[adult2034_female_list].sum(axis=1)

###

adult3544_list = list(first_data_analysis[['남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '여자35세부터39세생활인구수', '여자40세부터44세생활인구수']])
adult3544_male_list = list(first_data_analysis[['남자35세부터39세생활인구수', '남자40세부터44세생활인구수']])
adult3544_female_list = list(first_data_analysis[['여자35세부터39세생활인구수', '여자40세부터44세생활인구수']])

first_data_analysis["총3544인구수"] = first_data_analysis[adult3544_list].sum(axis=1)
first_data_analysis["남성3544인구수"] = first_data_analysis[adult3544_male_list].sum(axis=1)
first_data_analysis["여성3544인구수"] = first_data_analysis[adult3544_female_list].sum(axis=1)

###

adult4554_list = list(first_data_analysis[['남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수']])
adult4554_male_list = list(first_data_analysis[['남자45세부터49세생활인구수', '남자50세부터54세생활인구수']])
adult4554_female_list = list(first_data_analysis[['여자45세부터49세생활인구수', '여자50세부터54세생활인구수']])

first_data_analysis["총4554인구수"] = first_data_analysis[adult4554_list].sum(axis=1)
first_data_analysis["남성4554인구수"] = first_data_analysis[adult4554_male_list].sum(axis=1)
first_data_analysis["여성4554인구수"] = first_data_analysis[adult4554_female_list].sum(axis=1)

###

adult5564_list = list(first_data_analysis[['남자55세부터59세생활인구수', '남자60세부터64세생활인구수', '여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])
adult5564_male_list = list(first_data_analysis[['남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])
adult5564_female_list = list(first_data_analysis[['여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])

first_data_analysis["총5564인구수"] = first_data_analysis[adult5564_list].sum(axis=1)
first_data_analysis["남성5564인구수"] = first_data_analysis[adult5564_male_list].sum(axis=1)
first_data_analysis["여성5564인구수"] = first_data_analysis[adult5564_female_list].sum(axis=1)


# In[24]:


##

adult2034_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["총2034인구수", "남성2034인구수", "여성2034인구수"], aggfunc=np.sum)
adult3544_pivot = first_data_analysis.pivot_table(index=["집계구코드","기준일ID"], values=["총3544인구수", "남성3544인구수", "여성3544인구수"], aggfunc=np.sum)
adult4554_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["총4554인구수", "남성4554인구수", "여성4554인구수"], aggfunc=np.sum)
adult5564_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["총5564인구수", "남성5564인구수", "여성5564인구수"], aggfunc=np.sum)
###

adult2034_pivot.to_csv("adult2034.csv", encoding="CP949")
adult3544_pivot.to_csv("adult3544.csv", encoding="CP949")
adult4554_pivot.to_csv("adult4554.csv", encoding="CP949")
adult5564_pivot.to_csv("adult5564.csv", encoding="CP949")


# In[25]:


adult_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '남자55세부터59세생활인구수', '남자60세부터64세생활인구수','여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수', '여자35세부터39세생활인구수', '여자40세부터44세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수', '여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])
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

old_list = list(first_data_analysis[['남자65세부터69세생활인구수','여자65세부터69세생활인구수']])
old_female_list = list(first_data_analysis[['여자65세부터69세생활인구수']])
old_male_list = list(first_data_analysis[['남자65세부터69세생활인구수']])

first_data_analysis["6569인구수"] = first_data_analysis[old_list].sum(axis=1)
first_data_analysis["6569여성인구수"] = first_data_analysis[old_female_list].sum(axis=1)
first_data_analysis["6569남성인구수"] = first_data_analysis[old_male_list].sum(axis=1)

###

total_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["총성인인구수", "남성성인인구수", "여성성인인구수"], aggfunc=np.sum)
young_pivot = first_data_analysis.pivot_table(index=["집계구코드","기준일ID"], values=["1019인구수","1019여성인구수", "1019남성인구수"], aggfunc=np.sum)
old_pivot = first_data_analysis.pivot_table(index=["집계구코드", "기준일ID"], values=["6569인구수", "6569여성인구수", "6569남성인구수"], aggfunc=np.sum)

###

total_pivot.to_csv("adult.csv", encoding="CP949")
young_pivot.to_csv("minor.csv", encoding="CP949")
old_pivot.to_csv("elderly.csv", encoding="CP949")


# In[ ]:




