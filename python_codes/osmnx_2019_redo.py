#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install osmnx==1.5.1')


# In[3]:


import numpy as np
import osmnx as ox

get_ipython().run_line_magic('matplotlib', 'inline')
np.random.seed(0)
ox.__version__


# In[4]:


import os
import csv
import networkx as nx
import numpy as np
import pandas as pd
import sklearn
# import osm
from osmnx import distance

ox.config(use_cache=True, log_console=True)

# network_type은 walk로 한다
graph = ox.graph_from_place('Seoul, South Korea', network_type='walk', simplify=True)
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# impute missing edge speeds and add travel times
graph = ox.add_edge_speeds(graph)
graph = ox.add_edge_travel_times(graph)

fig, ax = ox.plot_graph(graph, node_color='r')


# In[5]:


ox.config(use_cache=True, log_console=True)

# network_type은 walk로 한다
graph = ox.graph_from_place('Seoul, South Korea', network_type='drive', simplify=True)
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# impute missing edge speeds and add travel times
graph = ox.add_edge_speeds(graph)
graph = ox.add_edge_travel_times(graph)

fig, ax = ox.plot_graph(graph, node_color='r')


# In[ ]:




