import pandas as pd
import argparse
import json
import ta as ta
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report


class price_analysis:

    def __init__(self, dataframe, parameters, verbose):





        self.verbose=verbose #print output or not

        split_point=int(len(dataframe.index)/2)
        self.df_norm=dataframe.iloc[:split_point,:]  #use first half of data for price and volume normalization
        self.df_data=dataframe.iloc[split_point:,:]  #use second half of data for analysis

        self.parameters=parameters          #assign parameters

        self.df_anal=pd.DataFrame(index=self.df_data.index)         #create dataframe for analysis
        self.df_anal['Date']=self.df_data['Date']

        max_vol=self.df_norm['Volume'].max()
        min_vol=self.df_norm['Volume'].min()

        max_price=self.df_norm['Adj Close'].max()
        min_price=self.df_norm['Adj Close'].min()

        self.calc_max_move()

        self.calc_daily_return(self.df_data, 'Close')

        self.df_strategy=pd.DataFrame(index=self.df_data.index)     #create dataframe for strategy results
        self.df_strategy['Issue']=1

        self.results={'dates': self.df_data['Date'].tolist() ,
                      'strategy':{},
					  'indicators':{},
                      'predict':{}}

    def strategy_returns(self):
        
        self.df_strategy_return=pd.DataFrame(index=self.df_data.index)
        for col_name in list(self.df_strategy):
            self.df_strategy_return[col_name+'_daily']=self.df_strategy[col_name]*self.df_data['Daily_return']

        self.df_strategy_return.dropna(inplace=True)
        for col_name in list(self.df_strategy):
            self.df_strategy_return[col_name]=self.df_strategy_return[col_name+'_daily'].cumsum()
            self.results['strategy'][col_name]=self.df_strategy_return[col_name].tolist()

    def calc_daily_return(self, dataframe, series):
        
        dataframe['Daily_return']=(dataframe[series]-dataframe[series].shift(1))/dataframe[series].shift(1)
        dataframe['Cum_return']=dataframe['Daily_return'].cumsum()

    #Allocates max move for prescribed term into defined bucket
    def calc_max_move(self):

        append_data=False
        
        for term in self.parameters['metric']['term']:
            term_series=pd.Series(index=self.df_data.index, dtype=float)
            term_hi_series=pd.Series(index=self.df_data.index, dtype=float)
            term_low_series=pd.Series(index=self.df_data.index, dtype=float)
            term_open_series=pd.Series(index=self.df_data.index, dtype=float)
            term_calc_max=pd.Series(index=self.df_data.index, dtype=float)
            if self.verbose: print ('term:', term)
            if self.verbose: print('start index:', self.df_data.index[0])
            if self.verbose: print('stop_index:', self.df_data.index[-1])
            if self.verbose: print('Open of row 1:', self.df_data.loc[130,'Open'])
            for i in range(self.df_data.index[0],self.df_data.index[-1]-term):
                open_val=self.df_data.loc[i,'Open']
                max_high=self.df_data.loc[i:i+term,'High'].max()
                max_low=self.df_data.loc[i:i+term,'Low'].min()
                max_up=(max_high-open_val)/open_val
                if (abs((max_low-open_val)/open_val)>max_up):
                    max_move=(max_low-open_val)/open_val
                else:
                    max_move=max_up                    
                for bucket in self.parameters['metric']['move']:
                    if max_move<bucket/100:
                        term_series[i]=int(self.parameters['metric']['move'].index(bucket))
                        break
                    else:
                        term_series[i]=len(self.parameters['metric']['move'])
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

        if self.parameters['metric']['acc_dist_index']['include']==True:
            self.indicator_list.append('acc_dist_index')
            self.df_anal['acc_dist_index']=ta.volume.acc_dist_index(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], self.df_data['Volume'])

        if self.parameters['metric']['chaikin_money_flow']['include']==True:
            self.indicator_list.append('chaikin_money_flow')
            period_cmf=self.parameters['metric']['chaikin_money_flow']['parameters']['period']
            self.df_anal['chaikin_money_flow']=ta.volume.chaikin_money_flow(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], self.df_data['Volume'], period_cmf)
            
        if self.parameters['metric']['ease_of_move']['include']==True:
            self.indicator_list.append('ease_of_move')
            period_eom=self.parameters['metric']['ease_of_move']['parameters']['period']
            self.df_anal['ease_of_move']=ta.volume.ease_of_movement(self.df_data['High'], self.df_data['Low'], self.df_data['Volume'], period_eom)

        if self.parameters['metric']['williams_r']['include']==True:
            self.indicator_list.append('williams_r')
            period_wr=self.parameters['metric']['williams_r']['parameters']['period']
            self.df_anal['williams_r']=ta.momentum.wr(self.df_data['High'], self.df_data['Low'], self.df_data['Close'], period_wr)

        if self.parameters['metric']['rel_strength']['include']==True:
            self.indicator_list.append('rel_strength')
            period_rsi=self.parameters['metric']['rel_strength']['parameters']['period']
            self.df_anal['rel_strength']=ta.momentum.rsi(self.df_data['Close'], period_rsi)

        self.results['predict']['indicator_list']=self.indicator_list
        

        self.random_forest_analysis()
        
    def add_strategy(self):
        self.strategy_list=[]

        if self.parameters['strategy']['bollinger']['include']==True:
            self.strategy_list.append('bollinger')
            self.bollinger_band()
            
        if self.parameters['strategy']['williams_r']['include']==True:
            self.strategy_list.append('williams_r')
            self.williams_r()

        self.results['strategy']['strategy_list']=self.strategy_list
    
    def random_forest_analysis(self):

        self.df_anal.dropna(inplace=True)
                
        for term in self.parameters['metric']['term']:
            x_data=self.df_anal.loc[:,self.indicator_list]
            y_data=self.df_anal.loc[:,'term_'+str(term)]

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
        for i in range(self.df_data.index[0]+period,self.df_data.index[-1]+1):
            if owned_long==0 and self.bb_df.loc[i,'Close']<self.bb_df.loc[i,'bollinger_low']:
                owned_long=1
            if owned_long==1 and self.bb_df.loc[i,'Close']>self.bb_df.loc[i,'Average']:
                owned_long=0
            if owned_short==0 and self.bb_df.loc[i,'Close']>self.bb_df.loc[i,'bollinger_hi']:
                owned_short=1
            if owned_short==1 and self.bb_df.loc[i,'Close']<self.bb_df.loc[i,'Average']:
                owned_short=0
            self.bb_df.loc[i,'BB_owned_short']=owned_short
            self.bb_df.loc[i,'BB_owned_long']=owned_long
            self.df_strategy.loc[i,'bollinger']=owned_long-owned_short


    def williams_r(self):

        period_wr=self.parameters['strategy']['williams_r']['parameters']['period']
        self.wr_df=self.df_data.copy()
        self.wr_df['williams_r']=ta.momentum.wr(self.wr_df['High'], self.wr_df['Low'], self.wr_df['Close'], period_wr)

        owned_long=0
        owned_short=0
        for i in range(self.df_data.index[0]+period_wr,self.df_data.index[-1]+1):
            if owned_long==0 and self.wr_df.loc[i,'williams_r']<-80:
                owned_long=1
            if owned_long==1 and self.wr_df.loc[i,'williams_r']>-50:
                owned_long=0
            if owned_short==0 and self.wr_df.loc[i,'williams_r']>-20:
                owned_short=1
            if owned_short==1 and self.wr_df.loc[i,'williams_r']<-50:
                owned_short=0
            self.wr_df.loc[i,'wr_owned_short']=owned_short
            self.wr_df.loc[i,'wr_owned_long']=owned_long
            self.df_strategy.loc[i,'williams_r']=owned_long-owned_short
        

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

    
    
   

