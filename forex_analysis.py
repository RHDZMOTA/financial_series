# -*- coding: utf-8 -*-
"""
General analysis

@author: Rodrigo
"""

from forex_data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


a = currency(units='MXN', base = 'USD', t0 = '2015/01/01', tf = '2016/01/01')
#a.download()
#a.calc_returns()
a.fill()


a.returns.Adj_close.plot(kind = 'line')
plt.show()

a.returns.Adj_close.plot(kind = 'hist')
plt.show()

print('\n')
print(a.returns.Adj_close.describe())

# %% 
# a.returns.loc[dt.datetime.strptime('2015-01-02', '%Y-%m-%d'):dt.datetime.strptime('2015-01-07', '%Y-%m-%d')]
# Series with binanry data
def mindelt_entropy(a):
    '''
    This functions searches for the time interval (delta) in days that 
    minimize the entropy...
    '''
    max_delta = (a.tf - dt.timedelta(days = 1)) - a.t0
    min_detla = dt.timedelta(days = 25)
    
    t_init = a.t0 + dt.timedelta(days = 1)
    t_end = a.tf
    
    # entropy( init_t = 0, delta = 0)
    rsl = pd.DataFrame(columns = ['Delta', 'Mean', 'Standard_dev', 'Obs'])
    det = min_detla
    cond = True 
    while cond:
        condit = True
        t = t_init 
        etry = np.array([])
        while condit:
            etry = np.append(etry, a.entropy(init_t = t, delta = det))
            t = t + dt.timedelta(days = 1)
            if t+det == t_end:
                condit = False
        dct = {'Delta':det, 'Mean':np.mean(etry), 'Standard_dev':np.std(etry),
        'Obs':len(etry)}
        dct = pd.DataFrame(dct, index = np.array([0]))
        rsl = rsl.append(dct)
        det += dt.timedelta(days = 1)
        if det == max_delta:
            cond = False
    
    rsl.reset_index(inplace = True, drop = True)
    
    td = rsl.loc[rsl['Mean'] == min(rsl['Mean'])].Delta
    td = (td.values[0] / np.timedelta64(1, 'D')).astype(int)
    
    plt.figure()
    plt.plot(rsl['Delta'],rsl['Mean'])
    plt.title('Mean entropy level per delta')
    plt.xlabel('Days in delta window')
    plt.ylabel('Average entropy')
    plt.show()
    
    return td




series_b = a.returns.Adj_close.map(lambda x: x > 0)




binary_ret = pd.DataFrame([])
binary_ret['Status'] = series_b.map(int).map(str).values
binary_ret['Sum'] = np.ones(len(series_b))
binary_ret.groupby('Status').sum().plot(kind = 'bar')

binary_ret['Increase'] = series_b.map(int).values
binary_ret['Decrease'] = (series_b == 0).map(int).values
binary_ret.sum()

