# python import

import requests, psycopg2

# tdapi import
import urls, utils


conn = psycopg2.connect(
	host="database-1.cjpoxlvxbftx.us-east-1.rds.amazonaws.com",
	port = 5432,
	database="postgres",
	user="team128user",
	password="Xvo3dVJCCX8nPhuOWJWz"
)

cur = conn.cursor()

select_spy = """SELECT * FROM stocks_indexesday where symbol = 'SPY' order by datetime_epoch"""

select_aapl = """SELECT * FROM stocks_nasdaqday WHERE symbol = 'AAPL'  order by datetime_epoch"""

cur.execute(select_spy)
spy_data = [row for row in cur.fetchall()]

cur.execute(select_aapl)
aapl_data = [row for row in cur.fetchall()]



cur.close()
conn.close()