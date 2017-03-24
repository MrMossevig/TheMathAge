'''
Created on 10. mar. 2017

@author: mrmossevig

License: CC-BY

Example Usage:
Duke with Might and Dragon Lance charging a Stygiosaur:
python TheMathAge_combat.py -tname eos-stank -aname koe-duke -kit might dragonlance

Breath Weapon S3, AP6 vs a Steam Tank:
python TheMathAge_combat.py -tname eos-stank -tohit 1 -armourroll 7 -aa 2D6

If you rather do all the character inputs yourself:
python TheMathAge_combat.py -tws 3 -tt 6 -tas 1 -twa 7 -tw 7 -aws 5 -as 4 -aa 5 -als 1 -amw D3+1

Or if you just want to input the die-rolls directly:
python TheMathAge_combat.py -tohit 2 -towound 3 rro -armourroll 4 -wardroll 6 -aa 10 -tw 10

DO NOT USE:
2D6 attacks combined with D3/D6 multiple wounds. It will crash and burn. Unless you're using a supercomputer.
'''

import copy
import argparse
from unit_objects import unit

# ws, s, t, w, a, as, wa
characters =  [["eos-heavyinf",   3, 3, 3, 3, 1, 5, 7],
               ["eos-marshal",    5, 4, 4, 3, 3, 4, 7],
               ["eos-prelate",    5, 4, 4, 3, 2, 5, 7],
               ["eos-stank",      3, 6, 6, 7, 1, 1, 7],
               ["he-lionchariot", 5, 5, 4, 4, 2, 3, 7],
               ["he-swordmasters",6, 3, 3, 1, 2, 5, 7],
               ["koe-archer",     3, 3, 3, 1, 1, 6, 6],
               ["koe-duke",       6, 4, 4, 3, 4, 5, 6],
               ["koe-grail",      5, 4, 4, 1, 2, 2, 6],
               ["koe-horse",      3, 3, 3, 1, 1, 7, 7],
               ["koe-paladin",    5, 4, 4, 3, 3, 5, 6],
               ["koe-questing",   4, 4, 3, 1, 1, 2, 6],
               ["koe-realm",      4, 4, 3, 1, 1, 2, 6],
               ["ok-tribesmen",   3, 4, 4, 3, 3, 6, 7],
               ["ok-bruisers",    3, 4, 4, 3, 3, 5, 7],
               ["sa-saurus",      3, 4, 4, 1, 2, 4, 7],
               ["sa-skink",       2, 3, 2, 1, 1, 5, 7],
               ["sa-stygiosaur",  4, 5, 5, 5, 4, 3, 7],
               ["sa-taurosaur",   3, 6, 6, 6, 4, 3, 7],
               ["ud-dreadsphinx", 5, 6, 8, 5, 4, 4, 7]]

