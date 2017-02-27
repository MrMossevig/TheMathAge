'''
Created on 27. feb. 2017

@author: tsy

License: CC-BY
'''
from random import randint
import numpy as np

if __name__ == '__main__':
    pass


def roll(dice):
    res = 0
    for n in range(dice):
        res =+ randint(1,6)
    return res
    

def charge(M=None,distance = None,swiftStride=False):
    assert M is not None
    assert distance is not None
    res = list()    
    chargePassed = False
    
    res.append(roll(1))
    res.append(roll(1))
    
    if swiftStride:
        res.append(roll(1))
        chargeRange= sum(res) - min(res)
    else:
        chargeRange=sum(res)
        
    if chargeRange >= distance:
        chargePassed = True 
        
    return chargePassed
    
    
def LdTest(Ld=None,reRoll=False,coldBlood=False):    
    assert Ld is not None
    
    def __test__(Ld,reRoll,coldBlood):        
        passTest = False 
        res = list()    
        res.append(roll(1))
        res.append(roll(1))
        
        if coldBlood:
            res.append(roll(1))
            score = sum(res) - max(res)
        else:
            score = sum(res)
        
        if score<=Ld:
            passTest = True
        
        return passTest
    
    passTest = __test__(Ld,reRoll,coldBlood)
    
    if passTest is False  and reRoll is True:
        passTest = __test__(Ld,reRoll,coldBlood)
    
    return passTest

def cast(dice=None,castValue=None):
    assert type(dice) is not None
    assert castValue is not None
    assert dice < 6
    assert castValue <20
    
    spellCast = True
        
    res = list()
    #cast dice
    for n in range(dice):
        res.append(roll(1))
    
    #check for OP and roll another dice if OP
    res.sort()
    if dice>1:
        if res[-1] is 6 and res[-2] is 6:
            res.append(roll(1))
    
    #summarize castScore
    castScore = sum(res)
    
    #check against castValue
    if castScore<castValue:
        spellCast = False
    
    return spellCast
    

def printTables():    
    N = 250000 # number of seeds for each simulation
    
    printCharge = True
    printLd = True
    printMagic = True
    
    if printCharge:
        '''charge range'''
        #distances to check
        chargeRes = list()    
        QSres = list()
        for m in range(3,13):        
            
            #runs/seeds
            res = list()
            append = res.append
            for n in range(N):
                append(charge(M=0,distance = m,swiftStride=False))
            chargeRes.append(np.mean(res)*100)
            
            res = list()
            append = res.append
            for n in range(N):
                append(charge(M=0,distance = m,swiftStride=True))
            QSres.append(np.mean(res)*100)
          
    
    if printLd:
        '''Leadership tests'''   
        resNormal= list()
        resColdBlood=list()
        resReRoll = list()
        resReRollCB = list()
        
        for ld in range(2,11):
            
            l1=list()
            l2 = list()
            l3 = list()
            l4 = list()
            for n in range(N):
                    l1.append(LdTest(Ld=ld,reRoll=False,coldBlood=False))
                    l2.append(LdTest(Ld=ld,reRoll=False,coldBlood=True))
                    l3.append(LdTest(Ld=ld,reRoll=True,coldBlood=False))
                    l4.append(LdTest(Ld=ld,reRoll=True,coldBlood=True))
            resNormal.append(np.mean(l1)*100)
            resColdBlood.append(np.mean(l2)*100)
            resReRoll.append(np.mean(l3)*100)
            resReRollCB.append(np.mean(l4)*100)
        
    if printMagic:
        '''casting tests'''
        res1d6 = list()
        res2d6 = list()   
        res3d6 = list()
        res4d6 = list()
        res5d6 = list()
        for castValue in range(3,20):
            l1=list()
            l2 = list()
            l3 = list()
            l4 = list()
            l5 = list()
            for n in range(N):
                l1.append(cast(dice=1,castValue=castValue))
                l2.append(cast(dice=2,castValue=castValue))
                l3.append(cast(dice=3,castValue=castValue))
                l4.append(cast(dice=4,castValue=castValue))
                l5.append(cast(dice=5,castValue=castValue))
                
            res1d6.append(np.mean(l1)*100)
            res2d6.append(np.mean(l2)*100)
            res3d6.append(np.mean(l3)*100)
            res4d6.append(np.mean(l4)*100)
            res5d6.append(np.mean(l5)*100)
        


    if printCharge:             
        print('         Charges:')
        print('Charge:      %s' % ', '.join('\t{:.1f}'.format(e) for e in chargeRes))
        print('Swiftstride: %s' % ', '.join('\t{:.1f}'.format(e) for e in QSres)    )
        print('----------------------------------------------------------------------------' )
    if printLd:    
        print('         Leadership Tests:')
        print('2d6:                       %s' % ', '.join('\t{:.1f}'.format(e) for e in resNormal)   )
        print('2d6 + reroll:              %s' % ', '.join('\t{:.1f}'.format(e) for e in resReRoll)   )
        print('d26 + Cold Blood:          %s' % ', '.join('\t{:.1f}'.format(e) for e in resColdBlood))
        print('d26 + Cold Blood + reroll: %s' % ', '.join('\t{:.1f}'.format(e) for e in resReRollCB) )
        print('----------------------------------------------------------------------------'  )  
    if printMagic:
        print('         Chance to Pass and dispel:')
        print('1d6:%s' % ', '.join('\t{:.1f}'.format(e) for e in res1d6))
        print('2d6:%s' % ', '.join('\t{:.1f}'.format(e) for e in res2d6))
        print('3d6:%s' % ', '.join('\t{:.1f}'.format(e) for e in res3d6))
        print('4d6:%s' % ', '.join('\t{:.1f}'.format(e) for e in res4d6))
        print('5d6:%s' % ', '.join('\t{:.1f}'.format(e) for e in res5d6))

printTables()  
