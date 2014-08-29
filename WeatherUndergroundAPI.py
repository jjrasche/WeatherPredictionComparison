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
import comparisonFunctions


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
print("in API")
goodData = False
# connext to API
try:
	data = requests.get(r'http://api.wunderground.com/api/30ee77078e4be97c/hourly/q/MI/Lansing.json').json()
	goodData = True
except:
	print(str(datetime.datetime.now()) + "   could not connect to network")
	print(traceback.format_exc())
	goodData = False
	#exit(0)

# API has a database, database has tables and current table 
class WeatherUndergroundAPI:
	db = sqlInterface.Database("WUnderground.db")

	def __init__(self):
		print(str(datetime.datetime.now()) + "   api constructor")
		if(goodData):
			predTable = self.addPrediction()
			print(predTable)
			if(predTable):
				comparisonFunctions.addNewStats(self.db, predTable)
		#comparisonFunctions.completeStatsTableBuild(self.db)



	def addPrediction(self):
		try:
			table = self.db.addNewTable("weatherUnderground", data)
			print(table.rows[0])
			return(table)
		except:
			print(str(datetime.datetime.now()) +"  table operation")
			print(traceback.format_exc())










