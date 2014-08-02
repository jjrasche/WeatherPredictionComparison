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

# return a datetime initialized to noon on my birthday
def initializeDatetime():
    return(datetime.datetime(1988, 01, 23, 0, 0, 0, 0))

def strToDatetime(string):
    string = string.replace(" ", "-")
    return(time.strptime(string, "%Y-%m-%d-%H:%M:%S"))


''' assume tableName will be valid when any of the methods are called'''
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
        if (new == False):
            self.addAllExistingRows()
        else:
            self.createTable()
            self.addAllNewRows(data, date)


    def addAllExistingRows(self):
        # pull table data 
        cmd = "select * from " + self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        rows = sqlite3.connect(self.dbName).execute(cmd)
        for row in rows:
            self.rows.append(row)

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
        if(self.isNew): 
            cmd = "insert into "
            cmd += self.tableName
            cmd += " values ("
            if(self.tableType == "prediction"):
                cmd += "'"
                cmd += str(prediction.timeStamp)
                cmd += "', '"
                cmd += str(prediction.timeOfPrediction)
                cmd += "', '"
                cmd += str(prediction.condition)
                cmd += "', "
                cmd += str(prediction.temperature)
                cmd += ", "
                cmd += str(prediction.humidity)
                cmd += ", "
                cmd += str(prediction.rainAmount)
                cmd += ", "
                cmd += str(prediction.rainChance)
                cmd += ", "
                cmd += str(prediction.wind)
                cmd += ")"        
            if(self.printThis):
                print("sqlInterface:  " + cmd)
            sqlite3.connect(self.dbName).execute(cmd)
            self.commitChanges()


    ''' check for error, if is a "table already exists" error, then consume
        exception. This solves the problem of erroring out when testing '''
    def createTable(self):
        cmd = "create table "
        cmd += self.tableName
        cmd += " ("
        if(self.tableType == "prediction"):
            cmd += "timeStamp TEXT, "
            cmd += "timeOfPrediction TEXT, "
            cmd += "condition TEXT, temperature REAL, humidity INTEGER, "
            cmd += "rainAmount REAL, rainChance INTEGER, wind REAL)"
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        try:
            sqlite3.connect(self.dbName).execute(cmd)
            self.commitChanges()
        except:
            print(str(datetime.datetime.now()) +" table already created")
            print(traceback.format_exc()) 


    def deleteTable(self):
        cmd = "drop table "
        cmd += self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        sqlite3.connect(self.dbName).execute(cmd)
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
        rows = sqlite3.connect(self.dbName).execute(cmd)
        for row in rows:
            self.rows.append(row)

    def commitChanges(self):
        sqlite3.connect(self.dbName).commit()
        sleep(.3)
        if(self.printThis):
            print("sqlInterface:  commiting changes")

    '''  return list of strings that are tables in this table's database '''
    def getAllTablesinDb(self):
        cursor = sqlite3.connect(self.dbName).execute("SELECT name FROM sqlite_master WHERE type='table';")
        return(cursor.fetchall())



'''  3 ways around not having name information at time of class instantiation
    X    1) declare dummy instance of connection first then override when get name
    G    2) redeclare connection in every function that needs it 
        3) create subclasses of Database e.g. WU database that has name hardcoded  '''
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

    # add a new table to the tables list, return this table for caller to add rows to
    def addNewTable(self, prefix, data):
        print(type(data['hourly_forecast'][0]['FCTTIME']['min']))
        date = datetime.datetime(int(data['hourly_forecast'][0]['FCTTIME']['year']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mon']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mday']),
                     int(data['hourly_forecast'][0]['FCTTIME']['hour']),
                     int(data['hourly_forecast'][0]['FCTTIME']['min']))
        tableName = prefix + str(date.year) + '_' + str(date.month) + '_' + str(date.day) + '_' + str(twoDigitNumber(date.hour)) + str(date.minute)
        tmpTable = Table(tableName, "prediction", self.name, True, data, date) 
        self.tables.append(tmpTable)


    def getTableNames(self):
        cursor = sqlite3.connect(self.name).execute("SELECT name FROM sqlite_master WHERE type='table';")
        return(cursor.fetchall())



# open table from database and create 


# pred = Prediction(initializeDatetime(), initializeDatetime(), "none", 75.0, 60, 0.2, 10, 15)
class Prediction:
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
sqlite3.register_converter("point", convert_point)

        
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


