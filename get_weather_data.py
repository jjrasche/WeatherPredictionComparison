from time import sleep
#sleep(30)
import WeatherUndergroundAPI
api = WeatherUndergroundAPI.WeatherUndergroundAPI()


'''
functionality to record statistics
- want it to persist, as evaluating a huge numer of tables each time is infeasible
- keep track of table names
 
option 1)   reprocess the tables to validate the prediciton and add statistics data
            for a particular prediction 
                - iterate over tables statistics data to assemble long term stats
            - benefit = have long term data that only need to read from to redo overall stats

option 2)   every new entry sparks looking at the previous  36 entries to add to the overall
            stats model.
            - have two operations, (recalc all stats) and add (new readings stats to model)

            - functions
            	- comparePredictions


What the stats table looks like
- option 1)		a table for each prediciton hour range [1-36] hours. Add an entry to this table 
				for each prediction comparison. To aggregate stats, pull-up table and find stats metrics



Graphical stats representation = mean is the middle, each incremental inaccuracy is tallyed and represented as
								 a bar graph 
    def __init__(self, time, top, cond, temp, hum, rainAmount, pop, wind):
	- temperateure degrees double ~(-30 - 110)
	- cond * enum
	- hum percent int (0 - 100)
	- rainAmount inches double
	- pop percent int (0 - 100)
	- wind speed double ~(0 - 150)
                
'''

'''		*
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
