from splinter import Browser
import threading,json,random,re,time


#funciton summary
#strip string and get value

#soilderType array is used to describ how many resource to use
soilderType = {
    'legionnaire' : [120, 100, 150, 30],
    'Praetorian' : [100, 130, 160, 70]
}



print soilderType['legionnaire'][0]
