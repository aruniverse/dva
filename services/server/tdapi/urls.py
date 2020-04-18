from accounts import TDAccount


class Url():
	'''
	def __init__(self, version = 'v1'):
		self.version = version

	This is not working for some reason but I am moving forward.
	'''
	_base_url = 'https://api.tdameritrade.com/{version}/'.format(version= 'v1')

	_url_dict = {
		'instruments' : 		 'instruments', # Complete
		'instrument' : 		 	 'instruments/{cusip}', # Complete
		'movers' : 		 	 	 'marketdata/{index}/movers', # Complete
		'option_chain' : 	 	 'marketdata/chains', # Complete
		'price_history' : 		 'marketdata/{ticker}/pricehistory',  # Complete
		'quote' : 				 'marketdata/{ticker}/quotes',  # Complete
		'quotes' : 				 'marketdata/quotes',  # Complete
		'specific_transaction' : 'accounts/{accountId}/transactions/{transactionId}',
		'transactions' : 		 'accounts/{accountId}/transactions',
		'preferences' : 		 'accounts/{accountId}/preferences',
		'subscription_key' : 	 'userprincipals/streamersubscriptionkeys',
		'user_principals' : 	 'userprincipals',
		'preferences' : 		 'accounts/{accountId}/preferences',
		'watchlist' : 			 'accounts/{accountId}/watchlists',
		'specific_watchlist' :   'accounts/{accountId}/watchlists/{watchlistId}',
		}
	for key, val in _url_dict.items():
		locals()[key] = _base_url + val


api_key = TDAccount.api_key
url_api_key_string = '?apikey=' + TDAccount.api_key
url = Url()

def price_history(ticker, periodType = None, period= None, frequencyType= None, frequency= None, endDate= None, startDate= None, needExtendedHoursData= None):
	'''
	# https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory#
	If any attributes are populated add it to the end of query_url with &.
	ex: if periodType request_url += + '&periodType={}'.format(periodType)
	periodType = ['day', 'month', 'year', 'ytd'] # default is day
	period = { # valid by periodType
		'day' : [1, 2, 3, 4, 5, 10], # default is 10
		'month' : [1, 2, 3, 6], # default is 1
		'year' : [1, 2, 3, 5, 10, 15, 20], # default is 1
		'ytd' : 1,
	}
	frequencyType = { # valid by periodtype
		'day': 'minute',
		'month' : ['daily', 'weekly'], # default is weekly
		'year' : ['daily', 'weekly', 'monthly'], # default is monthly
		'ytd' : ['daily', 'weekly'], # default is weekly
	}
	frequency = { # valid by frequencyType
		'minute' : [1, 5, 10, 15, 30], # default is 1
		'daily' : 1,
		'weekly': 1,
		'monthly' : 1
	}
	endDate milliseconds since epoch. default is previous trading day
	startDate as milliseconds since epoch
	'''
	request_url = url.price_history.format(ticker= ticker) + url_api_key_string
	request_url += '&periodType={}'.format(str(periodType)) if periodType else ''
	request_url += '&period={}'.format(str(period)) if period else ''
	request_url += '&frequencyType={}'.format(str(frequencyType)) if frequencyType else ''
	request_url += '&frequency={}'.format(str(frequency)) if frequency else ''
	request_url += '&endDate={}'.format(str(endDate)) if endDate else ''
	request_url += '&startDate={}'.format(str(startDate)) if startDate else ''
	request_url += '&needExtendedHoursData={}'.format(str(needExtendedHoursData)) if needExtendedHoursData else ''
	return request_url

def instrument(cusip):
	'''
	https://developer.tdameritrade.com/instruments/apis/get/instruments#
	projection = ['symbol-search','symbol-regex','desc-search','desc-regex','fundamental']
	'''
	request_url = url.instrument.format(cusip= cusip) + url_api_key_string

	return request_url

def instruments(symbol, projection= 'fundamental'):
	'''
	https://developer.tdameritrade.com/instruments/apis/get/instruments#
	projection = ['symbol-search','symbol-regex','desc-search','desc-regex','fundamental']
	'''
	request_url = url.instruments + url_api_key_string
	request_url += '&symbol={}'.format(str(symbol))
	request_url += '&projection={}'.format(str(projection))
	return request_url

