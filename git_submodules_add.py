'''
Created on 12 Feb 2021

@author: thomasgumbricht

Script that automatically defines packages having a predefined pattern as submodules
'''

# Standard library imports

from os import listdir


def GetSubmodules(root, pattern, skipL):
    ''' Copy project updates to local GitHub clone
    '''
    
    pl = len(pattern)
    
    #print (listdir(root))
    
    #print (pattern)
    
    #for item in listdir(root):
        
    #    print (item, item[0:pl])
    
    patterndirs = [f for f in listdir(root) if f[0:pl] == pattern and f not in skipL]
    
    for repo in patterndirs:
        
        #print (repo)
        
        cmd = 'git submodule add https://github.com/karttur/%s %s' %(repo, repo.split('-')[1])
        
        print (cmd)
        
    
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
    
    gitRoot = "/Users/thomasgumbricht/GitHub"
    
    pattern = "geoimagine02"
    
    skipL = ["geoimagine02","geoimagine02_frame","geoimagine02-docs"]
    
    GetSubmodules(gitRoot, pattern, skipL)
    
    
        


