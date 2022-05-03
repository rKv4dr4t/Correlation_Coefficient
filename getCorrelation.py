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

# function to get correlation
def getCorrelation(symbol1, symbol2, dict):

    for period_item, interval_item in zip(config['period_timeframe'], config['interval_timeframe']):
        ticker1 = yahooFinance.Ticker(symbol1)
        data1 = ticker1.history(period = period_item, interval = interval_item)
        ticker2 = yahooFinance.Ticker(symbol2)
        data2 = ticker2.history(period = period_item, interval = interval_item)

        # avoid pick data with different date info (index have 5 data weekly, crypto 7/7)
        res = list(set(data1.index)^set(data2.index))
        if res:
            for item in res:
                if item in data1.index:
                    data1 = data1.drop(labels=[item], axis=0)
                if item in data2.index:
                    data2 = data2.drop(labels=[item], axis=0)

        if symbol2 in dict:
            dict[symbol2].append( round( np.corrcoef(data1['Close'], data2['Close'])[0,1], 2) )
        else:
            dict[symbol2] = [ round( np.corrcoef(data1['Close'], data2['Close'])[0,1], 2) ]

# loop function through symbols
for idx, symbol in enumerate(tqdm(config['symbols'])):
    getCorrelation(config['comparison_symbols'][0], symbol, getTotal_correlation0)

header0 = [np.array([config['columnsNames'][0], config['columnsNames'][0], config['columnsNames'][0], config['columnsNames'][0]]), np.array(config['period_timeframe'])] 

df0 = pd.DataFrame(getTotal_correlation0, index = header0).transpose()
result = pd.concat([df0], axis=1)
# change row and columns names
result.index = config['rowNames']

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