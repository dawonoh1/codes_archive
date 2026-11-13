#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas import read_csv
from datetime import datetime

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from dask.diagnostics import ProgressBar

pbar = ProgressBar()
pbar.register()


# In[3]:


import pandas as pd
import dask.dataframe as dd

dataset = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\ds_lstm.csv", engine = 'python',  encoding="CP949", index_col=0)
dataset.drop('No', axis=1, inplace=True)


# In[4]:


dataset = dataset[['STD_YMD', 'distance', 'M_0009', 'M_1014', 'M_1519', 'M_2024', 'M_2529', 'M_3034', 'M_3539', 'M_4044', 'M_4549', 'M_5054', 'M_5559', 'M_6064', 'M_6569', 'M_7000', 'W_0009', 'W_1014', 'W_1519', 'W_2024', 'W_2529', 'W_3034', 'W_3539', 'W_4044', 'W_4549', 'W_5054', 'W_5559', 'W_6064', 'W_6569', 'W_7000']]


# In[5]:


dataset.head()


# In[6]:


dataset.index.name = 'date'

dataset['pollution'].fillna(0, inplace=True)

dataset = dataset[24:]

print(dataset.head(5))


# In[30]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
dataset.to_csv(path + "ds_lstm.csv", encoding = "CP949", single_file = True )


# In[7]:


dataset.index.name = 'STD_YMD'


# In[8]:


dataset.head()


# In[9]:


dataset.columns =['STD_YMD', 'distance', 'M_0009', 'M_1014', 'M_1519', 'M_2024', 'M_2529', 'M_3034', 'M_3539', 'M_4044', 'M_4549', 'M_5054', 'M_5559', 'M_6064', 'M_6569', 'M_7000', 'W_0009', 'W_1014', 'W_1519', 'W_2024', 'W_2529', 'W_3034', 'W_3539', 'W_4044', 'W_4549', 'W_5054', 'W_5559', 'W_6064', 'W_6569', 'W_7000']
dataset.index.name = 'STD_YMD'


# In[10]:


dataset['distance'].fillna(0)


# In[37]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
dataset.to_csv(path + "ds_lstm_1.csv", encoding = "CP949", single_file = True )


# In[41]:


dataset = dd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\ds_lstm.csv", header=0)
dataset.head()


# In[42]:


del dataset[['Unnamed: 0']]


# In[ ]:





# In[11]:


values = dataset.values

values


# In[16]:


groups = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
i = 1


# In[18]:


# plot column
plt.figure()
for group in groups:
    plt.subplot(len(groups), 1, i)
    plt.plot(values[:, group])
    plt.title(dataset.columns[group], y=0.5, loc='right')
    i += 1
plt.show()


# In[50]:


import tensorflow as tf
from tensorflow import keras

import tensorflow
import tensorflow.keras


# In[51]:


from math import sqrt
from numpy import concatenate
from matplotlib import pyplot

from pandas import read_csv
from pandas import DataFrame
from pandas import concat

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error


# In[52]:


from tensorflow.keras import backend
from keras import backend

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


# In[53]:


# series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    
    cols, names = list(), list()
    
    # input order (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    
    #  forecasting order (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    
    # aggregate
    agg = concat(cols, axis=1)
    agg.columns = names
    
    # drop NaN row
    if dropnan:
        agg.dropna(inplace=True)
        
    return agg


# In[54]:


# load dataset
import pandas as pd
dataset = pd. read_csv("E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\ds_lstm.csv", header=0)
values = dataset.values


# In[55]:


dataset


# In[72]:


del dataset['Unnamed: 0']


# In[73]:


dataset['distance'].fillna(0, inplace=True)


# In[74]:


dataset


# In[76]:


df_i = dataset.set_index('STD_YMD')
df_i


# In[80]:


path = "E:\\Dropbox\\Dropbox\\21_1학기수업\\AI/"   
df_i.to_csv(path + "ds_lstm_train.csv", encoding = "CP949")


# In[82]:


# load dataset
dataset = read_csv('E:\\Dropbox\\Dropbox\\21_1학기수업\\AI\\ds_lstm_train.csv', header=0, index_col=0)
values = dataset.values

# Converts a character to an integer starting from 0
encoder = LabelEncoder()
values[:,4] = encoder.fit_transform(values[:,4])

# data type: float
values = values.astype('float32')

# features normalization
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

# frame supervised learning (function)
reframed = series_to_supervised(scaled, 1, 1)


# Remove columns not to be predicted
reframed.drop(reframed.columns[[30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57 ]], axis=1, inplace=True)

print('======================= reframed ==========================')
print(reframed.head())


# In[83]:


# split train and test sets
values = reframed.values
n_train_days = 31
train = values[:n_train_days, :]
test = values[n_train_days:, :]

print('======================== reframed ==========================')
print(len(train))
print(len(test))


# In[84]:


# split input and output
train_X, train_y = train[:, :-1], train[:, -1]
test_X, test_y = test[:, :-1], test[:, -1]

print('================ shape of train_X ==========================')
print(train_X.shape)
print(train_X[:5])


# In[85]:


train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))

print('================ reshape 후 train_X 의 shape ===============')
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)


# In[86]:


# network design
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')


# In[87]:


# fit network
history = model.fit(train_X, train_y, epochs=200, batch_size=50, validation_data=(test_X, test_y), verbose=2, shuffle=False)


# In[88]:


# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()


# In[89]:


# make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))


# In[90]:


# invert scaling for forecast
inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0]


# In[91]:


# invert scaling for actual
test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,0]


# In[92]:


# RMSE(Root Mean Square Error)
rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
print('예측성능 비교지표 RMSE: %.3f' % rmse)


# In[ ]:




