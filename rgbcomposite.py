
import numpy as np
import gdal
import geoimagine.gis.mj_gis_v80 as mjgis
import os

def RGB(r,g,b, dstFPN, inputtyp):
    GDALpath = '/Library/Frameworks/GDAL.framework/Versions/2.1/Programs'
    cmd = os.path.join(GDALpath,'gdalbuildvrt')        
    cmdstr = '%(cmd)s -separate %(V)s %(R)s %(G)s %(B)s' %{'cmd':cmd, 'V':dstFPN,'R':r, 'G':g, 'B':b}
    os.system(cmdstr)
    
    BALLE
    rgb = [r,g,b]
    rgbAL = []
    #mjgis = 
    for x,band in enumerate(rgb):
        bandfile = gdal.Open(band)
        bandDataRaw = bandfile.GetRasterBand(1).ReadAsArray()
        if inputtyp == 'srfi':
            bandData = (bandDataRaw/40)+1
            bandData[bandDataRaw < 0] = 1
            bandData[bandDataRaw == -32768] = 0
            bandData[bandDataRaw > 12000] = 255
            bandData[bandDataRaw > 11000] = 254
            bandData[bandDataRaw > 10000] = 252
            bandData = bandData.astype('uint8')
        else:
            snule
            
        print (x,np.amax(bandData))
        rgbAL.append(bandData)
    
    rgb_bands = np.asarray([i for i in rgbAL])
    rgb_bands = rgb_bands.transpose([1, 2, 0])
    print (rgb_bands.shape)
    dst_ds = gdal.GetDriverByName('GTiff').Create(dstFPN, 7821, 7041, 3, gdal.GDT_Byte)
    dst_ds.GetRasterBand(1).WriteArray(rgb_bands[:,:,0])   # write r-band to the    raster
    dst_ds.GetRasterBand(2).WriteArray(rgb_bands[:,:,1])   # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(rgb_bands[:,:,2])   # write b-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None
    
    
def RGB2(gl,rl,nir,mir, dstFPN, inputtyp):
    from math import pow
    bandD = {'gl':gl, 'rl':rl, 'nir':nir, 'mir':mir}
    powD = {'r':0.9, 'g':0.9, 'b':0.9}
    if inputtyp == 'srfi':
        maxD = {'r':pow(10000,powD['r'])/250.0, 'g':pow(10000,powD['g'])/250.0, 'b':pow(10000,powD['b'])/250.0 }
    print ('maxD', maxD)
    arrD = {}
    for b in bandD:
        bandfile = gdal.Open(bandD[b])
        arrD[b] = bandfile.GetRasterBand(1).ReadAsArray()
    denom = (( arrD['gl'] + arrD['rl'] + arrD['nir'] ))/30000 * (arrD['rl']/10000)
    print ('min',np.amin(denom))
    print ('max',np.amax(denom))
    r = arrD['mir']/denom
    rpow = np.power(r, powD['r'])
    g = arrD['nir']/denom
    gpow = np.power(g, powD['g'])
    b = arrD['gl']/denom
    bpow = np.power(b, powD['b'])
    
    rgbD = {'r':r,'g':g,'b':b}
    
    rgbPowD = {'r':rpow,'g':gpow,'b':bpow}
    
    rgbAL = []
    
    if inputtyp == 'srfi':
        for b in rgbD:
            '''
            dstBANDIni = np.power(BAND, self.scaling.power)
                dstBANDIni *=  self.scaling.scalefac
                #dstBANDInv = np.power(-BAND, self.scaling.power)
                #dstBANDInv *= - self.scaling.scalefac
                #MASK = (BAND < 0)
                dstBAND = np.copy(dstBANDIni)
                #dstBAND[MASK] = dstBANDInv[MASK]
                dstBAND += self.scaling.offsetadd
            '''
            bandData = (rgbPowD[b]/maxD[b])+1
            bandData[rgbD[b] < 0] = 1
            bandData[arrD['rl'] == -32768] = 0
            bandData[rgbD[b] > 10000] = 252
            bandData[rgbD[b] > 11000] = 253
            bandData[rgbD[b] > 12000] = 254
            
            
            bandData = bandData.astype('uint8')
            rgbAL.append(bandData)
    else:
        snule
        
    rgb_bands = np.asarray([i for i in rgbAL])
    rgb_bands = rgb_bands.transpose([1, 2, 0])
    cols,rows,layers = rgb_bands.shape
    #print (rgb_bands.shape)
    dst_ds = gdal.GetDriverByName('GTiff').Create(dstFPN, rows, cols, layers, gdal.GDT_Byte)
    dst_ds.GetRasterBand(1).WriteArray(rgb_bands[:,:,0])   # write r-band to the    raster
    dst_ds.GetRasterBand(2).WriteArray(rgb_bands[:,:,1])   # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(rgb_bands[:,:,2])   # write b-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None
    BULLE
    
