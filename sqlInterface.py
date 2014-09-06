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
import MySQLdb
# return a datetime initialized to noon on my birthday
def initializeDatetime():
    return(datetime.datetime(1988, 01, 23, 0, 0, 0, 0))

def strToDatetime(string):
    string = string.replace(" ", "-")
    return(time.strptime(string, "%Y-%m-%d-%H:%M:%S"))

def strToDt(string):
    return(datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S"))


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
        self.timeStamp = strToDt(str(time))
        # small modificaiton to make the stats table work
        if(type(top) == int):
            self.timeOfPrediction = top
        else:
            self.timeOfPrediction = strToDt(str(top))
        self.condition = cond
        self.temperature = temp
        self.humidity = hum
        self.rainAmount = rainAmount
        self.rainChance = pop
        self.wind = wind

    def __repr__(self):
        if(type(self.timeOfPrediction) == int):
            return "'%s', %d, '%s', %.1f, %d, %.1f, %d, %d" % (self.timeStamp, self.timeOfPrediction, self.condition, 
                                self.temperature, self.humidity, self.rainAmount, 
                                self.rainChance, self.wind)
        else:
            return "'%s', '%s', '%s', %.1f, %d, %.1f, %d, %d" % (self.timeStamp, self.timeOfPrediction, self.condition, 
                                            self.temperature, self.humidity, self.rainAmount, 
                                            self.rainChance, self.wind)


class Table:

    def __init__(self, tableName, tableType, db, new, data, date):
        self.printThis = True
        self.db = db
        self.tableName = tableName  
        self.isNew = new
        self.tableType = tableType
        self.rows = []
        self.isStatsTable = self.statsTableLogic(tableName)

        if (new == False):
            self.addAllExistingRows()
        else:
            self.createTable()
            self.addAllNewRows(data, date)
            self.commitChanges()


    def statsTableLogic(self, tableName):
        if(tableName == "stats"):
            return(True)
        return(False)

    def addAllExistingRows(self):
        print("adding table: " + self.tableName)
        try:
            # pull table data 
            cmd = "SELECT * FROM " + self.tableName + ";"
            cur = self.db.conn.cursor()
            cur.execute(cmd)
            predictions = cur.fetchall()
            for p in predictions:
                self.rows.append(Prediction(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7]))
        except:
            print(str(datetime.datetime.now()) +"  table operation")
            print(traceback.format_exc())


    def addAllNewRows(self, data, date):
        for hr in range(0,36):
            # form arguments of prediction
            time = str(date)
            top = str(date + datetime.timedelta(hours=hr))
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
        
        cmd = "INSERT INTO  " + self.tableName + " Values ("
        cmd +=  str(prediction) + ");"

        if(self.printThis):
            print("sqlInterface: " + cmd)
        self.db.conn.cursor().execute(cmd)
        #self.commitChanges()
        


    def createTable(self):
        cmd = "CREATE TABLE "
        cmd += self.tableName
        cmd +=    "(ts DATETIME NOT NULL,"
        cmd +=     "top DATETIME NOT NULL,"
        cmd +=     "cond VARCHAR(30) NOT NULL,"
        cmd +=     "temp FLOAT(5,1) NOT NULL,"
        cmd +=     "hum TINYINT NOT NULL,"
        cmd +=     "rainAmnt FLOAT(4,1) NOT NULL,"
        cmd +=     "rainChnc TINYINT NOT NULL,"
        cmd +=     "wind TINYINT NOT NULL);"
    
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        try:
            self.db.conn.cursor().execute(cmd)
            self.commitChanges()
        except:
            #print(str(datetime.datetime.now()) +" table already created")
            #print(traceback.format_exc()) 
            raise

    def deleteTable(self):
        cmd = "DROP TABLE "
        cmd += self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        self.db.conn.cursor().execute(cmd)
        self.commitChanges()

    def printTable(self):
        count = 0
        for row in self.rows:
            print(str(count) + "  " + str(row))
            count = count + 1
        return(count)

    def printTableFromDatabase(self):
        cmd = "select * from " + self.tableName
        if(self.printThis):
            print("sqlInterface:  " + cmd)
        cur = self.db.conn.cursor()
        cur.execute(cmd)
        rows = cur.fetchall()
        for row in rows:
            print(str(type(row[0])) + "    " + str(row))

    def commitChanges(self):
        self.db.conn.commit()
        #sleep(.3)
        if(self.printThis):
            print("sqlInterface:  commiting changes")


