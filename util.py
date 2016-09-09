import math

def get_lvl(xp):
    xp = xp/1000.0
    if xp<1:
        return 0
    else:
        return int(math.log(xp,1.6))

def get_procent(lvl,xp):
    return int((100*xp)/(1000*((1.6)**lvl+1)))

def get_xp(userlvl,lvl):
    xp = 100*(10 + lvl-userlvl)/(10+userlvl)
    if xp<0:
        xp=0
    return xp