import requests, psycopg2, time, math

# tdapi import
import urls, utils


conn = psycopg2.connect(
	host="database-1.cjpoxlvxbftx.us-east-1.rds.amazonaws.com",
	port = 5432,
	database="postgres",
	user="team128user",
	password="Xvo3dVJCCX8nPhuOWJWz"
)

insert_statement_fundamental = """INSERT INTO {table_name} (
	"updated","symbol","high52","low52",
	"dividendAmount","dividendYield","dividendPayAmount","dividendDate","dividendPayDate","divGrowthRate3Year",
	"peRatio","pegRatio","pbRatio","prRatio","pcfRatio","beta","vol1DayAvg","vol10DayAvg","vol3MonthAvg",
	"epsTTM","epsChangePercentTTM","epsChangeYear","epsChange","grossMarginTTM","grossMarginMRQ",
	"netProfitMarginTTM","netProfitMarginMRQ","operatingMarginTTM","operatingMarginMRQ",
	"returnOnEquity","returnOnAssets","returnOnInvestment","quickRatio",
	"currentRatio","interestCoverage","totalDebtToCapital","ltDebtToEquity","totalDebtToEquity","revChangeYear","revChangeTTM",
	"revChangeIn","sharesOutstanding","marketCapFloat","marketCap","bookValuePerShare","shortIntToFloat","shortIntDayToCover"
)
values (
	current_date, '{symbol}',{high52},{low52},
	{dividendAmount},{dividendYield},{dividendPayAmount},TO_TIMESTAMP('{dividendDate}','YYYY-MM-DD HH24:MI:SS'),TO_TIMESTAMP('{dividendPayDate}','YYYY-MM-DD HH24:MI:SS'),
	{divGrowthRate3Year},
	{peRatio},{pegRatio},{pbRatio},{prRatio},{pcfRatio},{beta},{vol1DayAvg},{vol10DayAvg},{vol3MonthAvg},
	{epsTTM},{epsChangePercentTTM},{epsChangeYear},{epsChange},{grossMarginTTM},{grossMarginMRQ},
	{netProfitMarginTTM},{netProfitMarginMRQ},{operatingMarginTTM},{operatingMarginMRQ},
	{returnOnEquity},{returnOnAssets},{returnOnInvestment},{quickRatio},
	{currentRatio},{interestCoverage},{totalDebtToCapital},{ltDebtToEquity},{totalDebtToEquity},{revChangeYear},{revChangeTTM},
	{revChangeIn},{sharesOutstanding},{marketCapFloat},{marketCap},{bookValuePerShare},{shortIntToFloat},{shortIntDayToCover}
)

"""

cur = conn.cursor()
get_symbols = """SELECT distinct symbol from stocks_nasdaqday
where symbol not in (select symbol from stocks_fundamental)"""
cur.execute(get_symbols)
get_symbols = [row[0] for row in cur.fetchall()]
get_symbols= ["TBLT"]
for symbol in get_symbols:
	dividendDate = '2000-01-01 00:00:00.000'
	dividendPayDate = '2000-01-01 00:00:00.000'
	time.sleep(.75)

	response = requests.get(urls.instruments(symbol=symbol, projection= 'fundamental'))
	response = response.json()

	if response:
		_dict = response[symbol]['fundamental']

		if len(_dict['dividendDate']) > 10:
			dividendDate= _dict['dividendDate']

		if len(_dict['dividendDate']) > 10:
			dividendPayDate= _dict['dividendPayDate']
		try:
			cur.execute(insert_statement_fundamental.format(
				table_name= 'stocks_Fundamental',
				symbol= _dict['symbol'],
				high52= _dict['high52'],
				low52= _dict['low52'],
				dividendAmount= _dict['dividendAmount'],
				dividendYield= _dict['dividendYield'],
				dividendDate= dividendDate, #date
				peRatio= _dict['peRatio'],
				pegRatio= _dict['pegRatio'],
				pbRatio= _dict['pbRatio'],
				prRatio= _dict['prRatio'],
				pcfRatio= _dict['pcfRatio'],
				grossMarginTTM= _dict['grossMarginTTM'],
				grossMarginMRQ= _dict['grossMarginMRQ'],
				netProfitMarginTTM= _dict['netProfitMarginTTM'],
				netProfitMarginMRQ= _dict['netProfitMarginMRQ'],
				operatingMarginTTM= _dict['operatingMarginTTM'],
				operatingMarginMRQ= _dict['operatingMarginMRQ'],
				returnOnEquity= _dict['returnOnEquity'],
				returnOnAssets= _dict['returnOnAssets'],
				returnOnInvestment= _dict['returnOnInvestment'],
				quickRatio= _dict['quickRatio'],
				currentRatio= _dict['currentRatio'],
				interestCoverage= _dict['interestCoverage'],
				totalDebtToCapital= _dict['totalDebtToCapital'],
				ltDebtToEquity= _dict['ltDebtToEquity'],
				totalDebtToEquity= _dict['totalDebtToEquity'],
				epsTTM= _dict['epsTTM'],
				epsChangePercentTTM= _dict['epsChangePercentTTM'],
				epsChangeYear= _dict['epsChangeYear'],
				epsChange= _dict['epsChange'],
				revChangeYear= _dict['revChangeYear'],
				revChangeTTM= _dict['revChangeTTM'],
				revChangeIn= _dict['revChangeIn'],
				sharesOutstanding= _dict['sharesOutstanding'],
				marketCapFloat= _dict['marketCapFloat'],
				marketCap= _dict['marketCap'],
				bookValuePerShare= _dict['bookValuePerShare'],
				shortIntToFloat= _dict['shortIntToFloat'],
				shortIntDayToCover= _dict['shortIntDayToCover'],
				divGrowthRate3Year= _dict['divGrowthRate3Year'],
				dividendPayAmount= _dict['dividendPayAmount'],
				dividendPayDate= dividendPayDate, # Date
				beta= _dict['beta'],
				vol1DayAvg= _dict['vol1DayAvg'],
				vol10DayAvg= _dict['vol10DayAvg'],
				vol3MonthAvg= _dict['vol3MonthAvg'],
				)
			)
		except Exception as e:
			print('failed: ' + str(symbol))
			print(e)
			print(_dicts)
	conn.commit()

cur.close()
conn.close()
