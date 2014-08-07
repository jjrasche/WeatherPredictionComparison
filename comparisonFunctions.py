import datetime
import sqlInterface


'''  given a prediction and the reality, return a statistical analysis '''
def comparePrediction(prediction, groundTruth):
	return True


def completeStatsTableBuild(db):
	# for all tables in database
	for baseTable in db.tables:
		baseTime = strToDt(baseTable.rows[0].timeStamp)
		for compTable in db.tables:
			compTime = strToDt(compTable.rows[0].timeStamp)
			if(baseTime > compTime):
				diffInTableTime = timeDiff(baseTable.rows[0], compTable.rows[0])
				if(diffInTableTime < 36):
					pred = compTable.rows[diffInTableTime]
					print(str(baseTable.rows[0]) + "    " + str(pred) + "    " + str(diffInTableTime))
					print(getDiffBtwnPredictions(baseTable.rows[0], pred))


	# extract current weather from table

	# extract prediciton from previous 36 hours of table

	# do comparison

	# add comparison to appropriate stats table 


# return a prediction that is the
# Prediction(None, timeDiff, points_diff, degrees_diff, percent_diff, rain_amount_diff, percent_diff, mph_diff)
# pred = Prediction(initializeDatetime(), initializeDatetime(), "none", 75.0, 60, 0.2, 10, 15)
def getDiffBtwnPredictions(base, comp):
	return(sqlInterface.Prediction(None,
						timeDiff(base, comp),
						difInCondition(base,comp),
						(base.temperature - comp.temperature),
						(base.humidity - comp.humidity),
						(base.rainAmount - comp.rainAmount),
						(base.rainChance - comp.rainChance),
						(base.wind - comp.wind)
					)
			)

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
def difInCondition(base, comp):
	return(condToInt(base.condition) - condToInt(comp.condition))


def condToInt(cond):
	if(cond == "Clear" or cond == "Sunny"): 
		return(0)
	elif(cond == "Scattered Clouds" or cond == "Mostly Sunny" or cond == "Partly Cloudy"):
		return(1)
	elif(cond == "Mostly Cloudy" or cond == "Partly Sunny"):
		return(2)
	elif(cond == "Overcast" or cond == "Cloudy" or cond == "Fog" or cond == "Haze"):
		return(3)
	elif(cond == "Chance of Rain" or cond == "Chance of Freezing Rain" or cond == "Chance of Sleet" or cond == "Chance of Snow"):
		return(4)
	elif(cond == "Rain" or cond == "Freezing Rain" or cond == "Sleet" or cond == "Flurries" or cond == "Snow"):
		return(5)
	elif(cond == "Chance of a Thunderstorm"):
		return(6)
	elif(cond == "Thunderstorm"):
		return(7)
	else:
		raise Exception(cond + " is not a valid condition")
		print(cond + " is not a valid condition")


'''  iterate through entries in a statistics table and do analysis on each parameter '''
def analyzeStatsTable():
	return True

'''  return number of hours between datetimes '''
def timeDiff(base, comp):
	hours = 0
	deltaDays = strToDt(base.timeStamp) - strToDt(comp.timeStamp).days
	hours += tDelta.seconds/3600
	while(deltaDays > 0):
		hours += 24
		deltaDays -= 1
	return(hours)




def strToDt(string):
	return(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S"))
