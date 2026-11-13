#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


df = pd. read_csv("E:\\Dropbox\\Dropbox\\covid\\20201112 회의자료\\롯월성인.csv", engine = 'python')
df


# In[19]:


df[df['확진자수']]


# In[5]:


plt.title('롯데월드 성인')
sns.barplot(x='날짜', y='확진자수', data=df, palette='summer')


# In[20]:


sns.lineplot(x='날짜', y='2019', data=df, sort=False)


# In[14]:


#Create combo chart
fig, ax1 = plt.subplots(figsize=(10,6))
color = 'tab:green'
#bar plot creation
ax1.set_xlabel('날짜', fontsize=16)
ax1.set_ylabel('확진자수', fontsize=16)
ax1 = sns.barplot(x='날짜', y='확진자수', data = df, palette='summer')
ax1.tick_params(axis='y')
#specify we want to share the same x-axis
ax2 = ax1.twinx()
color = 'tab:red'
#line plot creation
ax2 = sns.lineplot(x='날짜', y='2020', data = df, sort=False, color=color)
ax2.tick_params(axis='y', color=color)
#show plot
plt.show()


# In[15]:


fig, ax1 = plt.subplots(figsize=(50,30))
color = 'tab:green' 
ax1.set_title('롯데월드 성인 인구', fontsize=16)
ax1.set_xlabel('날짜', fontsize=16)
ax1.set_ylabel('확진자수', fontsize=16, color=color)
ax2 = sns.barplot(x='날짜', y='확진자수', data = df, palette='summer')
ax1.tick_params(axis='x')
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('2020 성인인구', fontsize=16, color=color)
ax2 = sns.lineplot(x='날짜', y='2020', data = df, sort=False, color=color)
ax2.tick_params(axis='x', color=color)
plt.show()


# In[16]:


color = 'tab:red'

t = df[df['확진자수']]

ax1.set_xlabel('확진자')
ax1.set_ylabel('2020', color=color)
ax1.plot(t, df, color=color)
ax1.tick_params(axis='y', labelcolor=color)


# In[ ]:


# Create some mock data
t = np.arange(0.01, 10.0, 0.01)
data1 = np.exp(t)
data2 = np.sin(2 * np.pi * t)

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('exp', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
ax2.plot(t, data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

