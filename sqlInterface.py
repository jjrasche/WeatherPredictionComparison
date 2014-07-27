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
    dbName = "WUnderground.db"
    tableName = "none"
    tableType = "none"
    connection = sqlite3.connect(dbName)
    printThis = 0

    '''  if created without a valid tablename, then don't add a tablename, 
        if created without a valid db then exit
    '''
    def __init__(self, tableName, dbName):
        if(dbName == ""):
            print("db name invalid")
            exit(1)
        else:
            self.dbName = dbName

        if(tableName != ""):                
            self.tableName = tableName      # if tablename is valid set it otherwise wait 

    def insertRow(self, row):
        self.checkValidtableName()
        command = "insert into "
        command += self.tableName
        command += " values ("
        if(self.tableType == "prediction"):
            command += "'"
            command += str(row.timeStamp)
            command += "', '"
            command += str(row.timeOfPrediction)
            command += "', '"
            command += str(row.condition)
            command += "', "
            command += str(row.temperature)
            command += ", "
            command += str(row.humidity)
            command += ", "
            command += str(row.rainAmount)
            command += ", "
            command += str(row.rainChance)
            command += ", "
            command += str(row.wind)
            command += ")"        
        if(self.printThis):
            print("sqlInterface:  " + command)
        self.connection.execute(command)

    ''' check for error, if is a "table already exists" error, then consume
        exception. This solves the problem of erroring out when testing '''
    def createTable(self):
        self.checkValidtableName()
        command = "create table "
        command += self.tableName
        command += " ("
        if(self.tableType == "prediction"):
            command += "timeStamp TEXT, "
            command += "timeOfPrediction TEXT, "
            command += "condition TEXT, temperature REAL, humidity INTEGER, "
            command += "rainAmount REAL, rainChance INTEGER, wind REAL)"
        if(self.printThis):
            print("sqlInterface:  " + command)
        self.connection.execute(command)

    def deleteTable(self):
        self.checkValidtableName()
        command = "drop table "
        command += self.tableName
        if(self.printThis):
            print("sqlInterface:  " + command)
        self.connection.execute(command)

    def printTable(self):
        self.checkValidtableName()
        command = "select * from "
        command += self.tableName
        if(self.printThis):
            print("sqlInterface:  " + command)
        c = self.connection.execute(command)
        for row in c:
            Prediction.printRow(row)

    def checkValidtableName(self):
        if(self.tableName == "none"):
            return(False)
        return(True)

    def commitChanges(self):
        sleep(.5)
        self.connection.commit()
        if(self.printThis):
            print("sqlInterface:  commiting changes")
        sleep(.5)

    def listTablesinDb(self):
        cursor = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(type(cursor))
        print(cursor.fetchall())




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
        
    def printPrediction(self):
        print("time: " + str(self.timeStamp))
        print("top: " + str(self.timeOfPrediction))
        print("cond: " + self.condition)
        print("temp: " + str(self.temperature))
        print("hum: " + str(self.humidity))
        print("rain: " + str(self.rainAmount))
        print("pop: " + str(self.rainChance))
        print("wind: " + str(self.wind))

    @staticmethod
    def printRow(row):
        print("(" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + \
            str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]) + ", " + str(row[6]) + \
            ", " + str(row[7]) + ")")


