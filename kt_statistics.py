'''
Created on 19 mar 2019

@author: thomasg

Copied from mj_statistics_v30.py
'''

#
#imports
from __future__ import division
#from math import ceil, sqrt
import numpy as np
from scipy import linalg
import array as arr
#from scipy import linalg
_description = 'Script written by Thomas Gumbricht for statistical calculations'
_programV="kt_ttatistics.py"
_copyright =""
_producer ="Thomas Gumbricht"
_contact ="thomas dot  gumbricht  at gmail.com"
_organization = "MapJourney"
_address = ""
_url ="www.mapjourney.com"

def MapRely(x): 
    if x == _null: return(1)
    else: return(0)

def ForceFillTimeSeries(indexInList,nullVal):
    #create a new indexlist with expanded head and trail
    global _null
    _null = nullVal      
    relyInList = map(MapRely,indexInList)    
    weightList = arr.array('B',(4,)*(len(indexInList))) 
    #if max(relyInList) == 0, all input values are OK, just return the original list
    if max(relyInList) == 0: 
        return(indexInList, weightList)    
    steps = len(indexInList)      
    indexOut = indexInList[:]
    for i in range(steps):            
        if (indexInList[i] == nullVal): 
            #set the start and stop points of the array to use for filling this particular point
            startStep = max([0,i-steps])
            endStep = min([steps,i+steps+1])
            preIndexArray = indexInList[startStep:i] 
            preIndexArray.reverse()
            postIndexArray = indexInList[i+1:endStep]
            preRelyArray = relyInList[startStep:i] 
            preRelyArray.reverse()
            postRelyArray = relyInList[i+1:endStep]    
            try:
                preIndex = preRelyArray.index(0)
            except ValueError:
                preIndex = -1 # no match
            try:
                postIndex = postRelyArray.index(0)
            except ValueError:
                postIndex = -1 # no match
            if (postIndex == -1 and preIndex == -1):
                indexOut[i] = nullVal
                weightList[i] = 0
            elif preIndex == -1:
                indexOut[i] = postIndexArray[postIndex]
                weightList[i] = 1
            elif postIndex == -1:
                indexOut[i] = preIndexArray[preIndex]
                weightList[i] = 1                    
            else: 
                weightList[i] = 2
                indexOut[i] = (preIndexArray[preIndex]*(postIndex+1)+postIndexArray[postIndex]*(preIndex+1))/(preIndex+postIndex+2)
    return(indexOut, weightList)

def MapCopy(i):
    return i

def ForceFillTimeSeriesPhen(indexInList,nullVal):
    #create a new indexlist with expanded head and trail
    #print indexInList
    import array as fisk
    global _null
    _null = nullVal      
    relyInList = map(MapRely,indexInList)    
    weightList = fisk.array('B',(4,)*(len(indexInList))) 
    #if max(relyInList) == 0, all input values are OK, just return the original list
    if max(relyInList) == 0: 
        return(indexInList, 0)
     
    steps = len(indexInList)  
    maxSteps = len(indexInList)
    relyInList = map(MapRely,indexInList)    
    indexOut = map(MapCopy,indexInList)
       
    nrFill = 0
    for i in range(steps):            
            if (indexOut[i] == nullVal):
                nrFill += 1 
                #set the start and stop points of the array to use for filling this particular point
                startStep = max([0,i-maxSteps])
                endStep = min([steps,i+maxSteps+1])
                preIndexArray = indexOut[startStep:i] 
                preIndexArray.reverse()
                postIndexArray = indexOut[i+1:endStep]
                preRelyArray = relyInList[startStep:i] 
                preRelyArray.reverse()
                postRelyArray = relyInList[i+1:endStep]    
                try:
                    preIndex = preRelyArray.index(0)
                except ValueError:
                    preIndex = -1 # no match
                try:
                    postIndex = postRelyArray.index(0)
                except ValueError:
                    postIndex = -1 # no match
                if (postIndex == -1 and preIndex == -1):
                    indexOut[i] = nullVal
                    weightList[i] = 0
                elif preIndex == -1:
                    indexOut[i] = postIndexArray[postIndex]
                    weightList[i] = 1
                elif postIndex == -1:
                    indexOut[i] = preIndexArray[preIndex]
                    weightList[i] = 1                    
                else: 
                    weightList[i] = 2
                    indexOut[i] = (preIndexArray[preIndex]*(postIndex+1)+postIndexArray[postIndex]*(preIndex+1))/(preIndex+postIndex+2)
    return indexOut, nrFill

