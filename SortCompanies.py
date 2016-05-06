'''
This class acts like a preprocessor to the prepocessor. The orignal corpus contained over 1 GB of data.
While it may give better results with extra data, the time it would take to train with that much data
is impractical. In the future, there are parts that are parallelizable, such as striping html elements
that would provide some speed up benefits and may make tackling so much data feasible.
'''

import numpy as np
import pandas as pd

# Get a list of companies
company_data = np.array(pd.read_csv('snp500_company_list.txt', header=None, delimiter='\t').T)

'''
Apple\tAAPL\tInformation Technology\n
'''

sectors = np.unique(company_data[2])
number_sectors = np.size(sectors)

ticker_by_sector = [None] * number_sectors

# Get distribution of companies per sector
for index in range(number_sectors):
    ticker_by_sector[index] = company_data[1][np.where(company_data[2] == sectors[index])]
    '''
    Distribution of companies per sector
    0 ) Consumer Discretionary 80
    1 ) Consumer Staples 41
    2 ) Energy 45
    3 ) Financials 81
    4 ) Health Care 52
    5 ) Industrials 60
    6 ) Information Technology 71
    7 ) Materials 31
    8 ) Telecommunication Services 8
    9 ) Utilities 31

    '''

#print(index, ")", sectors[index], np.shape(ticker_by_sector[index])[0])

# create a list of commands to move the files of selected companies into a folder in terminal
tickers = company_data[1][np.where(company_data[2] == sectors[6])].T
for i in range(np.size(tickers)):
    print('mv', tickers[i]+'.csv prices')

for i in range(np.size(tickers)):
    print('mv', tickers[i]+'.gz stocks')
