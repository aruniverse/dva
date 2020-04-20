import pandas as pd
import argparse
import json
import ta as ta
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_selection import f_regression
import random

class price_analysis:

    def __init__(self, data_file, start_date_str, end_date_str, output_json_name, verbose):
        # start_date_str = start_date from user - 40 days
        # end_date_str = end_date from user + 60 days
        self.verbose=verbose #print output or not
        self.output_json_name=output_json_name  #name for output json object
        self.data_file = data_file
        self.create_df(self.data_file) #create dataframe from datafile

        with open('parameters.json', "r") as read_file: #assign parameters from parameters.json file
            self.parameters= read_file


        #Index in df_data to start analysis--this accounts for different backward looking periods for the different indicators
        start_date=self.check_date(pd.to_datetime(start_date_str))
        self.start_index=self.df_data.loc[self.df_data['Date']==start_date].index[0]
        if verbose: print ('Start index:', self.start_index)

        #Index in df data to stop analysis--this accounts for forward looking returns for binning
        stop_date=self.check_date(pd.to_datetime(end_date_str))
        self.stop_index=self.df_data.loc[self.df_data['Date']==stop_date].index[0]
        if verbose: print ('Stop index:', self.stop_index)

        self.df_anal=pd.DataFrame(index=self.df_data.index)         #create dataframe for analysis
        self.df_anal['Date']=self.df_data['Date']

        self.calc_max_move()

        self.calc_daily_return(self.df_data, 'Close')

        self.df_strategy=pd.DataFrame(index=self.df_data.index)     #create dataframe for strategy results


        self.results={'dates': self.df_data.loc[self.start_index:self.stop_index,'Date_str'].tolist(),
                      'daily_ret': self.df_data.loc[self.start_index:self.stop_index,'Daily_return'].tolist(),
                      'cum_return': self.df_data.loc[self.start_index:self.stop_index,'Cum_return'].tolist(),
                      'price': self.df_data.loc[self.start_index:self.stop_index,'Close'].tolist(),
                      'term':self.parameters['term'],
                      'move':self.parameters['move'],
                      'strategy':{},
                      'indicators':{},
                      'predict':{},
                      'f_regression':{}}


# df = pd.DataFrame(list(BlogPost.objects.all().values()))
# df = pd.DataFrame(list(BlogPost.objects.filter(date__gte=datetime.datetime(2012, 5, 1)).values()))
# df = pd.DataFrame(list(BlogPost.objects.all().values('author', 'date', 'slug')))

    def create_df(self, data_file):
        # # df = pd.DataFrame(list(BlogPost.objects.all().values()))
        # # df = pd.DataFrame(list(BlogPost.objects.filter(date__gte=datetime.datetime(2012, 5, 1)).values()))
        # # df = pd.DataFrame(list(BlogPost.objects.all().values('author', 'date', 'slug')))
        # if data_file == 'from_database':
        #     pd.DataFrame(list(
        # else:
        #     if data_file.endswith('.csv'):
        #         self.df_data= pd.read_csv(data_file)
        #         self.df_data['Date']= pd.to_datetime(self.df_data['Date'])   #Convert date to datetime

        #     elif data_file.endswith('.json'):
        #         self.df_data=pd.read_json(data_file)
        #         self.df_data.rename(inplace=True, columns={'open':'Open','high':'High','close':'Close','volume':'Volume','datetime':'Date'})
        #         self.df_data['Low']=self.df_data['Close']-random.random()*10  #Temporary placeholder for low

        #     else:
        #         print ('Invalid file extension on input file')
        # # self.df_data['Date_str']=self.df_data['Date'].dt.strftime('%m/%d/%Y') #Add column wiht text as dates for output

        self.df_data=pd.read_jsons(data_file)
        self.df_data.rename(inplace=True, columns={'open':'Open','high':'High','close':'Close','volume':'Volume','datetime':'Date'})
        self.df_data['Low']=self.df_data['Close']-random.random()*10  #Temporary placeholder for low
        self.df_data = pd.DataFrame(list(self.data_file))
        self.df_data['Date'] = self.df_data['datetime']

    def check_date(self, date):
        while True:
            if len(self.df_data.loc[self.df_data['Date']==date].index) != 0:
                break
            else:
                date=date+pd.Timedelta(1, unit='D')

        return date

    def get_max_period(self):
        max_period=0
        for indicator in self.parameters['indicator'].keys():
            if 'period' in self.parameters['indicator'][indicator]['parameters']:
                if self.parameters['indicator'][indicator]['parameters']['period']>max_period:
                    max_period=self.parameters['indicator'][indicator]['parameters']['period']
        for strategy in self.parameters['strategy'].keys():
            if 'period' in self.parameters['strategy'][strategy]['parameters']:
                if self.parameters['strategy'][strategy]['parameters']['period']>max_period:
                    max_period=self.parameters['strategy'][strategy]['parameters']['period']

        return max_period+1

    def get_max_term(self):
        return max(self.parameters['term'])

    def strategy_returns(self):

        self.df_strategy_return=pd.DataFrame(index=self.df_data.index)
        for col_name in list(self.df_strategy):
            self.df_strategy_return[col_name+'_daily']=self.df_strategy[col_name]*self.df_data['Daily_return']

        self.df_strategy_return.dropna(inplace=True)
        for col_name in list(self.df_strategy):
            self.df_strategy_return[col_name]=self.df_strategy_return[col_name+'_daily'].cumsum()
            self.results['strategy'][col_name]['cum_return']=self.df_strategy_return.loc[self.start_index:self.stop_index, col_name].tolist()

    def calc_daily_return(self, dataframe, series):

        dataframe['Daily_return']=(dataframe[series]-dataframe[series].shift(1))/dataframe[series].shift(1)
        dataframe['Cum_return']=dataframe['Daily_return'].cumsum()
        dataframe.dropna(inplace=True)

    #Allocates max move for prescribed term into defined bucket
    def calc_max_move(self):

        append_data=False

        for term in self.parameters['term']:
            term_series=pd.Series(index=self.df_data.index, dtype=float)
            term_hi_series=pd.Series(index=self.df_data.index, dtype=float)
            term_low_series=pd.Series(index=self.df_data.index, dtype=float)
            term_open_series=pd.Series(index=self.df_data.index, dtype=float)
            term_calc_max=pd.Series(index=self.df_data.index, dtype=float)
            if self.verbose: print ('term:', term)
            if self.verbose: print('start index:', self.df_data.index[0])
            if self.verbose: print('stop_index:', self.df_data.index[-1])
            for i in range(self.df_data.index[0],self.df_data.index[-1]-term):
                open_val=self.df_data.loc[i,'Open']
                max_high=self.df_data.loc[i:i+term,'High'].max()
                max_low=self.df_data.loc[i:i+term,'Low'].min()
                max_up=(max_high-open_val)/open_val
                if (abs((max_low-open_val)/open_val)>max_up):
                    max_move=(max_low-open_val)/open_val
                else:
                    max_move=max_up
                for bucket in self.parameters['move']:
                    if max_move<bucket/100:
                        term_series[i]=int(self.parameters['move'].index(bucket))
                        break
                    else:
                        term_series[i]=len(self.parameters['move'])
                term_hi_series[i]=max_up
                term_low_series[i]=(max_low-open_val)/open_val
                term_open_series[i]=open_val
                term_calc_max[i]=max_move
            if self.verbose: print ('term_'+str(term)+'\n', term_series)
            self.df_anal['term_'+str(term)]=term_series
            if append_data: self.df_data['term_'+str(term)+'_hi']=term_hi_series
            if append_data: self.df_data['term_'+str(term)+'_low']=term_low_series
            if append_data: self.df_data['term_'+str(term)+'_open']=term_open_series
            if append_data: self.df_data['term_'+str(term)+'_max']=term_calc_max

    def add_indicators(self):

        self.indicator_list=[]

        if self.parameters['indicator']['acc_dist_index']['include']==True:
            self.indicator_list.append('acc_dist_index')
            self.df_anal['acc_dist_index']=ta.volume.acc_dist_index(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], self.df_data['Volume'])

        if self.parameters['indicator']['chaikin_money_flow']['include']==True:
            self.indicator_list.append('chaikin_money_flow')
            period_cmf=self.parameters['indicator']['chaikin_money_flow']['parameters']['period']
            self.df_anal['chaikin_money_flow']=ta.volume.chaikin_money_flow(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], self.df_data['Volume'], period_cmf)

        if self.parameters['indicator']['ease_of_move']['include']==True:
            self.indicator_list.append('ease_of_move')
            period_eom=self.parameters['indicator']['ease_of_move']['parameters']['period']
            self.df_anal['ease_of_move']=ta.volume.ease_of_movement(self.df_data['High'], self.df_data['Low'], self.df_data['Volume'], period_eom)

        if self.parameters['indicator']['williams_r']['include']==True:
            self.indicator_list.append('williams_r')
            period_wr=self.parameters['indicator']['williams_r']['parameters']['period']
            self.df_anal['williams_r']=ta.momentum.wr(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], period_wr)

        if self.parameters['indicator']['rel_strength']['include']==True:
            self.indicator_list.append('rel_strength')
            period_rsi=self.parameters['indicator']['rel_strength']['parameters']['period']
            self.df_anal['rel_strength']=ta.momentum.rsi(self.df_data['Close'], period_rsi)

        self.results['predict']['indicator_list']=self.indicator_list
        self.random_forest_analysis()
        self.f_test_analysis()

    def add_strategy(self):
        self.strategy_list=[]

        if self.parameters['strategy']['bollinger']['include']==True:
            self.strategy_list.append('bollinger')
            self.results['strategy']['bollinger']={}
            self.bollinger_band()

        if self.parameters['strategy']['williams_r']['include']==True:
            self.strategy_list.append('williams_r')
            self.results['strategy']['williams_r']={}
            self.williams_r()

        #self.results['strategy']['strategy_list']=self.strategy_list


    def random_forest_analysis(self):

        #Select rows for analysis for given start and stop index
        rows_to_drop=[]
        for i in range(0,self.start_index):
            rows_to_drop.append(i)
        for i in range(self.stop_index+1, self.df_anal.index[-1]+1):
            rows_to_drop.append(i)

        print ("\nRows to drop:\n", rows_to_drop)

        self.df_anal.drop(rows_to_drop, inplace=True)
        print ("\ndf_anal:\n", self.df_anal)

        for term in self.parameters['term']:
            x_data=self.df_anal.loc[:,self.indicator_list] #start at reference index
            y_data=self.df_anal.loc[:,'term_'+str(term)]  #start at reference index

            x_train, x_test, y_train, y_test=train_test_split(x_data, y_data, test_size=0.25)
            clf = RandomForestClassifier(n_estimators=6)
            clf.fit(x_train, np.ravel(y_train))

            y_pred_train_rf=clf.predict(x_train)
            score_train_rf=accuracy_score(y_train, y_pred_train_rf)
            if self.verbose: print ('term_'+str(term)+'train:', score_train_rf)

            y_pred_test_rf=clf.predict(x_test)
            score_test_rf=accuracy_score(y_test, y_pred_test_rf)
            if self.verbose: print ('term_'+str(term)+'test:', score_test_rf)

            feat_import=clf.feature_importances_
            if self.verbose: print ('term_'+str(term)+'feat importance values:', feat_import)

            n=len(feat_import)
            if self.verbose: print ('term_'+str(term)+'feat importance values:', feat_import.argsort()[::-1][:n])

            self.df_anal['predict_term_'+str(term)]=clf.predict(x_data)

            self.results['predict']['term_'+str(term)]={'train_score':score_train_rf,
                                                        'test_score':score_test_rf,
                                                        'importance_values':feat_import.tolist(),
                                                        'importance_order':feat_import.argsort()[::-1][:n].tolist(),
                                                        'predict':clf.predict(x_data).tolist()}
            for ind in self.indicator_list:
                self.results['indicators'][ind]=self.df_anal[ind].tolist()

    def f_test_analysis(self):
        self.df_anal.dropna(inplace=True)
        self.results['f_regression']['indicator_list']=self.indicator_list

        for term in self.parameters['term']:
            x_data=self.df_anal.loc[:,self.indicator_list]
            y_data=self.df_anal.loc[:,'term_'+str(term)]

            #pval reutrning nan if all predicted values are the same--omit in output if that is the case
            f, pval=f_regression(x_data, y_data, center=True)
            for val in pval:
                if np.isnan(val):
                    self.results['f_regression']['term_'+str(term)]={'p_values': []}
                else:
                    self.results['f_regression']['term_'+str(term)]={'p_values': pval.tolist()}
            if self.verbose: print ('f_test results for ', term, ':', pval)



    def bollinger_band(self):

        period=self.parameters['strategy']['bollinger']['parameters']['period']
        num_dev=self.parameters['strategy']['bollinger']['parameters']['num_dev']

        self.bb_df=self.df_data.copy()
        for i in range(self.df_data.index[0]+period,self.df_data.index[-1]+1):
            self.bb_df.loc[i,'Average']=self.bb_df.loc[i-period:i,'Close'].mean()
            self.bb_df.loc[i,'StDev']=self.bb_df.loc[i-period:i,'Close'].std()
            self.bb_df['bollinger_hi']=self.bb_df['Average']+num_dev*self.bb_df['StDev']
            self.bb_df['bollinger_low']=self.bb_df['Average']-num_dev*self.bb_df['StDev']

        owned_long=0
        owned_short=0

        bollinger_actions=[]
        for i in range(self.df_data.index[0]+period,self.df_data.index[-1]+1):
            if owned_long==0 and self.bb_df.loc[i,'Close']<self.bb_df.loc[i,'bollinger_low']:
                owned_long=1
                bollinger_actions.append([self.df_data.loc[i,'Date_str'],'enter','long'])
            if owned_long==1 and self.bb_df.loc[i,'Close']>self.bb_df.loc[i,'Average']:
                owned_long=0
                bollinger_actions.append([self.df_data.loc[i,'Date_str'],'exit','long'])
            if owned_short==0 and self.bb_df.loc[i,'Close']>self.bb_df.loc[i,'bollinger_hi']:
                owned_short=1
                bollinger_actions.append([self.df_data.loc[i,'Date_str'],'enter','short'])
            if owned_short==1 and self.bb_df.loc[i,'Close']<self.bb_df.loc[i,'Average']:
                owned_short=0
                bollinger_actions.append([self.df_data.loc[i,'Date_str'],'exit','short'])
            self.bb_df.loc[i,'BB_owned_short']=owned_short
            self.bb_df.loc[i,'BB_owned_long']=owned_long
            self.df_strategy.loc[i,'bollinger']=owned_long-owned_short

        if self.verbose: print ("\nBollinger actions:\n",bollinger_actions, "\n")
        print (self.results)
        self.results['strategy']['bollinger']['actions']=bollinger_actions


    def williams_r(self):

        period_wr=self.parameters['strategy']['williams_r']['parameters']['period']
        self.wr_df=self.df_data.copy()
        self.wr_df['williams_r']=ta.momentum.wr(self.wr_df['High'], self.wr_df['Low'], self.wr_df['Close'], period_wr)

        owned_long=0
        owned_short=0
        williams_r_actions=[]
        for i in range(self.df_data.index[0]+period_wr,self.df_data.index[-1]+1):
            if owned_long==0 and self.wr_df.loc[i,'williams_r']<-80:
                owned_long=1
                williams_r_actions.append([self.df_data.loc[i,'Date_str'],'enter','long'])
            if owned_long==1 and self.wr_df.loc[i,'williams_r']>-50:
                owned_long=0
                williams_r_actions.append([self.df_data.loc[i,'Date_str'],'exit','long'])
            if owned_short==0 and self.wr_df.loc[i,'williams_r']>-20:
                owned_short=1
                williams_r_actions.append([self.df_data.loc[i,'Date_str'],'enter','short'])
            if owned_short==1 and self.wr_df.loc[i,'williams_r']<-50:
                owned_short=0
                williams_r_actions.append([self.df_data.loc[i,'Date_str'],'exit','short'])
            self.wr_df.loc[i,'wr_owned_short']=owned_short
            self.wr_df.loc[i,'wr_owned_long']=owned_long
            self.df_strategy.loc[i,'williams_r']=owned_long-owned_short

        if self.verbose: print ("\nWilliams_r actions:\n",williams_r_actions, "\n")
        self.results['strategy']['williams_r']['actions']=williams_r_actions


    def write_results_json(self):
        pass

    def write_data_to_csv(self):
        self.df_data.to_csv('data_out.csv')

    def write_analysis_to_csv(self):
        self.df_anal.to_csv('analysis_out.csv')

    def write_bollinger_band_to_csv(self):
        self.bb_df.to_csv('bollinger.csv')

    def write_williams_r_to_csv(self):
        self.wr_df.to_csv('williams_r.csv')

    def write_strategy_results(self):
        self.df_strategy_return.to_csv('strategy.csv')

    def get_data_df(self):
        return self.df_data

    def write_results_json(self):
        return json.dumps(pa.results)


