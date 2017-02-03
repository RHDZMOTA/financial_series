# financial_series
###Foreign Exchange Rate (FOREX) currency analysis. 

By: **Rodrigo Hernández Mota**


_**Status**: in development._ 


This repository contains "advanced" tools to aid in the analysis of exchange rates. The main advantage is the creation of a new datatype (class) named: _currency_. To use this datatype in a script just import forex_data as following:

`from forex_data import currency`

## Type Currency

Use currency type to facilitate forex exchange rate financial analysis. A basic intro to this type can be found in this repository as **Introduction_type_currency.ipnb** or **Introduction_type_currency.html**. 

**Example** _Initialize currency and basic operations_

```
a = currency(units='MXN', base = 'USD', t0 = '2014/01/01', tf = '2016/10/01')
a.fill()
```

This datatype downloads the currency empirical data from Yahoo!'s databases and stores it in memory as a Pandas DataFrame. 
If you want to save the data into a .csv file, use:
`a.download(save = True)`
This will generate a directory named 'general_database' with the .csv

Use the following command to show the downloaded prices: 
```
a.prices.head()
```

The financial returns are calculated by default as a logarithmic difference. To see the data type:
```
a.returns.head()
```
Plotting is fairly easy due to the internal Pandas structure:
```
a.prices.plot(grid = True, figsize=(10,5))
a.returns.plot(grid = True, figsize=(10,5))
```

Transform the returns into a binary variable (1 if the return > 0 and 0 otherwise).
```
a.binary_rend()
```

Calculate the information entropy based on the binary transformation. 
```
a.entropy()
```

And more in progres... 

## Requirements

This datatype depends on some basic and commony python 3 libraries: pandas, datetime, os, numpy and matplotlib.pyplot. And an external script aux_fun.py. 

[continue]
