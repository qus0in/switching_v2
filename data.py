import requests
import pandas as pd
from ast import literal_eval
import yfinance as yf
import streamlit as st

isa_universe = [
    '069500', '360750', '381180',
    '329750', '453870', '241180',
    '132030', '304660', '357870',
]

@st.cache_data(ttl='1h')
def get_etfs():
    URL = 'https://finance.naver.com/api/sise/etfItemList.nhn?etfType=0'
    response = requests.get(URL)
    response.raise_for_status()
    etfs = response.json()['result']['etfItemList']
    etfs = pd.DataFrame(etfs).loc[:, ['itemcode', 'itemname']]
    etfs.set_index('itemcode', inplace=True)
    return etfs

def get_etf_name(etf_code):
    etfs = get_etfs()
    return etfs.loc[etf_code, 'itemname']

@st.cache_data(ttl='1m')
def get_prices(symbol, count):
    URL = 'https://api.finance.naver.com/siseJson.naver'
    params = {
        'symbol': symbol,
        'timeframe': 'day',
        'requestType': 0,
        'count': count
    }
    res = requests.get(URL, params)
    res.raise_for_status()
    data = literal_eval(res.text.replace('\n', ''))
    return pd.DataFrame(data[1:], columns=data[0])

periods = [20, 50, 100, 200]

def get_score(symbol):
    prices = get_prices(symbol, 200).loc[:, '종가']
    score = 0
    for period in periods:
        p = prices.tail(period)
        score += (p.iloc[-1] / p.iloc[0] - 1) / period * 252 * 100
    return score / len(periods)

bond_universe = [
    'BIL', 'EMB', 'HYG',
    'IEF', 'LQD', 'TIP',
    'SHY', 'TLT', 'BWX',
]

@st.cache_data(ttl='1h')
def get_yf_etf_name(symbol):
    etf = yf.Ticker(symbol)
    return etf.info['shortName']

@st.cache_data(ttl='1m')
def get_yf_score(symbol):
    etf = yf.Ticker(symbol)
    hist = etf.history(period='1y')
    score = 0
    for period in periods:
        p = hist['Close'].tail(period)
        score += (p.iloc[-1] / p.iloc[0] - 1) / period * 252 * 100
    return score / len(periods)