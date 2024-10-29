import pandas as pd
import stockstats
import numpy as np
from truedata_ws.websocket.TD import TD
from datetime import date,datetime,time,timedelta
from dateutil.relativedelta import relativedelta,TH,FR,WE
import time
import psycopg2
from psycopg2 import Error
import statistics as stats
from configparser import *
import mysql.connector
import requests
from sqlalchemy import create_engine
from copy import deepcopy
import os

td_obj = TD('tdws119', 'mridul@119',live_port=None)


config = ConfigParser()
config.read('config.ini')

cred = {'host':config.get('db','host'),'port':config.get('db','port'),'user':config.get('db','user'),'password':config.get('db','password'),'database':config.get('db','database')}

def fetch_data_from_tru_data(symbol,time='5 Y'):
    ''' Fetching stock data from true data and return a Dataframe'''

    # td_obj = TD('tdws119', 'mridul@119',live_port=8082)
    pyr = td_obj.get_historic_data(symbol, duration=time, bar_size='EOD')
    df = pd.DataFrame.from_dict(pyr)
    df = df.rename(columns={"time":"date","c":"close","o":"open","l":"low","h":"high"})
    df['date'] = pd.to_datetime(df['date'])
    # td_obj.disconnect()

    return df


def fetch_data_from_tru_data_nandan(symbol,date1,day,bar_size):
    ''' Fetching stock data from true data and return a Dataframe'''

    pyr = td_obj.get_historic_data(symbol,start_time=date1-relativedelta(days=day),end_time=date1,bar_size=bar_size)
    df = pd.DataFrame(pyr)
    df = df.rename(columns={"time":"date","c":"close","o":"open","l":"low","h":"high"})
    df['date'] = pd.to_datetime(df['date'])

    return df


def calculate_stock_indicators(stockprices,type,columnName):
    ''' Stock Indicators '''

    stock = stockstats.StockDataFrame.retype(stockprices)
    stock = stock[type]
    stock = stock.reset_index()
    stock =stock.rename(columns={type:columnName})
    new1 = pd.merge(stockprices, stock, left_on='date',right_on='date')

    return new1

def isSupport(df,i):
  support = df['low'][i] < df['low'][i-1]  and df['low'][i] < df['low'][i+1] and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]
  return support

def isResistance(df,i):
  resistance = df['high'][i] > df['high'][i-1]  and df['high'][i] > df['high'][i+1] and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2]
  return resistance

def isFarFromLevel(l,levels,s):
   return np.sum([abs(l-x) < s  for x in levels]) == 0

def s_and_r(df):
    s =  np.mean(df['high'] - df['low'])
    support = []
    resistance = []
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['low'][i]
            if isFarFromLevel(l,levels,s):
                levels.append(l)
                support.append(round(l,2))
        elif isResistance(df,i):
            l = df['high'][i]
            if isFarFromLevel(l,levels,s):
                levels.append(l)
                resistance.append(round(l,2))

    return support,resistance


def fetch_and_rename(query):

    cnx = mysql.connector.connect(**cred)
    if(cnx):
        df = pd.read_sql(query,con=cnx)
        cnx.close()

    return df


def insert_dataframe_to_db(dataframe,table_name,exists='append'):
    ''' Insert DataFrame to DB'''
    engine = create_engine("mysql+mysqlconnector://" + config.get('db','user') + ":" + config.get('db','password') + "@" + config.get('db','host') + "/" + config.get('db','database'))
    conn = engine.connect()
    try:
        dataframe.to_sql(table_name,engine,if_exists=exists,index=False)
        error = True
    except Exception as e:
        error = False
        print(e)

    return error