def main(attacker=None,defender=None):
    if (attacker is None and defender is None):
        defender = unit()
        attacker = unit()
        getCharFromCmdLine = True
    else:
        '''alternative method of defining characteristics, from attacker/defender objects defined in parent environment'''
        getCharFromCmdLine = False

    verbose = True # For now
    # Getting characteristics from name
    if(getCharFromCmdLine):
        args    = ParseCmdLine()
        verbose = populateFromCmdLine(attacker, defender, args)

    print("Verbose(-v): %d" % verbose)

    # Calculating to-hit, to wound rolls
    global tohit
    global towound
    global armourroll
    global wardroll
    calcDice(attacker, defender, verbose)

    # Then overriding these with commandline
    if(getCharFromCmdLine):
        overrideRollsFromCmdLine(attacker, defender, args)

    if(verbose):
        print("Target Weapon Skill (-tws): %s" % defender.WS)
        print("Target Toughness    (-tt) : %s" % defender.T )
        print("Target Armour Save  (-tas): %s" % defender.AS)
        print("Target Ward Save    (-twa): %s" % defender.WA)
                 
        print("Attacker Weapon Skill  (-aws): %s" % attacker.WS)
        print("Attacker Strength      (-as) : %s" % attacker.S )
        print("Attacker Attacks       (-aa) : %s" % attacker.A )
        print("Attacker Lethal Strike (-als : %s" % attacker.special.lethal)
        print("Attacker Multiple W    (-amw): %s" % attacker.special.multiple)
        print("");

        print("To hit:      %s, a.reroll: %s, d.reroll: %s" % (tohit,      attacker.rerolls.hit,    defender.rerolls.hit   ))
        print("To wound:    %s, a.reroll: %s, d.reroll: %s" % (towound,    attacker.rerolls.wound,  defender.rerolls.wound ))
        print("Armour Roll: %s, a.reroll: %s, d.reroll: %s" % (armourroll, attacker.rerolls.armour, defender.rerolls.armour))
        print("Ward Roll:   %s, a.reroll: %s, d.reroll: %s" % (wardroll,   attacker.rerolls.ward,   defender.rerolls.ward  ))
        print("")

    # Creating tables to store the stats. Not all of these are strictly needed but it's okay for debugging purposes
    global hitTable
    global woundTable
    global woundAsTable
    global woundWaTable
    global woundMwTable
    global woundTotTable
    global woundMw2Table

    woundArray = [[0,0,0,0,0]] # Result, prob, frequency, cumsum_prop, extra (AVG, Op-chance)
    for i in range(1,16):
        woundArray.append([0,0,0,0,0]);
        woundArray[i][0] = i

    hitTable      =  copy.deepcopy(woundArray)
    woundTable    =  copy.deepcopy(woundArray)
    woundAsTable  =  copy.deepcopy(woundArray)
    woundWaTable  =  copy.deepcopy(woundArray)
    woundMwTable  =  copy.deepcopy(woundArray)
    woundTotTable =  copy.deepcopy(woundArray)

    for i in range(16, 300):
        woundTotTable.append([0,0,0,0,0]);
        woundTotTable[i][0] =i 

    woundMw2Table  =  copy.deepcopy(woundTotTable)

    resolveCombat(attacker, defender, verbose)
    sumProb(hitTable)
    sumProb(woundTable)
    sumProb(woundAsTable)
    sumProb(woundWaTable)
    sumProb(woundMwTable) # This applies multiple wounds for "Multiple Wounds on Lethal"
    multiplyAttacks(attacker, defender)
    sumProb(woundTotTable)
    sumProb(woundMw2Table)  # While if you have extra attacks, you need to add multiple wounds after extra attacks    

    if (verbose):
        print("To Hit:")
        printStats(hitTable)
        print("To Wound:")
        printStats(woundTable)
        print("After Armour Save:")
        printStats(woundAsTable)
        print("After Ward Save:")
        printStats(woundWaTable)
        print("Multiple Wounds:")
        printStats(woundMwTable)
        print("Total Probability for wounds")
        printStats(woundTotTable)
        print("Multiple Wounds added after extra attacks:")
        printStats(woundMw2Table)

    tw = defender.W
    if(attacker.special.extraAttacksOnWound):
        print('wound:\t%s+\tAVG' % '+\t'.join('{:d}'.format(e) for e in [row[0] for row in woundMw2Table[:(tw+1)]]))
        print('prob:\t%s\t%.3f' % ('\t'.join('{:.3f}'.format(e) for e in [row[3] for row in woundMw2Table[:(tw+1)]]), woundMw2Table[0][4]))
    else:
        print('wound:\t%s+\tAVG' % '+\t'.join('{:d}'.format(e) for e in [row[0] for row in woundTotTable[:(tw+1)]]))
        print('prob:\t%s\t%.3f' % ('\t'.join('{:.3f}'.format(e) for e in [row[3] for row in woundTotTable[:(tw+1)]]), woundTotTable[0][4]))

hitStats = [[4,3,3,3,3,3,3,3,3,3],
            [4,4,3,3,3,3,3,3,3,3],
            [5,4,4,3,3,3,3,3,3,3],
            [5,4,4,4,3,3,3,3,3,3],
            [5,5,4,4,4,3,3,3,3,3],
            [5,5,4,4,4,4,3,3,3,3],
            [5,5,5,4,4,4,4,3,3,3],
            [5,5,5,4,4,4,4,4,3,3],
            [5,5,5,5,4,4,4,4,4,3],
            [5,5,5,5,4,4,4,4,4,4]]

