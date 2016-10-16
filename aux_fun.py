# -*- coding: utf-8 -*-
"""
Auxiliar functions
"""
import pandas as pd
import numpy as np


# Function to calculate returns: 
def calc_rtns(prices, warning = True, met_log = True):
    
    # Warning function 
    def warn(sti = 0):
        w0 = 'Error: datatype must be numpy.ndarray'
        if sti == 0:
            sti = w0
        print(sti)
        return None 
    
    # identify variable type for prices
    ty = type(prices)
    if warning:
        # DataFrame 
        if ty == type(pd.DataFrame([])):
            if np.shape(prices)[1] == 1:
                prices = prices.values
            else:
                sti = 'Error: variable is a DataFrame, must be numpy.ndarray'
                return warn(sti)
        # Series 
        elif ty == type(pd.Series([])):
            prices = prices.values 
        # None 
        elif ty == type(None):
            sti = 'Error: The varialbe does not contain data (None)'
            return warn(sti)
        # Anything different to numpy.ndarray
        elif ty != type(np.array([])):
            return warn()
    
    # Calculate the returns 
    if met_log:
        returns = np.log(prices[1:] / prices[0:-1])
    else:
        returns = prices[1:] / prices[0:-1] - 1 
    
    return returns         