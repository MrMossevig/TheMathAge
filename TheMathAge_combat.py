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
python TheMathAge_combat.py -tws 3 -tt 6 -tas 1 -twa 7 -aws 5 -as 4 -aa 5 -als 1 -amw D3+1

Or if you just want to input the die-rolls directly:
python TheMathAge_combat.py -tohit 2 -wowound 3 rro -armourroll 4 -wardroll 6 -aa 10

DO NOT USE:
2D6 attacks combined with D3/D6 multiple wounds. It will crash and burn. Unless you're using a supercomputer.
'''

import copy
import argparse

# ws, s, t, w, a, as, wa
characters =  [["eos-heavyinf",   3, 3, 3, 3, 1, 5, 7],
               ["eos-marshal",    5, 4, 4, 3, 3, 4, 7],
               ["eos-prelate",    5, 4, 4, 3, 2, 5, 7],
               ["eos-stank",      3, 6, 6, 7, 1, 1, 7],
               ["he-lionchariot", 5, 5, 4, 4, 2, 3, 7],
               ["koe-duke",       6, 4, 4, 3, 4, 5, 6],
               ["koe-grail",      5, 4, 4, 1, 2, 2, 6],
               ["koe-horse",      3, 3, 3, 1, 1, 7, 7],
               ["koe-paladin",    5, 4, 4, 3, 3, 5, 6],
               ["koe-questing",   4, 4, 3, 1, 1, 2, 6],
               ["koe-realm",      4, 4, 3, 1, 1, 2, 6],
               ["sa-saurus",      3, 4, 4, 1, 2, 4, 7],
               ["sa-stygiosaur",  4, 5, 5, 5, 4, 3, 7],
               ["sa-taurosaur",   3, 6, 6, 6, 4, 3, 7],
               ["ud-dreadsphinx", 5, 6, 8, 5, 4, 4, 7]]

def main(attacker=None,defender=None):
    if (attacker is None and defender is None): 
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
    else:
        '''alternative method of defining characteristics, from attacker/defender objects defined in parent environment'''
        ''' more to come'''
        

    verbose = bool(args.verbose)
    print("Verbose(-v): %d" % verbose)

    global tname
    global tt 
    global tws
    global tw
    global tas
    global twa

    global aname
    global ast
    global aws
    global aa
    global als
    global amw

    global kit

    global tohit
    global towound
    global armourroll
    global wardroll

    global hit_rr
    global wound_rr
    global armour_rr
    global ward_rr

    tname = args.target_name
    aname = args.attacker_name
    if(args.kit):
        kit   = args.kit
    else:
        kit   = []

    # First parsing attacker and targets and kit by name
    initVars()
    parseCharacter(verbose)
    parseKit(verbose)

    # Then overriding with commandline stats
    if(args.target_toughness    ): tt  = int(args.target_toughness    )
    if(args.target_weaponskill  ): tws = int(args.target_weaponskill  )
    if(args.target_wounds       ): tw  = int(args.target_wounds       )
    if(args.target_armoursave   ): tas = int(args.target_armoursave   )
    if(args.target_wardsave     ): twa = int(args.target_wardsave     )

    if(args.attacker_strength    ): ast = int(args.attacker_strength    )
    if(args.attacker_weaponskill ): aws = int(args.attacker_weaponskill )
    if(args.attacker_attacks     ): aa  = args.attacker_attacks
    if(args.attacker_lethal      ): als = bool(int(args.attacker_lethal))

    if(args.attacker_multiple    ):
        try:
            amw = int(args.attacker_multiple)
        except ValueError:
            amw = args.attacker_multiple

    # Calculating to-hit, to wound rolls
    calcDice(verbose)

    # Then overriding these with commandline
    if(args.to_hit    ):
        tohit      = int(args.to_hit[0]    )
        if(len(args.to_hit) > 1):      hit_rr    = parseRrArgs(args.to_hit[1])
    if(args.to_wound  ): 
        towound    = int(args.to_wound[0]  )
        if(len(args.to_wound) > 1):    wound_rr  = parseRrArgs(args.to_wound[1])
    if(args.armourroll): 
        armourroll = int(args.armourroll[0])
        if(len(args.armourroll) > 1): armour_rr = parseRrArgs(args.armourroll[1])
    if(args.wardroll  ): 
        wardroll   = int(args.wardroll[0]  )
        if(len(args.wardroll) > 1):    ward_rr   = parseRrArgs(args.wardroll[1])

    if(verbose):
        print("Target Weapon Skill (-tws): %s" % tws)
        print("Target Toughness    (-tt) : %s" % tt )
        print("Target Armour Save  (-tas): %s" % tas)
        print("Target Ward Save    (-twa): %s" % twa)
                 
        print("Attacker Weapon Skill  (-aws): %s" % aws)
        print("Attacker Strength      (-as) : %s" % ast)
        print("Attacker Attacks       (-aa) : %s" % aa )
        print("Attacker Lethal Strike (-als : %s" % als)
        print("Attacker Multiple W    (-amw): %s" % amw)
        print("");

        print("To hit:      %s, reroll: %s" % (tohit,      hit_rr   ))
        print("To wound:    %s, reroll: %s" % (towound,    wound_rr ))
        print("Armour Roll: %s, reroll: %s" % (armourroll, armour_rr))
        print("Ward Roll:   %s, reroll: %s" % (wardroll,   ward_rr  ))
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

    resolveCombat(verbose)
    sumProb(hitTable)
    sumProb(woundTable)
    sumProb(woundAsTable)
    sumProb(woundWaTable)
    sumProb(woundMwTable) # This applies multiple wounds for "Multiple Wounds on Lethal"
    multiplyAttacks()
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

    if(extraAttacksOnWound):
        print('wound:\t%s+\tAVG' % '+\t'.join('{:d}'.format(e) for e in [row[0] for row in woundMw2Table[:(tw+1)]]))
        print('prob:\t%s\t%.3f' % ('\t'.join('{:.3f}'.format(e) for e in [row[3] for row in woundMw2Table[:(tw+1)]]), woundMw2Table[0][4]))
    else:
        print('wound:\t%s+\tAVG' % '+\t'.join('{:d}'.format(e) for e in [row[0] for row in woundTotTable[:(tw+1)]]))
        print('prob:\t%s\t%.3f' % ('\t'.join('{:.3f}'.format(e) for e in [row[3] for row in woundTotTable[:(tw+1)]]), woundTotTable[0][4]))
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
def initVars():
    global tname
    global tt 
    global tws
    global tw
    global tas
    global twa

    global aname
    global ast
    global aws
    global aa
    global amw
    global als

    # Re-rolls 0 = no reroll, 1 = reroll 1s, 2 = reroll 2s, 7 = reroll fails, -1 = reroll successes (e.g. divine attacks)
    global hit_rr
    global wound_rr
    global armour_rr
    global ward_rr

    global hitBonus
    global woundBonus
    global armourBonus
    global wardBonus

    global woundMin
    global extraAttacksOnWound
    global multipleWoundOnLethal
    global divine

    # Setting default characterstats
    if(not tname): tname = ""
    tt    = 3
    tws   = 3
    tw    = 10
    tas   = 7
    twa   = 7

    if(not aname): aname = ""
    ast   = 3
    aws   = 3
    aa    = 1
    amw   = 1
    als   = False

    hit_rr    = 0
    wound_rr  = 0
    armour_rr = 0
    ward_rr   = 0

    hitBonus   = 0
    woundBonus = 0
    armourBonus = 0
    wardBonus  = 0

    woundMin = 0
    extraAttacksOnWound = 0
    multipleWoundOnLethal = False
    divine = False
def parseCharacter(verbose):
    # Here we will parse the charactoer

    global tt 
    global tws
    global tw
    global tas
    global twa

    global ast
    global aws
    global aa

    found_attacker = False
    found_target   = False

    for row in characters:
        if(row[0] == aname):
            print("Found Attacker: %s; WS%d, S%d, A%d" % (row[0], row[1], row[2], row[5]))
            aws = row[1]
            ast = row[2]
            aa  = row[5]
            found_attacker = True
        if(row[0] == tname):
            print("Found Target: %s; WS%d, T%d, W%s, AS%d, WA%d" % (row[0], row[1], row[3], row[4], row[6], row[7]))
            tws = row[1]
            tt  = row[3]
            tw  = row[4]
            tas = row[6]
            twa = row[7]
            found_target = True
            
    if(not found_attacker):
        print("Could not find attacker '%s'. Using default values." % aname)

    if(not found_target):
        print("Could not find target '%s'. Using default values." % tname)


def parseKit(verbose):

    global tt 
    global tws
    global tw
    global tas
    global twa

    global ast
    global aws
    global aa
    global als
    global amw

    global hit_rr
    global wound_rr
    global armour_rr
    global ward_rr

    global hitBonus
    global woundBonus
    global armourBonus
    global wardBonus

    global divine
    global extraAttacksOnWound
    global multipleWoundOnLethal
    global woundMin

    for item in kit:
        # Virtues, Oaths and Blessing
        if   (item == "audacity"):
            print("Virtue: Audacity")
            hit_rr   = 7 # Reroll fails
            wound_rr = 7 # Reroll fails
        elif (item == "might"):
            print("Virtue: Might")
            aa  += 1
            ast += 1
            extraAttacksOnWound = 1
        elif (item == "renown"):
            print("Virtue: Renown")
            als = True
            amw = "D3+1"
            multipleWoundOnLethal = True
        elif (item == "qo"):
            print("Oath: Questing Oath")
            amw = 2
        elif (item == "go"):
            print("Oath: Grail Oath")
            aws += 1
        elif (item == "fotg"):
            print("Blessing: Favour of the Grail")
            if (armourBonus > 0): twa = 5
        elif (item == "fotk"):
            print("Blessing: Favour of the King")
            if (ast >= 5): twa = 5
        # Magical Weapons
        elif (item == "axeofbattle"):
            print("Kit: Axe of Battle")
            woundMin = 3
            aa = 6
        elif (item == "blessedsword"):
            print("Kit: Blessed Sword")
            divine = True
            wound_rr = 7  # Reroll fails
            ward_rr  = -1 # Reroll succesful wardsaves
        elif (item == "fleshrender"):
            print("Kit: Flesrender")
            armourBonus += 1
            ast += 2
        elif (item == "dragonlance"):
            print("Kit: Dragon Lance")
            amw = "D3"
            ast += 2
        # Magical Armour
        elif (item == "crusadershelm"):
            print("Kit: Crusader's Helm")
            tas -= 1
            armour_rr = 7
        elif (item == "bluffershelm"):
            print("Kit: Bluffer's Helm")
            tas -= 1
            wound_rr = -1
        elif (item == "dragonscalehelm"):
            print("Kit: Dragonscale Helm")
            tas -= 1
        elif (item == "dragonmantle"):
            print("Kit: Dragon Mantle")
            tas -= 2
        elif (item == "hardenedshield"):
            print("Kit: Hardened Shield")
            tas -= 2
        # Enchanted items
        elif (item == "pos"):
            print("Kit: Potion of Strength")
            ast += 2
        # Mundane Weapons
        elif (item == "greatweapon"):
            print("Kit: Great Weapon")
            ast += 2
        elif (item == "lance"):
            print("Kit: Lance")
            ast += 2
        # Mundane Armour
        elif (item == "horse"):
            print("Kit: Horse")
            tas -= 1
        elif (item == "hippogriff"):
            print("Kit: Hippogriff")
            tas -= 1
        elif (item == "barding"):
            print("Kit: Barding")
            tas -= 1
        elif (item == "shield"):
            print("Kit: Shield")
            tas -= 1
        # Other
        elif (item == "thunder"):
            print("Thunderous Charge")
            ast += 1

def calcDice(verbose):
    global tohit
    global towound
    global armourroll
    global wardroll

    # To hit, lookup table
    tohit      = hitStats[tws][aws] + hitBonus

    # To wound, can never be better than 2+ or worse than 6+
    towound    = (tt+4 - ast ) + woundBonus
    if (towound < 2):
        towound = 2
    elif (towound > 6):
        towound = 6
    if towound < woundMin:
        towound = woundMin
    
    # Armour, can never be better than 2+
    armourroll = (tas + (ast-3) + armourBonus)
    if (armourroll < 2):
        armourroll = 2

    # Ward, can never be better than 2+
    wardroll   = (twa + wardBonus)
    if (wardroll < 2):
        wardroll = 2


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

def getHit(die):
    return (die >= tohit)

def getWound(die):
    return (die >= towound)

def getWoundAs(die):
    return (die < armourroll)

def getWoundWa(die):
    return (die < wardroll)

def resolveCombat(verbose):
    # Here we will resolve the combat and get the percentage chance for a wound per attack
    # There are 4 rolls; hit, wound, armour save and ward save. Because each can be rerolled once we need 8 rolls.

    prob  = 1/6

    # First die, to hit
    for die1 in range(1,7):
        prob1   = prob
        hit = getHit(die1)

        if ((not hit) and (not hit_rr)):
            closeLoop(0, prob1)
            continue
        
        # Second die, to hit reroll
        for die2 in range(1,7):
            prob2   = prob1   * prob

            if(hit and (hit_rr == -1)): # Reroll succesful hit
                hit2 = getHit(die2)
            elif((not hit) and (die1 <= hit_rr)):
                hit2 = getHit(die2)
            else:
                hit2 = hit

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

                if ((not wound) and (not wound_rr)):
                    closeLoop(2, prob3)
                    continue

                # Fourth die, to wound reroll
                for die4 in range(1,7):
                    prob4   = prob3   * prob

                    if(wound and (wound_rr == -1)): # Reroll succesful wound
                        wound2  = getWound(die4)
                        lethal2 = (die4 == 6)
                    elif((not wound) and (die3 <= wound_rr)):
                        wound2  = getWound(die4)
                        lethal2 = (die4 == 6)
                    else:
                        wound2  = wound
                        lethal2 = lethal

                    if (not wound2):
                        closeLoop(3, prob4)
                        continue
                    else:
                        woundTable[1][1] += prob4
                        woundTable[1][2] += 1

                    # Fifth die, armour save
                    for die5 in range(1,7):
                        prob5   = prob4   * prob

                        wound_as = (getWoundAs(die5) or (lethal and als))

                        if((not wound_as) and (not armour_rr)):
                            closeLoop(4, prob5)
                            continue


                        # Sixth die, armour save reroll
                        for die6 in range(1,7):
                            prob6   = prob5   * prob
                            if(not (lethal2 and als)): # No need to reroll armour if lethal strike
                                if((not wound_as) and (armour_rr == -1)): # Reroll succesfull save (i.e not wound)
                                    wound_as2 = getWoundAs(die6)
                                elif(wound_as and (die5 <= armour_rr)): # Re-roll failed armour saves (i.e. wound)
                                    wound_as2 = getWoundAs(die6)
                                else:
                                    wound_as2 = wound_as

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

                                if ((not wound_wa) and (not ward_rr)):
                                    closeLoop(6, prob7)
                                    continue


                                # Eight die, ward save reroll
                                for die8 in range(1,7):
                                    prob8   = prob7   * prob
                                    
                                    if((not wound_wa) and (ward_rr == -1)): # Reroll succesfull save (i.e not wound)
                                        wound_wa2 = getWoundWa(die8)
                                    elif(wound_wa and (die7 <= wound_rr)): # Reroll failed save (i.e wound)
                                        wound_wa2 = getWoundWa(die8)
                                    else:
                                        wound_wa2 = wound_wa


                                    if (not wound_wa2):
                                        closeLoop(7, prob8)
                                        continue
                                    else:
                                        woundWaTable[1][1] += prob8
                                        woundWaTable[1][2] += 1

                                    if((not multipleWoundOnLethal) or lethal2):
                                        if(amw == "D3"):
                                            for die9 in range(1,4):
                                                prob9 = prob8   * prob*2
                                                woundMwTable[wound_wa2*die9][1] += prob9
                                                woundMwTable[wound_wa2*die9][2] += 1
                                        elif(amw == "D3+1"):
                                            for die9 in range(1,4):
                                                prob9 = prob8   * prob*2
                                                woundMwTable[wound_wa2*(die9+1)][1] += prob9
                                                woundMwTable[wound_wa2*(die9+1)][2] += 1
                                        elif(amw == "D6"):
                                            for die9 in range(1,7):
                                                prob9 = prob8   * prob
                                                woundMwTable[wound_wa2*die9][1] += prob9
                                                woundMwTable[wound_wa2*die9][2] += 1
                                        else:
                                            # Default case
                                            woundMwTable[wound_wa2*int(amw)][1] += prob8
                                            woundMwTable[wound_wa2*int(amw)][2] += 1
                                    else:
                                        # If multipleWoundOnLethal and not lethal
                                        woundMwTable[wound_wa2][1] += prob8
                                        woundMwTable[wound_wa2][2] += 1
                                       
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



def multiplyAttacks():
    # Multiplying attacks to see how many wounds the model/unit makes
    if (aa == "D3"):
        for die1 in range(1,4):
            addProb(die1, 0, 1/3, 0, extraAttacksOnWound)
    elif (aa == "D6"):
        for die1 in range(1,7):
            addProb(die1, 0, 1/6, 0, extraAttacksOnWound)
    elif (aa == "D6+1"):
        for die1 in range(1,7):
            addProb(die1+1, 0, 1/6, 0, extraAttacksOnWound)
    elif (aa == "2D6"):
        for die1 in range(1,7):
            for die2 in range(1,7):
                addProb(die1+die2, 0, 1/36, 0, extraAttacksOnWound)
    else:
        addProb(int(aa), 0, 1.0, 0, extraAttacksOnWound)


def addProb(attacks, eattacks, cumProb, cumWound, ea):
    # This is a recursive function that calls itself to populate the number of attacks
    
    global extraAttacksOnWound

    if (attacks > 0):
        if extraAttacksOnWound:
            for wound in range(0, woundWaTable[3][4]+1):
                addProb(attacks-1,
                        eattacks + wound*ea,
                        cumProb  * woundWaTable[wound][1],
                        cumWound + wound,
                        ea)
        else:
            for wound in range(0, woundMwTable[3][4]+1):
                addProb(attacks-1,
                        0,
                        cumProb  * woundMwTable[wound][1],
                        cumWound + wound,
                        0)

    elif (eattacks > 0):
        for wound in range(0, woundWaTable[3][4]+1):
            addProb(0,
                    eattacks-1,
                    cumProb  * woundWaTable[wound][1],
                    cumWound + wound,
                    0)
    else:
        woundTotTable[cumWound][1] += cumProb
        woundTotTable[cumWound][2] += 1
        if(amw == "D3"):
            for die9 in range(1,4):
                woundMw2Table[cumWound*die9][1] += cumProb*1/3
                woundMw2Table[cumWound*die9][2] += 1
        elif(amw == "D3+1"):
            for die9 in range(1,4):
                woundMw2Table[cumWound*(die9+1)][1] += cumProb*1/3
                woundMw2Table[cumWound*(die9+1)][2] += 1
        elif(amw == "D6"):
            for die9 in range(1,7):
                woundMw2Table[cumWound*die9][1] += cumProb*1/6
                woundMw2Table[cumWound*die9][2] += 1
        else:
            woundMw2Table[cumWound*int(amw)][1] += cumProb
            woundMw2Table[cumWound*int(amw)][2] += 1


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

if __name__ == "__main__":
   main()