def calcDice(attacker, defender, verbose):
    global tohit
    global towound
    global armourroll
    global wardroll

    # To hit, lookup table
    tohit      = hitStats[defender.WS][attacker.WS] + attacker.bonus.hit + defender.bonus.hit

    # To wound, can never be better than 2+ or worse than 6+
    towound    = (defender.T + 4 - attacker.S) + attacker.bonus.wound + defender.bonus.wound
    if towound < attacker.special.woundMin:
        towound = attacker.special.woundMin
    elif (towound > 6):
        towound = 6
    
    # Armour, can never be better than 2+
    armourroll = (defender.AS + (attacker.S - 3)) + attacker.bonus.armour + defender.bonus.armour
    if (armourroll < 2):
        armourroll = 2

    # Ward, can never be better than 2+
    wardroll   = defender.WA + attacker.bonus.ward + defender.bonus.ward
    if (wardroll < 2):
        wardroll = 2

def resolveCombat(attacker, defender, verbose):
    # Here we will resolve the combat and get the percentage chance for a wound per attack
    # There are 4 rolls; hit, wound, armour save and ward save. Because each can be rerolled once we need 8 rolls.

    global hitTable
    global woundTable
    global woundAsTable
    global woundWaTable
    global woundMwTable

    prob  = 1/6

    # First die, to hit
    for die1 in range(1,7):
        prob1   = prob
        hit = getHit(die1)

        if ((not hit) and (not (attacker.rerolls.hit or defender.rerolls.hit))):
            closeLoop(0, prob1)
            continue
        
        # Second die, to hit reroll
        for die2 in range(1,7):
            prob2   = prob1   * prob
            hit2 = hit

            if(hit and (defender.rerolls.hit == -1)): # Reroll succesful hit
                hit2 = getHit(die2)
            elif((not hit) and (die1 <= attacker.rerolls.hit)):
                hit2 = getHit(die2)

            if (not hit2):
                closeLoop(1, prob2)
                continue
            else:
                hitTable[1][1] += prob2
                hitTable[1][2] += 1


            # Third die, to wound
            for die3 in range(1,7):
                prob3   = prob2   * prob
                
                wound  = getWound(die3)
                lethal = (die3 == 6)

                if ((not wound) and (not (attacker.rerolls.wound or defender.rerolls.wound))):
                    closeLoop(2, prob3)
                    continue

                # Fourth die, to wound reroll
                for die4 in range(1,7):
                    prob4   = prob3   * prob
                    wound2  = wound
                    lethal2 = lethal

                    if(wound and (defender.rerolls.wound == -1)): # Reroll succesful wound
                        wound2  = getWound(die4)
                        lethal2 = (die4 == 6)
                    elif((not wound) and (die3 <= attacker.rerolls.wound)):
                        wound2  = getWound(die4)
                        lethal2 = (die4 == 6)

                    if (not wound2):
                        closeLoop(3, prob4)
                        continue
                    else:
                        woundTable[1][1] += prob4
                        woundTable[1][2] += 1

                    # Fifth die, armour save
                    for die5 in range(1,7):
                        prob5   = prob4   * prob

                        wound_as = (getWoundAs(die5) or (lethal2 and attacker.special.lethal))

                        if((not wound_as) and (not (attacker.rerolls.armour or defender.rerolls.armour))):
                            closeLoop(4, prob5)
                            continue


                        # Sixth die, armour save reroll
                        for die6 in range(1,7):
                            prob6   = prob5   * prob
                            wound_as2 = wound_as

                            if(not (lethal2 and attacker.special.lethal)): # No need to reroll armour if lethal strike
                                if((not wound_as) and (attacker.rerolls.armour == -1)): # Reroll succesfull save (i.e not wound)
                                    wound_as2 = getWoundAs(die6)
                                elif(wound_as and (die5 <= defender.rerolls.armour)): # Re-roll failed armour saves (i.e. wound)
                                    wound_as2 = getWoundAs(die6)

                            if (not wound_as2):
                                closeLoop(5, prob6)
                                continue
                            else:
                                woundAsTable[1][1] += prob6
                                woundAsTable[1][2] += 1

                            # Seventh die, ward save
                            for die7 in range(1,7):
                                prob7   = prob6   * prob

                                wound_wa = getWoundWa(die7)

                                if ((not wound_wa) and (not (attacker.rerolls.ward or defender.rerolls.ward))):
                                    closeLoop(6, prob7)
                                    continue


                                # Eight die, ward save reroll
                                for die8 in range(1,7):
                                    prob8   = prob7   * prob
                                    wound_wa2 = wound_wa

                                    if((not wound_wa) and (attacker.rerolls.ward == -1)): # Reroll succesfull save (i.e not wound)
                                        wound_wa2 = getWoundWa(die8)
                                    elif(wound_wa and (die7 <= defender.rerolls.ward)): # Reroll failed save (i.e wound)
                                        wound_wa2 = getWoundWa(die8)

                                    if (not wound_wa2):
                                        closeLoop(7, prob8)
                                        continue
                                    else:
                                        woundWaTable[1][1] += prob8
                                        woundWaTable[1][2] += 1
                                    
                                    # Ninth die, multiple attacks
                                    asmw = attacker.special.multiple
                                    if(((not attacker.special.multipleWoundOnLethal) or lethal2) and
                                       (defender.W > 1)):
                                        if(asmw == "D3"):
                                            for die9 in range(1,4):
                                                prob9 = prob8   * prob*2
                                                woundMwTable[die9][1] += prob9
                                                woundMwTable[die9][2] += 1
                                        elif(asmw == "D3+1"):
                                            for die9 in range(1,4):
                                                prob9 = prob8   * prob*2
                                                woundMwTable[(die9+1)][1] += prob9
                                                woundMwTable[(die9+1)][2] += 1
                                        elif(asmw == "D6"):
                                            for die9 in range(1,7):
                                                prob9 = prob8   * prob
                                                woundMwTable[die9][1] += prob9
                                                woundMwTable[die9][2] += 1
                                        else:
                                            # Default case
                                            woundMwTable[int(asmw)][1] += prob8
                                            woundMwTable[int(asmw)][2] += 1
                                    else:
                                        # If multipleWoundOnLethal and not lethal
                                        woundMwTable[1][1] += prob8
                                        woundMwTable[1][2] += 1


