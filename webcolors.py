'''
Created on 22 Jan 2018

@author: thomasgumbricht
'''

import struct
import xml.dom.minidom as minidom
from os import path

def ModulePath():
    ModuleFullPath = path.abspath(__file__)
    MP = path.split(ModuleFullPath)[0]
    return MP

def HexToRGB(hexcode):
    return struct.unpack('BBB',hexcode.decode('hex'))

def ReadColorHexXML():
    MP = ModulePath()
    xmlFPN = path.join(MP,'xml','web_hex_colors.xml')
    print (xmlFPN)
    #parse the xml file
    dom = minidom.parse(xmlFPN)   
    #get the userproject tag     
    colorTags = dom.getElementsByTagName('color')
    colorList = []
    colorDict = {}
    for i,ct in enumerate(colorTags):
        colorname = ct.getAttribute('name').lower()
        hexcode = ct.firstChild.nodeValue  
        #print colorname, hexcode, HexToRGB(hexcode[1:len(hexcode)])

        h = hexcode.lstrip('#')
        RGB = tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

        #colorList.append( HexToRGB(hexcode[1:len(hexcode)]) )
        colorList.append(RGB)
        colorDict[colorname] = i
    return colorDict, colorList

def CreateRGBPalette(): 
    [[0, 0, 0, 255], [1, 1, 0, 255]]   

if __name__ == '__main__':
    
    ReadColorHexXML()

