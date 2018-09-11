import logging

class Logging:
    """description of class"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler(r"C:\Raw_Data\Raw_1_sec_Bar_Data\US_Stocks_Log\US_Stocks.log")
        self.formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s | %(module)s | %(funcName)s | %(lineno)d | %(threadName)s")
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)