''' 
    - want to use a map rather than a list, to pull out a specific stats 'hour' table when I want to easier 
    - can't query sql arbitray objects stored using detect_types,  so will need to separate out the stats into tables based on hours
'''
class Database:

    def __init__(self, dbName):
        self.name = dbName
        self.conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                                    user="root", # your username
                                    passwd="password", # your password
                                    db="WUnderground") # name of the data base
        print(self.conn)
        self.dataTables = []
        self.statsTable = Table("stats", "prediction", self, False, None, None)
        self.loadTables()   # load tables


    def loadTables(self):
        nameList = self.getTableNames()
        print("type of nameList: " + str(type(nameList)))
        for name in nameList:
            if(name[0] == "stats"): continue
            self.dataTables.append(Table(name[0], "prediction", self, False, None, None))
            #self.dataTables[name] = Table(name[0], "prediction", self.name, False, None, None)

    def addNewTable(self, prefix, data):
        date = datetime.datetime(int(data['hourly_forecast'][0]['FCTTIME']['year']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mon']),
                     int(data['hourly_forecast'][0]['FCTTIME']['mday']),
                     int(data['hourly_forecast'][0]['FCTTIME']['hour']),
                     int(data['hourly_forecast'][0]['FCTTIME']['min']))
        tableName = prefix + str(date.year) + '_' + twoDigitNum(date.month) + '_' + twoDigitNum(date.day) + '_' + twoDigitNum(date.hour) +"00"
        tmpTable = Table(tableName, "prediction", self, True, data, date) 

        self.dataTables.append(tmpTable)
        print(tmpTable.rows[0])
        #self.dataTables[tableName] = tmpTable
        return(tmpTable)

    def getTableNames(self):
        cur = self.conn.cursor()
        cur.execute("SHOW TABLES;")
        return(cur.fetchall())


        
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

def createDatabaseWithOneTableForEachHour():
    con = sqlite3.connect("WUnderground_Stats.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    for num in range(1,36):
        cmd = "create table hour_"
        cmd += str(num)
        cmd += " (p Prediction)"

        print("sqlInterface:  " + cmd)
        cur.execute(cmd)


def createStatsTable():
    con = sqlite3.connect("WUnderground.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    cmd = "create table stats (p Prediction)"
    print("sqlInterface:  " + cmd)
    cur.execute(cmd)
    con.commit()

    con = sqlite3.connect("WUnderground.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    pred = Prediction(initializeDatetime(), initializeDatetime(), "none", 75.0, 60, 0.2, 10, 15)
    cmd = "insert into  stats (p) values (?)"
    print("sqlInterface: " + cmd)
    cur.execute(cmd, (pred,))
    con.commit()



'''


CREATE TABLE stats (ts DATETIME NOT NULL, 
                    ttp TINYINT NOT NULL,
                    cond VARCHAR(30) NOT NULL, 
                    temp DECIMAL(5,1) NOT NULL, 
                    hum TINYINT NOT NULL,
                    rainAmnt DECIMAL(4,1) NOT NULL,
                    rainChnc TINYINT NOT NULL,
                    wind TINYINT NOT NULL)



db = MySQLdb.connect(host="localhost",
                     user="root",
                      passwd="password",
                      db="jonhydb")


'''







'''  obsolete code

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

'''



