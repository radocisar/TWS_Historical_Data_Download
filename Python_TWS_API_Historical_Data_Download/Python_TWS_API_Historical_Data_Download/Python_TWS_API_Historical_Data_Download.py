from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
import datetime as dt
#from Utility_Functions import Utility_Functions
from Utility_Functions import Write_to_File
import Utility_Functions
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import Calendar_Class
#import US_Stock_Tickers
import FX_Tickers
from Making_Requests import Prep_and_iterating_class
import time
import threading
import math
import Logging
import Initialize_threads
import Drive_to_Save_Files_to
import time

#count = 0

#Partial_download_complete = threading.Event()

###This is where the events are returned (into the EWrapper)
class New_App (EWrapper, EClient, Write_to_File, Prep_and_iterating_class):
    #Pending_download = False
    #uf = Utility_Functions()
    #wtf = Write_to_File()
    count = 0

    def __init__(self, Ticks_List=None, RequestId=None):
        EClient.__init__(self,self)
        Prep_and_iterating_class.__init__(self)
        Write_to_File.__init__(self)
        self.FileisnowOpen = False
        if Ticks_List is None:
            self.Ticks_List = []
        else:
            self.Ticks_List = Ticks_List
        self.RequestId = RequestId
        self.prog_start_time = time.time()

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        print("Contract Details: ", reqId, contractDetails)

    def error(self, reqID:TickerId, errorCode:int, errorString:str):
        #print("Error: {} | {} | Request_ID: {} | Ticker: {} {}".format(errorCode, errorString, reqID, self.Ticker_Symbol, self.Sec_Type_and_Currency))
        Logging.lg.logger.debug("Error: {} | {} | Request_ID: {} | Ticker: {} {}".format(errorCode, errorString, reqID, self.Ticker_Symbol, self.Sec_Type_and_Currency))
        # excluded:
        #   errorCode == 2103 (Market data error)
        if errorCode == 2105 or errorCode == 1100 or errorCode == 1101 or errorCode == 1102 or errorCode == 1300 or errorCode == 2110:
           self.Update_Connection_OK(False)
        # excluded:
        #   errorCode == 2104 (Market data access restoration)
        #   errorCode == 2108 (Market data dormant access restoration)
        elif errorCode == 2106 or errorCode == 2107:
            if self.prog_start_time + 60 < time.time():
                time.sleep(20)
            self.Update_Connection_OK(True)

    def historicalData(self, reqId:int, bar:BarData):
        #returns the requested historical data bars
        #print(self.Trading_date_item)
        #print(dt.datetime.fromtimestamp(int(bar.date)).strftime("%Y%m%d"))
        if self.Trading_date_item == pd.to_datetime(int(bar.date), unit="s").tz_localize(tz="UTC").strftime("%Y%m%d"):
            self.Ticks_List.append(str(dt.datetime(1970,1,1)+dt.timedelta(seconds=int(bar.date))) + "|" + str(bar.open) + "|" + str(bar.high) + 
                               "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "|" + "\r\n")

        self.count += 1
        if math.fmod(self.count,100) == 0:
            #print("{} | {} UTC | {}".format(self.Ticker_Symbol, str(dt.datetime(1970,1,1)+dt.timedelta(seconds=int(bar.date))), str(self.count)))
            Logging.lg.logger.debug("{} | {} UTC | {}".format(self.Ticker_Symbol, str(dt.datetime(1970,1,1)+dt.timedelta(seconds=int(bar.date))), str(self.count)))
        #if self.FileisnowOpen == False:
            #Raw_File = open("C:\Python TWS API\Python_TWS_API_Historical_Data_Download\Python_TWS_API_Historical_Data_Download\TestFile.txt","w")
            #self.uf.open_File_to_Save_Ticks_to("C:\Python TWS API\Python_TWS_API_Historical_Data_Download\Python_TWS_API_Historical_Data_Download\TestFile.txt")            
            #self.FileisnowOpen = True
        #self.uf.saving_Bars_to_File(Raw_File, bar)
        #self.wtf.saving_Bars_to_File(bar)
        
        #Function and bars description:
        #region
        """reqId - the request's identifier
        date  - the bar's date and time (either as a yyyymmss hh:mm:ssformatted
                string or as system time according to the request)
        open  - the bar's open point
        high  - the bar's high point
        low   - the bar's low point
        close - the bar's closing point
        volume - the bar's traded volume if available
        count - the number of trades during the bar's timespan (only available
            for TRADES).
        WAP -   the bar's Weighted Average Price
        hasGaps  -indicates if the data has gaps or not."""
        #endregion
    Trading_date_item = ""
    Ticker_Symbol = ""
    Sec_Type_and_Currency = ""
    Current_end_trading_time = ""

    def Update_current_end_trading_time(self, current_end_trading_time):
        self.Current_end_trading_time = current_end_trading_time

    def Update_trading_date_item(self, trading_date_item):
        self.Trading_date_item = trading_date_item

    def Update_Ticker_Symbol(self, Ticker_Symbol):
        self.Ticker_Symbol = Ticker_Symbol

    def Update_Sec_Type_and_Currency(self, Sec_Type_and_Currency):
        self.Sec_Type_and_Currency = Sec_Type_and_Currency

    def historicalDataEnd(self, reqId:int, start:str, end:str):
        """ Marks the ending of the historical bars reception. """
        #self.wtf.close_File_to_Save_Bars_to()
        #Raw_File.close
        #self.uf.close_File_to_Save_Bars_to()
        global trading_date_item
        #global Partial_download_complete
        #print("Historical bar data download for {} from {} to {} done".format(self.Ticker_Symbol, start, end))
        #Logging.lg.logger.debug("Historical bar data download for {} from {} to {} done".format(self.Ticker_Symbol, start, end))
        pd_start = pd.to_datetime(start)
        pd_end = pd.to_datetime(end)
        pd_end_Eastern = pd_end.tz_localize(tz="US/Eastern")
        pd_end_UTC = pd_end_Eastern.tz_convert(tz="UTC")
        if Utility_Functions.Instrument_Type_Class.Inst_Type == "FX":
            Hist_data_end_time = dt.time(pd_end_UTC.hour, pd_end_UTC.minute, pd_end_UTC.second)
            EOD_time = dt.time(0,0,0)
        else: # Utility_Functions.Instrument_Type_Class.Inst_Type == "STK"                
            Hist_data_end_time = dt.time(pd_end_Eastern.hour, pd_end_Eastern.minute, pd_end_Eastern.second)
            EOD_time = dt.time(16,0,0)
        #EOD_time = dt.time(16,0,0)
        if Hist_data_end_time == EOD_time:
            self.saving_Bars_to_File(self.Ticks_List, self.Trading_date_item, self.Ticker_Symbol, self.Sec_Type_and_Currency)
        else:
            pass
        
        #Prep_and_iterating_class_1.Update_Pending_download(False)
        self.Update_Pending_download(False)
        pd_start_ET_tz = pd_start.tz_localize(tz="US/Eastern")
        pd_end_ET_tz = pd_end.tz_localize(tz="US/Eastern")
        pd_start_UTC_tz = pd_start_ET_tz.tz_convert(tz="UTC")
        pd_end_UTC_tz = pd_end_ET_tz.tz_convert(tz="UTC")
        #print("Historical bar data download for {} from {} UTC to {} UTC done and returned on RequestId: {}".format(self.Ticker_Symbol, pd_start_UTC_tz, pd_end_UTC_tz, reqId))
        Logging.lg.logger.debug("Historical bar data download for {} from {} UTC to {} UTC done and returned on RequestId: {}".format(self.Ticker_Symbol, pd_start_UTC_tz, pd_end_UTC_tz, reqId))
        #Should not be necessary as each instance of the app and prep_and_iterate class should be separate, hence request data call (from prep_and_iterate class) shold return data to the right instance of the app
        #if regId == 1501:
        #    Prep_and_iterating_class_1.Update_Pending_download(False)
        #    print("Historical bar data download for {} from {} to {} returned on RequestId: 1501".format(self.Ticker_Symbol, start, end))
        #    Logging.lg.logger.debug("Historical bar data download for {} from {} to {} returned on RequestId: 1501".format(self.Ticker_Symbol, start, end))
        #elif regId == 1502:
        #    Prep_and_iterating_class_2.Update_Pending_download(False)
        #    print("Historical bar data download for {} from {} to {} returned on RequestId: 1502".format(self.Ticker_Symbol, start, end))
        #    Logging.lg.logger.debug("Historical bar data download for {} from {} to {} returned on RequestId: 1502".format(self.Ticker_Symbol, start, end))
        #elif regId == 1503:
        #    Prep_and_iterating_class_3.Update_Pending_download(False)
        #    print("Historical bar data download for {} from {} to {} returned on RequestId: 1503".format(self.Ticker_Symbol, start, end))
        #    Logging.lg.logger.debug("Historical bar data download for {} from {} to {} returned on RequestId: 1503".format(self.Ticker_Symbol, start, end))
        #elif regId == 1504:
        #    Prep_and_iterating_class_4.Update_Pending_download(False)
        #    print("Historical bar data download for {} from {} to {} returned on RequestId: 1504".format(self.Ticker_Symbol, start, end))
        #    Logging.lg.logger.debug("Historical bar data download for {} from {} to {} returned on RequestId: 1504".format(self.Ticker_Symbol, start, end))
        #else:
        #    Prep_and_iterating_class_5.Update_Pending_download(False)
        #    print("Historical bar data download for {} from {} to {} returned on RequestId: 1505".format(self.Ticker_Symbol, start, end))
        #    Logging.lg.logger.debug("Historical bar data download for {} from {} to {} returned on RequestId: 1505".format(self.Ticker_Symbol, start, end))

        #Partial_download_complete.set()
    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast,done: bool):
        #returns the requested historical tick data
        for tick in ticks:
            self.Ticks_List.append(str(dt.datetime(1970,1,1)+dt.timedelta(seconds=tick.time)) + "|" + str(tick.price) + "|" + str(tick.size) + "|" + str(tick.exchange) + "|" + str(tick.specialConditions) + "|" + "\n")
        if done is True:
            self.historicalTicksDownloadDone(done)
    
    def historicalTicksDownloadDone(self, done: bool):
        Write_to_File.saving_Ticks_to_File(self.Ticks_List)
        print("Historical tick data download done")