def getHit(die):
    return (die >= tohit)

def getWound(die):
    return (die >= towound)

def getWoundAs(die):
    return (die < armourroll)

def getWoundWa(die):
    return (die < wardroll)
                                       
def closeLoop(level, prob):
    global hitTable
    global woundTable
    global woundAsTable
    global woundWaTable
    global woundMwTable
    if (level <= 1):
        hitTable[0][1]     += prob
        hitTable[0][2]     += 6**(1-level)
    if (level <= 3):
        woundTable[0][1]   += prob
        woundTable[0][2]   += 6**(3-level)
    if (level <= 5):
        woundAsTable[0][1] += prob
        woundAsTable[0][2] += 6**(5-level)
    if (level <= 7):
        woundWaTable[0][1] += prob
        woundWaTable[0][2] += 6**(7-level)
        woundMwTable[0][1] += prob
        woundMwTable[0][2] += 6**(7-level)

def multiplyAttacks(attacker, defender):
    # Multiplying attacks to see how many wounds the model/unit makes
    aseaow = attacker.special.extraAttacksOnWound
    if (defender.W > 1):
        if (attacker.A == "D3"):
            for die1 in range(1,4):
                addProb(attacker, die1,   0, 1/3, 0, aseaow)
        elif (attacker.A == "D6"):
            for die1 in range(1,7):
                addProb(attacker, die1,   0, 1/6, 0, aseaow)
        elif (attacker.A == "D6+1"):
            for die1 in range(1,7):
                addProb(attacker, die1+1, 0, 1/6, 0, aseaow)
        elif (attacker.A == "2D6"):
            for die1 in range(1,7):
                for die2 in range(1,7):
                    addProb(attacker, die1+die2, 0, 1/36, 0, aseaow)
        else:
            addProb(attacker, int(attacker.A), 0, 1.0, 0, aseaow)
    else:
        addProb(attacker, 1, 0, 1.0, 0, aseaow)



