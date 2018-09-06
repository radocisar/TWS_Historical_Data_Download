class Write_to_File:
    #def __init__(self):
       #Raw_File = open("C:\Python TWS API\Python_TWS_API_Historical_Data_Download\Python_TWS_API_Historical_Data_Download\TestFile.txt","w")

    #def open_File_to_Save_Ticks_to(self, PathFileName:str):
    #    self.Raw_File = open(PathFileName,"a")

    #def saving_Bars_to_File(self, bar):
    #    self.Raw_File.write(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
    #    #self.Raw_File.write(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
    #    print(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")

    ### For Bars
    @staticmethod
    def saving_Bars_to_File(Ticks_List, Trading_date_item, Ticker_Symbol, Sec_Type_and_Currency):
        if Sec_Type_and_Currency == "STK|USD":
            os.makedirs(r"C:\Raw_Data\Raw_1_sec_Bar_Data\US_Stocks\\" + Ticker_Symbol)
            Raw_File = open(r"C:\Raw_Data\Raw_1_sec_Bar_Data\US_Stocks\\" + Ticker_Symbol + "\\" + Ticker_Symbol + "_Bars_" + Trading_date_item + ".txt","w")
            Raw_File.write("DateTime_UTC|Open|High|Low|Close|Volume|Count|\n")
            for l in Ticks_List:
                Raw_File.write(l)
            Raw_File.close
        else:
            #hdd.Sec_Type_and_Currency != "STK|USD"
            os.makedirs(r"C:\Raw_Data\Raw_1_sec_Bar_Data\FX\\" + Ticker_Symbol)
            Raw_File = open(r"C:\Raw_Data\Raw_1_sec_Bar_Data\FX\\" + Ticker_Symbol + "_Bars_" + Trading_date_item + ".txt","w")
            Raw_File.write("DateTime_UTC|Open|High|Low|Close|Volume|Count|\n")
            for l in Ticks_List:
                Raw_File.write(l)
            Raw_File.close
        #self.Raw_File.write(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
        #print(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
    
    #@staticmethod
    #def close_File_to_Save_Bars_to():
    #    self.Raw_File.close
    
    ### For Ticks
    @staticmethod
    def saving_Ticks_to_File(Ticks_List):
        Raw_File = open("C:\Python TWS API\Python_TWS_API_Historical_Data_Download\Python_TWS_API_Historical_Data_Download\TestTicksFile.txt","w")
        Raw_File.write("DateTime_UTC|Price|Size|Exchange|Condition_Code\n")
        for l in Ticks_List:
            Raw_File.write(l)
        Raw_File.close
        #self.Raw_File.write(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
        #print(bar.date + "|" + str(bar.open) + "|" + str(bar.high) + "|" + str(bar.low) + "|" + str(bar.close) + "|" + str(bar.volume) + "|" + str(bar.barCount) + "\n")
    
    #@staticmethod
    #def close_File_to_Save_Ticks_to():
    #    self.Raw_File.close