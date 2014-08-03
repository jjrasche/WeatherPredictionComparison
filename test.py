import sqlite3
import datetime
import traceback
from time import sleep

# return a datetime initialized to noon on my birthday
def initializeDatetime():
    return(datetime.datetime(1988, 01, 23, 0, 0, 0, 0))

def strToDatetime(string):
    string = string.replace(" ", "-")
    return(time.strptime(string, "%Y-%m-%d-%H:%M:%S"))


class Prediction(object):
	timeStamp = initializeDatetime()            # datetime
	timeOfPrediction = initializeDatetime()     # datetime
	condition = "none"                          # (sunny, cloudy, partly cloudy, overcast, thunderstorms, snowing)
	temperature = 0.0                           # degrees farenheit
	humidity = 0                                # percent
	rainAmount = 0.0                            # in
	rainChance = 0                              # percent
	wind = 0.0                                  # mph
	
	def __init__(self, time, top, cond, temp, hum, rainAmount, pop, wind):
		self.timeStamp = time
		self.timeOfPrediction = top
		self.condition = cond
		self.temperature = temp
		self.humidity = hum
		self.rainAmount = rainAmount
		self.rainChance = pop
		self.wind = wind

	def __repr__(self):
		return "%s;%s;%s;%f;%d;%f;%d;%d" % (self.timeStamp, self.timeOfPrediction, self.condition, 
										self.temperature, self.humidity, self.rainAmount, 
										self.rainChance, self.wind)

def adapt_point(pred):
	return "%s;%s;%s;%f;%d;%f;%d;%d" % (pred.timeStamp, pred.timeOfPrediction, pred.condition, 
										pred.temperature, pred.humidity, pred.rainAmount, 
										pred.rainChance, pred.wind)

def convert_point(s):
	time, top, cond, temp, hum, rainAmount, pop, wind = s.split(";")
	return Prediction(time, top, cond, float(temp), int(hum), float(rainAmount), int(pop), int(wind))

# Register the adapter and converter
sqlite3.register_adapter(Prediction, adapt_point)
sqlite3.register_converter("doesn't matter", convert_point)

pred = Prediction(initializeDatetime(), initializeDatetime(), "awe", 7.0, 60, 0.2, 10, 15)
pred1 = Prediction(initializeDatetime(), initializeDatetime(), "snap", 7.0, 60, 0.2, 10, 15)

#########################
# 1) Using declared types
con = sqlite3.connect("test3.db", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

createCmd = "create table test(pred)"
try:
	cur.execute(createCmd)
except:
	cur.execute("drop table test")
	cur.execute(createCmd)


# stores p into test derived from pred, 
cur.execute("insert into test(pred) values (?)", (pred,))
cur.execute("insert into test(pred) values (?)", (pred1,))

cur.execute("select * from test")
#print "with declared types:", cur.fetchone()[0]
#need to copy to another variable right away, can only do one operation on the cursor
x = cur.fetchall()
print(type(x))
print(x)



