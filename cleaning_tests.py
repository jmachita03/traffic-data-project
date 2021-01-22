# CS 5010 Project 

# Team Metro

# Test the data cleaning

import unittest
from cleaning_data import dfClean # import the dataframe we created after cleaning the data


class DataTypesTestCase(unittest.TestCase):

    # we will test that each column has the correct data type
    # note that there is a strange occurence seen below when converting to a pandas dataframe

    def test_is_holiday_a_string(self):
        holiday = dfClean.iloc[4908,0]
        self.assertTrue(isinstance(holiday, str))
    
    def test_is_temperature_a_float(self):
        temp = dfClean.iloc[4908,1]
        self.assertTrue(isinstance(temp, float))
    
    def test_is_rain_a_float(self):
        rain = dfClean.iloc[4908,2]
        self.assertTrue(isinstance(rain, float))

    def test_is_snow_a_float(self):
        snow = dfClean.iloc[4908,3]
        self.assertTrue(isinstance(snow, float))

    def test_is_clouds_an_int(self):
        clouds = dfClean.iloc[4908,4]
        self.assertEqual(str(type(clouds)), "<class 'numpy.int64'>")
        # pandas converts all of the ints in the list to numpy.int64 
        # could not figure out how to avoid this

    def test_is_weather_main_a_string(self):
        weather = dfClean.iloc[4908,5]
        self.assertTrue(isinstance(weather, str))
    
    def test_is_weather_descrip_a_string(self):
        weather = dfClean.iloc[4908,6]
        self.assertTrue(isinstance(weather, str))

    def test_is_date_time_a_string(self):
        dateTime = dfClean.iloc[4908,7]
        self.assertTrue(isinstance(dateTime, str))

    def test_is_traffic_an_int(self):
        traffic = dfClean.iloc[4908,8]
        self.assertEqual(str(type(traffic)), "<class 'numpy.int64'>")

    def test_is_month_an_int(self):
        month = dfClean.iloc[4908,9]
        self.assertEqual(str(type(month)), "<class 'numpy.int64'>")

    def test_is_day_an_int(self):
        day = dfClean.iloc[4908,10]
        self.assertEqual(str(type(day)), "<class 'numpy.int64'>")

    def test_is_year_an_int(self):
        year = dfClean.iloc[4908,11]
        self.assertEqual(str(type(year)), "<class 'numpy.int64'>")
    
    def test_is_hour_an_int(self):
        hour = dfClean.iloc[4908,12]
        self.assertEqual(str(type(hour)), "<class 'numpy.int64'>")

    


class DateTimeFormatTestCase(unittest.TestCase):
    def test_does_month_have_two_digits(self):
        i = 0 
        booln = True
        while i < len(dfClean):
            if dfClean.iloc[i,7][2] != "/":
                booln = False
            i += 1
        self.assertTrue(booln)
        # make sure that every data point has a two digit month
        # in cleaning, 0 should have been added to make it two digits
    
    def test_does_day_have_two_digits(self):
        i = 0 
        booln = True
        while i < len(dfClean):
            if dfClean.iloc[i,7][5] != "/":
                booln = False
            i += 1
        self.assertTrue(booln)
        # all months in the date/time string should have two digits after cleaning

    def test_does_year_have_four_digits(self):
        i = 0 
        booln = True
        while i < len(dfClean):
            if dfClean.iloc[i,7][6:8] != "20":
                booln = False
            i += 1
        self.assertTrue(booln)
        # all years should be in the form 20xx in the date/time string
    
    def test_does_hour_have_two_digits(self):
        i = 0
        booln = True # since we already tested all of the other cleaning items on the date/time string
        while i < len(dfClean): # we can check the hour by checking the length of the whole string
            if len(dfClean.iloc[i,7]) != 16: # all in column should have the form "mm/dd/yyyy hh:00"
                booln = False
            i += 1
        self.assertTrue(booln) 
        # in cleaning, 0 should have been added to make a one digit hour (0-9) two digits (00-09)
        # without the other tests this would be a way to check all in one test but would not
        # tell us what part of the cleaning on the date/time string did not work correctly


class AppendColumnsTestCase(unittest.TestCase):
    # we will check that each of the four new columns (month, day, year, and hour)
    # appended correctly to the dataset
    def test_is_month_column_appending_correctly(self):
        i = 0
        booln = True
        while i < len(dfClean):
            if int(dfClean.iloc[i,9]) != int(dfClean.iloc[i,7][:2]):
                booln = False
            i += 1
        self.assertTrue(booln)
    # we check that the month in the month column matches that in the original date/time column
    
    def test_is_day_column_apending_correctly(self):
        i = 0
        booln = True
        while i < len(dfClean):
            if int(dfClean.iloc[i,10]) != int(dfClean.iloc[i,7][3:5]):
                booln = False
            i += 1
        self.assertTrue(booln)
    # we check that the day in the day column matches that in the original date/time column

    def test_is_year_column_apending_correctly(self):
        i = 0
        booln = True
        while i < len(dfClean):
            if int(dfClean.iloc[i,11]) != int(dfClean.iloc[i,7][6:10]):
                booln = False
            i += 1
        self.assertTrue(booln)
    # we check that the year in the year column matches that in the original date/time column


    def test_is_hour_column_apending_correctly(self):
        i = 0
        booln = True
        while i < len(dfClean):
            if int(dfClean.iloc[i,12]) != int(dfClean.iloc[i,7][11:13]):
                booln = False
            i += 1
        self.assertTrue(booln)
    # we check that the hour in the hour column matches that in the original date/time column
    

class HolidayTestCase(unittest.TestCase):
    # we test that every hour of the same day has a consistent holiday
    def test_are_all_hours_correct_holiday(self):
        i = 0
        booln = True
        hol = "None"
        while i < len(dfClean):
            if dfClean.iloc[i,12] == 0:
                hol = dfClean.iloc[i,0]
            else:
                if dfClean.iloc[i,0] != hol:
                    booln = False
            i += 1
        self.assertTrue(booln)


class UniqueDataPointsTestCase(unittest.TestCase):
    # this test ensures that no two data points have the exact same date and hour
    def test_are_all_datetimes_unique(self):
        i = 1
        booln = True
        while i < len(dfClean):
            if dfClean.iloc[i,7] == dfClean.iloc[i-1,7]:
                booln = False
            i += 1
        self.assertTrue(booln)
    

class TemperatureConversionTestCase(unittest.TestCase):
    # we test that the temperature was converted to Fahrenheit
    # note that since we overrode the original temperature, we simply check for 
    # outlier that would make sense as Kelvin values but not Fahrenheit values
    # This how we discovered there were some missing temperatures input as 0 Kelvin
    # because they converted to -450 Fahrenheit
    def test_is_temp_converting_from_kelvin_to_F(self):
        i = 1
        booln = True
        while i < len(dfClean):
            if (dfClean.iloc[i,1] > 120) | (dfClean.iloc[i,1] < -50):
                booln = False
            i += 1
        self.assertTrue(booln)

if __name__ == '__main__': 
    unittest.main() 