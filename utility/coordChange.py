# -*- coding: utf-8 -*-
import math

def deg2val(deg):
    du =deg[:deg.find('°')]
    fen =deg[deg.find('°') +2 :deg.find('\'')]
    miao =deg[deg.find('\'') +1 :deg.find('\"')]

    return float(du) +float(fen)/60 +float(miao)/3600

def val2deg(val):
    du =int(val)
    val =(val -du) *60
    fen =int(val)
    miao =int((val -fen) *60)

    return "%d°%d\'%d\"" % (du ,fen ,miao)



def ln2px(ln):
    return (ln +180) *256 /360

def lt2py(lt):
    siny =math.sin(lt *math.pi /180)
    y =math.log((1+siny)/(1-siny))
    return 128 *(1 -y/(2 *math.pi))

def px2ln(px):
    return px *360 /256 -180

def py2lt(py):
    latRadians =(py -128)/-(256/(2 *math.pi))
    lt =2 *math.atan(math.exp(latRadians)) -math.pi /2
    return lt *180 /math.pi

def ltperpx(zoom):
    return 180.0/math.pow(2 ,zoom)/256.

def lnperpx(zoom):
    return 360.0/math.pow(2 ,zoom)/256



