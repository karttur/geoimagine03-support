'''
Created on 24 Mar 2021

@author: thomasgumbricht

Tilefit is a script for finding corner points defining arbitrary region that fit the 
predefined systems of Kartturs GeoImagine Framework
'''

import json

from os import path


def DefRegJson(regionid, system, minx, miny, maxx, maxy, volume):
    
    suffix = 'v01-%s' %(system)
    dct = {
      "processid": "DefaultRegionFromCoords",
      "overwrite": True,
      "parameters": {
        "regioncat": "global",
        "regionid": regionid,
        "regionname": "%s hydro %s" %(regionid, system),
        "parentcat": "global",
        "parentid": "global",
        "stratum": "1",
        "minx": minx,
        "miny": miny,
        "maxx": maxx,
        "maxy": maxy,
        "version": "1.0",
        "title": "%s hydro %s" %(regionid, system),
        "label": "%s hydrological region for %s." %(regionid, system)
      },
      "dstpath": {
        "volume": volume
      },
      "dstcomp": [
        {
          regionid: {
            "masked": "N",
            "measure": "N",
            "source": "karttur",
            "product": "pubroi",
            "content": "roi",
            "layerid": "hydroreg",
            "prefix": "hydroreg",
            "suffix": suffix,
            "dataunit": "boundary",
            "celltype": "vector",
            "cellnull": "0"
          }
        }
      ]
    }
    
    return dct


def userProjJson(userid, regionid):
    '''
    '''
    projtractid = '%s-%s' %(userid,regionid)
    projtractname = '%s %s' %(userid,regionid)
    
    dct = {
      "processid": "ManageDefRegProj",
      "overwrite": False,
      "parameters": {
        "defaultregion": regionid,
        "tractid": projtractid,
        "tractname": projtractname,
        "tracttitle": projtractname,
        "tractlabel": projtractname,
        "projid": projtractid,
        "projname": projtractname,
        "projtitle": projtractname,
        "projlabel": projtractname
      }
    }
    
    return dct

def WriteMosacicJson(volume, userid, regionid, mosaicJsonFP, mosaicJsonFN):
    '''
    '''
    
    projtractid = '%s-%s' %(userid,regionid)
    
    mosaicJsonFN = mosaicJsonFN %(regionid)
    
    mosaicJsonFPN = path.join(mosaicJsonFP, mosaicJsonFN)
    
    dct = {
      "processid": "MosaicTiles",
      "version": "1.3",
      "overwrite": False,
      "parameters": {
        "resample": "near",
        "asscript": False,
        "fillnodata": False,
        "fillmaxdist": 0,
        "fillsmooth": 0
      },
      "srcpath": {
        "volume": volume
      },
      "dstpath": {
        "volume": volume
      },
      "srccomp": [
        {
          "dem": {
            "source": "ESA",
            "product": "copdem",
            "content": "dem",
            "layerid": "dem90",
            "prefix": "dem",
            "suffix": "v01-pfpf-hydrdem4+4-90m"
          }
        }
      ],
      "dstcopy": [
        {
          "dem": {
            "layerid": "dem90",
            "prefix": "dem",
            "suffix": "v01-pfpf-hydrdem4+4-90m"
          }
        }
      ]
    }
    
    ### ProcessMosaic
    
    jsonObj =  {"userproject": {
            "userid": "karttur",
            "projectid": projtractid,
            "tractid": projtractid,
            "siteid": "*",
            "plotid": "*",
            "system": system
          },
          "period": {
            "timestep": "static"
          },
          "process": [dct] }  
            
    dstF = open(mosaicJsonFPN, "w")
  
    json.dump(jsonObj, dstF, indent = 3)
  
    dstF.close()
    
    return mosaicJsonFPN

    
def js_r(filename: str):
    
    with open(filename) as f_in:
        
        return json.load(f_in)
    
def FindMin(edge,coord,resol,dimdiv):
    
    cells = (coord-edge)/resol
    
    minimum = edge + int(cells)*resol
        
    while True:
        
        if (minimum-edge) % dimdiv == 0:
            
            break
        
        minimum -= resol
        
        if minimum <= edge:
            
            return edge
    
    return minimum

def FindMax(minimum,coord,resol):
    
    cells = (coord-minimum)/resol
    
    maximum = minimum + int(cells)*resol
    
    return maximum

def AdjustDimDiv(dimdiv,x0,y0,xres,yres,llx,lly,urx,ury):
    
    x = 0
    
    while True:
        
        xdim = (urx-llx)/xres
        
        #print ( 'xdimfix',llx,(xdim % dimdiv), ( (llx-x0) % dimdiv))
                    
        #if xdim % dimdiv == 0 and (llx-x0) % dimdiv == 0:
            
        if xdim % dimdiv == 0:
            
            break
        
        urx += xres
        '''
        if x % 2 == 0:
            
            urx += xres
            
        elif llx-xdim >= x0:
            
            llx -= xres
            
        '''
            
        x +=1
       
    y = 0
    
    while True:
        
        ydim = (ury-lly)/yres
        
        #print ( 'ydimfix', lly, ydim, (ydim % dimdiv), ((lly-y0) % dimdiv) )
                    
        #if ydim % dimdiv == 0 and (lly-y0) % dimdiv == 0:
        if ydim % dimdiv == 0:
            break
        
        ury += yres
        
        '''
        if y % 2 == 0:
            
            ury += yres
            
        elif lly-ydim >= y0:
            
            lly -= yres
            
        else:
            
            NOTWORKING
            
        #if y > 100:
            
        #    SNULLE
        '''    
        y +=1
        
    return (llx,lly,urx,ury)


