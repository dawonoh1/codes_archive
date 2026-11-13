#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import datetime as dt


# In[35]:


path = "E:\\생활인구2019\\LOCAL_PEOPLE_201909/" 
list_dir = os.listdir(path)
list_dir


# In[36]:


first_data = pd.read_csv(path + list_dir[0], engine="python", encoding="utf_8_sig")
for i in list_dir[1:]:
    try:
        temp_data = pd.read_csv(path + i, engine="python", encoding="CP949")
    except:
        temp_data = pd.read_csv(path + i, engine="python", encoding="utf_8_sig")
    first_data = first_data.append(temp_data)
    print(i)


# In[37]:


first_data.info(memory_usage='deep')


# In[38]:


print(first_data.iloc[0:3])


# In[39]:


first_data = first_data.replace(to_replace={'*':'0'})


# In[45]:


# 2019년 9월은 일부 컬럼에서 NaN값이 있으니까 0으로 대체해주자

first_data['여자50세부터54세생활인구수'] = first_data['여자50세부터54세생활인구수'].fillna(0)
first_data['여자55세부터59세생활인구수'] = first_data['여자55세부터59세생활인구수'].fillna(0)
first_data['여자60세부터64세생활인구수'] = first_data['여자60세부터64세생활인구수'].fillna(0)
first_data['여자65세부터69세생활인구수'] = first_data['여자65세부터69세생활인구수'].fillna(0)
first_data['여자70세이상생활인구수'] = first_data['여자70세이상생활인구수'].fillna(0)


# In[49]:


###0으로 대체하면 불린 되니까 바꿔주기

first_data[["총생활인구수", "남자20세부터24세생활인구수", "남자25세부터29세생활인구수", "남자30세부터34세생활인구수", "남자35세부터39세생활인구수", "남자40세부터44세생활인구수", "남자45세부터49세생활인구수", "남자50세부터54세생활인구수", "남자55세부터59세생활인구수", "남자60세부터64세생활인구수", "남자65세부터69세생활인구수", "여자20세부터24세생활인구수",  "여자25세부터29세생활인구수", "여자30세부터34세생활인구수", "여자35세부터39세생활인구수", "여자40세부터44세생활인구수", "여자45세부터49세생활인구수", "여자50세부터54세생활인구수", "여자55세부터59세생활인구수", "여자60세부터64세생활인구수", "여자65세부터69세생활인구수"]] = first_data[["총생활인구수", "남자20세부터24세생활인구수", "남자25세부터29세생활인구수", "남자30세부터34세생활인구수", "남자35세부터39세생활인구수", "남자40세부터44세생활인구수", "남자45세부터49세생활인구수", "남자50세부터54세생활인구수", "남자55세부터59세생활인구수", "남자60세부터64세생활인구수", "남자65세부터69세생활인구수", "여자20세부터24세생활인구수",  "여자25세부터29세생활인구수", "여자30세부터34세생활인구수", "여자35세부터39세생활인구수", "여자40세부터44세생활인구수", "여자45세부터49세생활인구수", "여자50세부터54세생활인구수", "여자55세부터59세생활인구수", "여자60세부터64세생활인구수", "여자65세부터69세생활인구수"]].astype(float)


# In[46]:


first_data["집계구코드"] = first_data["집계구코드"].astype(str)


# In[43]:


first_data.isna().any()


# In[50]:


for i in first_data.columns[4:]:
    first_data[i] = first_data[i].astype(int)
    print("{} complete".format(i))


# In[24]:


first_data


# In[51]:


first_data_analysis = first_data[["기준일ID", "시간대구분", "행정동코드", "집계구코드", "총생활인구수", "남자20세부터24세생활인구수", "남자25세부터29세생활인구수", "남자30세부터34세생활인구수", "남자35세부터39세생활인구수", "남자40세부터44세생활인구수", "남자45세부터49세생활인구수", "남자50세부터54세생활인구수", "남자55세부터59세생활인구수", "남자60세부터64세생활인구수", "남자65세부터69세생활인구수", "여자20세부터24세생활인구수",  "여자25세부터29세생활인구수", "여자30세부터34세생활인구수", "여자35세부터39세생활인구수", "여자40세부터44세생활인구수", "여자45세부터49세생활인구수", "여자50세부터54세생활인구수", "여자55세부터59세생활인구수", "여자60세부터64세생활인구수", "여자65세부터69세생활인구수"]]

###총성인

