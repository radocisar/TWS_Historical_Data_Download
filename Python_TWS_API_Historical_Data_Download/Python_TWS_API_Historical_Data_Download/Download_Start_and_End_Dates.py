import pandas as pd

class Download_Start_and_End_Dates():
    """description of class"""
    start_dt=""
    end_dt=""

    def __init__():
        self.start_dt,self.end_dt = populate_Start_and_End_Dates()

    def populate_Start_and_End_Dates():
        dfr = pd.read_csv(r"C:\Raw_Data\Raw_1_sec_Bar_Data\Inputs\Start_and_End_Dates_Input.txt", delimiter="|")
        start_dt = dfr["Start_Date"][0]
        end_dt = dfr["End_Date"][0]
        return start_dt,end_dt


