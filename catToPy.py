'''
Created on 20. mar. 2017

@author: tsy
'''
import os
import xml.etree.ElementTree as ET


def charsToDict(filename,name):
    '''filename without extension'''    
    cwd = os.getcwd()    
    os.chdir('The-9th-Age')
    
    tree  = ET.parse(filename+'.cat')
    root = tree.getroot()
    
    def _childCharsToDict_(child=None):    
        assert child is not None
        returnDict = {'M':None,'WS':None,'BS':None,'S':None,'T':None,'W':None,'I':None,'A':None,'LD':None,'ArmourSave':7,'WardSave':7,}    
        for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}characteristic'):
            for char in returnDict:
                if child2.attrib['name']== char:
                    try:
                        returnDict[char] = int(child2.attrib['value'])
                    except KeyError: 
                        print('%s can not be found for %s'%(char,child.attrib['name']))
                    except ValueError:
                        #either '-' or '5+' 
                        try:
                            returnDict[char] = int(child2.attrib['value'][0])               
                        except ValueError:
                            returnDict[char] = None
                            print('%s will be left as None for %s'%(char,child.attrib['name']))
                        except IndexError:     
                            pass
        print('\n')            
        return returnDict

        
    for child in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}selectionEntry'):        
        if child.attrib['name']==name:
            if child.attrib['type']=='model':
                returnDict = _childCharsToDict_(child)
            elif child.attrib['type']=='unit':                
                returnDict = _childCharsToDict_(child) 
                
    
    os.chdir(cwd)
    return returnDict
    
def rulesToList(filename,name):
    'filename without extension'
    cwd = os.getcwd()    
    os.chdir('The-9th-Age')
    
    tree  = ET.parse(filename+'.cat')
    root = tree.getroot()
    
    
    def _childRulesToList_(child=None):    
        rules = []
        assert child is not None
        for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}infoLink'):
            if 'targetId' in child2.attrib:
                rules.append(child2.attrib['targetId'])
        
        return rules
    
    
    for child in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}selectionEntry'):        
        if child.attrib['name']==name:
            if child.attrib['type']=='model':
                ruleList = _childRulesToList_(child)
            elif child.attrib['type']=='unit':                
                ruleList = _childRulesToList_(child) 
                
    
    os.chdir(cwd)
    return ruleList

def rulesInterpreter(filename=None,ruleList=None):
    #Send a list of rule ID's. and this one returns the corresponding rule text
    assert ruleList is not None
    assert filename is not None
    
    cwd = os.getcwd()    
    os.chdir('The-9th-Age')
    
    tree  = ET.parse(filename+'.cat')
    root = tree.getroot()
    
    ruleDict = {}
    
    #SEARCHING RULES
    for child in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}rule'):
        if child.attrib['id'] in ruleList:
            id = child.attrib['id']
            name = child.attrib['name']
            for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}description'):                             
                text = child2.text
            
            for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}modifiers'):                             
                modifier = child2.text
            ruleDict[name] = [text,id,modifier]
    #SEARCHING PROFILES        
    for child in root.iter('{http://www.battlescribe.net/schema/catalogueSchema}profile'):
        if child.attrib['id'] in ruleList:
            id = child.attrib['id']
            name = child.attrib['name']
            for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}description'):                             
                text = child2.text
            
            for child2 in child.iter('{http://www.battlescribe.net/schema/catalogueSchema}modifiers'):                             
                modifier = child2.text
            ruleDict[name] = [text,id,modifier]        
                         
            
    
    
    os.chdir(cwd)
    return ruleDict
