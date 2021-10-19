'''
Created on 27 apr. 2018

@author: thomasgumbricht
'''

# Package application imports

from geoimagine.support import karttur_dt as mj_dt

def ConvertHVstring(hv):
    ''' Convert MODIS htile / vtile to a standardized string
    '''
    if hv[0] < 10:
        pathStr = 'h0%(h)d' %{'h': hv[0]}
    else:
        pathStr = 'h%(h)d' %{'h': hv[0]}
    if hv[1] < 10:
        rowStr = 'v0%(v)d' %{'v': hv[1]}
    else:
        rowStr = 'v%(v)d' %{'v': hv[1]}
    pathrowStr = '%(h)s%(v)s' %{'h':pathStr,'v':rowStr}
    values = [hv[0], hv[1], pathStr, rowStr, pathrowStr]
    params = ['p','r','pstr','rstr','prstr']
    D = dict(zip(params,values))
    return D

def ConvertHVinteger(h,v):
    ''' Convert MODIS htile / vtile to a standardized string
    '''
    if h < 10:
        pathStr = 'h0%(h)d' %{'h': h}
    else:
        pathStr = 'h%(h)d' %{'h': h}
    if v < 10:
        rowStr = 'v0%(v)d' %{'v': v}
    else:
        rowStr = 'v%(v)d' %{'v': v}
        
    pathrowStr = '%(h)s%(v)s' %{'h':pathStr,'v':rowStr}
    
    values = [h, v, pathStr, rowStr, pathrowStr]
    
    params = ['p','r','pstr','rstr','prstr']
    
    D = dict(zip(params,values))
    
    return D

def DisentangleModisTileName(modisFN):
    '''
    '''
    product, AdatumDoy, hvstr, version, id = modisFN.split('.')
    datumDoy = AdatumDoy.replace('A','')
    source = '%(p)sv%(v)s' %{'p':product, 'v':version}
    #year = int(datum[0:4])
    doy = int(datumDoy[4:7])
    acqdate = mj_dt.yyyydoyDate(datumDoy)
    return(source, product, version, hvstr, acqdate, doy)
    
    
            
    
