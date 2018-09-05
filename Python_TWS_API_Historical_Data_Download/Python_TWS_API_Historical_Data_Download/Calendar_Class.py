import pandas as pd
from pandas import DateOffset
from pandas.tseries.holiday import AbstractHolidayCalendar, nearest_workday, sunday_to_monday, next_monday_or_tuesday, previous_friday, next_monday, Holiday, MO, TU, WE, TH, FR, SA, SU
from pandas.tseries.offsets import CustomBusinessDay, Easter, Day

class US_Stocks_Trading_Calendar(AbstractHolidayCalendar):
    rules= [
        Holiday("New Year's Day", month=1, day=1, observance=sunday_to_monday), 
        Holiday("Martin Luther King, Jr. Day", month=1, day=1, offset=DateOffset(weekday=MO(3))), 
        Holiday("Washington’s Birthday", month=2, day=1, offset=DateOffset(weekday=MO(3))), 
        Holiday("Good Friday", month=1, day=1, offset=[Easter(),Day(-2)]), 
        Holiday("Memorial Day", month=5, day=31, offset=DateOffset(weekday=MO(-1))), 
        Holiday("Independence Day", month=7, day=4, observance=nearest_workday), 
        Holiday("Labor Day", month=9, day=1, offset=DateOffset(weekday=MO(1))), 
        Holiday("Thanksgiving Day", month=11, day=1, offset=DateOffset(weekday=TH(4))), 
        Holiday("Christmas Day", month=12, day=25, observance=nearest_workday), 
        Holiday("Day before Independence Day - Half day", month=7, day=3, observance=previous_friday), 
        Holiday("Day following Thanksgiving - Half day", month=11, day=1, offset=DateOffset(weekday=WE(4))), 
        Holiday("Christmas Eve - Half day", month=12, day=24, observance=previous_friday)
    ]

US_Stocks_Trading_Cal = CustomBusinessDay(calendar = US_Stocks_Trading_Calendar())

class FX_Trading_Calendar(AbstractHolidayCalendar):
    rules= [
        Holiday("New Year's Day", month=1, day=1), 
        Holiday("Christmas Day", month=12, day=25, observance=next_monday), 
    ]

FX_Trading_Cal = CustomBusinessDay(calendar = FX_Trading_Calendar())


