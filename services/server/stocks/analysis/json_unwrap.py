import pandas as pd

def check_date(date, df):
    while True:
        if len(df.loc[df['datetime']==date].index) != 0:
            break
        else:
            date=date+pd.Timedelta(1, unit='D')

    return date


json_df=pd.read_json('data_low.json')
print (json_df)



start_date=check_date(pd.to_datetime('2019-10-19'), json_df)
end_date=check_date(pd.to_datetime('2020-2-3'), json_df)

print ('start index: ', json_df.loc[json_df['datetime']==start_date].index)
print ('stop index: ', json_df.loc[json_df['datetime']==end_date].index)

json_df.rename(inplace=True, columns={'open':'Open','high':'High', 'low':'Low','close':'Close','volume':'Volume','datetime':'Date'})

print ('renamed json:\n', json_df)