def FindRegion(jsonFPN, volume, defRegJsonFPN, userRegJsonFPN, mosaicJsonFP, mosaicFN, mosaicPiloFPN):
    
    procL = []
    
    userProcL = []
    
    mosaicPilotL = ['###########################','###    mosaic tiles    ###','###########################']
    
    regionD = js_r(jsonFPN)
    
    print (regionD)
    
    for system in regionD:
        
        print ('system',system)
        
        for reg in regionD[system]:
            
            print ('    region:', reg['regionid'])
            
            dimdiv = reg['dimdiv']
            
            x0 = reg['x0']
            
            y0 = reg['y0']
            
            xres = reg['xres']
            
            yres = reg['yres']
            
            minx = reg['minx']
            
            miny = reg['miny']
            
            maxx = reg['maxx']
            
            maxy = reg['maxy']
            
            llx = FindMin(x0,minx,xres,dimdiv)
            
            lly = FindMin(y0,miny,yres,dimdiv)
            
            urx = FindMax(llx,maxx,xres)
            
            ury = FindMax(lly,maxy,yres)
            
            xdim = (urx-llx)/xres
            
            ydim = (ury-lly)/yres
            
            infostr = '        input: minx: %s, miny: %s maxx: %s, maxy: %s' %(minx,miny,maxx,maxy)

            print (infostr)
            
            infostr = '        initial: minx: %s, miny: %s maxx: %s, maxy: %s, xdim: %s, ydim: %s' %(llx,lly,urx,ury,xdim,ydim)
            
            print (infostr)
            
            llx,lly,urx,ury = AdjustDimDiv(dimdiv,x0,y0,xres,yres,llx,lly,urx,ury)
            
            xdim = (urx-llx)/xres
            
            ydim = (ury-lly)/yres
            
            infostr = '        adjusted: minx: %s, miny: %s maxx: %s, maxy: %s, xdim: %s, ydim: %s' %(llx,lly,urx,ury,xdim,ydim)

            print (infostr)
            
            procL.append( DefRegJson(reg['regionid'], system, llx, lly, urx, ury, volume) )
            
            userProcL.append( userProjJson('karttur', reg['regionid'] ) )
            
            mosaicPilotL.append( WriteMosacicJson(volume,'karttur',reg['regionid'],mosaicJsonFP, mosaicFN) )
            

     
    jsonObj =  {"userproject": {
            "userid": "karttur",
            "projectid": "karttur",
            "tractid": "karttur",
            "siteid": "*",
            "plotid": "*",
            "system": system
          },
          "period": {
            "timestep": "static"
          },
          "process": procL }  
            
    dstF = open(defRegJsonFPN, "w")
  
    json.dump(jsonObj, dstF, indent = 3)
  
    dstF.close()    
    
    
    jsonObj =  {"userproject": {
            "userid": "karttur",
            "projectid": "karttur",
            "tractid": "karttur",
            "siteid": "*",
            "plotid": "*",
            "system": "system"
          },
          "period": {
            "timestep": "static"
          },
          "process": userProcL }  
            
    dstF = open(userRegJsonFPN, "w")
  
    json.dump(jsonObj, dstF, indent = 3)
  
    dstF.close()    
    
    # Write the txt command for the mosacking
    
    with open(mosaicPilotFPN,'w') as file:
        
        for line in mosaicPilotL:
            
            print (line)
            
            file.write(line)
            
            file.write('\n')
    
if __name__ == "__main__":
    
    srcJsonFPN = 'doc/hydroregion_setup.json'
    
    defRegJsonFPN = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine/setup_processes/regiondoc/json/add_ease2n_hydro_regions_v090.json'
    
    userRegJsonFPN = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine/projects/doc/adduserprojs/json/add_user_projects-regions_arctic-hydro.json'
    
    mosaicJsonFP = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine/projects/doc/CopernicusDEM/json'

    mosaicJsonFN = '0313_CopDEM_mosaic-%s.json'
    
    mosaicPilotFPN = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine/projects/doc/CopernicusDEM/CopDEM_mosaic_arctic-hydro-regions.txt'
    #mosaicPilotFPN = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine/projects/doc/CopernicusDEM/json/0313_CopDEM_mosaic-alaskahydro_ease2n.json
    volume = 'Ancillary'
    
    system = 'ease2n'
    
    FindRegion(srcJsonFPN, volume, defRegJsonFPN, userRegJsonFPN,mosaicJsonFP, mosaicJsonFN,mosaicPilotFPN)
    
    
    
    
    