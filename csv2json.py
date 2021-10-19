'''
Created on 21 Mar 2021

@author: thomasgumbricht
'''


import csv
import json

csvfile = 'doc/northland_ease2n.csv'
#csvfile = open('doc/northland_ease2n.csv', 'r')
jsonfile = open('doc/northland_ease2n.json', 'w')

fieldnames = ("regionid","regiontype","xtile","ytile")

jsonL = []

with open(csvfile) as f:
    
    content = f.readlines()
    
# you may also want to remove whitespace characters like `\n` at the end of each line

content = [x.strip() for x in content]

for item in content:
    
    xtile = int(item[1:3])
    
    ytile = int(item[4:6])
    
    paramL = ["'northland'","'default'",str(xtile),str(ytile)]
    
    jsonObj =  ', '.join(f'"{w}"' for w in paramL) 
    
    L = []
    
    L.append(jsonObj )
    
    print(', '.join(f'"{w}"' for w in paramL) )
    
    jsonL.append(L)
    
jsonObj = {"values":jsonL}
    
print (jsonObj)
    
    
json.dump(jsonObj, jsonfile)
    

jsonfile.close()