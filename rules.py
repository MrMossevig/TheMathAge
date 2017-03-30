'''
Created on 30. mar. 2017

@author: tsy
'''

class rules(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.gen = {'Thunderous Charge':'self.S+=1',
             'Frenzy':'self.A +=1',
             'AP1':'self.bonus.armour +=1',
             'Innate Defence (2+)':'self.AS-=5',
             'Innate Defence (3+)':'self.AS-=4',
             'Innate Defence (4+)':'self.AS-=3',
             'Innate Defence (5+)':'self.AS-=2',
             'Innate Defence (6+)':'self.AS-=2',
             'Multiple Wounds (D3)':'self.special.multiple="D3"',
             'Lightning Reflexes':'self.bonus.hit -=1',
             'Mounts Protection (6+)': 'self.AS-=1'
         }
 
        self.SE = {
                   'Forest Walker':'self.rerolls.wound=1',
                   'Blades of Cenyrn - attack':'self.A+=1',
                   'Sylvan Blades':'self.A+=1;self.bonus.armour+=1'
                   
        }
        
        self.SA = {                                                                                 
             'Born Predator':'if self.rerolls.hit<1:self.rerolls.hit=1',
             'audacity':'self.rerolls.hit = 7; self.rerolls.wound = 7'                   
         }
 
        self.KOE = {                                                                                 
             'Born Predator':'if self.rerolls.hit<1:self.rerolls.hit=1',
             'audacity':'self.rerolls.hit = 7; self.rerolls.wound = 7',
             'might':'self.A +=1;self.S+=1;self.special.extraAttacksOnWound =1',
             'renown':'self.special.lethal = True;self.special.multipleWoundOnLethal ="d3+1" ',
             'Oath: Questing Oath': 'self.special.multiple = 2',
             'Oath: Grail Oath':'self.WS += 1',
             'Blessing: Favour of the Grail':'if (self.bonus.armour > 0): self.WA = 5',
             'Blessing: Favour of the King':'if (self.S >= 5): self.WA = 5',                    
             'Blessed Sword':'self.rerolls.wound = 7;self.rerolls.ward  = -1',
             'Crusaders Helm':'self.AS -= 1; self.rerolls.armour = 7'
         }
               
        self.magicItems = {
               'Axe of Battle':'self.special.woundMin   = 3;self.A = 6',
               'Flesrender':'self.bonus.armour += 1;self.S += 2;self.I=0',
               'Dragon Lance':'self.special.multiple = "D3";self.S        += 2',                      
               'Bluffers Helm':'self.AS -= 1;self.rerolls.wound = -1',
               'Dragonscale Helm':'self.AS -= 1;self.special.fireborn=True',
               'Dragon Mantle':'self.AS -= 2',
               'Hardened Shield':'self.AS -= 2; self.I = 1 if ((self.I - 3) < 1) else self.I -= 3',
               'Potion of Strength':'self.s+=2'

         }
        self.mundaneItems = {
                    'Shield':'self.AS-=1',
                    'Halberd':'self.S+=1',# WHAT ABOUT BOTH HANDS RULE
                    'Great Weapon':'self.S+=2;self.I=0',
                    'Lance':'self.S+=2',
                    'Barding':'self.AS-=1',
                    'spear':'self.bonus.armour +=1',
                    'Heavy Armor':'self.AS-=2'
         }
    def makefullDict(self):
        fullList = dict(self.gen)
        fullList.update(self.SA)
        fullList.update(self.SE)
        fullList.update(self.KOE)
        fullList.update(self.magicItems)
        fullList.update(self.mundaneItems)
        
        self.fullDict = fullList