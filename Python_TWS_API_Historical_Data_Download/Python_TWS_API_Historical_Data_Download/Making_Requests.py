import datetime as dt
from ibapi.contract import *
import US_Stock_Tickers
import FX_Tickers
import datetime as dt
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import Calendar_Class
import time
import Python_TWS_API_Historical_Data_Download
#import logging
import Logging

### Instantiate logging class
#lg = Logging.Logging()

### Tickers
US_Stocks_Ticker_Dict = US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict
FX_Ticker_Dict = FX_Tickers.FX_Tickers.FX_Tickers_Dict

### List of dates to download data for
start_dt="08/29/2018"
end_dt="08/31/2018"

#lg.logger.debug(end_dt)
# US_Stocks
Trading_Dates = pd.bdate_range(start_dt, end_dt, freq=Calendar_Class.US_Stocks_Trading_Cal)
Trading_Dates_Reversed = pd.DatetimeIndex(reversed(Trading_Dates))
Trading_Dates_Reversed_List = Trading_Dates_Reversed.strftime("%Y%m%d").tolist()
Trading_Date_30_minute_Intervals = [dt.time(10,0,0), dt.time(10,30,0)]#, dt.time(11,0,0), dt.time(11,30,0), dt.time(12,0,0), dt.time(12,30,0), dt.time(13,0,0), 
                                    #dt.time(13,30,0), dt.time(14,0,0), dt.time(14,30,0), dt.time(15,0,0), dt.time(15,30,0), dt.time(16,0,0)]
# FX
#Trading_Dates = pd.bdate_range(start_dt, end_dt, freq=Calendar_Class.FX_Trading_Cal)
#Trading_Dates_Reversed = Trading_Dates.strftime("%Y%m%d").tolist()
#Trading_Dates_Reversed.reverse()
#Trading_Date_30_minute_Intervals = [dt.time(0,30,0), dt.time(1,0,0), dt.time(1,30,0), dt.time(2,0,0), dt.time(2,30,0), dt.time(3,0,0), dt.time(3,30,0), 
#                                    dt.time(4,0,0), dt.time(4,30,0), dt.time(5,0,0), dt.time(5,30,0), dt.time(6,0,0), dt.time(6,30,0), dt.time(7,0,0)
#                                    , dt.time(7,30,0), dt.time(8,0,0), dt.time(8,30,0), dt.time(9,0,0), dt.time(9,30,0), dt.time(10,0,0), dt.time(10,30,0)
#                                    , dt.time(11,0,0), dt.time(11,30,0), dt.time(12,0,0), dt.time(12,30,0), dt.time(13,0,0), dt.time(13,30,0), dt.time(14,0,0)
#                                    , dt.time(14,30,0), dt.time(15,0,0), dt.time(15,30,0), dt.time(16,0,0), dt.time(16,30,0), dt.time(17,0,0), dt.time(17,30,0)
#                                    , dt.time(18,0,0), dt.time(18,30,0), dt.time(19,0,0), dt.time(19,30,0), dt.time(20,0,0), dt.time(20,30,0), dt.time(21,0,0)
#                                    , dt.time(21,30,0), dt.time(22,0,0), dt.time(22,30,0), dt.time(23,0,0), dt.time(23,30,0), dt.time(24,0,0)]

### Timing

class Making_Requests:
    """description of class"""
    @staticmethod
    def Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution):
        #global Pending_download
        app.reqHistoricalData(1502, contract, dt.datetime.combine(trading_date, end_trading_time).strftime("%Y%m%d %H:%M:%S"), time_duration, time_resolution, "TRADES", 1, 2, False, [])
        #Pending_download = True
        
    @staticmethod
    def Make_Ticks_Request(app, contract):
        app.reqHistoricalTicks(1003, contract,"20180829 09:30:00", "", 1000, "TRADES", 1, True, [])

Pending_download = False

def Update_Pending_download(status:bool):
    global Pending_download
    Pending_download = status

def Preparing_and_iterating_requests(app, Not_first_time):
    #global Partial_download_complete
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
        #global Ticker_Symbol
        #Ticker_Symbol = contract.symbol
        app.Update_Ticker_Symbol(contract.symbol)
        #global Sec_Type_and_Currency
        Sec_Type_and_Currency = contract.secType + "|" + contract.currency
        app.Update_Sec_Type_and_Currency(Sec_Type_and_Currency)
        # Time duration and resolution of requested seconds
        time_duration = "1800 S"
        time_resolution = "1 secs"
        for trading_date in Trading_Dates_Reversed:
            app.Update_trading_date_item(trading_date.strftime("%Y%m%d"))
            app.Ticks_List.clear()
            for end_trading_time in Trading_Date_30_minute_Intervals:
                # Sleeping to allow connection to complete
                if Not_first_time == True:    
                    #pass
                    time.sleep(20)
                    print("Slept for 2 secs")
                    Logging.lg.logger.debug("Slept for 2 secs")
                    print("Download of {} for {} trading date and {} time interval took: {}".format(stock, trading_date, end_trading_time, time.time() - start_time))
                    Logging.lg.logger.debug("Download took: {}".format(time.time() - start_time))
                else:
                    time.sleep(30)
                    #TODO Change to 15 seconds
                    print("Slept for 5 secs")
                    Logging.lg.logger.debug("Slept for 5 secs")
                    Not_first_time = True
                #time.sleep(15)
                global count
                count = 0
                #Python_TWS_API_Historical_Data_Download.Partial_download_complete.clear()
                Making_Requests.Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution)
                #app.run()
                start_time = time.time()
                #Python_TWS_API_Historical_Data_Download.Partial_download_complete.wait()
                
                Update_Pending_download(True)
                while Pending_download == True:
                        time.sleep(3)
                
                       
                #time.sleep(3)
