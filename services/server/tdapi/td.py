# python import

import requests
# tdapi import
import urls, utils


print(urls.price_history(ticker='SNAP'))


response = requests.get(urls.price_history(ticker= 'SPY', periodType= 'day', period= '10',needExtendedHoursData='false'))

response = response.json()

for trading_values in response['candles']:
	print(trading_values, utils.convert_tse_to_dt(trading_values['datetime']))