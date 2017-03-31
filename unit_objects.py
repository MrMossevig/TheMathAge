'''
Created on 17. mar. 2017

@author: tsy
'''
from rules import rules

class unit(object):
    '''
    classdocs
    '''

    def __init__(self,models = None,excelFile=None,XML=False):       

        assert models is not None
        '''object data'''
        if(excelFile):
            self.excelFile = excelFile
            self.readFrom = 'Excel'
            
        if(XML):
            self.readFrom = 'XML'

        '''unit data'''

        self.faction = None
        self.name = None
                
        
        self.M = None
        self.WS = None
        self.BS = None
        self.S = None
        self.T = None
        self.W = None
        self.I = None
        self.A = None
        self.LD = None
        self.AS = None          #Armorsave
        self.WA = None          #Ward save        
        self.models  = int( models )
        self.totA    = int( models )
        self.rerolls = reRolls()
        self.toroll  = toRoll()
        self.special = special()
        self.bonus   = bonus()
        self.rules = []

    def load_XML_basic_data(self):
        #subfunction of loadData
        from catToPy import charsToDict 
        
        #Load a dictionary data set from XML  
        d = charsToDict(name = self.name, filename= self.factionFileName)

        # The characteristics are not properly defined for all units
        try:
            self.M  = int( d['M']  )
        except:
            self.M = 0
        try:
            self.WS = int( d['WS'] )
        except:
            self.WS = 0
        try:
            self.BS = int( d['BS'] )
        except:
            self.BS = 0
        try:
            self.S  = int( d['S']  )
        except:
            self.S  = 0
        try:
            self.T  = int( d['T']  )
        except:
            self.T  = 0
        try:
            self.W  = int( d['W']  )
        except:
            self.W  = 1
        try:
            self.I  = int( d['I']  )
        except:
            self.I  = 0
        try:
            self.A  = int( d['A']  )
        except:
            self.A  = 1
        try:
            self.LD = int( d['LD'] )
        except:
            self.LD = 0
        try:
            self.AS = int( d['ArmourSave'] )
        except:
            self.AS = 7
        try:
            self.WA = int( d['WardSave'] )
        except:
            self.WA = 7
        self.rules = []
        self.XMLrules=None
    
    def load_XML_special_rules(self):
        #subfunction of loadData
        from catToPy import rulesToList         
        from catToPy import rulesInterpreter
        ruleList = rulesToList(name = self.name,filename=self.factionFileName)        
        ruleDict = rulesInterpreter(filename=self.factionFileName,ruleList=ruleList)        
        self.XMLrules = ruleDict 
    
    
    def loadData(self,name=None,factionFileName=None):
        ''' Main function to read in unit/model data''' 
        assert name is not None
               
        self.name = name
        self.factionFileName = factionFileName

        #Basic data (Characteristics)        
        if self.readFrom is 'XML':
            self.load_XML_basic_data()
            self.load_XML_special_rules()

        self.TotA = self.A * self.models
    
    def employRules(self,ruleList):
        #ruleList is name of rules (e.g. "Shield", "Halberd", "Innate Defence (5+)" etc
      
        #import rules 
        ruleDict = rules()
        ruleDict.makefullDict() 
        
        for rule in ruleList:
            try: 
                exec(ruleDict.fullDict[rule]) #ok                
                self.rules.append(rule)
            except KeyError:
                print('\n%s is not found in Dictionaries!\n'%rule)
                import time
                time.sleep(2)
        
class reRolls(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        self.hit = hit
        self.wound = wound
        self.armour = armour
        self.ward = ward
        
class toRoll(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        self.hit = hit
        self.wound = wound
        self.armour = armour
        self.ward = ward
        
        
class special(object):
    def __init__(self,
                 lethal              = False, # Lethal strike (AP6 on natural '6' to wound)
                 multiple            = 1,     # Multiple wounds
                 multipleOnLethal    = False, # Multiple wounds only on natural '6'
                 extraAttacksOnWound = 0,     # Unsaved wounds generates extra attacks
                 woundMin            = 2,      # Minimum value you can wound on
                 fireborn            =False
                 ):
        # Special rules
        self.lethal                = lethal
        self.multiple              = multiple
        self.multipleWoundOnLethal = multipleOnLethal
        self.extraAttacksOnWound   = extraAttacksOnWound
        self.woundMin               = woundMin
        self.fireborn               =fireborn

    
class bonus(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        # Extra bonus for hitting/wounding/armour/ward
        self.hit    = hit     # E.g. that elf shit
        self.wound  = wound
        self.armour = armour  # E.g. armour piercing
        self.ward   = ward    
        
