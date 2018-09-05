import datetime as dt

class Making_Requests:
    """description of class"""
    @staticmethod
    def Make_Bar_Request(app, contract):
        app.reqHistoricalData(1002, contract, dt.datetime(2018,8,29,10,0,0).strftime("%Y%m%d %H:%M:%S"), "1799 S","1 secs", "TRADES", 1, 2, False, [])

    @staticmethod
    def Make_Ticks_Request(app, contract):
        app.reqHistoricalTicks(1003, contract,"20180829 09:30:00", "", 1000, "TRADES", 1, True, [])


