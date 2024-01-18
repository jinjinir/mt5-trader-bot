# Trading bot automation
# Trading bot built on top of Python3.10
# This works only on Windows

# Documentation: https://www.mql5.com/en/docs/integration/python_metatrader5

import MetaTrader5 as mt  # use python3.10 only. `pip install MetaTrader5`
import pandas as pd  # `pip install pandas`
import plotly.express as px  # `pip install plotly`

from datetime import datetime

ticker = "EURUSD"  # change as needed e.g BTCUSD, AUDUSD, etc
qty = 2.0  # float. lot size to buy
buy_order_type = mt.ORDER_TYPE_BUY
sell_order_type = mt.ORDER_TYPE_SELL
buy_price = mt.symbol_info_tick(ticker).ask
sell_price = mt.symbol_info_tick(tikcer).bid
sl_pct = 0.05  # stop loss percent
tp_pct = 0.1  # take profit percent
buy_sl = buy_price * (1-sl_pct)# flaot. stop loss
buy_tp = buy_price * (1+tp_pct) # float. take profit
sell_sl = sell_price * (1+sl_pct)  # flaot. stop loss
sell_tp = sell_price * (1-tp_pct)  # float. take profit

# start the platform with initialize()
mt.initialize()

# login to Trade Account with login()
# make sure that the trade server is enabled in MT5 client terminal

login = 51294955  # login user. change this value as needed
password = '6n38WVby'  # login password. change this value as needed
server = 'ICMarketsSC-Demo'  # login server. change this value as needed

mt.login(login, password, server)

# get account info
account_info = mt.account_info()
print(account_info)

# getting specific account data
login_number = account_info.login
balance = account_info.balance
equity = account_info.equity

print()
print('login: ', login_number)
print('balance: ', balance)
print('equity: ', equity)

def create_order(ticker, qty, order_type, price, sl, tp):
  request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": ticker,
    "volume": qty,
    "type": order_type,
    # needs to be automated?
    "price": sell_price,
    "sl": sl,
    "tp": tp,
    "magic": 23400,  # used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script open",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
  }
  order = mt.order_send(request)
  return order

def close_order(ticker, qty, order_type, price):
  request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": ticker,
    "volume": qty,
    "type": order_type,
    "position": mt.positions_get()[0]._asdict()['ticket'],  # select the order ID you want to close.
    # needs to be automated?
    "price": sell_price,
    "magic": 23400,  # used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script close",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
  }
  order = mt.order_send(request)
  return order