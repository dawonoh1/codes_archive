#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


young = pd. read_csv("E:\\생활인구2020\\livingpop_\\minor.csv", engine = 'python')
young


# In[18]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# In[37]:


plt.title('청소년')
Young  = sns.barplot(x='기준일ID', y = '1019인구수', data = young, palette = 'summer')


# In[32]:


plt.title('청소년')
sns.lineplot(x='기준일ID', y='1019인구수', data=young, sort=False)


# In[33]:





# In[26]:


#Create combo chart
fig, ax1 = plt.subplots(figsize=(10,6))
color = 'tab:green'
#bar plot creation
ax1.set_title('청소년 공원 이용패턴', fontsize=16)
ax1.set_xlabel('기준일ID', fontsize=16)
ax1.set_ylabel('1019인구수', fontsize=16)
ax1 = sns.barplot(x='기준일ID', y='1019인구수', data = young , palette='summer')
ax1.tick_params(axis='y')
#specify we want to share the same x-axis
ax2 = ax1.twinx()
color = 'tab:red'
#line plot creation
ax2.set_ylabel('청소년 공원 이용패턴', fontsize=16)
ax2 = sns.lineplot(x='기준일ID', y='1019인구수', data = young, sort=False, color=color)
ax2.tick_params(axis='y', color=color)
#show plot
plt.show()


# In[ ]:




