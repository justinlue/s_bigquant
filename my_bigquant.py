#!/usr/bin/env python

import tushare as ts
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import datetime
import calendar

NMC_limit = 250000
MKTCAP_limit = 1000000
TURNOVER_limit = 5.0
NMCMKTRATIO_limit = 0.6

def get_top(date):
    ts.top_list(date).to_csv('top.csv', encoding='GBK')

def get_info(code):
    data = ts.get_notices(code)
    data.to_csv('info.csv', encoding='GBK')

def stock_nmc():    
    data = ts.get_today_all().iloc[:,0].tolist()
    data_t = ts.get_terminated().iloc[:,0].tolist()
    data_t = ts.get_terminated()
    all_stock = data.iloc[:,0].tolist() + data_t.iloc[:,0].tolist()
    for code in all_stock:
        df = ts.get_hist_data(code)
        df['ltsz'] = pd.Series.rolling(df['close'],1).sum() * pd.Series.rolling\
            (df['volume'],1).sum() / pd.Series.rolling(df['turnover'],1).sum() / 10000
        df.to_csv(str(code) + '.csv')

def stock_basic():
    data = ts.get_stock_basics()
    data = data[~data.name.str.contains('ST')]
    data.to_csv('basic.csv', encoding='GBK')

def all_data():    
    result_diagram = pd.DataFrame()
    # if not os.path.exists('origin.csv') is True:
    data = ts.get_today_all()
    data = data[~data.name.str.contains('ST')] # ignore st
    data.to_csv('origin.csv', encoding='GBK') # including all 
    # get small nmc data array
    for i in data.index:
        if data.ix[i]['nmc'] < NMC_limit and data.ix[i]['mktcap'] < MKTCAP_limit and data.ix[i]['volume'] > 0:
            if data.ix[i]['nmc'] / data.ix[i]['mktcap'] > NMCMKTRATIO_limit and data.ix[i]['turnoverratio'] < TURNOVER_limit:
                    result_diagram = result_diagram.append(data.ix[i], ignore_index=True)
    result_diagram.to_csv('pickup.csv', encoding='GBK', header=True)
  
    # w_data = pd.read_csv('test.csv')
    # output = pd.DataFrame(columns=('rate','code'))
    # for i in w_data.index:
    #     dg = ts.get_k_data(str(w_data.iloc[i]['code']), autype='hfq')
    #     dg.to_csv(str(w_data.iloc[i]['code']) + '.csv')

    # r_data = pd.read_csv(str(w_data.iloc[i]['code']) + '.csv')
    # # print(str((r_data.iloc[-1]['close'] - r_data.iloc[0]['close']) / r_data.iloc[0]['close']))
    # # cal = (r_data.iloc[-1]['close'] - r_data.iloc[0]['close']) / r_data.iloc[0]['close']
    # output['code'] = [r_data.iloc[0]['code']]
    # output['rate'] = [(r_data.iloc[-1]['close'] - r_data.iloc[0]['close']) / r_data.iloc[0]['close']]
    # output = output.append(output, ignore_index=True)
    # output.to_csv('output.csv')
    # dg.to_csv(w_data.ix[-1]['code'] + '.csv')

    # with open('test.csv', 'r') as myfile:
    #     lines = csv.DictReader(myfile)
    #     for idx, line in enumerate(lines):
    #         if idx > 0:
    #             dg = ts.get_k_data(line['code'], autype='hfq')
    #             if idx == 3:    
    #                 print(int(line['close'])) 
                    # dg.to_csv(line['code'] + '.csv')
        
def houfuquan(code):
    dg = ts.get_k_data(code, autype='hfq')
    dg.to_csv(code + '.csv')
    # draw the picture
    # plt.figure(figsize=(8, 6))
    # plt.plot(dg['date'], dg['close'])
    # plt.show()    

def qianfuquan(code):
    df = ts.get_k_data(code, autype='qfq')
    dg.to_csv('qfq.csv')

def wufuquan(code):
    dw = ts.get_k_data(code)
    dw.to_csv('wfq.csv')

def sina(code, date):
    data = ts.get_sina_dd(code, date)
    print(data['price'])
    data.to_csv('dd.csv', encoding='GBK') 

def parse_file(name):
    output = pd.DataFrame(columns=('rate','code','current','before'))
    r_data = pd.read_csv(name)
    output['code'] = [r_data.iloc[0]['code']]
    output['rate'] = [(r_data.iloc[-1]['close'] - r_data.iloc[0]['close']) / r_data.iloc[0]['close']]
    output['current'] = [r_data.iloc[-1]['close']]
    output['before'] = [r_data.iloc[0]['close']]
    # output = output.append(output, ignore_index=True)
    if not os.path.exists('output.csv') is False:
        output.to_csv('output.csv', mode='a', header=False)               
    else:
        output.to_csv('output.csv', header=True)               
        pass

def get_main():
    ts.get_index().to_csv('main.csv', encoding='GBK')

def get_cap_tops(day):
    ts.cap_tops(days=day).to_csv('top.csv', encoding='GBK')

if __name__ == '__main__':
    get_main()
    # get_cap_tops(10)
    # get_top('2019-04-17')
    # get_info('300573')
    # stock_basic()
    # sina('300131', '2019-04-15')
    all_data()
    # stock_nmc()
    # houfuquan('300131')
    # parse_file('300131.csv')