def addProb(attacker, attacks, eattacks, cumProb, cumWound, ea):
    # This is a recursive function that calls itself to populate the number of attacks
    global woundWaTable
    global woundMwTable
    global woundMw2Table
    global woundTotTable

    if (attacks > 0):
        if attacker.special.extraAttacksOnWound:
            for wound in range(0, woundWaTable[3][4]+1):
                addProb(attacker, 
                        attacks-1,
                        eattacks + wound*ea,
                        cumProb  * woundWaTable[wound][1],
                        cumWound + wound,
                        ea)
        else:
            for wound in range(0, woundMwTable[3][4]+1):
                addProb(attacker, 
                        attacks-1,
                        0,
                        cumProb  * woundMwTable[wound][1],
                        cumWound + wound,
                        0)

    elif (eattacks > 0):
        for wound in range(0, woundWaTable[3][4]+1):
            addProb(attacker, 
                    0,
                    eattacks-1,
                    cumProb  * woundWaTable[wound][1],
                    cumWound + wound,
                    0)
    else:
        woundTotTable[cumWound][1] += cumProb
        woundTotTable[cumWound][2] += 1
        if(attacker.special.multiple == "D3"):
            for die9 in range(1,4):
                woundMw2Table[cumWound*die9][1] += cumProb*1/3
                woundMw2Table[cumWound*die9][2] += 1
        elif(attacker.special.multiple == "D3+1"):
            for die9 in range(1,4):
                woundMw2Table[cumWound*(die9+1)][1] += cumProb*1/3
                woundMw2Table[cumWound*(die9+1)][2] += 1
        elif(attacker.special.multiple == "D6"):
            for die9 in range(1,7):
                woundMw2Table[cumWound*die9][1] += cumProb*1/6
                woundMw2Table[cumWound*die9][2] += 1
        else:
            woundMw2Table[cumWound*int(attacker.special.multiple)][1] += cumProb
            woundMw2Table[cumWound*int(attacker.special.multiple)][2] += 1


def sumProb(array):
    sum_p = 0
    sum_f = 0
    avg   = 0
    high  = 0
    for entry in reversed(array):
        sum_p += entry[1]
        sum_f += entry[2]
        avg   += entry[0]*entry[1]
        entry[3] = sum_p
        if (entry[2] != 0 and entry[0] > high):
            high = entry[0] # Finding highest (used for calculcating totWounds after MW)
        

    array[0][4] = avg
    array[1][4] = sum_p
    array[2][4] = sum_f
    array[3][4] = high

def printStats(array):
    # Here we will print the wound statistics
    for entry in array:
        statcurve = ''
        for p in range(1, round(entry[1]*100)):
            statcurve += 'X'
        if (entry[1] != 0):
            print("%d\t%d\t%.4f\t%.4f\t%s" % (entry[0], entry[2], entry[1], entry[3], statcurve))

    print("SUM:\t%d\t%.4f" % (array[2][4], array[1][4]))
    print("AVG:\t%f" % array[0][4])
    print("")

def ParseCmdLine():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v",   "--verbose",  action="store_true")
    
    parser.add_argument("-tname", "--target_name"     )
    parser.add_argument("-tt",  "--target_toughness"  )
    parser.add_argument("-tws", "--target_weaponskill")
    parser.add_argument("-tw",  "--target_wounds"     )
    parser.add_argument("-tas", "--target_armoursave" )
    parser.add_argument("-twa", "--target_wardsave"   )
    
    parser.add_argument("-aname", "--attacker_name"     )
    parser.add_argument("-as" , "--attacker_strength"   )
    parser.add_argument("-aws", "--attacker_weaponskill")
    parser.add_argument("-aa",  "--attacker_attacks"    ) # Can be D3, D6, D6+1, 2D6 or number
    parser.add_argument("-als", "--attacker_lethal"     )
    parser.add_argument("-amw", "--attacker_multiple"   )
    
    parser.add_argument("-kit", "--kit", nargs='*'   ) # list of kit. If e.g. lance it assumes charge and gives +2 strength
    
    parser.add_argument("-towound",    "--to_wound"  , nargs='*') # usage example: -to_wound 1
    parser.add_argument("-tohit",      "--to_hit"    , nargs='*') # usage example: -to_hit 4 rro
    parser.add_argument("-armourroll", "--armourroll", nargs='*') # usage example: -armourroll 2 rrf
    parser.add_argument("-wardroll",   "--wardroll"  , nargs='*') # usage example: -wardroll 5 rrs
    
    args = parser.parse_args()

    return args