# ##Main

# if __name__ == "__main__":

#     verbose=True

#     parser=argparse.ArgumentParser(description='sample command python price_analysis.py <input data file name> <start date> <end date> <output json file>')
#     parser.add_argument("data_file", help="name of data input file")
#     parser.add_argument("start_date", help="start date for analysis")
#     parser.add_argument("end_date", help="end date for analysis")
#     parser.add_argument("output_file", help="name of output file")
#     args=parser.parse_args()


#     #Price analysis
#     pa=price_analysis(args.data_file, args.start_date, args.end_date, args.output_file, verbose)
#     pa.add_indicators() #

#     #Strategy comparison"
#     pa.add_strategy()
#     pa.strategy_returns()
#     pa.write_results_json()




#     #Print values
#     if verbose: print ('Input data:\n', pd.read_csv(args.data_file))
#     if verbose: print ('Analyze dataframe:\n', pa.df_anal)
#     if verbose: print ('Bollinger bands dataframe:\n', pa.bb_df)
#     if verbose: print ('Final data dataframe:\n', pa.df_data)
#     if verbose: print ('Strategy dataframe:\n', pa.df_strategy)
#     if verbose: print ('Strategy returns:\n', pa.df_strategy_return)
#     if verbose: print ('Results dictionary:', pa.results)
#     if verbose: pa.write_data_to_csv()
#     if verbose: pa.write_analysis_to_csv()
#     if verbose: pa.write_bollinger_band_to_csv()
#     if verbose: pa.write_williams_r_to_csv()
#     if verbose: pa.write_strategy_results()


import datetime


# start_date = 03/01/2020 # start_date_str 03/01/2020
# end_date = 04/19/2020 # end_date_str