def RGB3(bl,gl,rl,nir,mir, dstFPN, inputtyp):
    #v6
    powD = {'r':0.87, 'g':0.85, 'b':0.8}
    limitD = {'r':10500, 'g':10000, 'b':6500}
    #v7
    powD = {'r':0.85, 'g':0.85, 'b':0.8}
    limitD = {'r':10000, 'g':10000, 'b':6500}
    
    #v8
    powD = {'r':0.85, 'g':0.85, 'b':0.8}
    limitD = {'r':9500, 'g':10000, 'b':6500}
    
    #v9
    powD = {'r':0.9, 'g':0.85, 'b':0.8}
    limitD = {'r':9500, 'g':10000, 'b':6500}
    
    #v10
    powD = {'r':0.88, 'g':0.85, 'b':0.8}
    limitD = {'r':9300, 'g':10000, 'b':6500}

    #v11
    powD = {'r':0.88, 'g':0.85, 'b':0.8}
    limitD = {'r':10200, 'g':10000, 'b':6500}
    
    #v12
    powD = {'r':0.88, 'g':0.87, 'b':0.8}
    limitD = {'r':10200, 'g':9800, 'b':6500}
    
    #v13
    powD = {'r':0.87, 'g':0.86, 'b':0.8}
    limitD = {'r':10500, 'g':11300, 'b':6500}
    
    #v14
    powD = {'r':0.88, 'g':0.87, 'b':0.81}
    limitD = {'r':10400, 'g':11300, 'b':6500}
    
    stretchD = {'r':32767/limitD['r'], 'g':32767/limitD['g'], 'b':32767/limitD['b']}

    bandD = {'bl':bl,'gl':gl, 'rl':rl, 'nir':nir, 'mir':mir}
    arrD = {}

    for b in bandD:
        bandfile = gdal.Open(bandD[b])
        arrD[b] = bandfile.GetRasterBand(1).ReadAsArray()


    denom = (arrD['gl'] + arrD['rl']  + arrD['nir']);
    denom[denom < 0] = 1

    r = 10*((arrD['rl']+arrD['mir'])/2) / denom * arrD['rl']
    r[(arrD['rl']<0) | (arrD['mir']<0)] = 0
    
    g = 10*((arrD['gl']+arrD['nir'])/2) / denom * arrD['rl']
    b = 10*((arrD['bl']+arrD['gl'])/2) / denom * arrD['rl']
    
    g[(arrD['gl']<0) | (arrD['nir']<0) ] = 0
    b[(arrD['bl']<0) | (arrD['gl']<0) ] = 0
    
    rgbD = {'r':r,'g':g,'b':b}
    
    rpow = np.power(r, powD['r'])

    gpow = np.power(g, powD['g'])

    bpow = np.power(b, powD['b'])

    rgbPowD = {'r':rpow*stretchD['r']/40,
               'g':gpow*stretchD['g']/40,
               'b':bpow*stretchD['b']/40}
    
    rgbAL = []
    
    if inputtyp == 'srfi':
        for b in rgbD:
            
            bandData = rgbPowD[b]+1
            bandData[rgbPowD[b] < 0] = 1
            bandData[rgbPowD[b] > 252] = 252
            bandData[arrD['rl'] == -32768] = 0

            bandData = bandData.astype('uint8')

            rgbAL.append(bandData)
    else:
        snule
        
    rgb_bands = np.asarray([i for i in rgbAL])
    rgb_bands = rgb_bands.transpose([1, 2, 0])
    cols,rows,layers = rgb_bands.shape
    #print (rgb_bands.shape)
    dst_ds = gdal.GetDriverByName('GTiff').Create(dstFPN, rows, cols, layers, gdal.GDT_Byte)

    dst_ds.GetRasterBand(1).WriteArray(rgb_bands[:,:,0])   # write r-band to the    raster
    dst_ds.GetRasterBand(2).WriteArray(rgb_bands[:,:,1])   # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(rgb_bands[:,:,2])   # write b-band to the raster
    dst_ds.FlushCache()                     # write to disk
    dst_ds = None

if __name__=='__main__':
    arr = np.arange(256)
    #print (arr)
    apow = np.power(arr, 0.9)
    #print (apow)

    '''
    dstBANDIni = np.power(BAND, self.scaling.power)
                dstBANDIni *=  self.scaling.scalefac
                #dstBANDInv = np.power(-BAND, self.scaling.power)
                #dstBANDInv *= - self.scaling.scalefac
                #MASK = (BAND < 0)
                dstBAND = np.copy(dstBANDIni)
                #dstBAND[MASK] = dstBANDInv[MASK]
                dstBAND += self.scaling.offsetadd
    '''            
    #r = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/rl-srfi_L1TP_p019r049_19940107_multi.tif'
    #g = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/gl-srfi_L1TP_p019r049_19940107_multi.tif'
    #b = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/bl-srfi_L1TP_p019r049_19940107_multi.tif'
    bl = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/bl-srfi_L1TP_p019r049_19940107_multi.tif'
    gl = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/gl-srfi_L1TP_p019r049_19940107_multi.tif'
    rl = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/rl-srfi_L1TP_p019r049_19940107_multi.tif'
    nir = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/na-srfi_L1TP_p019r049_19940107_multi.tif'
    mir = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/mb-srfi_L1TP_p019r049_19940107_multi.tif'
    
    
    
    dstFPN = '/Volumes/guatemala/landsat/LT05/scenes/srfi/p019/r049/19940107/rgb-tgsmlpb14bluer_L1TP_p019r049_19940107_multi.tif'

    #RGB2(gl,rl,nir,mir,dstFPN,'srfi')
    
    RGB3(bl,gl,rl,nir,mir,dstFPN,'srfi')