def movers(index= '$SPX.X', direction = None, change = None):
	'''
	https://developer.tdameritrade.com/movers/apis/get/marketdata/%7Bindex%7D/movers#
	accepted_index = ['$SPX.X', '$DJI', '$COMPX']
	direction = [null, 'up', 'down']
	change = ['percent', 'value']
	'''
	request_url = url.movers.format(index=index) + url_api_key_string
	request_url += '&direction={}'.format(str(period)) if direction else ''
	request_url += '&change={}'.format(str(period)) if change else ''
	return request_url

def option_chain(symbol, contractType= 'ALL', strikeCount= '8', includeQuotes = 'TRUE', strategy= None, interval= None, _range= 'ALL', fromDate= None, toDate= None, volatility= None, underlyingPrice= None, interestRate= None, daysToExpiration= None, expMonth='ALL', optionType='ALL'):
	'''
	https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains#
	contractType = ['ALL','CALL','PUT'] default is All
	includeQuotes = ['TRUE','FALSE'] # default is true
	strategy = ['COVERED', 'VERTICAL', 'CALENDAR', 'STRANGLE', 'STRADDLE', 'BUTTERFLY', 'CONDOR', 'DIAGONAL', 'COLLAR', or 'ROLL'] # default is SINGLE
		When strategy = ANALYTICAL then it allows the use of volatility, underlyingPrice, interestRate, and daysToExpiration params to calculate theoretical values.

	interval - strike interval for spread strategy chains
	range = ['ITM', 'NTM', 'OTM' 'SAK', 'SBK', 'SNK', 'ALL'] # default is all
	fromDate = Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz
	toDate = Valid ISO-8601 formats are: yyyy-MM-dd and yyyy-MM-dd'T'HH:mm:ssz
	volatility =
	underlyingPrice =
	interestRate =
	daysToExpiration
	expMonth default is ALL
	optionType = ['S', 'NS', 'ALL']

	'''
	request_url = url.option_chain + url_api_key_string
	request_url += '&symbol={}'.format(str(symbol))

	request_url += '&contractType={}'.format(str(contractType)) if contractType else ''
	request_url += '&strikeCount={}'.format(str(strikeCount)) if strikeCount else ''
	request_url += '&includeQuotes={}'.format(str(includeQuotes)) if includeQuotes else ''
	request_url += '&strategy={}'.format(str(strategy)) if strategy else ''
	request_url += '&interval={}'.format(str(interval)) if interval else ''
	request_url += '&range={}'.format(str(_range)) if _range else ''
	request_url += '&fromDate={}'.format(str(fromDate)) if fromDate else ''
	request_url += '&toDate={}'.format(str(toDate)) if toDate else ''
	request_url += '&volatility={}'.format(str(volatility)) if volatility else ''
	request_url += '&underlyingPrice={}'.format(str(underlyingPrice)) if underlyingPrice else ''
	request_url += '&interestRate={}'.format(str(interestRate)) if interestRate else ''
	request_url += '&daysToExpiration={}'.format(str(daysToExpiration)) if daysToExpiration else ''
	request_url += '&expMonth={}'.format(str(expMonth)) if expMonth else ''
	request_url += '&optionType={}'.format(str(optionType)) if optionType else ''

	return request_url

def quote(ticker):
	'''
	https://developer.tdameritrade.com/quotes/apis/get/marketdata/%7Bsymbol%7D/quotes
	'''
	request_url = url.quote + url_api_key_string
	request_url += '&quote={}'.format(str(quote))
	return request_url

def quotes(symbol):
	'''
	https://developer.tdameritrade.com/quotes/apis/get/marketdata/quotes
	Accepts a list of symbols and returns a url string.
	'''
	symbol = ','.join(symbol)
	request_url = url.quotes + url_api_key_string
	request_url += '&symbol={}'.format(str(symbol))

	return request_url


# print(price_history('KEYS', period=1))

# response = requests.get(urls.price_history(ticker= 'SPY', periodType= 'day', period= '10'))

# response = response.json()