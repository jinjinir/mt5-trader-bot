# Trading bot automation
# Trading bot built on top of Python3.10
# This works only on Windows

# Documentation: https://www.mql5.com/en/docs/integration/python_metatrader5

import MetaTrader5 as mt  # use python3.10 only. `pip install MetaTrader5`
import pandas as pd  # `pip install pandas`
import plotly.express as px  # `pip install plotly`
from datetime import datetime
import time

# declare variables
ticker = "EURUSD"  # change as needed e.g BTCUSD, AUDUSD, etc
qty = 2.0  # float. lot size to buy
buy_order_type = mt.ORDER_TYPE_BUY
sell_order_type = mt.ORDER_TYPE_SELL
buy_price = mt.symbol_info_tick(ticker).ask
sell_price = mt.symbol_info_tick(ticker).bid
sl_pct = 0.05  # stop loss percent
tp_pct = 0.1  # take profit percent
buy_sl = buy_price * (1-sl_pct)  # float. stop loss
buy_tp = buy_price * (1+tp_pct)  # float. take profit
sell_sl = sell_price * (1+sl_pct)  # flaot. stop loss
sell_tp = sell_price * (1-tp_pct)  # float. take profit
interval = mt.TIMEFRAME_D1  # change timeframe
timeframe = mt.TIMEFRAME_M1  # change timeframe
date_to = datetime.now()
date_from = datetime(2023, 1, 1)
no_of_rows = 100

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
        "price": price,
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
        # select the order ID you want to close.
        "position": mt.positions_get()[0]._asdict()['ticket'],
        # needs to be automated?
        "price": price,
        "magic": 23400,  # used to identify advisor/strategies
        # and can be seen in the comments as "expert ID"
        "comment": "python script close",
        "type_time": mt.ORDER_TIME_GTC,  # order stays until manually cancelled
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order = mt.order_send(request)
    return order

# historical rates
# rates = mt.copy_rates_from(ticker,interval,date_to,no_of_rows)
# rates


# uncomment while loop and comment for loop to run script indefinitely.
# uncomment for loop and comment while loop to run script only 100 times.
while True:  # runs the script indefinitely
    # for i in range(100):
    ohlc = pd.DataFrame(mt.copy_rates_range(
        ticker, timeframe, date_from, date_to))
    ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
    ohlc

    fig = px.line(ohlc, x=ohlc['time'], y=ohlc['close'])
    fig.show

    # pine script
    # LongCondition = close > high[1]
    # ShortCondition = close < Low[1]
    # closeLongCondition = close < close[1]
    # closeShortCondition = close > close[1]

    # change trading strategy as needed.
    current_close = list(ohlc[-1:]['close'])[0]
    last_close = list(ohlc[-2:]['close'])[0]
    last_high = list(ohlc[-2:]['high'])[0]
    last_low = list(ohlc[-2:]['low'])[0]
    long_condition = current_close > last_high
    short_condition = current_close < last_low
    close_long_condition = current_close < last_close
    close_short_condition = current_close > last_close

    already_buy = False
    already_sell = False

    try:
        already_sell = mt.positions_get()[0]._asdict()['type'] == 1
        already_buy = mt.positions_get()[0]._asdict()['type'] == 0
    except:
        pass

    no_positions = len(mt.positions_get()) == 0

    if long_condition:
        if no_positions:
            create_order(ticker, qty, buy_order_type,
                         buy_price, buy_sl, buy_tp)
            print("Buy Order Placed")
        if already_sell:
            close_order(ticker, qty, buy_order_type, buy_price)
            print("Sell Position Closed")
            time.sleep(1)
            create_order(ticker, qty, buy_order_type,
                         buy_price, buy_sl, buy_tp)
            print("Buy Order Placed")

    if short_condition:
        if no_positions:
            create_order(ticker, qty, sell_order_type,
                         sell_price, sell_sl, sell_tp)
            print("Sell Order Placed")
        if already_buy:
            close_order(ticker, qty, sell_order_type, sell_price)
            print("Buy Position Closed")
            time.sleep(1)
            create_order(ticker, qty, sell_order_type,
                         sell_price, sell_sl, sell_tp)
            print("Sell Order Placed")

    try:
        already_sell = mt.positions_get()[0]._asdict()['type'] == 1
        already_buy = mt.positions_get()[0]._asdict()['type'] == 0
    except:
        pass

    if close_long_condition and already_buy:
        close_order(ticker, qty, sell_order_type, sell_price)
        print("Only Buy Position Closed")

    if close_short_condition and already_sell:
        close_order(ticker, qty, buy_order_type, buy_price)
        print("Only Sell Position Closed")

    already_buy = False
    already_sell = False

    # change this value depending on the frequency you want the loop to run
    time.sleep(60)