def LOESS(xArray, yArray, wArray):    
    import array as fisk
    timesteps = len(xArray)
    distance = fisk.array('h',(0,)*7)
    weight = fisk.array('f',(0,)*(timesteps))
    tsVloess = fisk.array('h',(0,)*23)
    for iPoint in range(4, 27):
            iMin = iPoint-3
            iMax = iPoint+4
            xNow = xArray[iPoint] 
            #print 'xnow', xNow           
            for i in range(iMin, iMax):
                distance[i-iMin] = abs(xArray[i]-xNow); 
                #print i-iMin, xArray[i-iMin]
            #print 'distances',distance
            maxDist = max(distance)+4
            for i in range(iMin, iMax):
                triple = pow((distance[i-iMin]/maxDist), 2)
                weight[i] = wArray[i]*pow(1-triple,2)
            #print "weigths",weight[iMin:iMax]
            SumWts= 0; SumWtX = 0;SumWtX2 = 0;SumWtY = 0;SumWtXY = 0;
            #print xNow
            for i in range (iMin, iMax):
                SumWts += weight[i];
                SumWtX += xArray[i]*weight[i];
                SumWtX2 += xArray[i]*xArray[i]*weight[i];
                SumWtY += yArray[i] *weight[i];
                SumWtXY += xArray[i]*yArray[i]*weight[i];
            denom = SumWts*SumWtX2-SumWtX*SumWtX
            WLRSlope = ((SumWts*SumWtXY) - (SumWtX*SumWtY))/ denom;
            WLRIntercept = ((SumWtX2*SumWtY) - (SumWtX * SumWtXY))/ denom;
            tsVloess[iPoint-4] = int(WLRSlope*xNow+ WLRIntercept)
    return(tsVloess)

def loessTG(x, y, delta, r):
    '''
    '''
    x = np.asarray(x)
    y = np.asarray(y)
    delta = np.asarray(delta)
    n = len(x)
    h = [np.sort(np.abs(x - x[i]))[r] for i in range(n)]
    w = np.clip(np.abs((x[:,None] - x[None,:]) / h), 0.0, 1.0)
    w = (1 - w**3)**3
    #w = (1 - w**0.5)**0.5
    yest = np.zeros(n)
    for i in range(n):
        weights = delta * w[:,i]
        b = np.array([np.sum(weights*y), np.sum(weights*y*x)])
        A = np.array([[np.sum(weights), np.sum(weights*x)],
              [np.sum(weights*x), np.sum(weights*x*x)]])
        if np.isnan(np.sum(A)):
            yest[i] = x[i]
        else:
            beta = linalg.solve(A, b)
            yest[i] = beta[0] + beta[1]*x[i] 
    return yest.tolist()

def XSD(vals):
    from math import sqrt
    n, mean, std = len(vals), 0, 0
    for a in vals:
        mean = mean + a
    mean = mean / float(n)
    for a in vals:
        std = std + (a - mean)**2
    std = sqrt(std / float(n-1))
    return mean, std

def AssimilateStatsL(X,Ystats,Xstats):
    assimL = list()
    for x in X:
        a = x - Xstats[0]
        b = abs(Ystats[1])/abs(Xstats[1])
        c = Ystats[0]
        m = a*b+c
        assimL.append(m)        
    return assimL

def AssimilateFactors(X,Ystats,Xstats):
    subtract = Xstats[0]
    add = Ystats[0]
    multiply = abs(Ystats[1])/abs(Xstats[1])
    return (subtract,add,multiply)
    
def Assimilate(arr):
    assimL = list()
    for i in arr:
        m = (i-subtract)*multiply+add
        assimL.append(m) 
    return assimL
        
def AssimilateStatsSingle(x,Ystats,Xstats):
    a = x - Xstats[0]
    b = abs(Ystats[1])/abs(Xstats[1])
    c = Ystats[0]
    m = a*b+c
    return m

def Standardize(X):
    xsdStats = XSD(X)
    zList = list()
    for x in X:
        a = x - xsdStats[0]
        m = a/xsdStats[0]
        zList.append(m)
    return zList

def RemoveMean(XL):
    m,sd = XSD(XL)
    #min = min(XL)
    xmL = []
    for x in XL:
        xmL.append(x-m)  
    return xmL

def median(mylist):
    sorts = sorted(mylist)
    length = int(len(sorts))
    if not length % 2:
        l = int( length / 2 )
        return (sorts[l] + sorts[l - 1]) / 2.0
    return sorts[int(length / 2)]

def RemoveMedian(XL):
    #print XL
    m = median(XL)
    #print 'm',m
    xmL = []
    for x in XL:
        xmL.append(x-m)  
    return xmL