### This is where parameters are defined and requests are made from
def main():
    #global Drive

    t1 = threading.Thread(target=Initialize_threads.InitializeThreadforApp_1, name="Thread for app_1")
    t1.daemon = True
    t1.start()
    
    #t2 = threading.Thread(target=Initialize_threads.InitializeThreadforApp_2, name="Thread for app_2")
    #t2.daemon = True
    #t2.start()

    #t3 = threading.Thread(target=Initialize_threads.InitializeThreadforApp_3, name="Thread for app_3")
    #t3.daemon = True
    #t3.start()

    #t4 = threading.Thread(target=Initialize_threads.InitializeThreadforApp_4, name="Thread for app_4")
    #t4.daemon = True
    #t4.start()

    #t5 = threading.Thread(target=Initialize_threads.InitializeThreadforApp_5, name="Thread for app_5")
    #t5.daemon = True
    #t5.start()



    #### App_1
    #app_1 = New_App(RequestId=1501)
    ## Connection
    #app_1.connect("127.0.0.1",7496,1501)
    ## Properties:
    #Not_first_time = False
    ## Thread
    ##t1 = threading.Thread(target=app_1.Preparing_and_iterating_requests, name="Thread for app_1", args=(app_1, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_1))
    ##t1.daemon = True
    ##t1.start()
    
    #### App_2
    #app_2 = New_App(RequestId=1502)
    ## Connection
    #app_2.connect("127.0.0.1",7496,1502)
    ## Properties:
    #Not_first_time = False
    ## Thread
    ##t2 = threading.Thread(target=app_2.Preparing_and_iterating_requests, name="Thread for app_2", args=(app_2, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_2))
    ##t2.daemon = True
    ##t2.start()

    #### App_3
    #app_3 = New_App(RequestId=1503)
    ## Connection
    #app_3.connect("127.0.0.1",7496,1503)
    ## Properties:
    #Not_first_time = False
    # Thread
    #t3 = threading.Thread(target=app_3.Preparing_and_iterating_requests, name="Thread for app_3", args=(app_3, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_3))
    #t3.daemon = True
    #t3.start()

    #### App_4
    #app_4 = New_App(RequestId=1504)
    ## Connection
    #app_4.connect("127.0.0.1",7496,1111530)
    ## Properties:
    #Not_first_time = False
    ## Thread
    #t4 = threading.Thread(target=app_4.Preparing_and_iterating_requests, name="Thread for app_4", args=(app_4, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_4))
    #t4.daemon = True
    #t4.start()
   
    #### App_5
    #app_5 = New_App(RequestId=1505)
    ## Connection
    #app_5.connect("127.0.0.1",7496,1111530)
    ## Properties:
    #Not_first_time = False
    ## Thread
    #t5 = threading.Thread(target=app_5.Preparing_and_iterating_requests, name="Thread for app_5", args=(app_5, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_5))
    #t5.daemon = True
    #t5.start()

    ### Parameter definitions
    #contract = Contract()
    #contract.symbol = "CVA"
    #contract.secType = "STK"
    #contract.exchange = "SMART"
    #contract.currency = "USD"
    #contract.primaryExchange = "NYSE"
    
    #contract = Contract()
    #contract.symbol = "EUR"
    #contract.secType = "CASH"
    #contract.currency = "GBP"
    #contract.exchange = "IDEALPRO"

    ### Requests to TWS (using EClient)
    
    ### Requesting contract details
    #app_1.reqContractDetails(1001,contract)

    #app_1.run()
    #app_2.run()
    #app_3.run()
    #app_4.run()
    #app_5.run()

    #####t1 = threading.Thread(target=app_1.run, name="Thread for app_1")
    #####t1.daemon = True
    #####t2 = threading.Thread(target=app_2.run, name="Thread for app_2")
    #####t2.daemon = True
    #####t3 = threading.Thread(target=app_3.run, name="Thread for app_3")
    #####t3.daemon = True
    #####t4 = threading.Thread(target=app_4.run, name="Thread for app_4")
    #####t4.daemon = True
    #####t5 = threading.Thread(target=app_5.run, name="Thread for app_5")
    #####t5.daemon = True

    #####t1.start()
    #####t2.start()
    #####t3.start()
    #####t4.start()
    #####t5.start()

    #####app_1.Preparing_and_iterating_requests(app_1, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_1)
    #####app_2.Preparing_and_iterating_requests(app_2, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_2)
    #####app_3.Preparing_and_iterating_requests(app_3, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_3)
    #####app_4.Preparing_and_iterating_requests(app_4, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_4)
    #####app_5.Preparing_and_iterating_requests(app_5, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_5)

if __name__ == "__main__":
    main()