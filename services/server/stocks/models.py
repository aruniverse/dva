from django.db import models

# Create your models here.

class NYSEMin(models.Model):
	'''
	Stocks in the NYSE stock market.  Minute data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)

class NYSEDay(models.Model):
	'''
	Stocks in the NYSE stock market.  Daily data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)

class NASDAQMin(models.Model):
	'''
	Stocks in the NASDAQ stock market.  Minute data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)

class NASDAQDay(models.Model):
	'''
	Stocks in the NASDAQ stock market.  Daily data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)

class IndexesDay(models.Model):
	'''
	Popular Indexes and MISC.  Daily data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)


class IndexesMin(models.Model):
	'''
	Popular Indexes and MISC.  Min data.
	'''
	symbol = models.CharField(max_length=6)
	open =  models.FloatField()
	high =  models.FloatField()
	low =  models.FloatField()
	close =  models.FloatField()
	volume =  models.IntegerField()
	datetime_epoch =  models.BigIntegerField()
	datetime =  models.DateField(auto_now=False, auto_now_add=False, null=True)



class Fundamental(models.Model):
	updated = models.DateTimeField(auto_now=True)
	# fields from TD API below
	symbol = models.CharField(max_length=6)
	high52 = models.DecimalField(max_digits=10, decimal_places=4)
	low52 = models.DecimalField(max_digits=10, decimal_places=4)
	dividendAmount = models.FloatField()
	dividendYield = models.FloatField()
	dividendPayAmount = models.FloatField()
	dividendDate = models.DateField(auto_now=False, auto_now_add=False)
	dividendPayDate = models.DateField(auto_now=False, auto_now_add=False)
	divGrowthRate3Year = models.FloatField()
	peRatio = models.FloatField()
	pegRatio = models.FloatField()
	pbRatio = models.FloatField()
	prRatio = models.FloatField()
	pcfRatio = models.FloatField()
	beta = models.FloatField()
	vol1DayAvg = models.IntegerField()
	vol10DayAvg = models.IntegerField()
	vol3MonthAvg = models.IntegerField()
	epsTTM = models.FloatField()
	epsChangePercentTTM = models.FloatField()
	epsChangeYear = models.FloatField()
	epsChange = models.FloatField()
	grossMarginTTM = models.FloatField()
	grossMarginMRQ = models.FloatField()
	netProfitMarginTTM = models.FloatField()
	netProfitMarginMRQ = models.FloatField()
	operatingMarginTTM = models.FloatField()
	operatingMarginMRQ = models.FloatField()
	returnOnEquity =  models.FloatField()
	returnOnAssets =  models.FloatField()
	returnOnInvestment = models.FloatField()
	quickRatio =  models.FloatField()
	currentRatio =  models.FloatField()
	interestCoverage =  models.FloatField()
	totalDebtToCapital =  models.FloatField()
	ltDebtToEquity =  models.FloatField()
	totalDebtToEquity =  models.FloatField()
	revChangeYear =  models.FloatField()
	revChangeTTM =  models.FloatField()
	revChangeIn =  models.FloatField()
	sharesOutstanding =  models.FloatField()
	marketCapFloat =  models.FloatField()
	marketCap =  models.FloatField()
	bookValuePerShare =  models.FloatField()
	shortIntToFloat =  models.FloatField()
	shortIntDayToCover =  models.FloatField()

	class Meta:
		verbose_name = "Fundamental"
		verbose_name_plural = "Fundamentals"