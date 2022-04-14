import numpy as np
import pandas as pd
import yfinance as yahooFinance
import yaml
from tqdm import tqdm
from datetime import date


# open yaml file
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

getTotal_correlation0 = {}
getTotal_correlation1 = {}
getTotal_correlation2 = {}

# function to get correlation
def getCorrelation(symbol1, symbol2, dict):
    for period_item, interval_item in zip(config['period_timeframe'], config['interval_timeframe']):
        if period_item == '1d':
            period_item = '2d'
        ticker1 = yahooFinance.Ticker(symbol1)
        data1 = ticker1.history(period = period_item, interval = interval_item)
        ticker2 = yahooFinance.Ticker(symbol2)
        data2 = ticker2.history(period = period_item, interval = interval_item)

        if len(data1) > len(data2):
            length = len(data2) 
        else:
            length = len(data1) 
        if symbol2 in dict:
            dict[symbol2].append( round( np.corrcoef(data1['Close'][-length:], data2['Close'][-length:])[0,1], 2) )
        else:
            dict[symbol2] = [ round( np.corrcoef(data1['Close'][-length:], data2['Close'][-length:])[0,1], 2) ]

print('Loading...')

# loop function through symbols
for idx, symbol in enumerate(tqdm(config['symbols'])):
    getCorrelation(config['comparison_symbols'][0], symbol, getTotal_correlation0)
    getCorrelation(config['comparison_symbols'][1], symbol, getTotal_correlation1)
    getCorrelation(config['comparison_symbols'][2], symbol, getTotal_correlation2)

# ticker1 = yahooFinance.Ticker('SB=F')
# data1 = ticker1.history(period = '1d', interval = '1h')
# print(data1)

# dataframe the results
header0 = [np.array([config['columnsNames'][0], config['columnsNames'][0], config['columnsNames'][0], config['columnsNames'][0], config['columnsNames'][0]]), np.array(config['period_timeframe'])] 
header1 = [np.array([config['columnsNames'][1], config['columnsNames'][1], config['columnsNames'][1], config['columnsNames'][1], config['columnsNames'][1]]), np.array(config['period_timeframe'])] 
header2 = [np.array([config['columnsNames'][2], config['columnsNames'][2], config['columnsNames'][2], config['columnsNames'][2], config['columnsNames'][2]]), np.array(config['period_timeframe'])]
df0 = pd.DataFrame(getTotal_correlation0, index = header0).transpose()
df1 = pd.DataFrame(getTotal_correlation1, index = header1).transpose()
df2 = pd.DataFrame(getTotal_correlation2, index = header2).transpose()
result = pd.concat([df0, df1, df2], axis=1)
# change row and columns names
result.index = config['rowNames']

# print(result)   ###########

# get today date
today = date.today()
d1 = today.strftime("%d-%m-%Y")
d1Tot = 'getCorrelation-' + d1 + '.xlsx'
if config['dateOn'] == True:
    nameExcel = d1Tot
else:
    nameExcel = 'getCorrelation.xlsx'

# formatting the results in an Excel file
writer = pd.ExcelWriter(nameExcel, engine='xlsxwriter')
result.to_excel(writer, sheet_name='Sheet1')
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
format2 = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})
worksheet.conditional_format('B3:P100', {'type': 'cell',
                                         'criteria': '<=',
                                         'value': -0.5,
                                         'format': format1})
worksheet.conditional_format('B4:P100', {'type': 'cell',
                                         'criteria': '>=',
                                         'value': 0.5,
                                         'format': format2})
worksheet.set_column(0, 0, 20)
writer.save()