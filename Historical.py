#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 17:59:42 2020

@author: davidcarrera
"""

import datetime
from datetime import date
from Multivariate1 import multivariate1
import sklearn
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression


def calculateReturns(search_terms, stock_name, t): # t = desired "present week"
    strategy = multivariate1(search_terms, stock_name, t)
    
    # BackElim now takes care of predictitons
    pred = strategy.backwardsElimination(); # np array with two entries
    
    # Getting actual stock data at t+1 and t+2 based on t-1 and t of search data
    tplustwo = strategy.tplustwo
    tplusone = tplustwo + datetime.timedelta(weeks=-1)
    
    # Pulling stock data for those dates
    stock_check = yf.download(stock_name, tplusone, tplustwo + datetime.timedelta(days=1), interval="1d")
    
    stock_check_dates = stock_check.index
    stock_check_close = stock_check["Close"]
    close1 = 0
    close2 = 0
    if(stock_check_dates[0] == tplusone and stock_check_dates[-1] == tplustwo):
        close1 = stock_check_close[0]
        close2 = stock_check_close[-1]
    
    # Compare predicted close at t+1 to predicted close at t+2. Calculate return
    week_return = 0
    if(pred[1] > pred[0]):
        week_return = close2 - close1 # hold long from t + 1 to t + 2
    elif(pred[1] < pred[0]):
        week_return = close1 - close2 # hold short from t + 1 to t + 2
    else:
        week_return = 0 # in the event the two search volumes are the same.
    
    return week_return

related_terms = ["DJIA", "economy", "outlook", "business", "recession", "boom", "market", "stocks", "bear", "bull", "bank", "fed", "policy", "government", "tariffs", "protectionism", "trade", "exchange", "china", "united states", "fear", "confidence", "consumer", "company", "corporation", "tax", "direction", "concern", "equity", "debt", "fixed income"]

returns = 0

start_date = datetime.datetime(2014, 5, 16)
returns = calculateReturns(related_terms, "DJIA", start_date)






