'''
Created on 28 Jan 2021

@author: thomasgumbricht
'''

from string import whitespace

def CheckWhitespace(s):
        '''
        '''
        return True in [c in s for c in whitespace]
    
    
    
s = 'dumsnut'

print (CheckWhitespace(s))