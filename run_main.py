'''
Created on 17. mar. 2017

@author: tsy
'''

import TheMathAge_combat
from  unit_objects import unit

if __name__ == '__main__':
    pass

N=23
with open("TheMathAge_combat.py") as f:
    for i in range(N):
        line=f.next().strip()
        print(line)
        
        
attacker = unit(faction='SA', type='Saurus Warriors')
defender= unit(faction='KoE', type='Grail Knight')
TheMathAge_combat.main(attacker, defender) 

