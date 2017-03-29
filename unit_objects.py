'''
Created on 17. mar. 2017

@author: tsy
'''

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
        self.models  = models
        self.rerolls = reRolls()
        self.toroll  = toRoll()
        self.special = special()
        self.bonus   = bonus()
        

    def load_XML_basic_data(self):
               
        from catToPy import charsToDict 
        
        #Load a dictionary data set from XML  
        d = charsToDict(name = self.name,filename= self.factionFileName)
        
        self.M = d['M']
        self.WS = d['WS']
        self.BS = d['BS']
        self.S = d['S']
        self.T = d['T']
        self.W = d['W']
        self.I = d['I']
        self.A = d['A']
        self.LD = d['LD']
        self.AS = d['ArmourSave']
        self.WA = d['WardSave']

    
    def load_XML_special_rules(self):
        from catToPy import rulesToList         
        from catToPy import rulesInterpreter
        ruleList = rulesToList(name = self.name,filename=self.factionFileName)        
        ruleDict = rulesInterpreter(filename=self.factionFileName,ruleList=ruleList)
        for n in ruleDict:
            print(n)
    
    def loadData(self,name=None,factionFileName=None):
        assert name is not None
               
        self.name = name
        self.factionFileName = factionFileName

        #Basic data (Characteristics)        
        if self.readFrom is 'XML':
            self.load_XML_basic_data()
            self.load_XML_special_rules()
            
        
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
                 woundMin            = 2      # Minimum value you can wound on
                 ):
        # Special rules
        self.lethal                = lethal
        self.multiple              = multiple
        self.multipleWoundOnLethal = multipleOnLethal
        self.extraAttacksOnWound   = extraAttacksOnWound
        self.woundMin              = woundMin

    
class bonus(object):
    def __init__(self,hit=0,wound=0,armour=0,ward=0):
        # Extra bonus for hitting/wounding/armour/ward
        self.hit    = hit     # E.g. that elf shit
        self.wound  = wound
        self.armour = armour  # E.g. armour piercing
        self.ward   = ward    
        
