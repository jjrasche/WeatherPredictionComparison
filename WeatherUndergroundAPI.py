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


# connext to API
try:
	data = requests.get(r'http://api.wunderground.com/api/30ee77078e4be97c/hourly/q/MI/Lansing.json').json()
except:
	print(str(datetime.datetime.now()) + "   could not connect to network")
	print(traceback.format_exc())
	exit(0)

# API has a database, database has tables and current table 
class WeatherUndergroundAPI:
	db = sqlInterface.Database("WUnderground.db")


	def __init__(self):
		print(self.db.name)
		print(str(datetime.datetime.now()) + "   api constructor")
		self.addPrediction()


	def addPrediction(self):
		year = data['hourly_forecast'][0]['FCTTIME']['year']
		month = data['hourly_forecast'][0]['FCTTIME']['mon']
		day = data['hourly_forecast'][0]['FCTTIME']['mday']
		hour = data['hourly_forecast'][0]['FCTTIME']['hour']
		minute = data['hourly_forecast'][0]['FCTTIME']['min']
		sec = data['hourly_forecast'][0]['FCTTIME']['sec']
		tableName = 'weatherUnderground_' + year + '_' + month + '_' + day + '_' + twoDigitNumber(hour) + minute

		try:
			table = self.db.addNewTable(tableName)
			for hr in range(0,36):
				# form arguments of prediction
				time = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + sec
				top = year + "-" + month + "-" + addHoursToTimeStamp(hr, int(day), int(hour)) + ":" + minute + ":" + sec
				cond = data['hourly_forecast'][hr]['condition']
				temp = float(data['hourly_forecast'][hr]['temp']['english'])
				hum = int(data['hourly_forecast'][hr]['humidity'])
				rainAmount = float(data['hourly_forecast'][hr]['qpf']['english'])
				pop = int(data['hourly_forecast'][hr]['pop'])
				wind = int(data['hourly_forecast'][hr]['wspd']['english'])

				prediction = sqlInterface.Prediction(time, top, cond, temp, hum, rainAmount, pop, wind)
				table.addRow(prediction)

		except:
			print(str(datetime.datetime.now()) +"  table operation")
			print(traceback.format_exc())

		
		
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