def AssimilateXSD(XL,YL):
    if min(XL) == max(XL):
        return False
    Xstats = XSD(XL)
    Ystats = XSD(YL)
    assimL = list()
    '''
    for twi in X:
        twiX = (twi-twiStats[0])/(twiStats[1])
        twiY = twiX*(SMstats[1])+SMstats[0]
        twiN.append(twiY) 
    '''
    #From article, to check
    for x in XL:
        a = x - Xstats[0]
        b = abs(Ystats[1])/abs(Xstats[1])
        c = Ystats[0]
        m = a*b+c
        assimL.append(m)        
    return assimL

def FloatingMean(yArray, wArray, addons):    
    import array as fisk
    timesteps = len(yArray)
    mean = fisk.array('f',(0,)*(timesteps))   
    for iPoint in range(timesteps):
        total = 0
        iMin = max([iPoint-3,0])
        iMax = min([iPoint+4,timesteps])
        for i in range(iMin,iMax):
            total += wArray[i]*yArray[i]        
        summa = sum(wArray[iMin:iMax])        
        mean[iPoint] = total/summa
    return(mean)

def Linreg(X,Y):
    """
    Summary
        Linear regression of y = ax + b
    Usage
        real, real, real = linreg(list, list)
    Returns coefficients to the regression line "y=ax+b" from x[] and y[], and R^2 Value
    """
    #if len(X) != len(Y):  raise ValueError, 'unequal length'
    N = len(X)
    Sx = Sy = Sxx = Syy = Sxy = 0.0
    for x, y in map(None, X, Y):
        Sx = Sx + x
        Sy = Sy + y
        Sxx = Sxx + x*x
        Syy = Syy + y*y
        Sxy = Sxy + x*y
    det = Sxx * N - Sx * Sx
    a, b = (Sxy * N - Sy * Sx)/det, (Sxx * Sy - Sx * Sxy)/det
    meanerror = residual = RMSD = bias = 0.0
    for x, y in map(None, X, Y):
        meanerror = meanerror + (y - Sy/N)**2
        residual = residual + (y - a * x - b)*(y - a * x - b)
        RMSD += (y - (a * x + b))**2
        bias += (y - (a * x + b))
    bias /= len(X)
    RR = 1 - residual/meanerror
    residual = sqrt(residual/len(X))
    RMSD /= len(X)
    RMSD = sqrt(RMSD)
    return (RR,a,b,RMSD,residual,meanerror,bias)

def RMSE(X,Y):
    #if len(X) != len(Y):  raise ValueError, 'unequal length'
    N = len(X)
    meanerror = 0.0
    for x, y in map(None, X, Y):
        meanerror = meanerror + (y - x)**2

    RMSD = meanerror/N
    RMSD = sqrt(RMSD)
    return (RMSD)

def NashSutclif(M,Q):
    # Get the average of the measured Q
    Qm = sum(Q)/len(Q)
    #get sum of the squared difference in modeled and measured for each recording:
    sumQdiff = 0
    for x, q in enumerate(Q):
        Qdiff = Q[x] - M[x]
        Qdiff *= Qdiff
        sumQdiff += Qdiff
    #get sum of the squared difference in measured versus average measured for each recording:
    sumQdiffChance = 0
    for q in Q:
        Qdiff = q - Qm
        Qdiff *= Qdiff
        sumQdiffChance += Qdiff
    #Get the model efficiency
    E = 1 - (sumQdiff/sumQdiffChance)
    return E

if __name__ == "__main__":
    
    trueTimeSerie = [0,1,2,3,6,3,2,1,0]
    testTimeSeries = [1,2,2,4,2,1,1,0,0]
    testTimeSeries = [0,2,4,6,12,6,4,2,0]
    filterA = np.array([0.33,0.33,0.33])
    testA =np.array(testTimeSeries)
    testTS = np.convolve(testA, filterA, mode='same')
    print (testTS)
    testA = np.lib.pad(testA, (1, 1), 'wrap')
    testTS = np.convolve(testA, filterA, mode='valid')
    print (testTS)
    SNULLE
    trueStats = XSD(trueTimeSerie)
    testStats = XSD(testTimeSeries)
    print (trueTimeSerie)
    print (testTimeSeries)
                         
    # Assimilate the original data
    assMatchXT = AssimilateStatsL(testTimeSeries,trueStats,testStats) 
    print (assMatchXT)
    
    subtract,add,multiply = AssimilateFactors(testTimeSeries,trueStats,testStats)
    assGlobal = Assimilate(testTimeSeries)
    print (assGlobal)
    SNULLE
    # Assimilate the smoothed data
    #assSmoothXT = AssimilateStatsL(yMatchModL,yStats,xSmoothStats) 
    # Assimilate the smoothed and filled data
                                    
                                    
    smL = [-99.9, -99.9, -99.9, -99.9, -99.9, -99.9, 0.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    print (ForceFillTimeSeries(smL,-99.9)[1])
    pass