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

# function to get correlation
def getCorrelation(symbol1, symbol2, dict):
    for period_item, interval_item in zip(config['period_timeframe'], config['interval_timeframe']):
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

print('Caricamento degli indici...')

# loop function through symbols
# for idx, symbol in enumerate(tqdm(config['symbols'])):
#     getCorrelation(config['comparison_symbols'][0], symbol, getTotal_correlation0)
#     getCorrelation(config['comparison_symbols'][1], symbol, getTotal_correlation1)

#########################################################
# NOTA: il valore giornaliero potrebbe restituire 0, 3 o 7, a seconda del momento della giornata
# NOTA: non spammare per evitare blocchi
# getCorrelation('^GSPC', 'USD', getTotal_correlation0)
ticker1 = yahooFinance.Ticker('GOLD')
data1 = ticker1.history(period = '1d', interval = '1h')
print(data1)

#########################################################

# dataframe the results
header0 = [np.array([config['comparison_symbols'][0], config['comparison_symbols'][0], config['comparison_symbols'][0], config['comparison_symbols'][0], config['comparison_symbols'][0]]), np.array(config['period_timeframe'])] 
header1 = [np.array([config['comparison_symbols'][1], config['comparison_symbols'][1], config['comparison_symbols'][1], config['comparison_symbols'][1], config['comparison_symbols'][1]]), np.array(config['period_timeframe'])] 
df0 = pd.DataFrame(getTotal_correlation0, index = header0).transpose()
df1 = pd.DataFrame(getTotal_correlation1, index = header1).transpose()
result = pd.concat([df0, df1], axis=1)

# print(result)

# get today date
today = date.today()
d1 = today.strftime("%d-%m-%Y")
d1Tot = 'correlation-' + d1 + '.xlsx'
if config['dateOn'] == True:
    nameExcel = d1Tot
else:
    nameExcel = 'correlation.xlsx'

# formatting the results in an Excel file
writer = pd.ExcelWriter(nameExcel, engine='xlsxwriter')
result.to_excel(writer, sheet_name='Sheet1')
workbook  = writer.book
worksheet = writer.sheets['Sheet1']
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})
format2 = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})
worksheet.conditional_format('B3:K100', {'type': 'cell',
                                         'criteria': '<=',
                                         'value': -0.5,
                                         'format': format1})
worksheet.conditional_format('B4:K100', {'type': 'cell',
                                         'criteria': '>=',
                                         'value': 0.5,
                                         'format': format2})
worksheet.set_column(0, 0, 15)
writer.save()
# pd.DataFrame(result).to_excel(nameExcel) 