from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import *
from ibapi.contract import *
import datetime as dt
#from Utility_Functions import Utility_Functions
from Utility_Functions import Write_to_File
import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay
import Calendar_Class
import US_Stock_Tickers
import FX_Tickers
import Making_Requests
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

###This is where the events are returned (into the EWrapper)
class New_App (EWrapper, EClient, Write_to_File):
    
    #uf = Utility_Functions()
    #wtf = Write_to_File()

    def __init__(self, Ticks_List=None):
        EClient.__init__(self,self)
        self.FileisnowOpen = False
        if Ticks_List is None:
            self.Ticks_List = []
        else:
            self.Ticks_List = Ticks_List

    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        print("Contract Details: ", reqId, contractDetails)

    def error(self, reqID:TickerId, errorCode:int, errorString:str):
        print("Error: ", reqID, errorCode, errorString)
        
    def historicalData(self, reqId:int, bar:BarData):
        #returns the requested historical data bars
        self.Ticks_List.append(str(dt.datetime(1970,1,1)+dt.timedelta(seconds=int(bar.date))) + "|" + str(bar.open) + "|" + str(bar.high) + 
                               "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "|" + "\n")
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
    
    def historicalDataEnd(self, reqId:int, start:str, end:str):
        """ Marks the ending of the historical bars reception. """
        #self.wtf.close_File_to_Save_Bars_to()
        #Raw_File.close
        #self.uf.close_File_to_Save_Bars_to()
        print("Historical bar data download from", start, "to", end, "done")
        Hist_data_end_time = dt.time(pd.to_datetime(end).hour, pd.to_datetime(end).minute, pd.to_datetime(end).second)
        EOD_time = dt.time(10,29,59)
        if Hist_data_end_time == EOD_time:
            Write_to_File.saving_Bars_to_File(self.Ticks_List, trading_date_item, Ticker_Symbol, Sec_Type_and_Currency)
            self.disconnect()
        else:
            self.disconnect()
            
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
    app = New_App()
    
    ### Connection
    app.connect("127.0.0.1",7496,1111530)
    
    ### Parameter definitions
    contract = Contract()
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
    #app.reqContractDetails(1001,contract)

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
        time_duration = "1799 S"
        time_resolution = "1 secs"
        for trading_date in Trading_Dates_Reversed:
            global trading_date_item
            trading_date_item = trading_date.strftime("%Y%m%d")
            app.Ticks_List.clear()
            for end_trading_time in Trading_Date_30_minute_Intervals:
                Making_Requests.Making_Requests.Make_Bar_Request(app, contract, trading_date, end_trading_time, time_duration, time_resolution)
                app.run()
                time.sleep(3)
    #app.reqHistoricalData(1002, contract, dt.datetime(2018,8,29,10,0,0).strftime("%Y%m%d %H:%M:%S"), "1800 S","1 secs", "TRADES", 1, 2, False, [])
    #app.reqHistoricalData(1002, contract, (dt.datetime(2018,9,4,09,30,0)-dt.timedelta(days=1270)).strftime("%Y%m%d %H:%M:%S"), "1800 S","1 secs", "TRADES", 1, 1, False, [])

    ### Requesting historical tick resolution data
    #Making_Requests.Making_Requests.Make_Ticks_Request(app, contract)
    #app.reqHistoricalTicks(1003, contract,"20180829 09:30:00", "", 1000, "TRADES", 1, True, [])

    #Historical Data Request Description:
    #region
    #Requests contracts' historical data. When requesting historical data, a
    #finishing time and date is required along with a duration string. The
    #resulting bars will be returned in EWrapper.historicalData()
    #reqId:TickerId - The id of the request. Must be a unique value. When the
    #    market data returns, it whatToShowill be identified by this tag. This is also
    #    used when canceling the market data.
    #contract:Contract - This object contains a description of the contract for which
    #    market data is being requested.
    #endDateTime:str - Defines a query end date and time at any point during the past 6 mos.
    #    Valid values include any date/time within the past six months in the format:
    #    yyyymmdd HH:mm:ss ttt
    #    where "ttt" is the optional time zone.
    #durationStr:str - Set the query duration up to one week, using a time unit
    #    of seconds, days or weeks. Valid values include any integer followed by a space
    #    and then S (seconds), D (days) or W (week). If no unit is specified, seconds is used.
    #barSizeSetting:str - Specifies the size of the bars that will be returned (within IB/TWS listimits).
    #    Valid values include:
    #    1 sec
    #    5 secs
    #    15 secs
    #    30 secs
    #    1 min
    #    2 mins
    #    3 mins
    #    5 mins
    #    15 mins
    #    30 mins
    #    1 hour
    #    1 day
    #whatToShow:str - Determines the nature of data beinging extracted. Valid values include:
    #    TRADES
    #    MIDPOINT
    #    BID
    #    ASK
    #    BID_ASK
    #    HISTORICAL_VOLATILITY
    #    OPTION_IMPLIED_VOLATILITY
    #useRTH:int - Determines whether to return all data available during the requested time span,
    #    or only data that falls within regular trading hours. Valid values include:
    #    0 - all data is returned even where the market in question was outside of its
    #    regular trading hours.
    #    1 - only data within the regular trading hours is returned, even if the
    #    requested time span falls partially or completely outside of the RTH.
    #formatDate: int - Determines the date format applied to returned bars. validd values include:
    #    1 - dates applying to bars returned in the format: yyyymmdd{space}{space}hh:mm:dd
    #    2 - dates are returned as a long integer specifying the number of seconds since
    #        1/1/1970 GMT.
    #chartOptions:TagValueList - For internal use only. Use default value XYZ.
    #endregion

    #app.run()

if __name__ == "__main__":
    main()