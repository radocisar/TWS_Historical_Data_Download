import pandas as pd
import Drive_to_Save_Files_to

class FX_Tickers:

    def __init__(self):
        self.FX_Tickers_Dict = {}
        #self.US_Stock_Tickers_Dict_1 = populate_Tickers_Dict()

    def populate_Tickers_Dict():
        df = pd.read_csv(r"{}:\Raw_Data\Raw_1_sec_Bar_Data\FX_Inputs\Ticker_Input.txt".format(Drive_to_Save_Files_to.Drive_Function_Class.Dr), delimiter="|")
        REF_Ticker_list = df["REFERENCE_Ticker"].tolist()
        BASE_Ticker_list = df["BASE_Ticker"].tolist()
        Dic_Labels = [x for x in range(len(REF_Ticker_list))]
        dic = {Dic_Labels:[REF_Ticker_list, BASE_Ticker_list] for Dic_Labels, REF_Ticker_list,BASE_Ticker_list in zip(Dic_Labels, REF_Ticker_list,BASE_Ticker_list)}
        return dic

