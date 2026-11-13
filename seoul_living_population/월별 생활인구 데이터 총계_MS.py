#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import datetime as dt


# In[2]:


path = "C:\Lab\Data\서울생활인구\집계구 단위\내국인\LOCAL_PEOPLE_201812/"
list_dir = os.listdir(path)
list_dir


# In[4]:


first_data = pd.read_csv(path + list_dir[0], engine="python", encoding="utf_8_sig")
for i in list_dir[1:]:
    try:
        temp_data = pd.read_csv(path + i, engine="python", encoding="utf_8_sig")
    except:
        temp_data = pd.read_csv(path + i, engine="python", encoding="CP949")
    first_data = first_data.append(temp_data)
    print(i)


# In[5]:


first_data.info(memory_usage='deep')


# In[6]:


print(first_data.iloc[0:3])
#print(first_data.iloc[0:3,3])
#print(first_data.iloc[459649:459653])


# In[7]:


first_data = first_data.replace(to_replace={'*':'0'})
#제공 데이터는 개인정보 비 식별화를 위하여 ‘3명’ 이하인 경우 “ * ” 처리.


# In[8]:


first_data["집계구코드"] = first_data["집계구코드"].astype(str)


# In[9]:


#집계구코드 = 읍면동코드(7)+대구역번호(2)+집계구일련번호(2)+집계구분할번호(2)
#32비트 이상의 오버플로우에 걸리는 문제를 피하기 위하여 읍면동 코드 전후로 분리
dong_cd = first_data.집계구코드.str[:7].astype(str)
gipgye_cd = first_data.집계구코드.str[7:].astype(str)
first_data.insert(4,column='dong_cd',value=dong_cd)
first_data.insert(5,column='gipgye_cd',value=gipgye_cd) 
print(first_data.iloc[0:3])


# In[ ]:


#data로 바꿔서 하면 좋을텐데 시간이 너무 오래 걸리네 
#아래에서 주말 비교를 수정하기
#date = first_data["기준일ID"].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
#first_data.insert(1,column='date', value=date)
#print(first_data.iloc[0:3])


# In[10]:


for i in first_data.columns[6:]:
    first_data[i] = first_data[i].astype(int)
    print("{} complete".format(i))


# In[11]:


first_data_analysis = first_data[["기준일ID", "시간대구분", "행정동코드", "집계구코드", "dong_cd", "gipgye_cd", "총생활인구수", "남자20세부터24세생활인구수", "남자25세부터29세생활인구수", "남자30세부터34세생활인구수", "남자35세부터39세생활인구수", "여자20세부터24세생활인구수", "여자25세부터29세생활인구수", "여자30세부터34세생활인구수", "여자35세부터39세생활인구수"]]
#print(first_data_analysis.iloc[0:3])


# In[12]:


young_list = list(first_data_analysis[['남자20세부터24세생활인구수', '남자25세부터29세생활인구수', '남자30세부터34세생활인구수', '남자35세부터39세생활인구수','여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수', '여자35세부터39세생활인구수']])
F_young_list = list(first_data_analysis[['여자20세부터24세생활인구수', '여자25세부터29세생활인구수', '여자30세부터34세생활인구수', '여자35세부터39세생활인구수']])

first_data_analysis["2~30대청년인구수"] = first_data_analysis[young_list].sum(axis=1)
first_data_analysis["2~30대여성인구수"] = first_data_analysis[F_young_list].sum(axis=1)
#print(first_data_analysis.iloc[0:3])

#빨간색 warning msg 뜨지만 무시하면 됨
#warning 없애고 싶다면 이런 식으로 합 구하기
#first_data_analysis.assign(청년인구수 = first_data_analysis.남자20세부터24세생활인구수 + first_data_analysis.남자25세부터29세생활인구수)


# In[13]:


first_data_analysis = first_data_analysis[["기준일ID", "시간대구분", "행정동코드", "집계구코드", "dong_cd", "gipgye_cd", "총생활인구수", "2~30대청년인구수", "2~30대여성인구수"]]
print(first_data_analysis.iloc[0:3])


# In[17]:


dt.datetime.today()
start_day =dt.date(2017,1,1)
end_day = dt.date(2018,12,31)
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


# In[18]:


print(weekend)


# In[19]:


first_data_analysis["weekends"] = np.where(first_data_analysis["기준일ID"].isin(weekend), "Y","N")


# In[20]:


print(first_data_analysis.iloc[0:3])


# In[21]:


first_data_analysis_weekend = first_data_analysis[(first_data_analysis["weekends"]=="Y")]
first_data_analysis_weekday = first_data_analysis[(first_data_analysis["weekends"]=="N")] 


# In[22]:


total_pivot = first_data_analysis.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "2~30대청년인구수", "2~30대여성인구수"]]
weekend_pivot = first_data_analysis_weekend.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "2~30대청년인구수", "2~30대여성인구수"]]
weekday_pivot = first_data_analysis_weekday.pivot_table(index="집계구코드", aggfunc="sum")[["총생활인구수", "2~30대청년인구수", "2~30대여성인구수"]]


# In[23]:


print(weekend_pivot)
print(weekday_pivot)


# In[24]:


total_pivot.to_csv(path + "total_pivot.csv", encoding="CP949")
weekend_pivot.to_csv(path + "weekend_pivot.csv", encoding="CP949")
weekday_pivot.to_csv(path + "weekday_pivot.csv", encoding="CP949")


# In[26]:


weekend_time_pivot = first_data_analysis_weekend.pivot_table(index=["행정동코드","dong_cd","gypgye_cd" "시간대구분"], values=["총생활인구수", "2~30대청년인구수", "2~30대여성인구수"], aggfunc=np.sum)
weekday_time_pivot = first_data_analysis_weekday.pivot_table(index=["행정동코드","dong_cd", "시간대구분"], values=["총생활인구수", "2~30대청년인구수", "2~30대여성인구수"], aggfunc=np.sum)


# In[32]:


print(weekend_time_pivot)
print(weekday_time_pivot)


# In[28]:


weekend_time_pivot.to_csv(path + "weekend_time_pivot.csv", encoding="CP949")
weekday_time_pivot.to_csv(path + "weekday_time_pivot.csv", encoding="CP949")


# In[29]:


weekend_time_F_pivot = first_data_analysis_weekend.pivot_table(index="시간대구분", columns="dong_cd", values="2~30대여성인구수", aggfunc=np.sum)
weekday_time_F_pivot = first_data_analysis_weekday.pivot_table(index="시간대구분", columns="dong_cd", values="2~30대여성인구수", aggfunc=np.sum)


# In[30]:


weekend_time_F_pivot.to_csv(path + "weekend_time_F_pivot.csv", encoding="CP949")
weekday_time_F_pivot.to_csv(path + "weekday_time_F_pivot.csv", encoding="CP949")

