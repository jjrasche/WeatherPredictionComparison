'''
    All mutable variables in a class are shared with all instances of that class 
        >>> class A: foo = []
        >>> a, b = A(), A()
        >>> a.foo.append(5)
        >>> b.foo
        [5]
        >>> class A:
        ...  def __init__(self): self.foo = []
        >>> a, b = A(), A()
        >>> a.foo.append(5)
        >>> b.foo    
        []
    int and strings are not shared b/c they are inmutable
'''
import sqlite3
import datetime
import traceback
from time import sleep
import os

# return a datetime initialized to noon on my birthday
def initializeDatetime():
    return(datetime.datetime(1988, 01, 23, 0, 0, 0, 0))

def strToDatetime(string):
    string = string.replace(" ", "-")
    return(time.strptime(string, "%Y-%m-%d-%H:%M:%S"))


# pred = Prediction(initializeDatetime(), initializeDatetime(), "none", 75.0, 60, 0.2, 10, 15)
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
sqlite3.register_converter("Prediction", convert_point)


class Table:
    dbName = ""
    tableName = ""
    tableType = ""
    printThis = True
    isNew = False

    def __init__(self, tableName, tableType, dbName, new, data, date):
        self.dbName = dbName
        self.tableName = tableName  
        self.isNew = new
        self.tableType = tableType
        self.rows = []
        self.con = sqlite3.connect(dbName, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.con.cursor()
        if (new == False):
            self.addAllExistingRows()
        else:
            self.createTable()
            self.addAllNewRows(data, date)
            self.commitChanges()

    def addAllExistingRows(self):
        # pull table data 
        cmd = "select * from " + self.tableName
        predictions = self.cur.execute(cmd).fetchall()
        for pred in predictions:
            self.rows.append(pred[0])

    def addAllNewRows(self, data, date):
        for hr in range(0,36):
            # form arguments of prediction
            time = date
            top = date + datetime.timedelta(hours=hr)
            cond = data['hourly_forecast'][hr]['condition']
            temp = float(data['hourly_forecast'][hr]['temp']['english'])
            hum = int(data['hourly_forecast'][hr]['humidity'])
            rainAmount = float(data['hourly_forecast'][hr]['qpf']['english'])
            pop = int(data['hourly_forecast'][hr]['pop'])
            wind = int(data['hourly_forecast'][hr]['wspd']['english'])

            self.addRow(Prediction(time, top, cond, temp, hum, rainAmount, pop, wind))

    def addRow(self, prediction):
            # add to local row
        self.rows.append(prediction)
            # add to database if this is a new table
        cmd = "insert into " + self.tableName + "(p) values (?)"
        if(self.printThis):
            print("sqlInterface: " + cmd)
        self.cur.execute(cmd, (prediction,))

    def createTable(self):
        cmd = "create table "
        cmd += self.tableName
        cmd += " (p Prediction)"

        if(self.printThis):
            print("sqlInterface:  " + cmd)
        try:
            self.cur.execute(cmd)
            self.commitChanges()
        except:
            print(str(datetime.datetime.now()) +" table already created")
            print(traceback.format_exc()) 
            raise

    def deleteTable(self):
        cmd = "drop table "
        cmd += self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        self.cur.execute(cmd)
        self.commitChanges()

    def printTable(self):
        count = 0
        for row in self.rows:
            print(str(count) + str(row))
            count = count + 1
        return(count)

    def printTableFromDatabase(self):
        cmd = "select * from " + self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        rows = self.cur.execute(cmd).fetchall()
        for row in rows:
            print(str(type(row[0])) + "    " + str(row))

    def commitChanges(self):
        self.con.commit()
        sleep(.3)
        if(self.printThis):
            print("sqlInterface:  commiting changes")


class Database:
    name = ""
    tables = []

    def __init__(self, dbName):
        self.name = dbName
        self.loadTables()   # load tables

    def loadTables(self):
        nameList = self.getTableNames()
        for name in nameList:
            self.tables.append(Table(name[0], "prediction", self.name, False, None, None))

    def addNewTable(self, prefix, data):
        date = datetime.datetime(int(data['hourly_forecast'][0]['FCTTIME']['year']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mon']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mday']),
                     int(data['hourly_forecast'][0]['FCTTIME']['hour']),
                     int(data['hourly_forecast'][0]['FCTTIME']['min']))
        tableName = prefix + str(date.year) + '_' + twoDigitNum(date.month) + '_' + twoDigitNum(date.day) + '_' + twoDigitNum(date.hour) +"00"
        try:
            tmpTable = Table(tableName, "prediction", self.name, True, data, date) 
        except:
            return
        self.tables.append(tmpTable)

    def getTableNames(self):
        cursor = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES).execute("SELECT name FROM sqlite_master WHERE type='table';")
        return(cursor.fetchall())


        
def addHoursToTimeStamp(add_hours, day, hour):
    while((add_hours + hour) > 23):
        day += 1
        add_hours -= 24
    hour += add_hours
    return(str(day) + " " + str(hour))

def twoDigitNum(num):
    if(num < 10):
        return("0" + str(num))
    else:
        return(str(num))


