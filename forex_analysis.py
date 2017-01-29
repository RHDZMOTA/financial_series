# -*- coding: utf-8 -*-
"""
Test script...
@author: Rodrigo
"""

from forex_analysis.forex_data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# %% Download data


available_currencies = ['MXN', 'CZK', 'EUR', 'GBP', 'JPY', 'CAD', 'CHF', 'SEK',
                        'CNY']
obj = []
string = "currency(units='{}', base = 'USD', t0 = '2015/01/01', tf = '2016/01/01')"
for i in available_currencies:
    obj.append(eval(string.format(i)))
    obj[-1].fill()

    
a = currency(units='MXN', base = 'USD', t0 = '2015/01/01', tf = '2016/01/01')
a.fill()

b = currency(units='CZK', base = 'USD', t0 = '2015/01/01', tf = '2016/01/01')
b.fill()

# print general statistics of returns 
list(map(lambda x: print(x.name(),'\n',
                         x.returns.Adj_close.describe(),'\n\n',sep = ''), obj))

# TODO 
def describe(obj, variable = 'returns', col = 'Adj_close'):
    string = "list(map(lambda x: print(x.name(),'\n', x.{}.{}.describe(),'\n\n',sep = ''), obj))"
    eval(string.format(variable, col))

# %% General visualizations 

# returns 
for i in obj:
    i.returns.Adj_close.plot(kind = 'line', label = i.name())
    plt.legend()
    plt.show()
    
# histograms normalized
list(map(lambda i: i.returns.Adj_close.plot(kind = 'hist',alpha = 0.75,
                                            normed = True,
                                            label = i.name()),obj))
plt.legend(loc='best')


a.returns.Adj_close.plot(kind = 'hist', color = 'blue', normed = True)
b.returns.Adj_close.plot(kind = 'hist', color = 'red', alpha = 0.85, normed = True)
plt.show()

# prices 

obj[0].plot(obj[1:])

a.plot([b])




# %% correlation 
m = np.array([])
for i in obj:
    np.append(i.returns.Adj_close.values, m)
    
np.corrcoef(a.returns.Adj_close,b.returns.Adj_close)
v = np.array(list(map(lambda x: x.returns.Adj_close.values, obj)))
string = 'obj[0]'
for i in range(1, len(obj)):
    string = string + ', obj[{}]'.format(i)

string = 'np.corrcoef({})'.format(string)
eval(string)







