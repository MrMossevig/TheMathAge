'''
Created on 30. mar. 2017

@author: tsy
'''
import os
import xml.etree.ElementTree as ET


def list_factions():            
    ls = os.listdir('The-9th-Age') 
    #remove .cat extension
    newlist = []
    
    newlist.append([L[0:-4] for L in ls]) 
    return newlist
    
def list_units(filename=None):
    #filename without extension
    assert filename is not None
    cwd = os.getcwd()    
    os.chdir('The-9th-Age')
    
    tree  = ET.parse(filename+'.cat')
    root = tree.getroot()
    
    namelist=[]
    
    for child in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}selectionEntry'):        
        if child.attrib['type']=='model':
            namelist.append(child.attrib['name'])
        elif child.attrib['type']=='unit':                
            namelist.append(child.attrib['name']) 
    
    os.chdir(cwd)
    return(namelist)
    
