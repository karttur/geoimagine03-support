'''
Created on 18 Oct 2018

@author: thomasgumbricht
'''

# Standard library imports

import sys
import ftplib
import os
import time

server = "FTPHOST"
user = "anonymous"
password = "anonymous"
source = "/Folder/SourceFolder/"
destination = "/home/user/downloads/"
interval = 0.05

ftp = ftplib.FTP(server)
ftp.login(user, password)


def downloadFiles(server,user,pswd,src,dst):
    ftp = ftplib.FTP(server)
    ftp.login(user, pswd)
    try:
        ftp.cwd(src)       
        os.chdir(dst)
        mkdir_p(dst[0:len(dst)-1] + src)
        print ("Created: " + dst[0:len(dst)-1] + src)
    except OSError:     
        pass
    except ftplib.error_perm:       
        print ("Error: could not change to " + src)
        sys.exit("Ending Application")
    
    filelist=ftp.nlst()

    for file in filelist:
        time.sleep(interval)
        try:            
            ftp.cwd(src + file + "/")          
            downloadFiles(src + file + "/", destination)
        except ftplib.error_perm:
            os.chdir(dst[0:len(destination)-1] + src)
            
            try:
                ftp.retrbinary("RETR " + file, open(os.path.join(destination + src, file),"wb").write)
                print ("Downloaded: " + file)
            except:
                print ("Error: File could not be downloaded " + file)
    return
    
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        sys.exit('Error creating local dst path')


downloadFiles(source, destination)