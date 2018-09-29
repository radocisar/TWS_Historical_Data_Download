import threading
import US_Stock_Tickers
from Python_TWS_API_Historical_Data_Download import New_App
import FX_Tickers
import Utility_Functions

def InitializeThreadforApp_1():
    
    if Utililty_Functions.Instrument_Type_Class.Inst_Type == "FX":
        ### App_1
        app_1 = New_App(RequestId=1502)
        # Connection
        app_1.connect("127.0.0.1",7496,1502)
        # Properties:
        Not_first_time = False
        # Thread
        th1 = threading.Thread(target=app_1.Preparing_and_iterating_requests, name="Thread th1", args=(app_1, Not_first_time, FX_Tickers.FX_Tickers.populate_Tickers_Dict()))
        th1.deamon = True
        th1.start()
        #app_1.Preparing_and_iterating_requests(app_1, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_1)
        app_1.run()
    elif Utililty_Functions.Instrument_Type_Class.Inst_Type == "STK":
        ### App_1
        app_1 = New_App(RequestId=1501)
        # Connection
        app_1.connect("127.0.0.1",7496,1501)
        # Properties:
        Not_first_time = False
        # Thread
        th1 = threading.Thread(target=app_1.Preparing_and_iterating_requests, name="Thread th1", args=(app_1, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.populate_Tickers_Dict()))
        th1.deamon = True
        th1.start()
        #app_1.Preparing_and_iterating_requests(app_1, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_1)
        app_1.run()

def InitializeThreadforApp_2():
    ### App_2
    app_2 = New_App(RequestId=1502)
    # Connection
    app_2.connect("127.0.0.1",7496,1502)
    # Properties:
    Not_first_time = False
    # Thread
    th2 = threading.Thread(target=app_2.Preparing_and_iterating_requests, name="Thread th2", args=(app_2, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_2))
    th2.deamon = True
    th2.start()
    #app_2.Preparing_and_iterating_requests(app_2, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_2)
    app_2.run()

def InitializeThreadforApp_3():
    ### App_3
    app_3 = New_App(RequestId=1503)
    # Connection
    app_3.connect("127.0.0.1",7496,1503)
    # Properties:
    Not_first_time = False
    # Thread
    th3 = threading.Thread(target=app_3.Preparing_and_iterating_requests, name="Thread th3", args=(app_3, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_3))
    th3.deamon = True
    th3.start()
    #app_3.Preparing_and_iterating_requests(app_3, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_3)
    app_3.run()

def InitializeThreadforApp_4():
    ### App_4
    app_4 = New_App(RequestId=1504)
    # Connection
    app_4.connect("127.0.0.1",7496,1504)
    # Properties:
    Not_first_time = False
    # Thread
    th4 = threading.Thread(target=app_4.Preparing_and_iterating_requests, name="Thread th4", args=(app_4, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_4))
    th4.daemon = True
    th4.start()
    app_4.run()

def InitializeThreadforApp_5():
    ### App_5
    app_5 = New_App(RequestId=1505)
    # Connection
    app_5.connect("127.0.0.1",7496,1505)
    # Properties:
    Not_first_time = False
    # Thread
    th5 = threading.Thread(target=app_5.Preparing_and_iterating_requests, name="Thread th5", args=(app_5, Not_first_time, US_Stock_Tickers.US_Stock_Tickers.US_Stock_Tickers_Dict_5))
    th5.daemon = True
    th5.start()
    app_5.run()

