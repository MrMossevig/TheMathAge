'''
Created on 17. mar. 2017

@author: tsy
'''

import TheMathAge_combat
from  unit_objects import unit

if __name__ == '__main__':
    pass


defender= unit(XML=True,models=10)
attacker = unit(XML=True,models = 10)

attacker.loadData(factionFileName='2.0 Kingdom of Equitaine', name='Duke')
defender.loadData(factionFileName='2.0 Saurian Ancients', name='Saurian Warriors')



'''NO INPUT BELOW HERE'''       

TheMathAge_combat.main(attacker, defender) 

