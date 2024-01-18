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
buy_sl = buy_price * (1-sl)# flaot. stop loss
buy_tp = buy_price * (1+tp) # float. take profit
sell_sl = sell_price * (1+sl)  # flaot. stop loss
sell_tp = sell_price * (1-tp)  # float. take profit

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

# mostly graphs to show you trends
# get number of symbols with symbols_total()
num_symbols = mt.symbols_total()
num_symbols

# get all symbols and thier specifications
symbols = mt.symbols_get()
symbols

# get symbol specifications
# change this as needed for the symbol you want to query
symbol_info = mt.symbol_info(ticker)._asdict()

# get current symbol price
symbol_price = mt.symbol_info_tick(ticker)._asdict()
symbol_price

# ohlc_data (candlestick data)
ohlc_data = pd.Dataframe(mt.copy_rates_range(ticker,
                                             mt.TIMEFRAME_D1,
                                             datetime(2023, 1, 1),
                                             datetime.now()))

fig = px.line(ohlc_data, x=ohlc_data['time'], y=ohlc_data['close'])
fig.show()

ohlc_data

# requesting tick data
tick_data = pd.DataFrame(mt.copy_ticks_range(ticker,
                                             datetime(2023, 1, 1),
                                             datetime.now(),
                                             mt.COPY_TICKS_ALL))

fig = px.line(tick_data, x=tick_data['time'],
              y=tick_data['bid'], tick_data['ask'])
fig.show()

tick_data

# get historical prices
rates = mt.copy_rates_from(ticker, mt.TIMEFRAME_D1, datetime.now(), 100)

ticker = symbol
interval = mt.TIMEFRAME_D1
from_date = datetime.now()
no_of_rows = 100

rates = mt.copy_rates_from(ticker, interval, from_date, no_of_rows)
rates

# interacting with the MT5 platform
# total number of orders
num_orders = mt.orders_total()
num_orders

# list of orders
orders = mt.orders_get()
orders

# total number of positions
num_positions = mt.positions_total()
num_positions

# list of positions
positions = mt.positions_get()
positions

# number of history orders
num_order_history = mt.history_orders_total(datetime(2023, 1, 1),
                                            datetime.now())
num_order_history

# list of history orders
order_history = mt.history_orders_get(datetime(2023, 1, 1),
                                      datetime(2024, 1, 1))
order_history

# number of history deals
num_deal_history = mt.history_deals_total(datetime(2023, 1, 1),
                                          datetime.now())
num_deal_history

# number of history deals
deal_hisotry = mt.history_deals_get(datetime(2023, 1, 1),
                                    datetime.now())
deal_hisotry

# send order to market
# documentation:
# https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py

# ensure algo trading option is enabled in MT5 to trade with python

# open order either to buy
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,  # change as needed
    "volume": qty,
    "type": mt.ORDER_TYPE_BUY,
    "price": buy_price,
    "sl": buy_sl,
    "tp": buy_tp,
    "deviation": 20,  # integer. tolerance to when you want to place the order
    "magic": 23400,  # integer. used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script open",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)

# open order to sell
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": qty,
    "type": mt.ORDER_TYPE_SELL,
    "price": sell_price,
    "sl": sell_sl,
    "tp": sell_tp,
    "deviation": 20,  # integer
    "magic": 23400,  # used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script open",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)

# ensure algo trading option is enabled in MT5 to trade with python

# close buy position
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": sell_vol,
    "type": mt.ORDER_TYPE_SELL,
    "position": 12345678,  # select the order ID you want to close.
    # needs to be automated?
    "price": buy_price,
    "magic": 23400,  # used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script close",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)

# close sell position
request = {
    "action": mt.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": sell_vol,
    "type": mt.ORDER_TYPE_BUY,
    "position": 12345678,  # select the order ID you want to close.
    # needs to be automated?
    "price": sell_price,
    "magic": 23400,  # used to identify advisor/strategies
    # and can be seen in the comments as "expert ID"
    "comment": "python script close",
    "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
    "type_filling": mt.ORDER_FILLING_IOC,
}

order = mt.order_send(request)
print(order)
