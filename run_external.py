'''
Created on 17. mar. 2017

@author: tsy
'''
import os
import TheMathAge_combat
from  unit_objects import unit
from run_helpers import list_factions,list_units

if __name__ == '__main__':
    pass


faction_list = list_factions()
#print(faction_list)

unit_list = list_units('2.0 Kingdom of Equitaine')
print(unit_list)

#ATTACKER
#DEFENDER
defender = unit(XML=True,models = 15)
defender.loadData(factionFileName='2.0 Saurian Ancients', name='Alpha Carnosaur')
defender.employRules(['Born Predator','Innate Defence (3+)', 'Multiple Wounds (D3)'])

attacker = unit(XML=True,models = 2)
attacker.loadData(factionFileName='2.0 Kingdom of Equitaine', name='Duke')
attacker.employRules(['Lance','Heavy Armor','Shield','Barding','Mounts Protection (6+)'])

print(attacker.AS)
print(attacker.XMLrules.keys())
print(attacker.XMLrules)


'''NO INPUT BELOW HERE'''       

TheMathAge_combat.main(attacker, defender) 

