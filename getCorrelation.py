import numpy as np
# import pandas_datareader as pdr
# import datetime as dt
import pandas as pd
import yfinance as yahooFinance

comparison_symbols = ['^GSPC', 'USD']

# symbols = [
# 'AUDUSD=X', 'GBPUSD=X', 'EURUSD=X', 'JPYUSD=X', 'CHFUSD=X', 'USD', 'MXNUSD=X', 'NZDUSD=X', 'BTC-USD',
# '^GSPC', '^NDX', '^DJI',
# 'UCO', 'UGA', '^RUT',
# 'CORN',
# 'GOLD'
# ]

symbols = [
 'AUDUSD=X',
 'USD' 
]


period_timeframe = ['1d', '15d', '30d', '90d', '120d']
interval_timeframe = ['1h', '1d', '1d', '1wk', '1mo']
number_toget = [-3, -15, -30, -90, -120]
# number_toget = [-3, -3, -6, -3, -120]
getTotal_correlation0 = {}
getTotal_correlation1 = {}
periodName0 = ['1d (' + comparison_symbols[0] + ')', '15d (' + comparison_symbols[0] + ')', '30d (' + comparison_symbols[0] + ')', '90d (' + comparison_symbols[0] + ')', '120d (' + comparison_symbols[0] + ')']
periodName1 = ['1d (' + comparison_symbols[1] + ')', '15d (' + comparison_symbols[1] + ')', '30d (' + comparison_symbols[1] + ')', '90d (' + comparison_symbols[1] + ')', '120d (' + comparison_symbols[1] + ')']
# getCorr = []

def getCorrelation(symbol1, symbol2, dict):
    for period_item, interval_item, number_item in zip(period_timeframe, interval_timeframe, number_toget):
        ticker1 = yahooFinance.Ticker(symbol1)
        data1 = ticker1.history(period = period_item, interval = interval_item)
        ticker2 = yahooFinance.Ticker(symbol2)
        data2 = ticker2.history(period = period_item, interval = interval_item)
        if symbol2 in dict:
            dict[symbol2].append( round( np.corrcoef(data1['Close'][number_item:], data2['Close'][number_item:])[0,1], 2) )
        else:
            dict[symbol2] = [ round( np.corrcoef(data1['Close'][number_item:], data2['Close'][number_item:])[0,1], 2) ]

for symbol in symbols:
    getCorrelation('^GSPC', symbol, getTotal_correlation0)

for symbol in symbols:
    getCorrelation('USD', symbol, getTotal_correlation1)

# for symbol in symbols:
#     getCorrelation('USD', symbol, getTotal_correlation1)
# getCorrelation('^GSPC', 'AUDUSD=X')
# print(getTotal_correlation)

df0 = pd.DataFrame(getTotal_correlation0, index = periodName0).transpose()
df1 = pd.DataFrame(getTotal_correlation1, index = periodName1).transpose()

result = pd.concat([df0, df1], axis=1)
# df = pd.concat(getTotal_correlation0, getTotal_correlation1)
# print(df0)
# print(df1)
print(result)


# ticker1 = yahooFinance.Ticker('SPXL')
# data1 = ticker1.history(period = '1d', interval = '1h')
# print(data1)




# def getCorrelation(symbol1, symbol2):
#     for period_item, interval_item, number_item in zip(period_timeframe, interval_timeframe, number_toget):
#         ticker1 = yahooFinance.Ticker(symbol1)
#         data1 = ticker1.history(period = period_item, interval = interval_item)
#         ticker2 = yahooFinance.Ticker(symbol2)
#         data2 = ticker2.history(period = period_item, interval = interval_item)
#         getCorr.append( round( np.corrcoef(data1['Close'][number_item:], data2['Close'][number_item:])[0,1], 2) )
#         if len(getCorr) == len(period_timeframe):
#             return getCorr


# for i in symbols:
#     print(getCorrelation('^GSPC', i))
    # if len(getCorr) % len(period_timeframe) == 0:
    #     test = np.array( getCorrelation('^GSPC', i) )
    #     print(test)
        # data[i] = getCorrelation('^GSPC', i)
    # print(data)
    # total_getCorr.append( getCorrelation('^GSPC', i) )
    # print(i + " " + str(total_getCorr) + "\n")


# print( getCorrelation('^GSPC', 'BTC-USD') )
# pd.DataFrame(data).to_excel("data.xlsx") 


