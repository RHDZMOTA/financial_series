# -*- coding: utf-8 -*-

'''

script to download financial data...


'''


import numpy as np
import pandas as pd
import pandas_datareader.data as web
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
                # save the data
                data.to_csv(dr + '\\' + self.file_name(warning = False))
                # confirmation message
                txt1 = '\nData downloaded and '
                txt2 = 'saved successfully into: \n{} \n\n'
                print(txt1+txt2.format(dr))
                # return data
        else:
            data = pd.read_csv(self.file(warning = False), index_col=[0])
        
        # update the prices
        self.prices = data 
        if ret:
            return data
    
    def calc_returns(self, ret = 0):
        '''
        
        '''
        
        # empty dataframe for returns 
        idx = self.prices.index[1:-1]
        rt = pd.DataFrame([], index = idx)
        
        # calculate the returns for each column of the prices df
        for i in self.prices.columns:
            rt[i] = calc_rtns(self.prices[i].values)
        
        # update the returns 
        self.returns = rt
        if ret:
            return rt
    
    
    

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