##Main

if __name__ == "__main__":

    verbose=True

    parser=argparse.ArgumentParser(description='sample command python price_analysis.py <input csv data file> <input json param file> <output json file>')
    parser.add_argument("data_file", help="name of data input file")
    parser.add_argument("param_file", help="name of parameter file")
    parser.add_argument("output_file", help="name of output file")
    args=parser.parse_args()
    
    with open(args.param_file, "r") as read_file:
        parameters=json.load(read_file)


    #Price analysis
    pa=price_analysis(pd.read_csv(args.data_file), parameters, verbose)
    pa.add_indicators()

    #Strategy comparison"
    pa.add_strategy()
    pa.strategy_returns()

    with open(args.output_file, "w") as write_file:
        json.dump(pa.results, write_file)
    

    #Print values
    if verbose: print ('Input parameters:', parameters)
    if verbose: print ('Input data:\n', pd.read_csv(args.data_file))
    if verbose: print ('Analyze dataframe:\n', pa.df_anal)
    if verbose: print ('Bollinger bands dataframe:\n', pa.bb_df)
    if verbose: print ('Final data dataframe:\n', pa.df_data)
    if verbose: print ('Strategy dataframe:\n', pa.df_strategy)
    if verbose: print ('Strategy returns:\n', pa.df_strategy_return)
    if verbose: print ('Results dictionary:', pa.results)
    if verbose: pa.write_data_to_csv()
    if verbose: pa.write_analysis_to_csv()
    if verbose: pa.write_bollinger_band_to_csv()
    if verbose: pa.write_williams_r_to_csv()
    if verbose: pa.write_strategy_results()

    
    

    
