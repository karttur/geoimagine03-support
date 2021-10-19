'''
Created on 27 apr. 2018

@author: thomasgumbricht
'''

from math import floor

# Package application imports

from geoimagine.support import karttur_dt as mj_dt


def ConvertXYstring(xy):
    ''' Convert EASE grid xtile / ytile to a standardized string
    '''
    if xy[0] < 10:
        pathStr = 'x0%(x)d' %{'x': xy[0]}
    else:
        pathStr = 'x%(x)d' %{'x': xy[0]}
        
    if xy[1] < 10:
        rowStr = 'y0%(y)d' %{'y': xy[1]}
    else:
        rowStr = 'y%(y)d' %{'y': xy[1]}
    pathrowStr = '%(x)s%(y)s' %{'x':pathStr,'y':rowStr}
    values = [xy[0], xy[1], pathStr, rowStr, pathrowStr]
    params = ['p','r','pstr','rstr','prstr']
    D = dict(zip(params,values))
    return D

def ConvertXYinteger(x,y):
    ''' Convert EASEGRID xtile / ytile to a standardized string
    '''
    if x < 10:
        pathStr = 'x0%(x)d' %{'x': x}
    else:
        pathStr = 'x%(x)d' %{'x': x}
    if y < 10:
        rowStr = 'y0%(y)d' %{'y': y}
    else:
        rowStr = 'y%(y)d' %{'y': y}
        
    pathrowStr = '%(x)s%(y)s' %{'x':pathStr,'y':rowStr}
    
    values = [x, y, pathStr, rowStr, pathrowStr]
    
    params = ['p','r','pstr','rstr','prstr']
    
    D = dict(zip(params,values))
    
    return D
    
    
def EaseGridNcoordToTile(x,y):   
    ''' Find Ease-GRID north tile for given coordinate
    '''   
    # ease2n edges
    minx = miny = -9000000
    
    #maxx = maxy = -9000000
    
    # ease2n extent
    xlength = ylength = 9000000*2
    
    # ease2n nr of tiles
    xtiles = 20
    
    ytiles = 20
    
    
    # ease2n tile for coordinate point
    ease2nxtile = floor( xtiles * (x-minx) / xlength )
    
    ease2nytile = floor( ytiles * (y-miny) / ylength )
    
    return (ease2nxtile, ease2nytile)
        
    
