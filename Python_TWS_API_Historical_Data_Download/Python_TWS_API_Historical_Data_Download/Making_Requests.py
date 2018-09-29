import datetime as dt
from ibapi.contract import *
import US_Stock_Tickers
import FX_Tickers
import datetime as dt
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import Calendar_Class
import time
#import Python_TWS_API_Historical_Data_Download
#import logging
import Logging
import threading
import Download_Start_and_End_Dates
import Utility_Functions

### Instantiate logging class
#lg = Logging.Logging()

### Timing

#class Making_Requests:
#    """description of class"""


#Pending_download 

class Prep_and_iterating_class:

    Start_and_End_Dates = Download_Start_and_End_Dates.Download_Start_and_End_Dates()

    ### List of dates to download data for
    start_dt,end_dt = Start_and_End_Dates.populate_Start_and_End_Dates()

    if Utililty_Functions.Instrument_Type_Class.Inst_Type == "FX":
        # FX
        Trading_Dates = pd.bdate_range(start_dt, end_dt, freq="B")
        Trading_Dates_Reversed = Trading_Dates.strftime("%Y%m%d").tolist()
        Trading_Dates_Reversed.reverse()
        Trading_Date_30_minute_Intervals = [dt.time(0,30,0), dt.time(1,0,0), dt.time(1,30,0), dt.time(2,0,0), dt.time(2,30,0), dt.time(3,0,0), dt.time(3,30,0), 
                                            dt.time(4,0,0), dt.time(4,30,0), dt.time(5,0,0), dt.time(5,30,0), dt.time(6,0,0), dt.time(6,30,0), dt.time(7,0,0)
                                            , dt.time(7,30,0), dt.time(8,0,0), dt.time(8,30,0), dt.time(9,0,0), dt.time(9,30,0), dt.time(10,0,0), dt.time(10,30,0)
                                            , dt.time(11,0,0), dt.time(11,30,0), dt.time(12,0,0), dt.time(12,30,0), dt.time(13,0,0), dt.time(13,30,0), dt.time(14,0,0)
                                            , dt.time(14,30,0), dt.time(15,0,0), dt.time(15,30,0), dt.time(16,0,0), dt.time(16,30,0), dt.time(17,0,0), dt.time(17,30,0)
                                            , dt.time(18,0,0), dt.time(18,30,0), dt.time(19,0,0), dt.time(19,30,0), dt.time(20,0,0), dt.time(20,30,0), dt.time(21,0,0)
                                            , dt.time(21,30,0), dt.time(22,0,0), dt.time(22,30,0), dt.time(23,0,0), dt.time(23,30,0), dt.time(24,0,0)]

    else: # Utililty_Functions.Instrument_Type_Class.Inst_Type == "STK"
        # US_Stocks
        Trading_Dates = pd.bdate_range(start_dt, end_dt, freq=Calendar_Class.US_Stocks_Trading_Cal)
        Trading_Dates_Reversed = pd.DatetimeIndex(reversed(Trading_Dates))
        Trading_Dates_Reversed_List = Trading_Dates_Reversed.strftime("%Y%m%d").tolist()
        Trading_Date_30_minute_Intervals = [dt.time(10,0,0), dt.time(10,30,0), dt.time(11,0,0), dt.time(11,30,0), dt.time(12,0,0), dt.time(12,30,0), dt.time(13,0,0), 
                                    dt.time(13,30,0), dt.time(14,0,0), dt.time(14,30,0), dt.time(15,0,0), dt.time(15,30,0), dt.time(16,0,0)]

    while_loop_counter = 0

    def __init__(self):
        self.contract = Contract()
        ### Tickers
        #self.Ticker_Dict = Ticker_Dict
        self.Pending_download:bool = None
        self.Connection_OK:bool = True

    @staticmethod
    def Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution):
        
        if Utililty_Functions.Instrument_Type_Class.Inst_Type == "FX":
            # FX
            app.reqHistoricalData(app.RequestId, contract, dt.datetime.combine(trading_date, end_trading_time).strftime("%Y%m%d %H:%M:%S"), time_duration, time_resolution, "MIDPOINT", 1, 2, False, [])
        else: # Utililty_Functions.Instrument_Type_Class.Inst_Type == "STK"
            # Stocks
            app.reqHistoricalData(app.RequestId, contract, dt.datetime.combine(trading_date, end_trading_time).strftime("%Y%m%d %H:%M:%S"), time_duration, time_resolution, "TRADES", 1, 2, False, [])            

    @staticmethod
    def Make_Ticks_Request(app, contract):
        app.reqHistoricalTicks(app.RequestId, contract,"20180829 09:30:00", "", 1000, "TRADES", 1, True, [])

    def Update_Pending_download(self, status:bool):
        self.Pending_download = status

    def Update_Connection_OK(self, conn_status:bool):
        self.Connection_OK = conn_status

    def Preparing_and_iterating_requests(self, app, Not_first_time, Ticker_Dict):
        #global Partial_download_complete
        ### Contract:
        ### Requesting historical 1 second resolution data
        print(Ticker_Dict.items())
        print(threading.current_thread().name)
        Logging.lg.logger.debug(Ticker_Dict.items())
        for stock in Ticker_Dict.items():
            if Utililty_Functions.Instrument_Type_Class.Inst_Type == "FX":
                # Contract
                self.contract.symbol = stock[0] #REF currency
                self.contract.secType = "CASH"
                self.contract.exchange = "IDEALPRO"
                self.contract.currency = stock[1] #BASE currency
                app.Update_Ticker_Symbol("{}|{}".format(self.contract.symbol, self.contract.currency))
                #self.contract.primaryExchange = stock[1]
            else: # Utililty_Functions.Instrument_Type_Class.Inst_Type == "STK"
                # Contract
                self.contract.symbol = stock[0]
                self.contract.secType = "STK"
                self.contract.exchange = "SMART"
                self.contract.currency = "USD"
                self.contract.primaryExchange = stock[1]
                app.Update_Ticker_Symbol(self.contract.symbol)
            #global Ticker_Symbol
            #Ticker_Symbol = contract.symbol
            
            #global Sec_Type_and_Currency
            Sec_Type_and_Currency = self.contract.secType + "|" + self.contract.currency
            app.Update_Sec_Type_and_Currency(Sec_Type_and_Currency)
            # Time duration and resolution of requested seconds
            time_duration = "1800 S"
            time_resolution = "1 secs"
            for trading_date in self.Trading_Dates_Reversed:
                app.Update_trading_date_item(trading_date.strftime("%Y%m%d"))
                app.Ticks_List.clear()
                for end_trading_time in self.Trading_Date_30_minute_Intervals:
                    # Convert end_trading_time to show start of the 30 minute time window and convert it to UTC at the same time
                    #app.Update_current_end_trading_time(end_trading_time)
                    correct_end_trading_time = dt.datetime.combine(dt.date(2018,9,15), end_trading_time) - dt.timedelta(minutes=30)
                    correct_end_trading_time_pandas_series =  pd.to_datetime(correct_end_trading_time)
                    correct_end_trading_time_pandas_series_ET_tz = correct_end_trading_time_pandas_series.tz_localize(tz="US/Eastern")
                    correct_end_trading_time_pandas_series_UTC_tz = correct_end_trading_time_pandas_series_ET_tz.tz_convert(tz="UTC")
                    if Not_first_time == True:    
                        #pass
                        time.sleep(8.5)
                        print("In between requsted intraday trading intervals sleep for 10 secs")
                        Logging.lg.logger.debug("In between requsted intraday trading intervals sleep for 10 secs")
                        # This conversion is for the correctness of the following print statement
                        print("Download of {} for {} trading date and {} UTC (30 minutes after this time) time interval took: {}".format(stock, trading_date.strftime("%Y%m%d"), 
                                 correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S"), time.time() - start_time))
                        Logging.lg.logger.debug("Download of {} for {} trading date and {} UTC (30 minutes after to this time) time interval took: {}".format(stock, 
                                 trading_date.strftime("%Y%m%d"), correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S"), time.time() - start_time))
                    else:
                        # Sleeping to allow connection to complete
                        time.sleep(8)
                        #TODO Change to 15 seconds
                        print("{}\'s start up sleep for 8 secs".format(app))
                        Logging.lg.logger.debug("{}\'s start up sleep for 8 secs".format(app))
                        Not_first_time = True
                    #time.sleep(15)
                    #global count
                    #count = 0
                    #Python_TWS_API_Historical_Data_Download.Partial_download_complete.clear()
                    print("Attemtping download of {} for {} trading date and {} UTC (30 minutes after this time) time interval".format(stock, trading_date.strftime("%Y%m%d"), 
                                                                                                                                       correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S")))
                    Logging.lg.logger.debug("Attemtping download of {} for {} trading date and {} UTC (30 minutes after this time) time interval".format(stock, trading_date.strftime("%Y%m%d"), 
                                                                                                                                                         correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S")))
                    
                    self.Make_Bar_Request(app, self.contract, trading_date, end_trading_time, time_duration, time_resolution)
                    #app.run()
                    start_time = time.time()
                    #Python_TWS_API_Historical_Data_Download.Partial_download_complete.wait()
                
                    self.Update_Pending_download(True)
                    while_loop_counter = 0
                    while self.Pending_download == True or self.Connection_OK == False:
                        while_loop_counter += 1      
                        time.sleep(2.1)
                        if while_loop_counter == 30:
                            #Hist_data_end_time = dt.time(pd_end.hour, pd_end.minute, pd_end.second)
                            if Utililty_Functions.Instrument_Type_Class.Inst_Type == "FX":
                                EOD_time = dt.time(24,0,0)
                            else: # Utililty_Functions.Instrument_Type_Class.Inst_Type == "STK"                
                                EOD_time = dt.time(16,0,0)
                            if end_trading_time == EOD_time:
                                app.saving_Bars_to_File(app.Ticks_List, trading_date.strftime("%Y%m%d"), contract.symbol, Sec_Type_and_Currency)
                            print("While loop counter of 30 hit. Download of {} for {} trading date and {} UTC (30 minutes after to this time) time interval failed. Skipping it.".format(
                                stock, trading_date.strftime("%Y%m%d"), correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S")))
                            Logging.lg.logger.debug("While loop counter of 30 hit. Download of {} for {} UTC trading date and {} (30 minutes after to this time) time interval failed. Skipping it.".format(
                                stock, trading_date.strftime("%Y%m%d"), correct_end_trading_time_pandas_series_UTC_tz.strftime("%H:%M:%S")))
                            self.Update_Pending_download(False)
                            #break

# For US Stocks:
#Prep_and_iterating_class_1 = Prep_and_iterating_class(US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_1)
#Prep_and_iterating_class_2 = Prep_and_iterating_class(US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_2)
#Prep_and_iterating_class_3 = Prep_and_iterating_class(US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_3)
#Prep_and_iterating_class_4 = Prep_and_iterating_class(US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_4)
#Prep_and_iterating_class_5 = Prep_and_iterating_class(US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_5)

# For FX:
#Prep_and_iterating_class_FX = Prep_and_iterating_class(FX_Tickers.FX_Tickers.FX_Tickers_Dict)

#time.sleep(3)