def populateFromCmdLine(attacker, defender, args):
    verbose = bool(args.verbose)

    attacker.name = args.attacker_name
    defender.name = args.target_name
    parseCharacter(attacker, defender, verbose)

    # Modifying characteristics from kit
    if(args.kit):
        kit   = args.kit
    else:
        kit   = []
        
    parseKit(attacker, defender, kit, verbose)
    
    # Then overriding with commandline stats
    if(args.target_toughness    ): defender.T  = int(args.target_toughness    )
    if(args.target_weaponskill  ): defender.WS = int(args.target_weaponskill  )
    if(args.target_wounds       ): defender.W  = int(args.target_wounds       )
    if(args.target_armoursave   ): defender.AS = int(args.target_armoursave   )
    if(args.target_wardsave     ): defender.WA = int(args.target_wardsave     )

    if(args.attacker_strength    ): attacker.S  = int(args.attacker_strength    )
    if(args.attacker_weaponskill ): attacker.WS = int(args.attacker_weaponskill )
    if(args.attacker_attacks     ): attacker.A  = args.attacker_attacks
    if(args.attacker_lethal      ): attacker.special.lethal = bool(int(args.attacker_lethal))

    if(args.attacker_multiple    ):
        try:
            attacker.special.multiple = int(args.attacker_multiple)
        except ValueError:
            attacker.special.multiple = args.attacker_multiple

    return verbose

def overrideRollsFromCmdLine(attacker, defender, args):
    global tohit
    global towound
    global armourroll
    global wardroll

    if(args.to_hit    ):
        tohit      = int(args.to_hit[0]    )
        if(len(args.to_hit) > 1):
            rr    = parseRrArgs(args.to_hit[1])
            if(rr < 0):
                defender.rerolls.hit = rr
            else:
                attacker.rerolls.hit = rr
    if(args.to_wound  ): 
        towound    = int(args.to_wound[0]  )
        if(len(args.to_wound) > 1):
            rr  = parseRrArgs(args.to_wound[1])
            if(rr < 0):
                defender.rerolls.wound = rr
            else:
                attacker.rerolls.wound = rr
    if(args.armourroll): 
        armourroll = int(args.armourroll[0])
        if(len(args.armourroll) > 1):
            rr = parseRrArgs(args.armourroll[1])
            if(rr < 0):
                attacker.rerolls.armour = rr
            else:
                defender.rerolls.armour = rr
    if(args.wardroll  ): 
        wardroll   = int(args.wardroll[0]  )
        if(len(args.wardroll) > 1):
            rr   = parseRrArgs(args.wardroll[1])
            if(rr < 0):
                attacker.rerolls.ward = rr
            else:
                defender.rerolls.ward = rr

def parseRrArgs(rerollText):
    # Parses the input string for reroll, e.g. rro or rrs to an understandable variable
    if(rerollText == "rro"):
        return 1
    elif(rerollText == "rrt"):
        return 2
    elif(rerollText == "rrf"):
        return 7
    elif(rerollText == "rrs"):
        return -1
    else:
        print("Do not understand: %s" % rerollText)

def parseCharacter(attacker, defender, verbose):
    # Here we will parse the character

    found_attacker = False
    found_target   = False

    for row in characters:
        if(row[0] == attacker.name):
            print("Found Attacker: %s; WS%d, S%d, A%d" % (row[0], row[1], row[2], row[5]))
            attacker.WS = row[1]
            attacker.S  = row[2]
            attacker.A  = row[5]
            found_attacker = True
        if(row[0] == defender.name):
            print("Found Target: %s; WS%d, T%d, W%s, AS%d, WA%d" % (row[0], row[1], row[3], row[4], row[6], row[7]))
            defender.WS = row[1]
            defender.T  = row[3]
            defender.W  = row[4]
            defender.AS = row[6]
            defender.WA = row[7]
            found_target = True
            
    if(not found_attacker):
        print("Could not find attacker '%s'. Using default values." % attacker.name)
        attacker.WS = 3
        attacker.S  = 3
        attacker.A  = 1

    if(not found_target):
        print("Could not find target '%s'. Using default values." % defender.name)
        defender.WS = 3
        defender.T  = 3
        defender.W  = 1
        defender.AS = 7
        defender.WA = 7


