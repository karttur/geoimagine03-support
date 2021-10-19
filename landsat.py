'''
Created on 7 Oct 2018

@author: thomasgumbricht
'''

def ConvertLandsatScenesToStr(pr):
    ''' Convert wrs path and row to a standardized string
    '''
    if pr[0] < 10:
        pathStr = 'p00%(p)d' %{'p': pr[0]}
    elif pr[0] < 100:
        pathStr = 'p0%(p)d' %{'p': pr[0]}
    else:
        pathStr = 'p%(p)d' %{'p': pr[0]}
    if pr[1] < 10:
        rowStr = 'r00%(r)d' %{'r': pr[1]}
    elif pr[1] < 100:
        rowStr = 'r0%(r)d' %{'r': pr[1]}
    else:
        rowStr = 'r%(r)d' %{'r': pr[1]}
    pathrowStr = '%(p)s%(r)s' %{'p':pathStr,'r':rowStr}
    prpath = '%(p)s/%(r)s' %{'p':pathStr,'r':rowStr}
    values = [pr[0], pr[1], pathStr, rowStr, pathrowStr, prpath]
    
    params = ['p','r','pstr','rstr','prstr','prpath']
    D = dict(zip(params,values))
    return D
