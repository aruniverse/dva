import os

class TDAccount(object):
	'''
	Stores account details including the TD Consumer Key needed as an API key.
	consumer_key should be stored as an environment variable and imported.
	Useful URLS
	https://developer.tdameritrade.com/user/me/apps
	https://developer.tdameritrade.com/apis
	'''
	consumer_key = 'JCLOBS729M6SGX9TXT9IBG1QPDFGL8KL'
	api_key = consumer_key # I prefer to use api_key

	def __init__(self,account_id):
		self.account_id = None

time_zone = ''