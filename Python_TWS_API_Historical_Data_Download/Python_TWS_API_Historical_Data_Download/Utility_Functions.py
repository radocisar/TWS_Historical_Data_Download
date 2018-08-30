class Utility_Functions:
    #def __init__(self):
    #   return(self)

    def open_File_to_Save_Ticks_to(self, PathFileName:str):
        self.Raw_File = open(PathFileName,"w")

    def saving_Ticks_to_File(self, bar):
        self.Raw_File.write(bar.date,  + " "  + bar.open + " " + bar.high + " " + bar.low + " " + bar.close + " " + bar.volume + " " + bar.count + "\n")
        
    def close_File_to_Save_Ticks_to(self):
        self.Raw_File.close