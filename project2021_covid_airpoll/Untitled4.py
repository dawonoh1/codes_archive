#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

from urllib.request import urlopen
from urllib import parse
from urllib.request import Request
from urllib.error import HTTPError


# In[2]:


from bs4 import BeautifulSoup

import json


# In[3]:


## naver api

client_id = 'YOUR_NAVER_CLIENT_ID'
client_pw = 'YOUR_NAVER_CLIENT_SECRET'

api_url ='https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='


# In[20]:


data = pd.read_excel("E:\\Dropbox\\Dropbox\\covid\\20210509 회의자료\\park425.xlsx",  usecols = 'b, c', names = ['구주소', '도로명주소'])


# In[ ]:


# 네이버 지도 API 이용해서 위경도 찾기
geo_coordi = []    # geographic coordinates
for add in data['구주소']:
    add_urlenc= parse.quote(add)   # 주소를 URL에서 사용할 수 있도록 URL Encoding
    url = api_url + add_urlenc
    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_pw)
    try:
        response = urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    except IndexError:
        print('IndexError')
    else:
        rescode = response.getcode()  # 정상이면 200 리턴
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)   # json
            if 'addresses' in response_body:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                print("Success!")
            else:
                print("'result' not exist!")
                latitude = None
                longitude = None
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None

    geo_coordi.append([latitude, longitude])

np_geo_coordi = np.array(geo_coordi)
pd_geo_coordi = pd.DataFrame({"구주소": data['구주소'].values,
                              "도로명": data['도로명주소'].values,
                              "위도": np_geo_coordi[:, 0],
                              "경도": np_geo_coordi[:, 1]})

