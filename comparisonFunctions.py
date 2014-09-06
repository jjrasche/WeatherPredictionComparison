import datetime
import sqlInterface


'''  given a prediction and the reality, return a statistical analysis '''
def predarePrediction(prediction, groundTruth):
	return True


def completeStatsTableBuild(db):
	for observTable in db.dataTables:
		addNewStats(db, observTable)




def addNewStats(db, observTable):
	for predTable in db.dataTables:
		print(predTable.tableName + "   " + observTable.tableName)
		diff = timeDiff(observTable.rows[0], predTable.rows[0])

		if (0 < diff and diff < 36):
			pred = predTable.rows[diff]
			comp = getDiffBtwnPredictions(observTable.rows[0], pred)
			#print(str(observTable.rows[0]) + "    " + str(pred) + "    " + str(timeDiff))
			#print(comp)
			db.statsTable.addRow(comp)
	db.statsTable.commitChanges()







# return a prediction that is the
# Prediction(None, timeDiff, points_diff, degrees_diff, percent_diff, rain_amount_diff, percent_diff, mph_diff)
# pred = Prediction(initializeDatetime(), initializeDatetime(), "none", 75.0, 60, 0.2, 10, 15)
def getDiffBtwnPredictions(observ, pred):
	print(str(observ) + "   " + str(type(observ.temperature)))
	print(str(pred) + "   " + str(type(pred.temperature))) 
	return(sqlInterface.Prediction(observ.timeStamp,
						timeDiff(pred, observ),
						difInCondition(pred,observ),
						(pred.temperature - observ.temperature),
						(pred.humidity - observ.humidity),
						(pred.rainAmount - observ.rainAmount),
						(pred.rainChance - observ.rainChance),
						(pred.wind - observ.wind)
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


def difInCondition(observ, pred):
	return(condToInt(observ.condition) - condToInt(pred.condition))


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
def timeDiff(observ, pred):
	hours = 0
	tDelta = observ.timeStamp - pred.timeStamp
	#print(observ.timeStamp + "   " + pred.timeStamp + "    tDelta: " + str(tDelta))

	changeAmount = 0
	deltaDays = tDelta.days
	hours += tDelta.seconds/3600
	if(deltaDays >= 0):			# positive amount of time
		changeAmount = 1
	else:
		changeAmount = -1

	while(deltaDays != 0):
		hours += changeAmount*24
		deltaDays -= changeAmount
	return(hours)

