'''
Created on 12 Feb 2021

@author: thomasgumbricht
'''

# Standard library imports

import os, shutil

import  time

import datetime

import csv

def CopyProject():
    ''' Copy project updates to local GitHub clone
    '''
       
    for item in submoduleL:
        
        submoduleGitHubDirName = '%s-%s' %(prefix,item)
        
        dstRootFP = os.path.join(gitHubFP,submoduleGitHubDirName)
        
        print ("copying updates for package", item)
                  
        srcFP = os.path.join(srcProjectFP,item)
        
        for subdir, dirs, files in os.walk(srcFP, topdown=True):
            
            files = [f for f in files if not f.endswith('pyc')] 
            
            for file in files:
                
                print ('file',file)
                
                srcFPN = os.path.join(subdir,file)
                
                if not os.path.isfile(srcFPN):
                
                    continue
                
                if file in ignoreL:
                
                    continue
                
                if file[0] == '.':
                    
                    continue
                
                srcFPN = os.path.join(srcFP, subdir, file)
                                   
                print ('srcFPN',srcFPN)
                
                subdirL = []
                
                rPath = srcFPN
                
                while True:
                    
                     rPath, subD = os.path.split(rPath)
                     
                     if subD == item:
                         
                         break
                     
                     subdirL.append(subD)
                     
                
                print ('subdir',subdir)
                print ('dstRootFP',dstRootFP)
               
                print ('subdirL',subdirL)
                
                subdirL.reverse()
                    
                dstFP = dstRootFP
                     
                for d in subdirL:
                    
                    dstFP = os.path.join(dstFP,d)
                    
                    
                    
                print ('dstFP',dstFP)
                
                if not os.path.isdir(os.path.split(dstFP)[0]):
                        
                    print ('dstRootFP',dstRootFP)
                        
                    print ('dstFP',os.path.split(dstFP)[0])
                        
                    os.makedirs(os.path.split(dstFP)[0])

                #dstSubdir = os.path.split( subdir.replace(srcFP,'') )[1]
                
                #print ('dstSubdir',dstSubdir)
                
                #BALLE
                
                #if len(dstFP) > 0:
                
                #    #dstFP =  os.path.join(dstRootFP,  dstSubdir)
                    
                #    if not os.path.isdir(os.path.split(dstFP)[0]):
                        
                #        print ('dstRootFP',dstRootFP)
                        
                #        print ('dstFP',os.path.split(dstFP)[0])
                        
                #        os.makedirs(os.path.split(dstFP)[0])
                    
                #else:
                    
                #    dstFP = dstRootFP
                                    
                #dstFPN =  os.path.join(dstFP, file)
                
                dstFPN =  dstFP
                
                print ('dstFPN',dstFPN)
                                    
                try:
                
                    srcTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(srcFPN)) )
                    
                    dstTime = datetime.datetime.fromtimestamp( int(os.path.getmtime(dstFPN)) )
                                        
                    if int( os.stat(srcFPN).st_mtime) <= int(os.stat(dstFPN).st_mtime):

                        continue
                
                except OSError:
                    
                    pass
                
                    print ('error - target probably non-existing')
                
                print ('    copying', item, file, dstFPN)
                
                print ('')
                
                shutil.copy(srcFPN, dstFPN) #copying from source to destination
         
        # Create .gitignore if it does not exist, or overwrite is set to true       
        gitignoreFPN = os.path.join(dstRootFP,'.gitignore')
        
        if not os.path.isfile( gitignoreFPN ) or overwriteGitIgnore:
            
            with open(gitignoreFPN, 'w', encoding='UTF8', newline='') as f:
                
                writer = csv.writer(f)
                                    
                # write multiple rows
                writer.writerows(gitignore)
                              

def WriteScript():
    ''' Write script that loops over all the repos and stage, commit and push
    '''
    
    shF = open(scriptFPN, 'w')
    
    for item in submoduleL:
        
        submoduleGitHubDirName = '%s-%s' %(prefix,item)
        
        FP = os.path.join(gitHubFP,submoduleGitHubDirName)
        
        cdCmd = 'cd %s\n' %(FP)
                    
        shF.write(cdCmd)
        
        shF.write('echo "${PWD}"\n')
                    
        stageCmd = 'git add .\n'
        
        shF.write(stageCmd)
        
        commitCmd = 'git commit -m "%s"\n' %(commitMsg)
        
        shF.write(commitCmd)
        
        pushCmd = 'git push origin %s\n' %(branch)
    
        shF.write(pushCmd)
        
        shF.write('\n')
    
    shF.close()
    
    print ('Script file:', scriptFPN)

if __name__ == "__main__":
    
    copyProject = True
    
    overwriteGitIgnore = False
    
    branch = 'main'
    
    commitMsg = 'updates oct 2021'
    
    ignoreL = ['__pycache__','.DS_Store','README.md']
    
    home = os.path.expanduser('~')
    
    scriptFPN = os.path.join(home, 'submodule_stage_commit_push.sh')
    
    #srcProjectFP = '/Users/thomasgumbricht/eclipse-workspace/2020-03_geoimagine/karttur_v202003/geoimagine'
    srcProjectFP = '/Users/thomasgumbricht/eclipse-workspace_2021-09/test-20211022/test_20211026/geoimagine'
    
    gitHubFP = '/Users/thomasgumbricht/GitHub/'
    
    gitHubAccount = 'karttur'
    
    prefix = 'geoimagine03'
    
    gitignore = [['.DS_Store'],['__pycache__/']]
    
    submoduleL = ['ancillary','assets','basins','copernicus',
                  'dem','export','extract',
                  'gis','grace','grass','ktgdal',
                  'ktgrass','ktnumba',
                  'ktpandas','landsat','layout',
                  'modis','npproc',
                  'params','postgresdb','projects',
                  'region','sentinel',
                  'setup_db','setup_processes','smap','support',
                  'timeseries','updatedb','userproj',
                  'zipper']
       
    if copyProject:
        
        CopyProject()
        
    WriteScript()