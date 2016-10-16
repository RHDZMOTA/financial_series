# -*- coding: utf-8 -*-

'''

script to download financial data...


'''


import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
#import pandas.io.data as wb
#import pandas_datareader as pdr
#from pandas_datareader.oanda import get_oanda_currency_historical_rates as get_oanda
from aux_fun import *
import datetime as dt
import os.path

class currency:
    '''
    General class to download forex exchange currency data and facilitate
    its manipulation. 
    '''
    desc = 'Foreign Exchange Rate'

    # basic information
    def __init__(self, units, base, t0, tf):
        self.units = units
        self.base  = base
        self.t0 = dt.datetime.strptime(t0, '%Y/%m/%d')
        self.tf = dt.datetime.strptime(tf, '%Y/%m/%d')
        self.prices  = None
        self.returns = None

    #prices = self.download()
    
    # name of the exchange rate
    def name(self):
        stri = self.base+'/'+self.units
        return stri

    # returns the file name regardless if exists or not
    def file_name(self, warning = True):
        # name of the document --> file id (fid)
        lid1 = []; lid2 = []
        lid1.append(self.t0); lid2.append(self.tf)
        fid = lid1[0].strftime('%y%d%m') + lid2[0].strftime('%y%d%m')
        nm = ''.join(self.name().split('/'))
        gen_fid = nm + fid + ".csv"

        # Warning if file does not exits         
        if os.path.isfile('general_database\\{}'.format(gen_fid)) == 0:
            if warning:
                w0 = '\nWarning: there is no file containing the data'
                w1 = ' for this variable.'
                print(w0+w1)
                
        return gen_fid
        
    # check if the file exists
    def file(self, warning = True):
        
        # get the name of the file
        gen_fid = self.file_name(warning)
        
        if os.path.isfile('general_database\\{}'.format(gen_fid)):
            return os.path.abspath('general_database')+'\\{}'.format(gen_fid)#os.path.abspath(gen_fid)
        else:
            return 0 


    # download data
    def download(self, save = 0, ret = 0):
        '''
        Description: 
        '''

        # absolute path 
        dr = os.path.abspath('general_database')

        if self.file(warning = False) == 0:

            # determine yho as the name of the series in yahoo.
            if self.base == 'USD':
                yho = self.units+'=X'
            else:
                yho = self.base+self.units+'=X'
        
            # read data into memory
            data = web.DataReader(yho, 'yahoo', self.t0, self.tf)
            del data['Volume']
            data.rename(columns = {'Adj Close':'Adj_close'}, inplace = True)
            
            # save if file is does not exists
            if save:
                # create directory if not existis
                if not os.path.exists('general_database'):
                    os.makedirs('general_database')
                # save the data
                data.to_csv(dr + '\\' + self.file_name(warning = False))
                # confirmation message
                txt1 = '\nData downloaded and '
                txt2 = 'saved successfully into: \n{} \n\n'
                print(txt1+txt2.format(dr))
                # return data
        else:
            data = pd.read_csv(self.file(warning = False), index_col=[0])
            indx = pd.to_datetime(data.index)
            data = data.reindex(indx)
        
        # update the prices
        self.prices = data 
        if ret:
            return data
    
    def calc_returns(self, ret = 0):
        '''
        
        '''
        
        # empty dataframe for returns 
        idx = self.prices.index[1:]
        rt = pd.DataFrame([], index = idx)
        
        # calculate the returns for each column of the prices df
        for i in self.prices.columns:
            rt[i] = calc_rtns(self.prices[i].values)
        
        # update the returns 
        self.returns = rt
        if ret:
            return rt
    
    def fill(self):
        self.download()
        self.calc_returns()
    
    def binary_rend(self, init_t = 0, delta = 0):
        '''
        
        '''
        # determine initial date
        if init_t != 0:
            init_t = dt.datetime.strptime(init_t, '%Y/%m/%d')
        else:
            init_t = self.t0 + dt.timedelta(days = 1)
        
        # determine delta (days)
        aux_delt = self.tf - init_t
        if delta == 0:
            dys = aux_delt
        elif type(delta) == type(dt.timedelta(days = 0)):
            dys = delta
        else:
            dys = dt.timedelta(days = delta)
            
        df_aux = self.returns.Adj_close.loc[init_t:init_t+dys].map(lambda x: x > 0)
        return df_aux.values
    
    def entropy(self, init_t = 0, delta = 0, level = 1):
        '''
        desc. This function calculates the binary information entropy. 
        '''
        # determine initial date
        if init_t != 0:
            init_t = dt.datetime.strptime(init_t, '%Y/%m/%d')
        else:
            init_t = self.t0 + dt.timedelta(days = 1)
        
        # determine delta (days)
        aux_delt = self.tf - init_t
        if delta == 0:
            dys = aux_delt
        elif type(delta) == type(dt.timedelta(days = 0)):
            dys = delta
        else:
            dys = dt.timedelta(days = delta)
        
        # error conditional 
        if dys > aux_delt:
            print('Not enought data... Only {} available.'.format(str(aux_delt)))
            return 0
        
        # auxiliar dataframe and binary string 
        df_aux = self.returns.Adj_close.loc[init_t:init_t+dys].map(lambda x: x > 0)
        string_b = ''.join(df_aux.map(int).map(str))
        
        # probability of one and zero 
        p_one  = string_b.count('1') / len(string_b)
        p_zero = string_b.count('0') / len(string_b)
        
        # calculate binary information entropy
        information_entropy = lambda x: x*np.log2(1/x)
        h = information_entropy(p_one) + information_entropy(p_zero)
        
        return h
        
    def mindelt_entropy(self):
        '''
        This functions searches for the time interval (delta) in days that 
        minimize the entropy...
        '''
        max_delta = (self.tf - dt.timedelta(days = 1)) - self.t0
        min_detla = dt.timedelta(days = 16)
        
        t_init = self.t0 + dt.timedelta(days = 1)
        t_end = self.tf
        
        # entropy( init_t = 0, delta = 0)
        rsl = pd.DataFrame(columns = ['Delta', 'Mean', 'Standard_dev', 'Obs'])
        det = min_detla
        cond = True 
        while cond:
            condit = True
            t = t_init 
            etry = np.array([])
            while condit:
                etry = np.append(etry, self.entropy(init_t = t.strftime('%Y/%m/%d'), delta = det))
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


"""
'''
Example


'''

a = currency(units='MXN', base = 'USD', t0 = '2015/01/01', tf = '2016/01/01')

# Download the data... 
a.download()
a.prices.head()
a.prices.plot()

# Calculate the returns
a.calc_returns()
a.returns.head()
a.returns.plot()


"""