def parseKit(attacker, defender, kit, verbose):

    for item in kit:
        # Virtues, Oaths and Blessing
        if   (item == "audacity"):
            print("Virtue: Audacity")
            attacker.rerolls.hit   = 7 # Reroll fails
            attacker.rerolls.wound = 7 # Reroll fails
        elif (item == "might"):
            print("Virtue: Might")
            attacker.A += 1
            attacker.S += 1
            attacker.special.extraAttacksOnWound = 1
        elif (item == "renown"):
            print("Virtue: Renown")
            attacker.special.lethal       = True
            attacker.special.multiple     = "D3+1"
            attacker.special.multipleWoundOnLethal = True
        elif (item == "qo"):
            print("Oath: Questing Oath")
            attacker.special.multiple = 2
        elif (item == "go"):
            print("Oath: Grail Oath")
            attacker.WS += 1
        elif (item == "fotg"):
            print("Blessing: Favour of the Grail")
            if (attacker.bonus.armour > 0): defender.WA = 5
        elif (item == "fotk"):
            print("Blessing: Favour of the King")
            if (attacker.S >= 5): defender.WA = 5
        # Magical Weapons
        elif (item == "axeofbattle"):
            print("Kit: Axe of Battle")
            attacker.special.woundMin   = 3
            attacker.A = 6
        elif (item == "blessedsword"):
            print("Kit: Blessed Sword")
            attacker.rerolls.wound = 7  # Reroll fails
            attacker.rerolls.ward  = -1 # Reroll succesful wardsaves
        elif (item == "fleshrender"):
            print("Kit: Flesrender")
            attacker.bonus.armour += 1
            attacker.S += 2
        elif (item == "dragonlance"):
            print("Kit: Dragon Lance")
            attacker.special.multiple = "D3"
            attacker.S        += 2
        # Magical Armour
        elif (item == "crusadershelm"):
            print("Kit: Crusader's Helm")
            defender.AS -= 1
            defender.rerolls.armour = 7
        elif (item == "bluffershelm"):
            print("Kit: Bluffer's Helm")
            defender.AS -= 1
            defender.rerolls.wound = -1
        elif (item == "dragonscalehelm"):
            print("Kit: Dragonscale Helm")
            defender.AS -= 1
        elif (item == "dragonmantle"):
            print("Kit: Dragon Mantle")
            defender.AS -= 2
        elif (item == "hardenedshield"):
            print("Kit: Hardened Shield")
            defender.AS -= 2
            if ((defender.I - 3) < 1):
                defender.I = 1
            else:
                defender.I -= 3
        # Enchanted items
        elif (item == "pos"):
            print("Kit: Potion of Strength")
            attacker.S += 2
        # Mundane Weapons
        elif (item == "greatweapon"):
            print("Kit: Great Weapon")
            attacker.S += 2
        elif (item == "lance"):
            print("Kit: Lance")
            attacker.S += 2 # Implicit: Charge
        # Mundane Armour
        elif (item == "horse"):
            print("Kit: Horse")
            defender.AS -= 1
        elif (item == "hippogriff"):
            print("Kit: Hippogriff")
            defender.AS -= 1
        elif (item == "barding"):
            print("Kit: Barding")
            defender.AS -= 1
        elif (item == "shield"):
            print("Kit: Shield")
            defender.AS -= 1
        # Other
        elif (item == "thunder"):
            print("Thunderous Charge")
            defender.S += 1
        elif (item == "AP1"):
            print("Armour Piercing(1)")
            attacker.bonus.armour +=1

if __name__ == "__main__":
   main()
