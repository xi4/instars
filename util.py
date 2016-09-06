import datetime
import math


def time_left():

    nowtime = datetime.datetime.now()
    newtime = datetime.datetime.now()+datetime.timedelta(minutes=2)
    time = (newtime-nowtime).total_seconds()
    print newtime-nowtime
    mins = 60
    hour = 60*60

    r_hour = math.floor(time/hour)
    r_min = math.floor((time-(r_hour*hour))/mins)
    r_sec = ((time -(r_hour  * hour) - (r_min * mins)))

    print str(r_hour)+":

