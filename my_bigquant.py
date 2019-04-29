#!/usr/bin/env python

import tushare as ts
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import datetime
import calendar
import getopt, sys

# NMC_limit = 250000
# MKTCAP_limit = 1000000
# TURNOVER_limit = 25.0
# NMCMKTRATIO_limit = 0.0

def usage():
    print("python my_bigquant.py -n nmc -m mkt -t turnover -r ratio")

class Stock_fun(object):

    def __init__(self, nmc_limit, mktcap_limit, turnover_limit, nmcmktratio_limit):
        try:
            self.nmc_limit = nmc_limit
            self.mktcap_limit = mktcap_limit
            self.turnover_limit = turnover_limit
            self.nmcmktratio_limit = nmcmktratio_limit
        except Exception as e:
            print("init error" + e)
            print(usage())
        else:
            print("init successfully") 

    def stock_basic(self):
        data = ts.get_stock_basics()
        data = data[~data.name.str.contains('ST')]
        # data = data[data.columns.difference(['name', 'area', 'industry'])]
        data.to_csv('basic.csv', encoding='GBK')           

    def all_data(self):    
        result_diagram = pd.DataFrame()
        # if not os.path.exists('origin.csv') is True:
        data = ts.get_today_all()
        data = data[~data.name.str.contains('ST')] # ignore st
        data.to_csv('origin.csv', encoding='GBK') # including all 
        # get small nmc data array
        print(self.nmc_limit)
        print(self.mktcap_limit)
        print(self.turnover_limit)
        print(self.nmcmktratio_limit)

        for i in data.index:
            if data.ix[i]['nmc'] < int(self.nmc_limit) and data.ix[i]['mktcap'] < int(self.mktcap_limit) and data.ix[i]['volume'] > 0:
                if data.ix[i]['nmc'] / data.ix[i]['mktcap'] > float(self.nmcmktratio_limit) and data.ix[i]['turnoverratio'] < float(self.turnover_limit):
                        result_diagram = result_diagram.append(data.ix[i], ignore_index=True)
        result_diagram.to_csv('pickup.csv', encoding='GBK', header=True)   

    def houfuquan(self, code):
        dg = ts.get_k_data(code, autype='hfq')
        dg.to_csv(code + '.csv')
        # draw the picture
        # plt.figure(figsize=(8, 6))
        # plt.plot(dg['date'], dg['close'])
        # plt.show()       

    def sina(self, code, date):
        data = ts.get_sina_dd(code, date)
        print(data['price'])
        data.to_csv('dd.csv', encoding='GBK')

    def qianfuquan(self, code):
        df = ts.get_k_data(code, autype='qfq')
        dg.to_csv('qfq.csv')

    def parse_file(self, name):
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

    def wufuquan(self, code):
        dw = ts.get_k_data(code)
        dw.to_csv('wfq.csv')   

    def get_main(self):
        ts.get_index().to_csv('main.csv', encoding='GBK')

    def get_cap_tops(self, day):
        ts.cap_tops(days=day).to_csv('top.csv', encoding='GBK')                  

    def get_top(self, date):
        ts.top_list(date).to_csv('top.csv', encoding='GBK')

    def get_info(self, code):
        data = ts.get_notices(code)
        data.to_csv('info.csv', encoding='GBK')

# def stock_nmc():    
#     data = ts.get_today_all().iloc[:,0].tolist()
#     data_t = ts.get_terminated().iloc[:,0].tolist()
#     data_t = ts.get_terminated()
#     all_stock = data.iloc[:,0].tolist() + data_t.iloc[:,0].tolist()
#     for code in all_stock:
#         df = ts.get_hist_data(code)
#         df['ltsz'] = pd.Series.rolling(df['close'],1).sum() * pd.Series.rolling\
#             (df['volume'],1).sum() / pd.Series.rolling(df['turnover'],1).sum() / 10000
#         df.to_csv(str(code) + '.csv')

def pre_deal_fun(opts, args, arry):
    for op, value in opts:
        if op == "-n":
            arry[0] = value
        elif op == "-m":
            arry[1] = value
        elif op == "-t":
            arry[2] = value
        elif op == "-r":
            arry[3] = value
        elif op == "-h":
            usage()
            sys.exit()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "hn:m:t:r:")
    arry = [0] * 16

    if len(sys.argv) < 9:
        usage()
        sys.exit()  

    pre_deal_fun(opts, args, arry)       
    
    # print(len(sys.argv))
    stock_app = Stock_fun(arry[0], arry[1], arry[2], arry[3])
    # stock_app.stock_basic()
    stock_app.all_data()
    
    # get_main()
    # get_cap_tops(10)
    # get_top('2019-04-17')
    # get_info('300573')
    # stock_basic()
    # sina('300131', '2019-04-15')
    # all_data()
    # stock_nmc()
    # houfuquan('603136')
    # parse_file('603136.csv')
