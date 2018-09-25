import pandas as pd
import Drive_to_Save_Files_to

class Download_Start_and_End_Dates():
    """description of class"""
    
    def __init__(self):
        #cls.start_dt,self.end_dt = populate_Start_and_End_Dates()
        self.start_dt = ""
        self.end_dt = ""
        
    def populate_Start_and_End_Dates(self):
        dfr = pd.read_csv(r"{}:\Raw_Data\Raw_1_sec_Bar_Data\Inputs\Start_and_End_Dates_Input.txt".format(Drive_to_Save_Files_to.Drive_Function_Class.Drive_Function.Drive), delimiter="|")
        self.start_dt = dfr["Start_Date"][0]
        self.end_dt = dfr["End_Date"][0]
        return self.start_dt,self.end_dt


