import logging
import datetime as dt
import threading
import time

class Logging:
    
    Current_Date = time.strftime("%Y%m%d_%H%M", time.gmtime())
    File_Location = r"C:\Raw_Data\Raw_1_sec_Bar_Data\US_Stocks_Log\{}_US_Stocks.log".format(Current_Date)

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(self.File_Location)
        self.formatter = logging.Formatter("%(asctime)s |File Name: %(filename)s | %(levelname)s | Message: %(message)s | Module: %(module)s | Function Name: %(funcName)s | Line No: %(lineno)d | Thread: %(threadName)s | %(processName)s")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

    def Date_Updater(self):
        while True:
            print("Initiated infinite While loop")
            while Logging.Current_Date == time.strftime("%Y%m%d_%H%M", time.gmtime()):
                print("Passing")
                time.sleep(1)
                pass
            Logging.Current_Date = time.strftime("%Y%m%d_%H%M", time.gmtime())
            #Logging.File_Open = False
            #self.f.close()
            print("New File")
            self.File_Location = r"C:\Raw_Data\Raw_1_sec_Bar_Data\US_Stocks_Log\{}_US_Stocks.log".format(self.Current_Date)
            #self.logger.removeHandler(self.file_handler)
            self.file_handler = logging.FileHandler(self.File_Location)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)
            #self.f = open(self.File_Location,"w")
            #Logging.File_Open = True
        
        #def Roll_file_handler_to_new_day(self):
        #    while True:
        #        while self.Current_Date == time.strftime("%Y%m%d", time.gmtime()): 
        #            self.file_handler = logging.FileHandler(self.File_Location)
        
lg = Logging()

t = threading.Thread(target=lg.Date_Updater)
t.deamon = True
t.start()