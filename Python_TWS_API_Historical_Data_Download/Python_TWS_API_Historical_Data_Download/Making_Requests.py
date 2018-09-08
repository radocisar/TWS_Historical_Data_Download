import datetime as dt
from ibapi.contract import *
import US_Stock_Tickers
import FX_Tickers
import datetime as dt
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import Calendar_Class
import time

### Tickers
US_Stocks_Ticker_Dict = US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict
FX_Ticker_Dict = FX_Tickers.FX_Tickers.FX_Tickers_Dict

### List of dates to download data for
start_dt="08/29/2018"
end_dt="08/31/2018"
# US_Stocks
Trading_Dates = pd.bdate_range(start_dt, end_dt, freq=Calendar_Class.US_Stocks_Trading_Cal)
Trading_Dates_Reversed = pd.DatetimeIndex(reversed(Trading_Dates))
Trading_Dates_Reversed_List = Trading_Dates_Reversed.strftime("%Y%m%d").tolist()
Trading_Date_30_minute_Intervals = [dt.time(9,59,59), dt.time(10,29,59)]#, dt.time(10,59,59), dt.time(11,29,59), dt.time(11,59,59), dt.time(12,29,59), dt.time(12,59,59), 
                                    #dt.time(13,29,59), dt.time(13,59,59), dt.time(14,29,59), dt.time(14,59,59), dt.time(15,29,59), dt.time(15,59,59)]
# FX
#Trading_Dates = pd.bdate_range(start_dt, end_dt, freq=Calendar_Class.FX_Trading_Cal)
#Trading_Dates_Reversed = Trading_Dates.strftime("%Y%m%d").tolist()
#Trading_Dates_Reversed.reverse()
#Trading_Date_30_minute_Intervals = [dt.time(0,29,59), dt.time(0,59,59), dt.time(1,29,59), dt.time(1,59,59), dt.time(2,29,59), dt.time(2,59,59), dt.time(3,29,59), 
#                                    dt.time(3,59,59), dt.time(4,29,59), dt.time(4,59,59), dt.time(5,29,59), dt.time(5,59,59), dt.time(6,29,59), dt.time(6,59,59)
#                                    , dt.time(7,29,59), dt.time(7,59,59), dt.time(8,29,59), dt.time(8,59,59), dt.time(9,29,59), dt.time(9,59,59), dt.time(10,29,59)
#                                    , dt.time(10,59,59), dt.time(11,29,59), dt.time(11,59,59), dt.time(12,29,59), dt.time(12,59,59), dt.time(13,29,59), dt.time(13,59,59)
#                                    , dt.time(14,29,59), dt.time(14,59,59), dt.time(15,29,59), dt.time(15,59,59), dt.time(16,29,59), dt.time(16,59,59), dt.time(17,29,59)
#                                    , dt.time(17,59,59), dt.time(18,29,59), dt.time(18,59,59), dt.time(19,29,59), dt.time(19,59,59), dt.time(20,29,59), dt.time(20,59,59)
#                                    , dt.time(21,29,59), dt.time(21,59,59), dt.time(22,29,59), dt.time(22,59,59), dt.time(23,29,59), dt.time(23,59,59)]

class Making_Requests:
    """description of class"""
    @staticmethod
    def Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution):
        app.reqHistoricalData(1002, contract, dt.datetime.combine(trading_date, end_trading_time).strftime("%Y%m%d %H:%M:%S"), time_duration, time_resolution, "TRADES", 1, 2, False, [])

    @staticmethod
    def Make_Ticks_Request(app, contract):
        app.reqHistoricalTicks(1003, contract,"20180829 09:30:00", "", 1000, "TRADES", 1, True, [])

def Preparing_and_iterating_requests(app, Not_first_time):
    ### Contract:
    contract = Contract()
    ### Requesting historical 1 second resolution data
    for stock in US_Stocks_Ticker_Dict.items():
        # Contract
        contract.symbol = stock[0]
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = stock[1]
        global Ticker_Symbol
        Ticker_Symbol = contract.symbol
        global Sec_Type_and_Currency
        Sec_Type_and_Currency = contract.secType + "|" + contract.currency
        # Time duration and resolution of requested seconds
        time_duration = "1800 S"
        time_resolution = "1 secs"
        for trading_date in Trading_Dates_Reversed:
            global trading_date_item
            trading_date_item = trading_date.strftime("%Y%m%d")
            app.Ticks_List.clear()
            for end_trading_time in Trading_Date_30_minute_Intervals:
                if Not_first_time == True:
                    time.sleep(30)
                    print("Slept for 50 secs")
                else:
                    time.sleep(5)
                    print("Slept for 5 secs")
                    Not_first_time = True
                #time.sleep(15)
                global count
                count = 0
                Making_Requests.Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution)
                #app.run()
                time.sleep(3)
