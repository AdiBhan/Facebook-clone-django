#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:14:51 2024

@author: azs
"""

import math
import plotly
import plotly.graph_objs as go

# generate some data
x = [i/10 for i in range(100)]
y = [math.sin(v) for v in x]

# check the data!
# print(f'x={x}')
# print(f'y={y}')


fig = go.Scatter(x=x, y=y)
fig = go.Bar(x=[1], y=[5])
# fig = go.Bar(x=x, y=y)
plotly.offline.plot({'data':[fig]})

# pie chart example
x = ['apple pie', 
     'pumpkin pie', 
     'chocolate pecan pie',
     'chocolate bourbon pecan pie',
     ]
y = [14,
     3,
     9,
     2
     ]
fig = go.Pie(labels=x, values=y)
# plotly.offline.plot({'data':[fig]})
graph_div = plotly.offline.plot({'data':[fig]},
                                auto_open=False,
                                output_type='div',)