adult_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])
male_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])
female_list = list(first_data_analysis[['여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수', '여자35세부터39세생활인구수', '여자40세부터44세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수', '여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])

first_data_analysis["총성인인구수"] = first_data_analysis[adult_list].sum(axis=1)
first_data_analysis["남성성인인구수"] = first_data_analysis[male_list].sum(axis=1)
first_data_analysis["여성성인인구수"] = first_data_analysis[female_list].sum(axis=1)

###청년

FM_young_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수']])
F_young_list = list(first_data_analysis[['여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수']])
M_young_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수']])

first_data_analysis["2034청년인구수"] = first_data_analysis[FM_young_list].sum(axis=1)
first_data_analysis["2034여성인구수"] = first_data_analysis[F_young_list].sum(axis=1)
first_data_analysis["2034남성인구수"] = first_data_analysis[M_young_list].sum(axis=1)

###중년

FM_old_list = list(first_data_analysis[['남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수', '여자35세부터39세생활인구수', '여자40세부터44세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수']])
F_old_list = list(first_data_analysis[['여자35세부터39세생활인구수', '여자40세부터44세생활인구수', '여자45세부터49세생활인구수', '여자50세부터54세생활인구수']])
M_old_list = list(first_data_analysis[['남자35세부터39세생활인구수', '남자40세부터44세생활인구수', '남자45세부터49세생활인구수', '남자50세부터54세생활인구수']])

first_data_analysis["3554중년인구수"] = first_data_analysis[FM_old_list].sum(axis=1)
first_data_analysis["3554여성인구수"] = first_data_analysis[F_old_list].sum(axis=1)
first_data_analysis["3554남성인구수"] = first_data_analysis[M_old_list].sum(axis=1)

###베이비부머

FM_old_list = list(first_data_analysis[['남자55세부터59세생활인구수', '남자60세부터64세생활인구수', '여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])
F_old_list = list(first_data_analysis[['여자55세부터59세생활인구수', '여자60세부터64세생활인구수']])
M_old_list = list(first_data_analysis[['남자55세부터59세생활인구수', '남자60세부터64세생활인구수']])

first_data_analysis["5564노년인구수"] = first_data_analysis[FM_old_list].sum(axis=1)
first_data_analysis["5564여성인구수"] = first_data_analysis[F_old_list].sum(axis=1)
first_data_analysis["5564남성인구수"] = first_data_analysis[M_old_list].sum(axis=1)


# In[52]:


first_data_analysis = first_data_analysis[["기준일ID", "시간대구분", "행정동코드", "집계구코드", "총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"]]
print(first_data_analysis.iloc[0:3])


# In[53]:


dt.datetime.today()
start_day =dt.date(2019,1,1)
end_day = dt.date(2019,12,31)
gap = end_day - start_day
gap.days

#this_day= start_day + dt.timedelta(5)
#this_day.weekday()

weekend =[]
for i in range(gap.days):
    this_day = start_day + dt.timedelta(i)
    i +=1
    if this_day.weekday() > 4:
        weekend.append(this_day.strftime("%Y%m%d"))
#print(weekend)


# In[54]:


print(weekend)


# In[55]:


first_data_analysis["weekends"] = np.where(first_data_analysis["기준일ID"].isin(weekend), "Y","N")


# In[56]:


print(first_data_analysis.iloc[0:3])


# In[57]:


first_data_analysis_weekend = first_data_analysis[(first_data_analysis["weekends"]=="Y")]
first_data_analysis_weekday = first_data_analysis[(first_data_analysis["weekends"]=="N")] 


# In[58]:


total_pivot = first_data_analysis.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"]]
weekend_pivot = first_data_analysis_weekend.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"]]
weekday_pivot = first_data_analysis_weekday.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"]]


# In[34]:


print(weekend_pivot)
print(weekday_pivot)


# In[277]:


total_pivot.to_csv(path + "total_pivot.csv", encoding="CP949")
weekend_pivot.to_csv(path + "weekend_pivot.csv", encoding="CP949")
weekday_pivot.to_csv(path + "weekday_pivot.csv", encoding="CP949")


# In[278]:


weekend_time_pivot = first_data_analysis_weekend.pivot_table(index=["집계구코드", "시간대구분"], values=["총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"], aggfunc=np.sum)
weekday_time_pivot = first_data_analysis_weekday.pivot_table(index=["집계구코드", "시간대구분"], values=["총생활인구수", "총성인인구수", "남성성인인구수", "여성성인인구수", "2034청년인구수", "2034여성인구수", "2034남성인구수", "3554중년인구수", "3554여성인구수", "3554남성인구수", "5564노년인구수", "5564여성인구수", "5564남성인구수"], aggfunc=np.sum)


# In[279]:


print(weekend_time_pivot)
print(weekday_time_pivot)


# In[280]:


weekend_time_pivot.to_csv(path + "weekend_time_pivot.csv", encoding="CP949")
weekday_time_pivot.to_csv(path + "weekday_time_pivot.csv", encoding="CP949")


# In[ ]:





# In[ ]:





# In[ ]:


del first_data['?"기준일ID"']
first_data


# In[ ]:


###

total_pivot = first_data_analysis.pivot_table(index=["집계구코드", "시간대구분"], values=["총성인인구수", "남성성인인구수", "여성성인인구수"], aggfunc=np.sum)
young_pivot = first_data_analysis.pivot_table(index=["집계구코드", "시간대구분"], values=["2034청년인구수","2034여성인구수", "2034남성인구수"], aggfunc=np.sum)
old_pivot = first_data_analysis.pivot_table(index=["집계구코드", "시간대구분"], values=["3554중년인구수", "3554여성인구수", "3554남성인구수"], aggfunc=np.sum)
boom_pivot = first_data_analysis.pivot_table(index=["집계구코드", "시간대구분"], values=["5564노년인구수", "5564여성인구수", "5564남성인구수"], aggfunc=np.sum)

###

total_pivot.to_csv(path + "total_pivot_2019.csv", encoding="CP949")
young_pivot.to_csv(path + "young_pivot_2019.csv", encoding="CP949")
old_pivot.to_csv(path + "old_pivot_2019.csv", encoding="CP949")  
boom_pivot.to_csv(path + "boom_pivot_2019.csv", encoding="CP949")  

