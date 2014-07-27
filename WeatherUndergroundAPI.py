'''
- Is there a label for this problem of wanting to declare an instance of a
    non-base class without having the data yet to do work on that class
        - solutions: have multiple types of constructors, or take funcitonality out of constructor

TODO
- write prints and errors to log
- automate
- setup sleep wake times to do this every hour
    - check how long it takes to reconnect to wifi
- parse exception to not create table if the error is table already created
'''

import logging
import sqlInterface
import traceback
import datetime
import requests
from time import sleep

'''
        arrange by clearness of condition, then possibly by temperature of occurence

        clear:                      0(clear, sunny)

        cloudy:                     1(scattered Clouds, mostly sunny, partly cloudy)
                                    2(mostly cloudy, partly sunny)
                                    3(overcast, cloudy, fog, haze)

        chance of precipitation:    4('Chance of Rain','Chance of Freezing Rain','Chance of Sleet','Chance of Snow')
        precipitation:              5(rain, freezing rain, sleet, flurries, snow)
                                    6(chance of thunderstorm)
                                    7(thunderstorm)
    error prediciton [-7, 7] -7= predicted thunderstorms and was sunny, 7= predicted clear and thunderstorms 

'''
typesOfConditions = ['Chance of Rain','Chance of Freezing Rain','Chance of Sleet','Chance of Snow', \
                    'Chance of Thunderstorms','Clear','Mostly Cloudy','Partly Cloudy','Cloudy','Flurries', \
                    'Fog','Haze','Mostly Sunny','Partly Sunny','Freezing Rain','Rain','Sleet','Sunny',\
                    'Thunderstorm','Unknown','Overcast','Snow','Scattered Clouds']


class WeatherUndergroundAPI:
    table = sqlInterface.Table("", "WUnderground.db")

    try:
        data = requests.get(r'http://api.wunderground.com/api/30ee77078e4be97c/hourly/q/MI/Lansing.json').json()
    except:
        print(str(datetime.datetime.now()) + "   could not connect to network")
        print(traceback.format_exc())
        exit(0)

    def __init__(self):
        print(str(datetime.datetime.now()) + "   api constructor")
        year = self.data['hourly_forecast'][0]['FCTTIME']['year']
        month = self.data['hourly_forecast'][0]['FCTTIME']['mon']
        day = self.data['hourly_forecast'][0]['FCTTIME']['mday']
        hour = self.data['hourly_forecast'][0]['FCTTIME']['hour']
        minute = self.data['hourly_forecast'][0]['FCTTIME']['min']
        sec = self.data['hourly_forecast'][0]['FCTTIME']['sec']
        tableName = 'weatherUnderground_' + year + '_' + month + '_' + day + '_' + twoDigitNumber(hour) + minute
        self.table.tableName = tableName
        self.table.tableType = "prediction"

        go = 1

        try:
            self.table.createTable()
            for h in range(0,36):
                # form timeStamp
                time = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + sec
                top = year + "-" + month + "-" + addHoursToTimeStamp(h, int(day), int(hour)) + ":" + minute + ":" + sec
                cond = self.data['hourly_forecast'][h]['condition']
                temp = self.data['hourly_forecast'][h]['temp']['english']
                hum = self.data['hourly_forecast'][h]['humidity']
                rainAmount = self.data['hourly_forecast'][h]['qpf']['english']
                pop = self.data['hourly_forecast'][h]['pop']
                wind = self.data['hourly_forecast'][h]['wspd']['english']
                p = sqlInterface.Prediction(time, top, cond, temp, hum, rainAmount, pop, float(wind))
                self.table.insertRow(p)
        except:
            print(str(datetime.datetime.now()) +"  table operation")
            print(traceback.format_exc())
            go = 0

        if(go):
            self.table.commitChanges()
            self.table.printTable()


        

def logAndPrint(msg, level):
    print(msg)
    if(level == "info"):
        logging.info(msg)
    elif(level == "debug"):
        logging.debug(msg)
    elif(level == "warning"):
        logging.warning(msg)
    elif(level == "error"):
        logging.error(msg)
    else:
        logAndPrint("logging level must be info, debug, or warning", "error")
        sys.exit(0)

def addHoursToTimeStamp(add_hours, day, hour):
    while((add_hours + hour) > 23):
        day += 1
        add_hours -= 24
    hour += add_hours
    return(str(day) + " " + str(hour))

def twoDigitNumber(num):
    if(num < 10):
        return("0" + str(num))
    else:
        return(str(num))
