'''
Created on 17. mar. 2017

@author: tsy
'''

import TheMathAge_combat
from  unit_objects import unit

if __name__ == '__main__':
    pass

#ATTACKER
attacker = unit(XML=True,models = 15)
attacker.loadData(factionFileName='2.0 Saurian Ancients', name='Temple Guard')
attacker.A = 15

#DEFENDER
defender = unit(XML=True,models = 15)
defender.loadData(factionFileName='2.0 Saurian Ancients', name='Temple Guard')
defender.employRules(['Born Predator','Halberd'])
defender.AS = 4

print(defender.rules)


'''NO INPUT BELOW HERE'''       

TheMathAge_combat.main(attacker, defender) 

