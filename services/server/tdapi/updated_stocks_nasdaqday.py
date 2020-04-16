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


get_symbols = """SELECT symbol, max(DATETIME_EPOCH) as DATETIME_EPOCH, SUM(VOLUME) AS VOL_SUM from stocks_nasdaqday
					group by symbol
					order by VOL_SUM desc"""

insert_statement = """INSERT INTO {table_name} (symbol, open, high, low, close, volume, datetime_epoch, datetime)
						values ('{symbol}', {open}, {high}, {low}, {close}, {volume}, {datetime_epoch}, TIMESTAMP '{datetime}')
"""

cur = conn.cursor()

cur.execute(get_symbols)
get_symbols = [row for row in cur.fetchall()]

for row in get_symbols:
	'''
	The function below updates the AWS DB from TD's API.  The query gets the max date from the AWS DB and adds 86400000 to the max start date.
	86400000 is added to the start date to get the newest data.
	'''
	time.sleep(1)
	response = requests.get(urls.price_history(ticker= row[0], periodType= 'year', startDate= row[1], frequencyType= 'daily', frequency= 1))
	response = response.json()
	for trading_values in response['candles']:
		if trading_values['datetime'] > row[1]:
			try:
				if not (math.isnan(float(trading_values['open'])) and math.isnan(float(trading_values['high']))):
					cur.execute(insert_statement.format(
						table_name= 'stocks_nasdaqday',
						symbol= row[0],
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
	print(row[0])


cur.close()
conn.close()