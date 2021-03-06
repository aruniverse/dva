# Generated by Django 2.2.6 on 2020-04-05 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fundamental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('symbol', models.CharField(max_length=6)),
                ('high52', models.DecimalField(decimal_places=4, max_digits=8)),
                ('low52', models.DecimalField(decimal_places=4, max_digits=8)),
                ('dividendAmount', models.FloatField()),
                ('dividendYield', models.FloatField()),
                ('dividendPayAmount', models.FloatField()),
                ('dividendDate', models.DateField()),
                ('dividendPayDate', models.DateField()),
                ('divGrowthRate3Year', models.FloatField()),
                ('peRatio', models.FloatField()),
                ('pegRatio', models.FloatField()),
                ('pbRatio', models.FloatField()),
                ('prRatio', models.FloatField()),
                ('pcfRatio', models.FloatField()),
                ('beta', models.FloatField()),
                ('vol1DayAvg', models.IntegerField()),
                ('vol10DayAvg', models.IntegerField()),
                ('vol3MonthAvg', models.IntegerField()),
                ('epsTTM', models.FloatField()),
                ('epsChangePercentTTM', models.FloatField()),
                ('epsChangeYear', models.FloatField()),
                ('epsChange', models.FloatField()),
                ('grossMarginTTM', models.FloatField()),
                ('grossMarginMRQ', models.FloatField()),
                ('netProfitMarginTTM', models.FloatField()),
                ('netProfitMarginMRQ', models.FloatField()),
                ('operatingMarginTTM', models.FloatField()),
                ('operatingMarginMRQ', models.FloatField()),
                ('returnOnEquity', models.FloatField()),
                ('returnOnAssets', models.FloatField()),
                ('returnOnInvestment', models.FloatField()),
                ('quickRatio', models.FloatField()),
                ('currentRatio', models.FloatField()),
                ('interestCoverage', models.FloatField()),
                ('totalDebtToCapital', models.FloatField()),
                ('ltDebtToEquity', models.FloatField()),
                ('totalDebtToEquity', models.FloatField()),
                ('revChangeYear', models.FloatField()),
                ('revChangeTTM', models.FloatField()),
                ('revChangeIn', models.FloatField()),
                ('sharesOutstanding', models.FloatField()),
                ('marketCapFloat', models.FloatField()),
                ('marketCap', models.FloatField()),
                ('bookValuePerShare', models.FloatField()),
                ('shortIntToFloat', models.FloatField()),
                ('shortIntDayToCover', models.FloatField()),
            ],
            options={
                'verbose_name': 'Fundamental',
                'verbose_name_plural': 'Fundamentals',
            },
        ),
        migrations.CreateModel(
            name='IndexesDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IndexesMin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NASDAQDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NASDAQMin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NYSEDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='NYSEMin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=6)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
                ('datetime_epoch', models.IntegerField()),
            ],
        ),
    ]
