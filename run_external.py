'''
Created on 17. mar. 2017

@author: tsy
'''

import TheMathAge_combat
from  unit_objects import unit

if __name__ == '__main__':
    pass


defender= unit(excelFile='Unit_Data.xlsx')
attacker = unit(excelFile='Unit_Data.xlsx')

defender.loadData(faction='SA', name='Saurian Warriors')
attacker.loadData(faction='SA', name='Caiman')

'''NO INPUT BELOW HERE'''       

TheMathAge_combat.main(attacker, defender) 
#TheMathAge_combat.main(attacker=None, defender=None)