_list = [
{'id': 18606, 'symbol': 'AAPL', 'open': 198.58, 'high': 199.85, 'low': 198.01, 'close': 199.23, 'volume': 17536646, 'datetime_epoch': 1555304400000, 'datetime': datetime.date(2019, 4, 15)},
{'id': 18607, 'symbol': 'AAPL', 'open': 199.46, 'high': 201.37, 'low': 198.56, 'close': 199.25, 'volume': 25696385, 'datetime_epoch': 1555390800000, 'datetime': datetime.date(2019, 4, 16)}, {'id': 18608, 'symbol': 'AAPL', 'open': 199.54, 'high': 203.38, 'low': 198.61, 'close': 203.13, 'volume': 28906780, 'datetime_epoch': 1555477200000, 'datetime': datetime.date(2019, 4, 17)}, {'id': 18609, 'symbol': 'AAPL', 'open': 203.12, 'high': 204.15, 'low': 202.52, 'close': 203.86, 'volume': 24195766, 'datetime_epoch': 1555563600000, 'datetime': datetime.date(2019, 4, 18)}, {'id': 18610, 'symbol': 'AAPL', 'open': 202.83, 'high': 204.94, 'low': 202.34, 'close': 204.53, 'volume': 19439545, 'datetime_epoch': 1555909200000, 'datetime': datetime.date(2019, 4, 22)}, {'id': 18611, 'symbol': 'AAPL', 'open': 204.43, 'high': 207.75, 'low': 203.9, 'close': 207.48, 'volume': 23322991, 'datetime_epoch': 1555995600000, 'datetime': datetime.date(2019, 4, 23)}, {'id': 18612, 'symbol': 'AAPL', 'open': 207.36, 'high': 208.48, 'low': 207.05, 'close': 207.16, 'volume': 17540609, 'datetime_epoch': 1556082000000, 'datetime': datetime.date(2019, 4, 24)}, {'id': 18613, 'symbol': 'AAPL', 'open': 206.83, 'high': 207.76, 'low': 205.12, 'close': 205.28, 'volume': 18543206, 'datetime_epoch': 1556168400000, 'datetime': datetime.date(2019, 4, 25)}, {'id': 18614, 'symbol': 'AAPL', 'open': 204.9, 'high': 205.0, 'low': 202.12, 'close': 204.3, 'volume': 18649102, 'datetime_epoch': 1556254800000, 'datetime': datetime.date(2019, 4, 26)}, {'id': 18615, 'symbol': 'AAPL', 'open': 204.4, 'high': 205.97, 'low': 203.86, 'close': 204.61, 'volume': 22204716, 'datetime_epoch': 1556514000000, 'datetime': datetime.date(2019, 4, 29)}, {'id': 18616, 'symbol': 'AAPL', 'open': 203.06, 'high': 203.4, 'low': 199.11, 'close': 200.67, 'volume': 46534923, 'datetime_epoch': 1556600400000, 'datetime': datetime.date(2019, 4, 30)}, {'id': 18617, 'symbol': 'AAPL', 'open': 209.88, 'high': 215.31, 'low': 209.23, 'close': 210.52, 'volume': 64827328, 'datetime_epoch': 1556686800000, 'datetime': datetime.date(2019, 5, 1)}, {'id': 18618, 'symbol': 'AAPL', 'open': 209.84, 'high': 212.65, 'low': 208.13, 'close': 209.15, 'volume': 31996324, 'datetime_epoch': 1556773200000, 'datetime': datetime.date(2019, 5, 2)}, {'id': 18619, 'symbol': 'AAPL', 'open': 210.89, 'high': 211.84, 'low': 210.23, 'close': 211.75, 'volume': 20892378, 'datetime_epoch': 1556859600000, 'datetime': datetime.date(2019, 5, 3)}, {'id': 18620, 'symbol': 'AAPL', 'open': 204.29, 'high': 208.84, 'low': 203.5, 'close': 208.48, 'volume': 32443113, 'datetime_epoch': 1557118800000, 'datetime': datetime.date(2019, 5, 6)}, {'id': 18621, 'symbol': 'AAPL', 'open': 205.88, 'high': 207.4175, 'low': 200.825, 'close': 202.86, 'volume': 38763698, 'datetime_epoch': 1557205200000, 'datetime': datetime.date(2019, 5, 7)}, {'id': 18622, 'symbol': 'AAPL', 'open': 201.9, 'high': 205.34, 'low': 201.75, 'close': 202.9, 'volume': 26339504, 'datetime_epoch': 1557291600000, 'datetime': datetime.date(2019, 5, 8)}, {'id': 18623, 'symbol': 'AAPL', 'open': 200.4, 'high': 201.68, 'low': 196.66, 'close': 200.72, 'volume': 34908607, 'datetime_epoch': 1557378000000, 'datetime': datetime.date(2019, 5, 9)}, {'id': 18624, 'symbol': 'AAPL', 'open': 197.419, 'high': 198.85, 'low': 192.77, 'close': 197.18, 'volume': 41208712, 'datetime_epoch': 1557464400000, 'datetime': datetime.date(2019, 5, 10)}, {'id': 18625, 'symbol': 'AAPL', 'open': 187.71, 'high': 189.48, 'low': 182.85, 'close': 185.72, 'volume': 57430623, 'datetime_epoch': 1557723600000, 'datetime': datetime.date(2019, 5, 13)}, {'id': 18626, 'symbol': 'AAPL', 'open': 186.41, 'high': 189.7, 'low': 185.41, 'close': 188.66, 'volume': 36529677, 'datetime_epoch': 1557810000000, 'datetime': datetime.date(2019, 5, 14)}, {'id': 18627, 'symbol': 'AAPL', 'open': 186.27, 'high': 191.75, 'low': 186.02, 'close': 190.92, 'volume': 26544718, 'datetime_epoch': 1557896400000, 'datetime': datetime.date(2019, 5, 15)}, {'id': 18628, 'symbol': 'AAPL', 'open': 189.91, 'high': 192.4689, 'low': 188.84, 'close': 190.08, 'volume': 33031364, 'datetime_epoch': 1557982800000, 'datetime': datetime.date(2019, 5, 16)}, {'id': 18629, 'symbol': 'AAPL', 'open': 186.93, 'high': 190.9, 'low': 186.76, 'close': 189.0, 'volume': 32879090, 'datetime_epoch': 1558069200000, 'datetime': datetime.date(2019, 5, 17)}, {'id': 18630, 'symbol': 'AAPL', 'open': 183.52, 'high': 184.349, 'low': 180.2839, 'close': 183.09, 'volume': 38612290, 'datetime_epoch': 1558328400000, 'datetime': datetime.date(2019, 5, 20)}, {'id': 18631, 'symbol': 'AAPL', 'open': 185.22, 'high': 188.0, 'low': 184.7, 'close': 186.6, 'volume': 28364848, 'datetime_epoch': 1558414800000, 'datetime': datetime.date(2019, 5, 21)}, {'id': 18632, 'symbol': 'AAPL', 'open': 184.66, 'high': 185.71, 'low': 182.55, 'close': 182.78, 'volume': 29748556, 'datetime_epoch': 1558501200000, 'datetime': datetime.date(2019, 5, 22)}, {'id': 18633, 'symbol': 'AAPL', 'open': 179.8, 'high': 180.54, 'low': 177.81, 'close': 179.66, 'volume': 36529736, 'datetime_epoch': 1558587600000, 'datetime': datetime.date(2019, 5, 23)}, {'id': 18634, 'symbol': 'AAPL', 'open': 180.2, 'high': 182.14, 'low': 178.62, 'close': 178.97, 'volume': 23714686, 'datetime_epoch': 1558674000000, 'datetime': datetime.date(2019, 5, 24)}, {'id': 18635, 'symbol': 'AAPL', 'open': 178.92, 'high': 180.59, 'low': 177.91, 'close': 178.23, 'volume': 27948160, 'datetime_epoch': 1559019600000, 'datetime': datetime.date(2019, 5, 28)}, {'id': 18636, 'symbol': 'AAPL', 'open': 176.42, 'high': 179.35, 'low': 176.0, 'close': 177.38, 'volume': 28481165, 'datetime_epoch': 1559106000000, 'datetime': datetime.date(2019, 5, 29)}, {'id': 18637, 'symbol': 'AAPL', 'open': 177.95, 'high': 179.23, 'low': 176.67, 'close': 178.3, 'volume': 21218412, 'datetime_epoch': 1559192400000, 'datetime': datetime.date(2019, 5, 30)}, {'id': 18638, 'symbol': 'AAPL', 'open': 176.23, 'high': 177.99, 'low': 174.99, 'close': 175.07, 'volume': 27043584, 'datetime_epoch': 1559278800000, 'datetime': datetime.date(2019, 5, 31)}, {'id': 18639, 'symbol': 'AAPL', 'open': 175.6, 'high': 177.92, 'low': 170.27, 'close': 173.3, 'volume': 40396069, 'datetime_epoch': 1559538000000, 'datetime': datetime.date(2019, 6, 3)}, {'id': 18640, 'symbol': 'AAPL', 'open': 175.44, 'high': 179.83, 'low': 174.52, 'close': 179.64, 'volume': 30967961, 'datetime_epoch': 1559624400000, 'datetime': datetime.date(2019, 6, 4)}, {'id': 18641, 'symbol': 'AAPL', 'open': 184.28, 'high': 184.99, 'low': 181.14, 'close': 182.54, 'volume': 29773427, 'datetime_epoch': 1559710800000, 'datetime': datetime.date(2019, 6, 5)}, {'id': 18642, 'symbol': 'AAPL', 'open': 183.08, 'high': 185.47, 'low': 182.1489, 'close': 185.22, 'volume': 22526311, 'datetime_epoch': 1559797200000, 'datetime': datetime.date(2019, 6, 6)}, {'id': 18643, 'symbol': 'AAPL', 'open': 186.51, 'high': 191.92, 'low': 185.77, 'close': 190.15, 'volume': 30684393, 'datetime_epoch': 1559883600000, 'datetime': datetime.date(2019, 6, 7)}, {'id': 18644, 'symbol': 'AAPL', 'open': 191.81, 'high': 195.37, 'low': 191.62, 'close': 192.58, 'volume': 26220851, 'datetime_epoch': 1560142800000, 'datetime': datetime.date(2019, 6, 10)}, {'id': 18645, 'symbol': 'AAPL', 'open': 194.86, 'high': 196.0, 'low': 193.6, 'close': 194.81, 'volume': 26932882, 'datetime_epoch': 1560229200000, 'datetime': datetime.date(2019, 6, 11)}, {'id': 18646, 'symbol': 'AAPL', 'open': 193.95, 'high': 195.97, 'low': 193.385, 'close': 194.19, 'volume': 18253189, 'datetime_epoch': 1560315600000, 'datetime': datetime.date(2019, 6, 12)}, {'id': 18647, 'symbol': 'AAPL', 'open': 194.7, 'high': 196.79, 'low': 193.6, 'close': 194.15, 'volume': 21674625, 'datetime_epoch': 1560402000000, 'datetime': datetime.date(2019, 6, 13)}, {'id': 18648, 'symbol': 'AAPL', 'open': 191.545, 'high': 193.5863, 'low': 190.3, 'close': 192.74, 'volume': 18761474, 'datetime_epoch': 1560488400000, 'datetime': datetime.date(2019, 6, 14)}, {'id': 18649, 'symbol': 'AAPL', 'open': 192.9, 'high': 194.96, 'low': 192.17, 'close': 193.89, 'volume': 14669144, 'datetime_epoch': 1560747600000, 'datetime': datetime.date(2019, 6, 17)}, {'id': 18650, 'symbol': 'AAPL', 'open': 196.05, 'high': 200.29, 'low': 195.21, 'close': 198.45, 'volume': 26551004, 'datetime_epoch': 1560834000000, 'datetime': datetime.date(2019, 6, 18)}, {'id': 18651, 'symbol': 'AAPL', 'open': 199.68, 'high': 199.88, 'low': 197.31, 'close': 197.87, 'volume': 21124235, 'datetime_epoch': 1560920400000, 'datetime': datetime.date(2019, 6, 19)}, {'id': 18652, 'symbol': 'AAPL', 'open': 200.37, 'high': 200.61, 'low': 198.03, 'close': 199.46, 'volume': 21513988, 'datetime_epoch': 1561006800000, 'datetime': datetime.date(2019, 6, 20)}, {'id': 18653, 'symbol': 'AAPL', 'open': 198.8, 'high': 200.85, 'low': 198.15, 'close': 198.78, 'volume': 47800589, 'datetime_epoch': 1561093200000, 'datetime': datetime.date(2019, 6, 21)}, {'id': 18654, 'symbol': 'AAPL', 'open': 198.54, 'high': 200.16, 'low': 198.17, 'close': 198.58, 'volume': 18220421, 'datetime_epoch': 1561352400000, 'datetime': datetime.date(2019, 6, 24)}, {'id': 18655, 'symbol': 'AAPL', 'open': 198.43, 'high': 199.26, 'low': 195.29, 'close': 195.57, 'volume': 21070334, 'datetime_epoch': 1561438800000, 'datetime': datetime.date(2019, 6, 25)}, {'id': 18656, 'symbol': 'AAPL', 'open': 197.77, 'high': 200.99, 'low': 197.35, 'close': 199.8, 'volume': 26067512, 'datetime_epoch': 1561525200000, 'datetime': datetime.date(2019, 6, 26)}, {'id': 18657, 'symbol': 'AAPL', 'open': 200.29, 'high': 201.57, 'low': 199.57, 'close': 199.74, 'volume': 20899717, 'datetime_epoch': 1561611600000, 'datetime': datetime.date(2019, 6, 27)}, {'id': 18658, 'symbol': 'AAPL', 'open': 198.68, 'high': 199.495, 'low': 197.05, 'close': 197.92, 'volume': 31110642, 'datetime_epoch': 1561698000000, 'datetime': datetime.date(2019, 6, 28)}, {'id': 18659, 'symbol': 'AAPL', 'open': 203.17, 'high': 204.49, 'low': 200.65, 'close': 201.55, 'volume': 27316739, 'datetime_epoch': 1561957200000, 'datetime': datetime.date(2019, 7, 1)}, {'id': 18660, 'symbol': 'AAPL', 'open': 201.41, 'high': 203.1323, 'low': 201.36, 'close': 202.73, 'volume': 16935217, 'datetime_epoch': 1562043600000, 'datetime': datetime.date(2019, 7, 2)}, {'id': 18661, 'symbol': 'AAPL', 'open': 203.28, 'high': 204.44, 'low': 202.6901, 'close': 204.41, 'volume': 11362045, 'datetime_epoch': 1562130000000, 'datetime': datetime.date(2019, 7, 3)}, {'id': 18662, 'symbol': 'AAPL', 'open': 203.35, 'high': 205.08, 'low': 202.9, 'close': 204.23, 'volume': 17265518, 'datetime_epoch': 1562302800000, 'datetime': datetime.date(2019, 7, 5)}, {'id': 18663, 'symbol': 'AAPL', 'open': 200.81, 'high': 201.4, 'low': 198.41, 'close': 200.02, 'volume': 25338628, 'datetime_epoch': 1562562000000, 'datetime': datetime.date(2019, 7, 8)}, {'id': 18664, 'symbol': 'AAPL', 'open': 199.2, 'high': 201.51, 'low': 198.81, 'close': 201.24, 'volume': 20578015, 'datetime_epoch': 1562648400000, 'datetime': datetime.date(2019, 7, 9)}, {'id': 18665, 'symbol': 'AAPL', 'open': 201.85, 'high': 203.73, 'low': 201.56, 'close': 203.23, 'volume': 17897138, 'datetime_epoch': 1562734800000, 'datetime': datetime.date(2019, 7, 10)}, {'id': 18666, 'symbol': 'AAPL', 'open': 203.31, 'high': 204.39, 'low': 201.71, 'close': 201.75, 'volume': 20191842, 'datetime_epoch': 1562821200000, 'datetime': datetime.date(2019, 7, 11)}, {'id': 18667, 'symbol': 'AAPL', 'open': 202.45, 'high': 204.0, 'low': 202.2, 'close': 203.3, 'volume': 17595212, 'datetime_epoch': 1562907600000, 'datetime': datetime.date(2019, 7, 12)}, {'id': 18668, 'symbol': 'AAPL', 'open': 204.09, 'high': 205.87, 'low': 204.0, 'close': 205.21, 'volume': 16947420, 'datetime_epoch': 1563166800000, 'datetime': datetime.date(2019, 7, 15)}, {'id': 18669, 'symbol': 'AAPL', 'open': 204.59, 'high': 206.11, 'low': 203.5, 'close': 204.5, 'volume': 16866816, 'datetime_epoch': 1563253200000, 'datetime': datetime.date(2019, 7, 16)}, {'id': 18670, 'symbol': 'AAPL', 'open': 204.05, 'high': 205.0915, 'low': 203.27, 'close': 203.35, 'volume': 14107450, 'datetime_epoch': 1563339600000, 'datetime': datetime.date(2019, 7, 17)}, {'id': 18671, 'symbol': 'AAPL', 'open': 204.0, 'high': 205.88, 'low': 203.7, 'close': 205.66, 'volume': 18582161, 'datetime_epoch': 1563426000000, 'datetime': datetime.date(2019, 7, 18)}, {'id': 18672, 'symbol': 'AAPL', 'open': 205.79, 'high': 206.5, 'low': 202.36, 'close': 202.59, 'volume': 20929307, 'datetime_epoch': 1563512400000, 'datetime': datetime.date(2019, 7, 19)}, {'id': 18673, 'symbol': 'AAPL', 'open': 203.65, 'high': 207.23, 'low': 203.61, 'close': 207.22, 'volume': 22277932, 'datetime_epoch': 1563771600000, 'datetime': datetime.date(2019, 7, 22)}, {'id': 18674, 'symbol': 'AAPL', 'open': 208.46, 'high': 208.91, 'low': 207.29, 'close': 208.84, 'volume': 18355210, 'datetime_epoch': 1563858000000, 'datetime': datetime.date(2019, 7, 23)}, {'id': 18675, 'symbol': 'AAPL', 'open': 207.67, 'high': 209.15, 'low': 207.17, 'close': 208.67, 'volume': 14991567, 'datetime_epoch': 1563944400000, 'datetime': datetime.date(2019, 7, 24)}, {'id': 18676, 'symbol': 'AAPL', 'open': 208.89, 'high': 209.24, 'low': 206.73, 'close': 207.02, 'volume': 13909562, 'datetime_epoch': 1564030800000, 'datetime': datetime.date(2019, 7, 25)}, {'id': 18677, 'symbol': 'AAPL', 'open': 207.48, 'high': 209.73, 'low': 207.14, 'close': 207.74, 'volume': 17618874, 'datetime_epoch': 1564117200000, 'datetime': datetime.date(2019, 7, 26)}, {'id': 18678, 'symbol': 'AAPL', 'open': 208.46, 'high': 210.64, 'low': 208.44, 'close': 209.68, 'volume': 21673389, 'datetime_epoch': 1564376400000, 'datetime': datetime.date(2019, 7, 29)}, {'id': 18679, 'symbol': 'AAPL', 'open': 208.76, 'high': 210.16, 'low': 207.31, 'close': 208.78, 'volume': 33935718, 'datetime_epoch': 1564462800000, 'datetime': datetime.date(2019, 7, 30)}, {'id': 18680, 'symbol': 'AAPL', 'open': 216.42, 'high': 221.37, 'low': 211.3, 'close': 213.04, 'volume': 69281361, 'datetime_epoch': 1564549200000, 'datetime': datetime.date(2019, 7, 31)}, {'id': 18681, 'symbol': 'AAPL', 'open': 213.9, 'high': 218.03, 'low': 206.7435, 'close': 208.43, 'volume': 54017922, 'datetime_epoch': 1564635600000, 'datetime': datetime.date(2019, 8, 1)}, {'id': 18682, 'symbol': 'AAPL', 'open': 205.53, 'high': 206.43, 'low': 201.63, 'close': 204.02, 'volume': 40862122, 'datetime_epoch': 1564722000000, 'datetime': datetime.date(2019, 8, 2)}, {'id': 18683, 'symbol': 'AAPL', 'open': 197.99, 'high': 198.649, 'low': 192.58, 'close': 193.34, 'volume': 52392969, 'datetime_epoch': 1564981200000, 'datetime': datetime.date(2019, 8, 5)}, {'id': 18684, 'symbol': 'AAPL', 'open': 196.31, 'high': 198.067, 'low': 194.04, 'close': 197.0, 'volume': 35824787, 'datetime_epoch': 1565067600000, 'datetime': datetime.date(2019, 8, 6)}, {'id': 18685, 'symbol': 'AAPL', 'open': 195.41, 'high': 199.56, 'low': 193.82, 'close': 199.04, 'volume': 33364400, 'datetime_epoch': 1565154000000, 'datetime': datetime.date(2019, 8, 7)}, {'id': 18686, 'symbol': 'AAPL', 'open': 200.2, 'high': 203.53, 'low': 199.39, 'close': 203.43, 'volume': 27009523, 'datetime_epoch': 1565240400000, 'datetime': datetime.date(2019, 8, 8)}, {'id': 18687, 'symbol': 'AAPL', 'open': 201.3, 'high': 202.76, 'low': 199.29, 'close': 200.99, 'volume': 24619746, 'datetime_epoch': 1565326800000, 'datetime': datetime.date(2019, 8, 9)}, {'id': 18688, 'symbol': 'AAPL', 'open': 199.62, 'high': 202.0516, 'low': 199.15, 'close': 200.48, 'volume': 22481889, 'datetime_epoch': 1565586000000, 'datetime': datetime.date(2019, 8, 12)}, {'id': 18689, 'symbol': 'AAPL', 'open': 201.02, 'high': 212.14, 'low': 200.83, 'close': 208.97, 'volume': 47539786, 'datetime_epoch': 1565672400000, 'datetime': datetime.date(2019, 8, 13)}, {'id': 18690, 'symbol': 'AAPL', 'open': 203.16, 'high': 206.44, 'low': 202.5869, 'close': 202.75, 'volume': 36547443, 'datetime_epoch': 1565758800000, 'datetime': datetime.date(2019, 8, 14)}, {'id': 18691, 'symbol': 'AAPL', 'open': 203.46, 'high': 205.14, 'low': 199.67, 'close': 201.74, 'volume': 27883363, 'datetime_epoch': 1565845200000, 'datetime': datetime.date(2019, 8, 15)}, {'id': 18692, 'symbol': 'AAPL', 'open': 204.28, 'high': 207.16, 'low': 203.84, 'close': 206.5, 'volume': 28813624, 'datetime_epoch': 1565931600000, 'datetime': datetime.date(2019, 8, 16)}, {'id': 18693, 'symbol': 'AAPL', 'open': 210.62, 'high': 212.7307, 'low': 210.025, 'close': 210.35, 'volume': 24431915, 'datetime_epoch': 1566190800000, 'datetime': datetime.date(2019, 8, 19)}, {'id': 18694, 'symbol': 'AAPL', 'open': 210.88, 'high': 213.35, 'low': 210.32, 'close': 210.36, 'volume': 26919529, 'datetime_epoch': 1566277200000, 'datetime': datetime.date(2019, 8, 20)}, {'id': 18695, 'symbol': 'AAPL', 'open': 212.99, 'high': 213.65, 'low': 211.6032, 'close': 212.64, 'volume': 21564747, 'datetime_epoch': 1566363600000, 'datetime': datetime.date(2019, 8, 21)}, {'id': 18696, 'symbol': 'AAPL', 'open': 213.19, 'high': 214.435, 'low': 210.75, 'close': 212.46, 'volume': 22267819, 'datetime_epoch': 1566450000000, 'datetime': datetime.date(2019, 8, 22)}, {'id': 18697, 'symbol': 'AAPL', 'open': 209.43, 'high': 212.051, 'low': 201.0, 'close': 202.64, 'volume': 46882843, 'datetime_epoch': 1566536400000, 'datetime': datetime.date(2019, 8, 23)}, {'id': 18698, 'symbol': 'AAPL', 'open': 205.86, 'high': 207.19, 'low': 205.0573, 'close': 206.49, 'volume': 26066130, 'datetime_epoch': 1566795600000, 'datetime': datetime.date(2019, 8, 26)}, {'id': 18699, 'symbol': 'AAPL', 'open': 207.86, 'high': 208.55, 'low': 203.53, 'close': 204.16, 'volume': 25897344, 'datetime_epoch': 1566882000000, 'datetime': datetime.date(2019, 8, 27)}, {'id': 18700, 'symbol': 'AAPL', 'open': 204.1, 'high': 205.72, 'low': 203.32, 'close': 205.53, 'volume': 15957632, 'datetime_epoch': 1566968400000, 'datetime': datetime.date(2019, 8, 28)}, {'id': 18701, 'symbol': 'AAPL', 'open': 208.5, 'high': 209.32, 'low': 206.655, 'close': 209.01, 'volume': 21007652, 'datetime_epoch': 1567054800000, 'datetime': datetime.date(2019, 8, 29)}, {'id': 18702, 'symbol': 'AAPL', 'open': 210.16, 'high': 210.45, 'low': 207.2, 'close': 208.74, 'volume': 21162561, 'datetime_epoch': 1567141200000, 'datetime': datetime.date(2019, 8, 30)}, {'id': 18703, 'symbol': 'AAPL', 'open': 206.43, 'high': 206.98, 'low': 204.22, 'close': 205.7, 'volume': 20059574, 'datetime_epoch': 1567486800000, 'datetime': datetime.date(2019, 9, 3)}, {'id': 18704, 'symbol': 'AAPL', 'open': 208.39, 'high': 209.48, 'low': 207.32, 'close': 209.19, 'volume': 19216820, 'datetime_epoch': 1567573200000, 'datetime': datetime.date(2019, 9, 4)}, {'id': 18705, 'symbol': 'AAPL', 'open': 212.0, 'high': 213.97, 'low': 211.51, 'close': 213.28, 'volume': 23946984, 'datetime_epoch': 1567659600000, 'datetime': datetime.date(2019, 9, 5)}, {'id': 18706, 'symbol': 'AAPL', 'open': 214.05, 'high': 214.42, 'low': 212.51, 'close': 213.26, 'volume': 19362294, 'datetime_epoch': 1567746000000, 'datetime': datetime.date(2019, 9, 6)}, {'id': 18707, 'symbol': 'AAPL', 'open': 214.84, 'high': 216.44, 'low': 211.07, 'close': 214.17, 'volume': 27309401, 'datetime_epoch': 1568005200000, 'datetime': datetime.date(2019, 9, 9)}, {'id': 18708, 'symbol': 'AAPL', 'open': 213.86, 'high': 216.78, 'low': 211.71, 'close': 216.7, 'volume': 31777931, 'datetime_epoch': 1568091600000, 'datetime': datetime.date(2019, 9, 10)}, {'id': 18709, 'symbol': 'AAPL', 'open': 218.07, 'high': 223.71, 'low': 217.73, 'close': 223.59, 'volume': 44289646, 'datetime_epoch': 1568178000000, 'datetime': datetime.date(2019, 9, 11)}, {'id': 18710, 'symbol': 'AAPL', 'open': 224.8, 'high': 226.42, 'low': 222.86, 'close': 223.085, 'volume': 32226669, 'datetime_epoch': 1568264400000, 'datetime': datetime.date(2019, 9, 12)}, {'id': 18711, 'symbol': 'AAPL', 'open': 220.0, 'high': 220.79, 'low': 217.02, 'close': 218.75, 'volume': 39763296, 'datetime_epoch': 1568350800000, 'datetime': datetime.date(2019, 9, 13)}, {'id': 18712, 'symbol': 'AAPL', 'open': 217.73, 'high': 220.13, 'low': 217.56, 'close': 219.9, 'volume': 21158141, 'datetime_epoch': 1568610000000, 'datetime': datetime.date(2019, 9, 16)}, {'id': 18713, 'symbol': 'AAPL', 'open': 219.96, 'high': 220.82, 'low': 219.12, 'close': 220.7, 'volume': 18386468, 'datetime_epoch': 1568696400000, 'datetime': datetime.date(2019, 9, 17)}, {'id': 18714, 'symbol': 'AAPL', 'open': 221.06, 'high': 222.85, 'low': 219.44, 'close': 222.77, 'volume': 25643093, 'datetime_epoch': 1568782800000, 'datetime': datetime.date(2019, 9, 18)}, {'id': 18715, 'symbol': 'AAPL', 'open': 222.01, 'high': 223.76, 'low': 220.37, 'close': 220.96, 'volume': 22187876, 'datetime_epoch': 1568869200000, 'datetime': datetime.date(2019, 9, 19)}, {'id': 18716, 'symbol': 'AAPL', 'open': 221.38, 'high': 222.56, 'low': 217.473, 'close': 217.73, 'volume': 57977094, 'datetime_epoch': 1568955600000, 'datetime': datetime.date(2019, 9, 20)}, {'id': 18717, 'symbol': 'AAPL', 'open': 218.95, 'high': 219.84, 'low': 217.65, 'close': 218.72, 'volume': 19419648, 'datetime_epoch': 1569214800000, 'datetime': datetime.date(2019, 9, 23)}, {'id': 18718, 'symbol': 'AAPL', 'open': 221.03, 'high': 222.49, 'low': 217.19, 'close': 217.68, 'volume': 31434367, 'datetime_epoch': 1569301200000, 'datetime': datetime.date(2019, 9, 24)}, {'id': 18719, 'symbol': 'AAPL', 'open': 218.55, 'high': 221.5, 'low': 217.1402, 'close': 221.03, 'volume': 22481006, 'datetime_epoch': 1569387600000, 'datetime': datetime.date(2019, 9, 25)}, {'id': 18720, 'symbol': 'AAPL', 'open': 220.0, 'high': 220.94, 'low': 218.83, 'close': 219.89, 'volume': 19088312, 'datetime_epoch': 1569474000000, 'datetime': datetime.date(2019, 9, 26)}, {'id': 18721, 'symbol': 'AAPL', 'open': 220.54, 'high': 220.96, 'low': 217.2814, 'close': 218.82, 'volume': 25361285, 'datetime_epoch': 1569560400000, 'datetime': datetime.date(2019, 9, 27)}, {'id': 18722, 'symbol': 'AAPL', 'open': 220.9, 'high': 224.58, 'low': 220.79, 'close': 223.97, 'volume': 26318583, 'datetime_epoch': 1569819600000, 'datetime': datetime.date(2019, 9, 30)}, {'id': 18723, 'symbol': 'AAPL', 'open': 225.07, 'high': 228.22, 'low': 224.2, 'close': 224.59, 'volume': 36187163, 'datetime_epoch': 1569906000000, 'datetime': datetime.date(2019, 10, 1)}, {'id': 18724, 'symbol': 'AAPL', 'open': 223.06, 'high': 223.58, 'low': 217.93, 'close': 218.96, 'volume': 35767257, 'datetime_epoch': 1569992400000, 'datetime': datetime.date(2019, 10, 2)}, {'id': 18725, 'symbol': 'AAPL', 'open': 218.43, 'high': 220.96, 'low': 215.132, 'close': 220.82, 'volume': 30352686, 'datetime_epoch': 1570078800000, 'datetime': datetime.date(2019, 10, 3)}, {'id': 18726, 'symbol': 'AAPL', 'open': 225.64, 'high': 227.49, 'low': 223.89, 'close': 227.01, 'volume': 34755553, 'datetime_epoch': 1570165200000, 'datetime': datetime.date(2019, 10, 4)}, {'id': 18727, 'symbol': 'AAPL', 'open': 226.27, 'high': 229.93, 'low': 225.84, 'close': 227.06, 'volume': 30889269, 'datetime_epoch': 1570424400000, 'datetime': datetime.date(2019, 10, 7)}, {'id': 18728, 'symbol': 'AAPL', 'open': 225.82, 'high': 228.06, 'low': 224.33, 'close': 224.4, 'volume': 29282700, 'datetime_epoch': 1570510800000, 'datetime': datetime.date(2019, 10, 8)}, {'id': 18729, 'symbol': 'AAPL', 'open': 227.03, 'high': 227.79, 'low': 225.64, 'close': 227.03, 'volume': 19029424, 'datetime_epoch': 1570597200000, 'datetime': datetime.date(2019, 10, 9)}, {'id': 18730, 'symbol': 'AAPL', 'open': 227.93, 'high': 230.44, 'low': 227.3, 'close': 230.09, 'volume': 28962984, 'datetime_epoch': 1570683600000, 'datetime': datetime.date(2019, 10, 10)}, {'id': 18731, 'symbol': 'AAPL', 'open': 232.95, 'high': 237.64, 'low': 232.3075, 'close': 236.21, 'volume': 41990210, 'datetime_epoch': 1570770000000, 'datetime': datetime.date(2019, 10, 11)}, {'id': 18732, 'symbol': 'AAPL', 'open': 234.9, 'high': 238.1342, 'low': 234.6701, 'close': 235.87, 'volume': 24413484, 'datetime_epoch': 1571029200000, 'datetime': datetime.date(2019, 10, 14)}, {'id': 18733, 'symbol': 'AAPL', 'open': 236.39, 'high': 237.65, 'low': 234.88, 'close': 235.32, 'volume': 23040483, 'datetime_epoch': 1571115600000, 'datetime': datetime.date(2019, 10, 15)}, {'id': 18734, 'symbol': 'AAPL', 'open': 233.37, 'high': 235.24, 'low': 233.2, 'close': 234.37, 'volume': 19286694, 'datetime_epoch': 1571202000000, 'datetime': datetime.date(2019, 10, 16)}, {'id': 18735, 'symbol': 'AAPL', 'open': 235.09, 'high': 236.15, 'low': 233.52, 'close': 235.28, 'volume': 17272897, 'datetime_epoch': 1571288400000, 'datetime': datetime.date(2019, 10, 17)}, {'id': 18736, 'symbol': 'AAPL', 'open': 234.59, 'high': 237.58, 'low': 234.29, 'close': 236.41, 'volume': 24377166, 'datetime_epoch': 1571374800000, 'datetime': datetime.date(2019, 10, 18)}, {'id': 18737, 'symbol': 'AAPL', 'open': 237.52, 'high': 240.99, 'low': 237.32, 'close': 240.51, 'volume': 22367483, 'datetime_epoch': 1571634000000, 'datetime': datetime.date(2019, 10, 21)}, {'id': 18738, 'symbol': 'AAPL', 'open': 241.16, 'high': 242.2, 'low': 239.6218, 'close': 239.96, 'volume': 22684001, 'datetime_epoch': 1571720400000, 'datetime': datetime.date(2019, 10, 22)}, {'id': 18739, 'symbol': 'AAPL', 'open': 242.1, 'high': 243.24, 'low': 241.22, 'close': 243.18, 'volume': 19932545, 'datetime_epoch': 1571806800000, 'datetime': datetime.date(2019, 10, 23)}, {'id': 18740, 'symbol': 'AAPL', 'open': 244.51, 'high': 244.8, 'low': 241.805, 'close': 243.58, 'volume': 17916255, 'datetime_epoch': 1571893200000, 'datetime': datetime.date(2019, 10, 24)}, {'id': 18741, 'symbol': 'AAPL', 'open': 243.16, 'high': 246.73, 'low': 242.88, 'close': 246.58, 'volume': 18369296, 'datetime_epoch': 1571979600000, 'datetime': datetime.date(2019, 10, 25)}, {'id': 18742, 'symbol': 'AAPL', 'open': 247.42, 'high': 249.25, 'low': 246.72, 'close': 249.05, 'volume': 24143241, 'datetime_epoch': 1572238800000, 'datetime': datetime.date(2019, 10, 28)}, {'id': 18743, 'symbol': 'AAPL', 'open': 248.97, 'high': 249.75, 'low': 242.57, 'close': 243.29, 'volume': 35709867, 'datetime_epoch': 1572325200000, 'datetime': datetime.date(2019, 10, 29)}, {'id': 18744, 'symbol': 'AAPL', 'open': 244.76, 'high': 245.3, 'low': 241.21, 'close': 243.26, 'volume': 31130522, 'datetime_epoch': 1572411600000, 'datetime': datetime.date(2019, 10, 30)}, {'id': 18745, 'symbol': 'AAPL', 'open': 247.24, 'high': 249.17, 'low': 237.26, 'close': 248.76, 'volume': 34790520, 'datetime_epoch': 1572498000000, 'datetime': datetime.date(2019, 10, 31)}, {'id': 18746, 'symbol': 'AAPL', 'open': 249.54, 'high': 255.93, 'low': 249.16, 'close': 255.82, 'volume': 37781334, 'datetime_epoch': 1572584400000, 'datetime': datetime.date(2019, 11, 1)}, {'id': 18747, 'symbol': 'AAPL', 'open': 257.33, 'high': 257.845, 'low': 255.38, 'close': 257.5, 'volume': 25817952, 'datetime_epoch': 1572847200000, 'datetime': datetime.date(2019, 11, 4)}, {'id': 18748, 'symbol': 'AAPL', 'open': 257.05, 'high': 258.19, 'low': 256.32, 'close': 257.13, 'volume': 19974427, 'datetime_epoch': 1572933600000, 'datetime': datetime.date(2019, 11, 5)}, {'id': 18749, 'symbol': 'AAPL', 'open': 256.77, 'high': 257.49, 'low': 255.365, 'close': 257.24, 'volume': 18966124, 'datetime_epoch': 1573020000000, 'datetime': datetime.date(2019, 11, 6)}, {'id': 18750, 'symbol': 'AAPL', 'open': 258.74, 'high': 260.35, 'low': 258.11, 'close': 259.43, 'volume': 23735083, 'datetime_epoch': 1573106400000, 'datetime': datetime.date(2019, 11, 7)}, {'id': 18751, 'symbol': 'AAPL', 'open': 258.69, 'high': 260.44, 'low': 256.85, 'close': 260.14, 'volume': 17520495, 'datetime_epoch': 1573192800000, 'datetime': datetime.date(2019, 11, 8)}, {'id': 18752, 'symbol': 'AAPL', 'open': 258.3, 'high': 262.47, 'low': 258.28, 'close': 262.2, 'volume': 20507459, 'datetime_epoch': 1573452000000, 'datetime': datetime.date(2019, 11, 11)}, {'id': 18753, 'symbol': 'AAPL', 'open': 261.55, 'high': 262.79, 'low': 260.92, 'close': 261.96, 'volume': 21847226, 'datetime_epoch': 1573538400000, 'datetime': datetime.date(2019, 11, 12)}, {'id': 18754, 'symbol': 'AAPL', 'open': 261.13, 'high': 264.78, 'low': 261.07, 'close': 264.47, 'volume': 25817593, 'datetime_epoch': 1573624800000, 'datetime': datetime.date(2019, 11, 13)}, {'id': 18755, 'symbol': 'AAPL', 'open': 263.75, 'high': 264.88, 'low': 262.1, 'close': 262.64, 'volume': 22395556, 'datetime_epoch': 1573711200000, 'datetime': datetime.date(2019, 11, 14)}, {'id': 18756, 'symbol': 'AAPL', 'open': 263.68, 'high': 265.78, 'low': 263.01, 'close': 265.76, 'volume': 25093666, 'datetime_epoch': 1573797600000, 'datetime': datetime.date(2019, 11, 15)}, {'id': 18757, 'symbol': 'AAPL', 'open': 265.8, 'high': 267.43, 'low': 264.23, 'close': 267.1, 'volume': 21700897, 'datetime_epoch': 1574056800000, 'datetime': datetime.date(2019, 11, 18)}, {'id': 18758, 'symbol': 'AAPL', 'open': 267.9, 'high': 268.0, 'low': 265.3926, 'close': 266.29, 'volume': 19069597, 'datetime_epoch': 1574143200000, 'datetime': datetime.date(2019, 11, 19)}, {'id': 18759, 'symbol': 'AAPL', 'open': 265.54, 'high': 266.083, 'low': 260.4, 'close': 263.19, 'volume': 26609919, 'datetime_epoch': 1574229600000, 'datetime': datetime.date(2019, 11, 20)}, {'id': 18760, 'symbol': 'AAPL', 'open': 263.69, 'high': 264.005, 'low': 261.18, 'close': 262.01, 'volume': 30348778, 'datetime_epoch': 1574316000000, 'datetime': datetime.date(2019, 11, 21)}, {'id': 18761, 'symbol': 'AAPL', 'open': 262.59, 'high': 263.18, 'low': 260.84, 'close': 261.78, 'volume': 16331263, 'datetime_epoch': 1574402400000, 'datetime': datetime.date(2019, 11, 22)}, {'id': 18762, 'symbol': 'AAPL', 'open': 262.71, 'high': 266.44, 'low': 262.52, 'close': 266.37, 'volume': 21029517, 'datetime_epoch': 1574661600000, 'datetime': datetime.date(2019, 11, 25)}, {'id': 18763, 'symbol': 'AAPL', 'open': 266.94, 'high': 267.16, 'low': 262.5, 'close': 264.29, 'volume': 26334882, 'datetime_epoch': 1574748000000, 'datetime': datetime.date(2019, 11, 26)}, {'id': 18764, 'symbol': 'AAPL', 'open': 265.58, 'high': 267.98, 'low': 265.31, 'close': 267.84, 'volume': 16386122, 'datetime_epoch': 1574834400000, 'datetime': datetime.date(2019, 11, 27)}, {'id': 18765, 'symbol': 'AAPL', 'open': 266.6, 'high': 268.0, 'low': 265.9, 'close': 267.25, 'volume': 11654363, 'datetime_epoch': 1575007200000, 'datetime': datetime.date(2019, 11, 29)}, {'id': 18766, 'symbol': 'AAPL', 'open': 267.27, 'high': 268.25, 'low': 263.45, 'close': 264.16, 'volume': 23693550, 'datetime_epoch': 1575266400000, 'datetime': datetime.date(2019, 12, 2)}, {'id': 18767, 'symbol': 'AAPL', 'open': 258.31, 'high': 259.53, 'low': 256.29, 'close': 259.45, 'volume': 29377268, 'datetime_epoch': 1575352800000, 'datetime': datetime.date(2019, 12, 3)}, {'id': 18768, 'symbol': 'AAPL', 'open': 261.07, 'high': 263.31, 'low': 260.68, 'close': 261.74, 'volume': 16810388, 'datetime_epoch': 1575439200000, 'datetime': datetime.date(2019, 12, 4)}, {'id': 18769, 'symbol': 'AAPL', 'open': 263.79, 'high': 265.89, 'low': 262.73, 'close': 265.58, 'volume': 18661343, 'datetime_epoch': 1575525600000, 'datetime': datetime.date(2019, 12, 5)}, {'id': 18770, 'symbol': 'AAPL', 'open': 267.48, 'high': 271.0, 'low': 267.3, 'close': 270.71, 'volume': 26547493, 'datetime_epoch': 1575612000000, 'datetime': datetime.date(2019, 12, 6)}, {'id': 18771, 'symbol': 'AAPL', 'open': 270.0, 'high': 270.8, 'low': 264.91, 'close': 266.92, 'volume': 32182645, 'datetime_epoch': 1575871200000, 'datetime': datetime.date(2019, 12, 9)}, {'id': 18772, 'symbol': 'AAPL', 'open': 268.6, 'high': 270.07, 'low': 265.86, 'close': 268.48, 'volume': 22632383, 'datetime_epoch': 1575957600000, 'datetime': datetime.date(2019, 12, 10)}, {'id': 18773, 'symbol': 'AAPL', 'open': 268.81, 'high': 271.1, 'low': 268.5, 'close': 270.77, 'volume': 19723391, 'datetime_epoch': 1576044000000, 'datetime': datetime.date(2019, 12, 11)}, {'id': 18774, 'symbol': 'AAPL', 'open': 267.78, 'high': 272.5599, 'low': 267.321, 'close': 271.46, 'volume': 34437042, 'datetime_epoch': 1576130400000, 'datetime': datetime.date(2019, 12, 12)}, {'id': 18775, 'symbol': 'AAPL', 'open': 271.46, 'high': 275.3, 'low': 270.93, 'close': 275.15, 'volume': 33432806, 'datetime_epoch': 1576216800000, 'datetime': datetime.date(2019, 12, 13)}, {'id': 18776, 'symbol': 'AAPL', 'open': 277.0, 'high': 280.79, 'low': 276.98, 'close': 279.86, 'volume': 32081105, 'datetime_epoch': 1576476000000, 'datetime': datetime.date(2019, 12, 16)}, {'id': 18777, 'symbol': 'AAPL', 'open': 279.57, 'high': 281.77, 'low': 278.8, 'close': 280.41, 'volume': 28575798, 'datetime_epoch': 1576562400000, 'datetime': datetime.date(2019, 12, 17)}, {'id': 18778, 'symbol': 'AAPL', 'open': 279.8, 'high': 281.9, 'low': 279.12, 'close': 279.74, 'volume': 29024687, 'datetime_epoch': 1576648800000, 'datetime': datetime.date(2019, 12, 18)}, {'id': 18779, 'symbol': 'AAPL', 'open': 279.5, 'high': 281.18, 'low': 278.95, 'close': 280.02, 'volume': 24626947, 'datetime_epoch': 1576735200000, 'datetime': datetime.date(2019, 12, 19)}, {'id': 18780, 'symbol': 'AAPL', 'open': 282.23, 'high': 282.65, 'low': 278.56, 'close': 279.44, 'volume': 69032743, 'datetime_epoch': 1576821600000, 'datetime': datetime.date(2019, 12, 20)}, {'id': 18781, 'symbol': 'AAPL', 'open': 280.53, 'high': 284.25, 'low': 280.3735, 'close': 284.0, 'volume': 24677883, 'datetime_epoch': 1577080800000, 'datetime': datetime.date(2019, 12, 23)}, {'id': 18782, 'symbol': 'AAPL', 'open': 284.69, 'high': 284.89, 'low': 282.9197, 'close': 284.27, 'volume': 12119714, 'datetime_epoch': 1577167200000, 'datetime': datetime.date(2019, 12, 24)}, {'id': 18783, 'symbol': 'AAPL', 'open': 284.82, 'high': 289.98, 'low': 284.7, 'close': 289.91, 'volume': 23334004, 'datetime_epoch': 1577340000000, 'datetime': datetime.date(2019, 12, 26)}, {'id': 18784, 'symbol': 'AAPL', 'open': 291.12, 'high': 293.97, 'low': 288.12, 'close': 289.8, 'volume': 36592936, 'datetime_epoch': 1577426400000, 'datetime': datetime.date(2019, 12, 27)}, {'id': 18785, 'symbol': 'AAPL', 'open': 289.46, 'high': 292.69, 'low': 285.22, 'close': 291.52, 'volume': 36059614, 'datetime_epoch': 1577685600000, 'datetime': datetime.date(2019, 12, 30)}, {'id': 18786, 'symbol': 'AAPL', 'open': 289.93, 'high': 293.68, 'low': 289.52, 'close': 293.65, 'volume': 25247625, 'datetime_epoch': 1577772000000, 'datetime': datetime.date(2019, 12, 31)}, {'id': 18787, 'symbol': 'AAPL', 'open': 296.24, 'high': 300.6, 'low': 295.19, 'close': 300.35, 'volume': 33911864, 'datetime_epoch': 1577944800000, 'datetime': datetime.date(2020, 1, 2)}, {'id': 18788, 'symbol': 'AAPL', 'open': 297.15, 'high': 300.58, 'low': 296.5, 'close': 297.43, 'volume': 36633878, 'datetime_epoch': 1578031200000, 'datetime': datetime.date(2020, 1, 3)}, {'id': 18789, 'symbol': 'AAPL', 'open': 293.79, 'high': 299.96, 'low': 292.75, 'close': 299.8, 'volume': 29644644, 'datetime_epoch': 1578290400000, 'datetime': datetime.date(2020, 1, 6)}, {'id': 18790, 'symbol': 'AAPL', 'open': 299.84, 'high': 300.9, 'low': 297.48, 'close': 298.39, 'volume': 27877655, 'datetime_epoch': 1578376800000, 'datetime': datetime.date(2020, 1, 7)}, {'id': 18791, 'symbol': 'AAPL', 'open': 297.16, 'high': 304.4399, 'low': 297.156, 'close': 303.19, 'volume': 33090946, 'datetime_epoch': 1578463200000, 'datetime': datetime.date(2020, 1, 8)}, {'id': 18792, 'symbol': 'AAPL', 'open': 307.235, 'high': 310.43, 'low': 306.2, 'close': 309.63, 'volume': 42621542, 'datetime_epoch': 1578549600000, 'datetime': datetime.date(2020, 1, 9)}, {'id': 18793, 'symbol': 'AAPL', 'open': 310.6, 'high': 312.67, 'low': 308.25, 'close': 310.33, 'volume': 35217272, 'datetime_epoch': 1578636000000, 'datetime': datetime.date(2020, 1, 10)}, {'id': 18794, 'symbol': 'AAPL', 'open': 311.64, 'high': 317.07, 'low': 311.15, 'close': 316.96, 'volume': 30521722, 'datetime_epoch': 1578895200000, 'datetime': datetime.date(2020, 1, 13)}, {'id': 18795, 'symbol': 'AAPL', 'open': 316.7, 'high': 317.57, 'low': 312.17, 'close': 312.68, 'volume': 40653457, 'datetime_epoch': 1578981600000, 'datetime': datetime.date(2020, 1, 14)}, {'id': 18796, 'symbol': 'AAPL', 'open': 311.85, 'high': 315.5, 'low': 309.55, 'close': 311.34, 'volume': 30480882, 'datetime_epoch': 1579068000000, 'datetime': datetime.date(2020, 1, 15)}, {'id': 18797, 'symbol': 'AAPL', 'open': 313.59, 'high': 315.7, 'low': 312.09, 'close': 315.24, 'volume': 27207254, 'datetime_epoch': 1579154400000, 'datetime': datetime.date(2020, 1, 16)}, {'id': 18798, 'symbol': 'AAPL', 'open': 316.27, 'high': 318.74, 'low': 315.0, 'close': 318.73, 'volume': 34454117, 'datetime_epoch': 1579240800000, 'datetime': datetime.date(2020, 1, 17)}, {'id': 18799, 'symbol': 'AAPL', 'open': 317.19, 'high': 319.02, 'low': 316.0, 'close': 316.57, 'volume': 27710814, 'datetime_epoch': 1579586400000, 'datetime': datetime.date(2020, 1, 21)}, {'id': 18800, 'symbol': 'AAPL', 'open': 318.58, 'high': 319.99, 'low': 317.31, 'close': 317.7, 'volume': 25458115, 'datetime_epoch': 1579672800000, 'datetime': datetime.date(2020, 1, 22)}, {'id': 18801, 'symbol': 'AAPL', 'open': 317.92, 'high': 319.56, 'low': 315.65, 'close': 319.23, 'volume': 26117993, 'datetime_epoch': 1579759200000, 'datetime': datetime.date(2020, 1, 23)}, {'id': 18802, 'symbol': 'AAPL', 'open': 320.25, 'high': 323.33, 'low': 317.5188, 'close': 318.31, 'volume': 36634380, 'datetime_epoch': 1579845600000, 'datetime': datetime.date(2020, 1, 24)}, {'id': 18803, 'symbol': 'AAPL', 'open': 310.06, 'high': 311.77, 'low': 304.88, 'close': 308.95, 'volume': 40485005, 'datetime_epoch': 1580104800000, 'datetime': datetime.date(2020, 1, 27)}, {'id': 18804, 'symbol': 'AAPL', 'open': 312.6, 'high': 318.4, 'low': 312.19, 'close': 317.69, 'volume': 40558486, 'datetime_epoch': 1580191200000, 'datetime': datetime.date(2020, 1, 28)}, {'id': 18805, 'symbol': 'AAPL', 'open': 324.45, 'high': 327.85, 'low': 321.38, 'close': 324.34, 'volume': 54149928, 'datetime_epoch': 1580277600000, 'datetime': datetime.date(2020, 1, 29)}, {'id': 18806, 'symbol': 'AAPL', 'open': 320.5435, 'high': 324.09, 'low': 318.75, 'close': 323.87, 'volume': 31685808, 'datetime_epoch': 1580364000000, 'datetime': datetime.date(2020, 1, 30)}, {'id': 18807, 'symbol': 'AAPL', 'open': 320.93, 'high': 322.68, 'low': 308.29, 'close': 309.51, 'volume': 49897096, 'datetime_epoch': 1580450400000, 'datetime': datetime.date(2020, 1, 31)}, {'id': 18808, 'symbol': 'AAPL', 'open': 304.3, 'high': 313.49, 'low': 302.22, 'close': 308.66, 'volume': 43496401, 'datetime_epoch': 1580709600000, 'datetime': datetime.date(2020, 2, 3)}, {'id': 18809, 'symbol': 'AAPL', 'open': 315.31, 'high': 319.64, 'low': 313.6345, 'close': 318.85, 'volume': 34154134, 'datetime_epoch': 1580796000000, 'datetime': datetime.date(2020, 2, 4)}, {'id': 18810, 'symbol': 'AAPL', 'open': 323.52, 'high': 324.76, 'low': 318.95, 'close': 321.45, 'volume': 29706718, 'datetime_epoch': 1580882400000, 'datetime': datetime.date(2020, 2, 5)}, {'id': 18811, 'symbol': 'AAPL', 'open': 322.57, 'high': 325.22, 'low': 320.2648, 'close': 325.21, 'volume': 26356385, 'datetime_epoch': 1580968800000, 'datetime': datetime.date(2020, 2, 6)}, {'id': 18812, 'symbol': 'AAPL', 'open': 322.37, 'high': 323.4, 'low': 318.0, 'close': 320.03, 'volume': 29421012, 'datetime_epoch': 1581055200000, 'datetime': datetime.date(2020, 2, 7)}, {'id': 18813, 'symbol': 'AAPL', 'open': 314.18, 'high': 321.55, 'low': 313.85, 'close': 321.55, 'volume': 27337215, 'datetime_epoch': 1581314400000, 'datetime': datetime.date(2020, 2, 10)}, {'id': 18814, 'symbol': 'AAPL', 'open': 323.6, 'high': 323.9, 'low': 318.71, 'close': 319.61, 'volume': 23580780, 'datetime_epoch': 1581400800000, 'datetime': datetime.date(2020, 2, 11)}, {'id': 18815, 'symbol': 'AAPL', 'open': 321.47, 'high': 327.22, 'low': 321.47, 'close': 327.2, 'volume': 28432573, 'datetime_epoch': 1581487200000, 'datetime': datetime.date(2020, 2, 12)}, {'id': 18816, 'symbol': 'AAPL', 'open': 324.19, 'high': 326.22, 'low': 323.35, 'close': 324.87, 'volume': 23686892, 'datetime_epoch': 1581573600000, 'datetime': datetime.date(2020, 2, 13)}, {'id': 18817, 'symbol': 'AAPL', 'open': 324.74, 'high': 325.98, 'low': 322.85, 'close': 324.95, 'volume': 20028447, 'datetime_epoch': 1581660000000, 'datetime': datetime.date(2020, 2, 14)}, {'id': 18818, 'symbol': 'AAPL', 'open': 315.36, 'high': 319.75, 'low': 314.61, 'close': 319.0, 'volume': 38190545, 'datetime_epoch': 1582005600000, 'datetime': datetime.date(2020, 2, 18)}, {'id': 18819, 'symbol': 'AAPL', 'open': 320.0, 'high': 324.57, 'low': 320.0, 'close': 323.62, 'volume': 23495991, 'datetime_epoch': 1582092000000, 'datetime': datetime.date(2020, 2, 19)}, {'id': 18820, 'symbol': 'AAPL', 'open': 322.63, 'high': 324.65, 'low': 318.21, 'close': 320.3, 'volume': 25141489, 'datetime_epoch': 1582178400000, 'datetime': datetime.date(2020, 2, 20)}, {'id': 18821, 'symbol': 'AAPL', 'open': 318.62, 'high': 320.45, 'low': 310.5, 'close': 313.05, 'volume': 32426415, 'datetime_epoch': 1582264800000, 'datetime': datetime.date(2020, 2, 21)}, {'id': 18822, 'symbol': 'AAPL', 'open': 297.26, 'high': 304.18, 'low': 289.23, 'close': 298.18, 'volume': 55548828, 'datetime_epoch': 1582524000000, 'datetime': datetime.date(2020, 2, 24)}, {'id': 18823, 'symbol': 'AAPL', 'open': 300.95, 'high': 302.53, 'low': 286.13, 'close': 288.08, 'volume': 57668364, 'datetime_epoch': 1582610400000, 'datetime': datetime.date(2020, 2, 25)}, {'id': 18824, 'symbol': 'AAPL', 'open': 286.53, 'high': 297.88, 'low': 286.5, 'close': 292.65, 'volume': 49678431, 'datetime_epoch': 1582696800000, 'datetime': datetime.date(2020, 2, 26)}, {'id': 18825, 'symbol': 'AAPL', 'open': 281.1, 'high': 286.0, 'low': 272.96, 'close': 273.52, 'volume': 80151381, 'datetime_epoch': 1582783200000, 'datetime': datetime.date(2020, 2, 27)}, {'id': 18826, 'symbol': 'AAPL', 'open': 257.26, 'high': 278.41, 'low': 256.37, 'close': 273.36, 'volume': 106721230, 'datetime_epoch': 1582869600000, 'datetime': datetime.date(2020, 2, 28)}, {'id': 18827, 'symbol': 'AAPL', 'open': 282.28, 'high': 301.44, 'low': 277.72, 'close': 298.81, 'volume': 85349339, 'datetime_epoch': 1583128800000, 'datetime': datetime.date(2020, 3, 2)}, {'id': 18828, 'symbol': 'AAPL', 'open': 303.67, 'high': 304.0, 'low': 285.8, 'close': 289.32, 'volume': 79868852, 'datetime_epoch': 1583215200000, 'datetime': datetime.date(2020, 3, 3)}, {'id': 18829, 'symbol': 'AAPL', 'open': 296.44, 'high': 303.4, 'low': 293.13, 'close': 302.74, 'volume': 54794568, 'datetime_epoch': 1583301600000, 'datetime': datetime.date(2020, 3, 4)}, {'id': 18830, 'symbol': 'AAPL', 'open': 295.52, 'high': 299.55, 'low': 291.41, 'close': 292.92, 'volume': 46893219, 'datetime_epoch': 1583388000000, 'datetime': datetime.date(2020, 3, 5)}, {'id': 18831, 'symbol': 'AAPL', 'open': 282.0, 'high': 290.82, 'low': 281.23, 'close': 289.03, 'volume': 56544246, 'datetime_epoch': 1583474400000, 'datetime': datetime.date(2020, 3, 6)}, {'id': 18832, 'symbol': 'AAPL', 'open': 263.75, 'high': 278.09, 'low': 263.0, 'close': 266.17, 'volume': 71686208, 'datetime_epoch': 1583730000000, 'datetime': datetime.date(2020, 3, 9)}, {'id': 18833, 'symbol': 'AAPL', 'open': 277.14, 'high': 286.44, 'low': 269.37, 'close': 285.34, 'volume': 71322520, 'datetime_epoch': 1583816400000, 'datetime': datetime.date(2020, 3, 10)}, {'id': 18834, 'symbol': 'AAPL', 'open': 277.39, 'high': 281.22, 'low': 271.86, 'close': 275.43, 'volume': 64094970, 'datetime_epoch': 1583902800000, 'datetime': datetime.date(2020, 3, 11)}, {'id': 18835, 'symbol': 'AAPL', 'open': 255.94, 'high': 270.0, 'low': 248.0, 'close': 248.23, 'volume': 104618517, 'datetime_epoch': 1583989200000, 'datetime': datetime.date(2020, 3, 12)}, {'id': 18836, 'symbol': 'AAPL', 'open': 264.89, 'high': 279.92, 'low': 252.95, 'close': 277.97, 'volume': 92683032, 'datetime_epoch': 1584075600000, 'datetime': datetime.date(2020, 3, 13)}, {'id': 18837, 'symbol': 'AAPL', 'open': 241.95, 'high': 259.08, 'low': 240.0, 'close': 242.21, 'volume': 80605865, 'datetime_epoch': 1584334800000, 'datetime': datetime.date(2020, 3, 16)}, {'id': 18838, 'symbol': 'AAPL', 'open': 247.51, 'high': 257.61, 'low': 238.4, 'close': 252.86, 'volume': 81013965, 'datetime_epoch': 1584421200000, 'datetime': datetime.date(2020, 3, 17)}, {'id': 18839, 'symbol': 'AAPL', 'open': 239.77, 'high': 250.0, 'low': 237.12, 'close': 246.67, 'volume': 75058406, 'datetime_epoch': 1584507600000, 'datetime': datetime.date(2020, 3, 18)}, {'id': 18840, 'symbol': 'AAPL', 'open': 247.385, 'high': 252.84, 'low': 242.61, 'close': 244.78, 'volume': 67964255, 'datetime_epoch': 1584594000000, 'datetime': datetime.date(2020, 3, 19)}, {'id': 18841, 'symbol': 'AAPL', 'open': 247.18, 'high': 251.83, 'low': 228.0, 'close': 229.24, 'volume': 100423346, 'datetime_epoch': 1584680400000, 'datetime': datetime.date(2020, 3, 20)}, {'id': 18842, 'symbol': 'AAPL', 'open': 228.08, 'high': 228.4997, 'low': 212.61, 'close': 224.37, 'volume': 84188208, 'datetime_epoch': 1584939600000, 'datetime': datetime.date(2020, 3, 23)}, {'id': 18843, 'symbol': 'AAPL', 'open': 236.36, 'high': 247.69, 'low': 234.3, 'close': 246.88, 'volume': 71882773, 'datetime_epoch': 1585026000000, 'datetime': datetime.date(2020, 3, 24)}, {'id': 18844, 'symbol': 'AAPL', 'open': 250.75, 'high': 258.25, 'low': 244.3, 'close': 245.52, 'volume': 75900510, 'datetime_epoch': 1585112400000, 'datetime': datetime.date(2020, 3, 25)}, {'id': 18845, 'symbol': 'AAPL', 'open': 246.52, 'high': 258.68, 'low': 246.36, 'close': 258.44, 'volume': 63140169, 'datetime_epoch': 1585198800000, 'datetime': datetime.date(2020, 3, 26)}, {'id': 18846, 'symbol': 'AAPL', 'open': 252.75, 'high': 255.87, 'low': 247.05, 'close': 247.74, 'volume': 51054153, 'datetime_epoch': 1585285200000, 'datetime': datetime.date(2020, 3, 27)}, {'id': 18847, 'symbol': 'AAPL', 'open': 250.74, 'high': 255.52, 'low': 249.4, 'close': 254.81, 'volume': 41994110, 'datetime_epoch': 1585544400000, 'datetime': datetime.date(2020, 3, 30)}, {'id': 18848, 'symbol': 'AAPL', 'open': 255.6, 'high': 262.49, 'low': 252.0, 'close': 254.29, 'volume': 49250501, 'datetime_epoch': 1585630800000, 'datetime': datetime.date(2020, 3, 31)}, {'id': 18849, 'symbol': 'AAPL', 'open': 246.5, 'high': 248.72, 'low': 239.13, 'close': 240.91, 'volume': 44054638, 'datetime_epoch': 1585717200000, 'datetime': datetime.date(2020, 4, 1)}, {'id': 18850, 'symbol': 'AAPL', 'open': 240.34, 'high': 245.15, 'low': 236.9, 'close': 244.93, 'volume': 41483493, 'datetime_epoch': 1585803600000, 'datetime': datetime.date(2020, 4, 2)}, {'id': 5728234, 'symbol': 'AAPL', 'open': 242.8, 'high': 245.7, 'low': 238.9741, 'close': 241.41, 'volume': 32470017, 'datetime_epoch': 1585890000000, 'datetime': datetime.date(2020, 4, 3)}, {'id': 5728235, 'symbol': 'AAPL', 'open': 250.9, 'high': 263.11, 'low': 249.38, 'close': 262.47, 'volume': 50455071, 'datetime_epoch': 1586149200000, 'datetime': datetime.date(2020, 4, 6)}, {'id': 5728236, 'symbol': 'AAPL', 'open': 270.8, 'high': 271.7, 'low': 259.0, 'close': 259.43, 'volume': 50721831, 'datetime_epoch': 1586235600000, 'datetime': datetime.date(2020, 4, 7)}, {'id': 5728237, 'symbol': 'AAPL', 'open': 262.74, 'high': 267.37, 'low': 261.23, 'close': 266.07, 'volume': 42223821, 'datetime_epoch': 1586322000000, 'datetime': datetime.date(2020, 4, 8)}, {'id': 5736392, 'symbol': 'AAPL', 'open': 268.7, 'high': 270.07, 'low': 264.7, 'close': 267.99, 'volume': 40529123, 'datetime_epoch': 1586408400000, 'datetime': datetime.date(2020, 4, 9)}, {'id': 5736399, 'symbol': 'AAPL', 'open': 268.31, 'high': 273.7, 'low': 265.83, 'close': 273.25, 'volume': 32755731, 'datetime_epoch': 1586754000000, 'datetime': datetime.date(2020, 4, 13)}, {'id': 5736394, 'symbol': 'AAPL', 'open': 280.0, 'high': 288.25, 'low': 278.05, 'close': 287.05, 'volume': 48748672, 'datetime_epoch': 1586840400000, 'datetime': datetime.date(2020, 4, 14)}]

pa=price_analysis(
    data_file= _list,
    start_date_str= "2020-01-16", # first date in _list
    end_date_str= "2020-05-30",   # last date in _list
    output_json_name='joe_test_file.json',
    verbose=False)
pa.add_indicators() #

#Strategy comparison"
pa.add_strategy()
pa.strategy_returns()
pa.write_results_json()