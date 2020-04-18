# python import


import requests, psycopg2, time, math

# tdapi import
import urls, utils
from nasdaq import nasdaq_tickers

conn = psycopg2.connect(
	host="database-1.cjpoxlvxbftx.us-east-1.rds.amazonaws.com",
	port = 5432,
	database="postgres",
	user="team128user",
	password="Xvo3dVJCCX8nPhuOWJWz"
)

insert_statement = """INSERT INTO {table_name} (symbol, open, high, low, close, volume, datetime_epoch, datetime)
						values ('{symbol}', {open}, {high}, {low}, {close}, {volume}, {datetime_epoch}, TIMESTAMP '{datetime}')
"""


cur = conn.cursor()


# response = requests.get(urls.price_history(ticker= 'SPY', periodType= 'year', startDate= '1262584800000', frequencyType= 'daily', frequency= 1))
# response = response.json()

# for trading_values in response['candles']:
# 	print(trading_values, utils.convert_tse_to_dt(trading_values['datetime']))


for symbol in nasdaq_tickers:
	time.sleep(.5)
	response = requests.get(urls.price_history(ticker= symbol, periodType= 'year', startDate= '1262584800000', frequencyType= 'daily', frequency= 1))
	response = response.json()
	try:
		for trading_values in response['candles']:
			if not (math.isnan(float(trading_values['open'])) and math.isnan(float(trading_values['high']))):
				cur.execute(insert_statement.format(
					table_name= 'stocks_nasdaqday',
					symbol= symbol,
					open= trading_values['open'],
					high= trading_values['high'],
					low= trading_values['low'],
					close= trading_values['close'],
					volume= trading_values['volume'],
					datetime_epoch= trading_values['datetime'],
					datetime= utils.convert_tse_to_dt(trading_values['datetime'])
					)
				)
	except KeyError:
		print('No data for:')
	conn.commit()
	print(symbol)

'''
for symbol in nasdaq_tickers:
	response = requests.get(urls.price_history(ticker= symbol, periodType= 'year', startDate= '1262584800000', frequencyType= 'daily', frequency= 1))
	response = response.json()
	for trading_values in response['candles']:
		cur.execute(insert_statement.format(
			table_name= 'stocks_nasdaqmin',
			symbol= symbol,
			open= trading_values['open'],
			high= trading_values['high'],
			low= trading_values['low'],
			close= trading_values['close'],
			volume= trading_values['volume'],
			datetime_epoch= trading_values['datetime'],
			datetime= utils.convert_tse_to_dt(trading_values['datetime'])
			)
		)
	conn.commit()
	print(symbol)

'''
cur.close()
conn.close()
