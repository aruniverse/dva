import datetime, time, pytz

def convert_dt_to_tse(dt= None):
	'''
		Takes a date in string or datetime format and converts to milliseconds since epoch.
		default is today to the second.
		handles ISO format (e.g. 2019-10-23 13:01:09')

	'''
	#epoch = datetime.datetime.utcfromtimestamp(0)

	if type(dt) == str:
		date, time = dt.split(' ')
		year, month, day = map(int, date.split('-'))
		hour, minute, second = map(int, time.split(':'))
		dt = datetime.datetime(year, month, day, hour, minute, second)
		dt = dt.astimezone((pytz.timezone('US/Central')))
	if not dt:
		dt = datetime.datetime.utcnow()
	return int(dt.timestamp()*1000)

def convert_tse_to_dt(tse, str_fmt= False):
	'''
		Converts milliseconds since epoch to datetime.  Optional return of a string.
	'''
	tse /= 1000
	if str_fmt:
		return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tse))
	return datetime.datetime.utcfromtimestamp(tse)
