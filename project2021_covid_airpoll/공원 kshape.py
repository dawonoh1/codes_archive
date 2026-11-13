#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy
import matplotlib.pyplot as plt

from tslearn.clustering import KShape
from tslearn.datasets import CachedDatasets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance


# In[2]:


seed = 0
numpy.random.seed(seed)
X_train, y_train, X_test, y_test = CachedDatasets().load_dataset("Trace")

# Keep first 3 classes and 50 first time series
X_train = X_train[y_train < 4]
X_train = X_train[:50]
numpy.random.shuffle(X_train)

# For this method to operate properly, prior scaling is required
X_train = TimeSeriesScalerMeanVariance().fit_transform(X_train)
sz = X_train.shape[1]


# In[3]:


# kShape clustering
ks = KShape(n_clusters=3, verbose=True, random_state=seed)
y_pred = ks.fit_predict(X_train)


# In[11]:


import pandas as pd
filenames = pd.read_csv("E:\\Dropbox\\Dropbox\\covid\\20210311 회의자료\\shp70pivot.csv", engine= 'python', encoding = 'CP949')
filenames


# In[12]:


filenames = filenames.set_index('LABEL')
filenames


# In[13]:


ks = KShape(n_clusters=3, n_init=100, verbose=True, random_state=seed)
y_pred = ks.fit_predict(filenames)


# In[17]:


plt.figure()
for yi in range(3):
    plt.subplot(3, 1, 1 + yi)
    for xx in X_train:
        plt.plot(xx.ravel(), "k-", alpha=.1)
    plt.plot(ks.cluster_centers_[yi].ravel(), "r-")
    plt.xlim(0, 351)
    plt.ylim(-4, 4)
    plt.title("Cluster %d" % (yi + 1))
    
    plt.rcParams['figure.figsize']=[10,6]


# In[15]:


from kshape.core import kshape, zscore


# In[16]:


time_series = [[1,2,3,4], [0,1,2,3], [0,1,2,3], [1,2,2,3]]
cluster_num = 2
clusters = kshape(zscore(time_series, axis=1), cluster_num)
clusters


# In[18]:


import pandas as pd
filenames = pd.read_csv("E:\\Dropbox\\Dropbox\\covid\\20210311 회의자료\\shp70pivot.csv", engine= 'python', encoding = 'CP949')
filenames


# In[ ]:


# assuming the time series are stored in a tab seperated file, where `time` is
# the name of the column containing the timestamp
df = pd.read_csv(filename, sep="\t", index_col='time', parse_dates=True)
# use a meaningful sample size depending on how the frequency of your time series:
# Higher is more accurate, but if series gets too long, the calculation gets cpu and memory intensive.
# Keeping the length below 2000 values is usually a good idea.
df = df.resample("500ms").mean()

