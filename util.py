import math

def get_lvl(xp):
    xp = xp/1000.0
    if xp<1:
        return 0
    else:
        return int(math.log(xp,1.6))

def get_procent(lvl,xp):
    xp_to_lvl = int(1000*((1.6)**(lvl+1)))
    xp_lvl = 0

    if lvl >0:
        xp_lvl = (1000*((1.6)**lvl))
    lvl_xp = 1
    if xp>0:
        lvl_xp = round(xp-xp_lvl,1)
        if lvl_xp <=0:
            lvl_xp=1
    p = int(100/((xp_to_lvl-xp_lvl)/lvl_xp))
    return p

def get_xp(userlvl,lvl):
    xp = 20*(10 + lvl-userlvl)/(10+userlvl)
    if xp<0:
        xp=0
    return xp