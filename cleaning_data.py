# Project for CS 5010

# Team Metro

import csv
import pandas

# import dataset
with open("traffic.csv", newline="") as traffic:
    reader = csv.reader(traffic)
    data = list(reader)
    data = data[1:] # remove the row of headers from the data
    

    # strip the whitespace from all strings
    i = 0
    for row in data:
        j = 0
        for item in row:
            data[i][j] = data[i][j].strip(' ')
            j += 1
        i += 1


    # type cast ints and floats
    i = 0
    ints = [4,8] # columns with int values
    floats = [1,2,3] # columns with float values
    for row in data:
        j = 0
        for item in row:
            if j in ints:
                data[i][j] = int(data[i][j]) # convert integer values from string to int
            if j in floats:
                data[i][j] = float(data[i][j]) # convert floating point values from string to float
            j += 1
        i += 1


    # make date/time column have a consistent format
    # originally one row may have "1/7/13 9:00" and another "10/23/13 13:00"
    # we need to add zeros so that all strings are the same length
    i = 0
    for row in data:
        if row[7][1] == "/": # add a zero if the month is a single digit
            data[i][7] = "0" + row[7]
        if row[7][4] == "/": # add a zero if the day is a single digit
            data[i][7] = row[7][:3] + "0" + row[7][3:]
        data[i][7] = row[7][:6] + "20" + row[7][6:] # expand the year to 4 digits
        if row[7][-5] == " ": # add a zero if the hour is a single digit
            data[i][7] = row[7][:11] + "0" + row[7][11:]
        i += 1

    # extract specifics from the date and time string and make new columns
    i = 0 
    for row in data:
        month = int(row[7][:2]) # append the month as an integer
        data[i].append(month)
        day = int(row[7][3:5]) # append the day as an integer
        data[i].append(day)
        year = int(row[7][6:10]) # append the year as an integer
        data[i].append(year)
        hour = int(row[7][11:13]) # append the hour as an integer
        data[i].append(hour)
        i += 1

    # fix holiday issue
    # issue: the holiday column only displayed the holiday at the zero hour
    # so hours 1-23 of the holiday were marked as "None" like every ordinary day
    i = 0
    holiday = ""
    for row in data:
        if data[i][12] == 0:
            holiday = data[i][0] # take the holilday of the zero hour
        elif i == 0: # account for the first datapoint not starting at hour zero
            holiday = data[i][0]
        else:
            data[i][0] = holiday # make the holiday of every other hour of the day the same as hour 0
        i += 1


    # multiple values for weather and weather description
    # essentially, some data points had different types of weather within the same hour
    # all field values (including exact date and hour) were identical except weather_main and weather_description
    # this creates duplicate data points for the same date and hour
    # we solve this by storing all of the weather items in the first instance of the duplicated data
    # we separate them by a semicolon and delete the extra rows (ends up deleting ~7,500 rows)
    # this ensures we do not loose the weather info but also that we do not have duplicate data points
    i = 1
    while i < len(data):
        if data[i][7] == data[i-1][7]:
            data[i-1][5] = data[i-1][5] + ";" + data[i][5]
            data[i-1][6] = data[i-1][6] + ";" + data[i][6]
            del data[i]
        else:
            i += 1
    
    # Convert temperature from Kelvin to Farenheit
    for row in range(len(data)):
        if data[row][1] == 0: # if the temperature is missing use the temp from the previous hour
            data[row][1] = round(float((lastK - 273.15)*(9/5)+32),2) # ~20 data points missing temperature
        else:
            lastK = data[row][1]
            data[row][1] = round(float((data[row][1] - 273.15)*(9/5)+32),2)


headers = ['Holiday', 'Temperature', "Rain_1h", "Snow_1h", "Clouds_All", "Weather_Main", \
        "Weather_Description", "Date_Time", "Traffic_Volume", "Month", "Day", "Year", "Hour"]
# create a list of the column names we want

dfClean = pandas.DataFrame(data, columns=headers)
# store the data in a pandas dataframe for easy manipulation

# export the cleaned data into a new csv
with open("cleaned_traffic.csv", "w") as cleaned:
    writer = csv.writer(cleaned)
    writer.writerow(headers)
    writer.writerows(data)

    

