'''
Created on 20. feb. 2017

@author: mrmossevig

License: CC-BY
'''

import copy
import math
import heapq
import argparse

def main():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",  action="store_true")
    parser.add_argument("-d", "--sides", default=6)
    args = parser.parse_args()

    verbose = args.verbose
    sides = int(args.sides)
 
    print("Verbose(-v): %d" % verbose)
    print("Sides  (-d): %d" % sides)
    
    # Creating and printing diethrow tables
    createTables(sides)
    printTables(verbose)

def sum_prob(array):
    sum_p = 0
    sum_f = 0
    avg   = 0
    for entry in array:
        sum_p += entry[1]
        sum_f += entry[2]
        avg   += entry[0]*entry[1]
        entry[3] = sum_p

    array[0][4] = avg
    array[1][4] = sum_p
    array[2][4] = sum_f

def print_prob(array):
    for entry in array:
        statcurve = ''
        for p in range(1, round(entry[1]*100)):
            statcurve += 'X'
        if (entry[2] != 0):
            print("%d\t%d\t%.4f\t%.4f\t%s" % (entry[0], entry[2], entry[1], entry[3], statcurve))

    print("SUM:\t%d\t%.4f" % (array[2][4], array[1][4]))
    print("AVG:\t%f" % array[0][4])

def createTables(sides):
    ### Creating diethrow arrays ###

    # Normal die rolls
    global onedie       
    global twodice      
    global threedice    
    global fourdice     
    global fivedice     
    global sixdice      

    # Reroll ones
    global od_rerollone 
    global twd_rerollone
    global thd_rerollone

    # Drop low/high
    global thd_droplow  
    global thd_drophigh 

    # Reroll, take highest
    global twd_rr       
    global thd_dl_rr    

    # Reroll ones + drop low
    global thd_rro_dl

    # Drop low, add d3 (SS + Audacity)
    global thd_dl_d3

    # Magic throws
    global twd_opchance
    global thd_opchance
    global fod_opchance
    global fid_opchance

    ### Filling diethrow arrays with 0s ###

    diearray = [[0,0,0,0,0]] # Result, prob, frequency, cumsum_prop, extra (AVG, Op-chance)
    for i in range(1,37):
        diearray.append([0,0,0,0,0]);
        diearray[i][0] = i

    # Normal die rolls
    onedie        = copy.deepcopy(diearray)
    twodice       = copy.deepcopy(diearray)
    threedice     = copy.deepcopy(diearray)
    fourdice      = copy.deepcopy(diearray)
    fivedice      = copy.deepcopy(diearray)
    sixdice       = copy.deepcopy(diearray)

    # Reroll ones
    od_rerollone  = copy.deepcopy(diearray)
    twd_rerollone = copy.deepcopy(diearray)
    thd_rerollone = copy.deepcopy(diearray)

    # Drop low/high
    thd_droplow   = copy.deepcopy(diearray)
    thd_drophigh  = copy.deepcopy(diearray)

    # Reroll, take highest
    twd_rr       = copy.deepcopy(diearray)
    thd_dl_rr    = copy.deepcopy(diearray)

    # Reroll ones + drop low
    thd_rro_dl    = copy.deepcopy(diearray)

    # Drop low, add d3 (SS + Audacity)
    thd_dl_d3     = copy.deepcopy(diearray)

    # Magic throws
    twd_opchance  = copy.deepcopy(diearray)
    thd_opchance  = copy.deepcopy(diearray)
    fod_opchance  = copy.deepcopy(diearray)
    fid_opchance  = copy.deepcopy(diearray)

    prob = 1/sides

    ### Populating diethrow arrays ###    

    # First die
    for die1 in range(1,sides+1):
        result1 = die1
        prob1   = prob
        onedie[result1][1] += prob1
        onedie[result1][2] += 1
    
        # Second die
        for die2 in range(1,sides+1):
            result2 = result1 + die2
            prob2   = prob1   * prob
            twodice[result2][1] += prob2
            twodice[result2][2] += 1
    
            # Adding probs for 1D6 with reroll one
            if(die1 == 1):
                od_rerollone[die2][1] += prob2
                od_rerollone[die2][2] += 1
            else:
                od_rerollone[die1][1] += prob2
                od_rerollone[die1][2] += 1
    
            # Third die
            for die3 in range(1,sides+1):
                result3 = result2 + die3
                prob3   = prob2   * prob
                threedice[result3][1] += prob3
                threedice[result3][2] += 1
    
                # Add result to drop-low (Swiftstride)
                result_dl = result3 - min(die1, die2, die3)
                thd_droplow[result_dl][1] += prob3
                thd_droplow[result_dl][2] += 1

                # Add result to drop-high (cold-blooded Ld)
                result_dh = result3 - max(die1, die2, die3)
                thd_drophigh[result_dh][1] += prob3
                thd_drophigh[result_dh][2] += 1
                
                # Add result to magic die throw with two dice
                if ((die1 == 6) and (die2 == 6)):
                    twd_opchance[result3][1] += prob3
                    twd_opchance[result3][2] += 1
                    twd_opchance[4][4]       += prob3
                else:
                    twd_opchance[result2][1] += prob3
                    twd_opchance[result2][2] += 1
                
                # Fourth die
                for die4 in range(1,sides+1):
                    result4 = result3 + die4
                    prob4   = prob3   * prob
                    fourdice[result4][1] += prob4
                    fourdice[result4][2] += 1

                    # Add result to Drop low, add d3 (SS + Audacity)
                    if die4 in range (1,4):
                        thd_dl_d3[result_dl + die4][1] += prob3*(1/3)
                        thd_dl_d3[result_dl + die4][2] += 1

                    # Add result to magic die throw with three dice
                    if (   (die1 == 6) and (die2 == 6)
                        or (die1 == 6) and (die3 == 6)
                        or (die2 == 6) and (die3 == 6)):
                        thd_opchance[result4][1] += prob4
                        thd_opchance[result4][2] += 1
                        thd_opchance[4][4]       += prob4
                    else:
                        thd_opchance[result3][1] += prob4
                        thd_opchance[result3][2] += 1
            
                    # Adding probs for 2D6 with reroll one
                    if ((die1 == 1) and (die2 == 1)):
                        twd_rerollone[die3+die4][1] += prob4
                        twd_rerollone[die3+die4][2] += 1
                    elif (die1 == 1):
                        twd_rerollone[die2+die3][1] += prob4
                        twd_rerollone[die2+die3][2] += 1
                    elif (die2 == 1):
                        twd_rerollone[die1+die3][1] += prob4
                        twd_rerollone[die1+die3][2] += 1
                    else:
                        twd_rerollone[die1+die2][1] += prob4
                        twd_rerollone[die1+die2][2] += 1
    
                    # Result for charge+RR  - only used for average charge length
                    result_rr1 = die1 + die2
                    result_rr2 = die3 + die4
                    result_rr  = max(result_rr1, result_rr2)
                    twd_rr[result_rr][1] += prob4
                    twd_rr[result_rr][2] += 1
    
                    # Fifth die
                    for die5 in range(1,sides+1):
                        result5 = result4 + die5
                        prob5   = prob4   * prob
                        fivedice[result5][1] += prob5
                        fivedice[result5][2] += 1
    
                        # Add result to magic die throw with four dice
                        # If the sum of the two largest equals 12, we have OP
                        if (sum(heapq.nlargest(2,[die1,die2,die3,die4])) == 12):
                            fod_opchance[result5][1] += prob5
                            fod_opchance[result5][2] += 1
                            fod_opchance[4][4]       += prob5
                        else:
                            fod_opchance[result4][1] += prob5
                            fod_opchance[result4][2] += 1
    
                        # Sixth die
                        for die6 in range(1,sides+1):
                            result6 = result5 + die6
                            prob6   = prob5   * prob
                            sixdice[result6][1] += prob6
                            sixdice[result6][2] += 1
    
                            # Add result to magic die throw with five dice
                            # If the sum of the two largest equals 12, we have OP
                            if (sum(heapq.nlargest(2,[die1,die2,die3,die4,die5])) == 12):
                                fid_opchance[result6][1] += prob6
                                fid_opchance[result6][2] += 1
                                fid_opchance[4][4]       += prob6
                            else:
                                fid_opchance[result5][1] += prob6
                                fid_opchance[result5][2] += 1
    
                            # Adding probs for 2D6 with reroll one
                            if ((die1 == 1) and (die2 == 1) and (die3 == 1)):
                                dice_used = [die4, die5, die6]                         
                            elif ((die1 == 1) and (die2 == 1)):
                                dice_used = [die3 ,die4, die5]
                            elif ((die1 == 1) and (die3 == 1)):
                                dice_used = [die2, die4, die5]
                            elif ((die2 == 1) and (die3 == 1)):
                                dice_used = [die1, die4, die5]
                            elif (die1 == 1):
                                dice_used = [die2, die3, die4]
                            elif (die2 == 1):
                                dice_used = [die1, die3, die4]
                            elif (die3 == 1):
                                dice_used = [die1, die2, die4]
                            else:
                                dice_used = [die1, die2, die3]
                            
                            sum_faces = sum(dice_used)
                            thd_rerollone[sum_faces][1] += prob6
                            thd_rerollone[sum_faces][2] += 1  
    
                            thd_rro_dl[sum_faces - min(dice_used)][1] += prob6
                            thd_rro_dl[sum_faces - min(dice_used)][2] += 1
    
                            # Result for Swiftstride+reroll (drop low, reroll, take highest) - only used for average charge length
                            result_dl1   = die1 + die2 + die3 - min(die1, die2, die3)
                            result_dl2   = die4 + die5 + die6 - min(die4, die5, die6)
                            result_dl_rr = max(result_dl1, result_dl2)
                            thd_dl_rr[result_dl_rr][1] += prob6
                            thd_dl_rr[result_dl_rr][2] += 1
    
    # Summing up probs
    sum_prob(onedie)
    sum_prob(twodice)
    sum_prob(threedice)
    sum_prob(fourdice)
    sum_prob(fivedice)
    sum_prob(sixdice)
    # Drop high/low
    sum_prob(thd_droplow)
    sum_prob(thd_drophigh)
    # Reroll all
    sum_prob(twd_rr)
    sum_prob(thd_dl_rr)
    # Reroll ones
    sum_prob(od_rerollone)
    sum_prob(twd_rerollone)
    sum_prob(thd_rerollone)
    sum_prob(thd_rro_dl)
    # Drop low, add d3
    sum_prob(thd_dl_d3)
    # Magic dice
    sum_prob(twd_opchance)
    sum_prob(thd_opchance)
    sum_prob(fod_opchance)
    sum_prob(fid_opchance)

def printTables(verbose):
    if (verbose == 1):
        print("\n1D6:")
        print_prob(onedie)
    
        print("\n2D6:")
        print_prob(twodice)
        
        print("\n3D6:")
        print_prob(threedice)
    
        print("\n4D6:")
        print_prob(fourdice)
    
        print("\n5D6:")
        print_prob(fivedice)
    
        print("\n6D6:")
        print_prob(sixdice)
    
        print("\n3D6 drop low:")
        print_prob(thd_droplow)
    
        print("\n3D6 drop high:")
        print_prob(thd_drophigh)
    
        print("\n2D6, reroll, take highest:")
        print_prob(twd_rr)
    
        print("\n3D6 drop low, reroll, take highest:")
        print_prob(thd_dl_rr)
    
        print("\n1D6 reroll ones:")
        print_prob(od_rerollone)
    
        print("\n2D6 reroll ones:")
        print_prob(twd_rerollone)
    
        print("\n3D6 reroll ones:")
        print_prob(thd_rerollone)
    
        print("\n3D6 reroll ones, drop lowest:")
        print_prob(thd_rro_dl)

        print("\n3D6, drop lowest, add d3")
        print_prob(thd_dl_d3)
    
        print("\n2D6 with OP-chance:")
        print_prob(twd_opchance)
    
        print("\n3D6 with OP-chance:")
        print_prob(thd_opchance)
    
        print("\n4D6 with OP-chance:")
        print_prob(fod_opchance)
    
        print("\n5D6 with OP-chance:")
        print_prob(fid_opchance)
    
    print("\nLeaderhip\t2\t3\t4\t5\t6\t7\t8\t9\t10")
    print("Normal\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%" %
          (100*(twodice[2][3]), 100*(twodice[3][3]), 100*(twodice[4][3]), 100*(twodice[5][3]), 100*(twodice[6][3]),
           100*(twodice[7][3]), 100*(twodice[8][3]), 100*(twodice[9][3]), 100*(twodice[10][3])))
    print("Reroll\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%" %
          (100*(1-(1-twodice[2][3])**2), 100*(1-(1-twodice[3][3])**2), 100*(1-(1-twodice[4][3])**2), 100*(1-(1-twodice[5][3])**2), 100*(1-(1-twodice[6][3])**2),
           100*(1-(1-twodice[7][3])**2), 100*(1-(1-twodice[8][3])**2), 100*(1-(1-twodice[9][3])**2), 100*(1-(1-twodice[10][3])**2)))
    print("Cold-blooded\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%" %
          (100*(thd_drophigh[2][3]), 100*(thd_drophigh[3][3]), 100*(thd_drophigh[4][3]), 100*(thd_drophigh[5][3]), 100*(thd_drophigh[6][3]),
           100*(thd_drophigh[7][3]), 100*(thd_drophigh[8][3]), 100*(thd_drophigh[9][3]), 100*(thd_drophigh[10][3])))
    print("CB+Reroll\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%" %
          (100*(1-(1-thd_drophigh[2][3])**2), 100*(1-(1-thd_drophigh[3][3])**2), 100*(1-(1-thd_drophigh[4][3])**2), 100*(1-(1-thd_drophigh[5][3])**2), 100*(1-(1-thd_drophigh[6][3])**2),
           100*(1-(1-thd_drophigh[7][3])**2), 100*(1-(1-thd_drophigh[8][3])**2), 100*(1-(1-thd_drophigh[9][3])**2), 100*(1-(1-thd_drophigh[10][3])**2)))
    
    print("\nCharge Range\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t\tAVG")
    print("Charge\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
          (100, 
           100*(1-twodice[2][3]), 100*(1-twodice[3][3]), 100*(1-twodice[4][3]), 100*(1-twodice[5][3]),  100*(1-twodice[6][3]), 
           100*(1-twodice[7][3]), 100*(1-twodice[8][3]), 100*(1-twodice[9][3]), 100*(1-twodice[10][3]), 100*(1-twodice[11][3]), 
           twodice[0][4]))
    # Equivalent to the one below
    #print("Charge+Reroll\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
    #      (100, 
    #       100*(1-twodice[2][3]**2), 100*(1-twodice[3][3]**2), 100*(1-twodice[4][3]**2), 100*(1-twodice[5][3]**2),  100*(1-twodice[6][3]**2), 
    #       100*(1-twodice[7][3]**2), 100*(1-twodice[8][3]**2), 100*(1-twodice[9][3]**2), 100*(1-twodice[10][3]**2), 100*(1-twodice[11][3]**2), 
    #       twd_rr[0][4]))
    print("Charge+Reroll\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
          (100, 
           100*(1-twd_rr[2][3]), 100*(1-twd_rr[3][3]), 100*(1-twd_rr[4][3]), 100*(1-twd_rr[5][3]),  100*(1-twd_rr[6][3]), 
           100*(1-twd_rr[7][3]), 100*(1-twd_rr[8][3]), 100*(1-twd_rr[9][3]), 100*(1-twd_rr[10][3]), 100*(1-twd_rr[11][3]), 
           twd_rr[0][4]))
    print("Swiftstride\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
          (100,
           100*(1-thd_droplow[2][3]), 100*(1-thd_droplow[3][3]), 100*(1-thd_droplow[4][3]), 100*(1-thd_droplow[5][3]),  100*(1-thd_droplow[6][3]), 
           100*(1-thd_droplow[7][3]), 100*(1-thd_droplow[8][3]), 100*(1-thd_droplow[9][3]), 100*(1-thd_droplow[10][3]), 100*(1-thd_droplow[11][3]),
           thd_droplow[0][4]))
    print("SS+BotS\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
          (100,
           100*(1-thd_rro_dl[2][3]), 100*(1-thd_rro_dl[3][3]), 100*(1-thd_rro_dl[4][3]), 100*(1-thd_rro_dl[5][3]),  100*(1-thd_rro_dl[6][3]),
           100*(1-thd_rro_dl[7][3]), 100*(1-thd_rro_dl[8][3]), 100*(1-thd_rro_dl[9][3]), 100*(1-thd_rro_dl[10][3]), 100*(1-thd_rro_dl[11][3]),
           thd_rro_dl[0][4]))
    # Equivalent to the one below
    #print("SS+Reroll\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" % 
    #      (100,
    #       100*(1-thd_droplow[2][3]**2), 100*(1-thd_droplow[3][3]**2), 100*(1-thd_droplow[4][3]**2), 100*(1-thd_droplow[5][3]**2),  100*(1-thd_droplow[6][3]**2),
    #       100*(1-thd_droplow[7][3]**2), 100*(1-thd_droplow[8][3]**2), 100*(1-thd_droplow[9][3]**2), 100*(1-thd_droplow[10][3]**2), 100*(1-thd_droplow[11][3]**2),
    #       thd_dl_rr[0][4]))
    print("SS+Reroll\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" %
          (100,
           100*(1-thd_dl_rr[2][3]), 100*(1-thd_dl_rr[3][3]), 100*(1-thd_dl_rr[4][3]), 100*(1-thd_dl_rr[5][3]),  100*(1-thd_dl_rr[6][3]),
           100*(1-thd_dl_rr[7][3]), 100*(1-thd_dl_rr[8][3]), 100*(1-thd_dl_rr[9][3]), 100*(1-thd_dl_rr[10][3]), 100*(1-thd_dl_rr[11][3]),
           thd_dl_rr[0][4]))
    print("SS+Audacity\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" %
          (100,
           100*(1-thd_dl_d3[2][3]), 100*(1-thd_dl_d3[3][3]), 100*(1-thd_dl_d3[4][3]), 100*(1-thd_dl_d3[5][3]),  100*(1-thd_dl_d3[6][3]),
           100*(1-thd_dl_d3[7][3]), 100*(1-thd_dl_d3[8][3]), 100*(1-thd_dl_d3[9][3]), 100*(1-thd_dl_d3[10][3]), 100*(1-thd_dl_d3[11][3]),
           thd_dl_d3[0][4]))

    #print("SS+BotS+RR\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f" %
    #      (100,
    #       100*(1-thd_rro_dl[2][3]**2), 100*(1-thd_rro_dl[3][3]**2), 100*(1-thd_rro_dl[4][3]**2), 100*(1-thd_rro_dl[5][3]**2),  100*(1-thd_rro_dl[6][3]**2),
    #       100*(1-thd_rro_dl[7][3]**2), 100*(1-thd_rro_dl[8][3]**2), 100*(1-thd_rro_dl[9][3]**2), 100*(1-thd_rro_dl[10][3]**2), 100*(1-thd_rro_dl[11][3]**2),
    #       thd_rro_dl[0][4]))
    
    print("\nExtra die available:")
    print("Cast/Dispel\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\t17\t18\t19\t\tAVG\tOP")
    print("1D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (0, 100*(1-onedie[2][3]), 100*(1-onedie[3][3]), 100*(1-onedie[4][3]), 100*(1-onedie[5][3]), 100*(1-onedie[6][3]), 
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
           onedie[0][4], 0))
    print("2D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-twd_opchance[1][3]),   100*(1-twd_opchance[2][3]),  100*(1-twd_opchance[3][3]),  100*(1-twd_opchance[4][3]),  100*(1-twd_opchance[5][3]),  100*(1-twd_opchance[6][3] ), 
           100*(1-twd_opchance[7][3]),   100*(1-twd_opchance[8][3]),  100*(1-twd_opchance[9][3]),  100*(1-twd_opchance[10][3]), 100*(1-twd_opchance[11][3]), 100*(1-twd_opchance[12][3]), 
           100*(1-twd_opchance[13][3]),  100*(1-twd_opchance[14][3]), 100*(1-twd_opchance[15][3]), 100*(1-twd_opchance[16][3]), 100*(1-twd_opchance[17][3]), 100*(1-twd_opchance[18][3]), 
           twd_opchance[0][4], 100*twd_opchance[4][4]))
    print("3D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-thd_opchance[1][3]),   100*(1-thd_opchance[2][3]),  100*(1-thd_opchance[3][3]),  100*(1-thd_opchance[4][3]),  100*(1-thd_opchance[5][3]),  100*(1-thd_opchance[6][3] ), 
           100*(1-thd_opchance[7][3]),   100*(1-thd_opchance[8][3]),  100*(1-thd_opchance[9][3]),  100*(1-thd_opchance[10][3]), 100*(1-thd_opchance[11][3]), 100*(1-thd_opchance[12][3]), 
           100*(1-thd_opchance[13][3]),  100*(1-thd_opchance[14][3]), 100*(1-thd_opchance[15][3]), 100*(1-thd_opchance[16][3]), 100*(1-thd_opchance[17][3]), 100*(1-thd_opchance[18][3]), 
           thd_opchance[0][4], 100*thd_opchance[4][4]))
    print("4D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-fod_opchance[1][3]),   100*(1-fod_opchance[2][3]),  100*(1-fod_opchance[3][3]),  100*(1-fod_opchance[4][3]),  100*(1-fod_opchance[5][3]),  100*(1-fod_opchance[6][3] ), 
           100*(1-fod_opchance[7][3]),   100*(1-fod_opchance[8][3]),  100*(1-fod_opchance[9][3]),  100*(1-fod_opchance[10][3]), 100*(1-fod_opchance[11][3]), 100*(1-fod_opchance[12][3]), 
           100*(1-fod_opchance[13][3]),  100*(1-fod_opchance[14][3]), 100*(1-fod_opchance[15][3]), 100*(1-fod_opchance[16][3]), 100*(1-fod_opchance[17][3]), 100*(1-fod_opchance[18][3]), 
           fod_opchance[0][4], 100*fod_opchance[4][4]))
    print("5D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-fid_opchance[1][3]),   100*(1-fid_opchance[2][3]),  100*(1-fid_opchance[3][3]),  100*(1-fid_opchance[4][3]),  100*(1-fid_opchance[5][3]),  100*(1-fid_opchance[6][3] ),
           100*(1-fid_opchance[7][3]),   100*(1-fid_opchance[8][3]),  100*(1-fid_opchance[9][3]),  100*(1-fid_opchance[10][3]), 100*(1-fid_opchance[11][3]), 100*(1-fid_opchance[12][3]), 
           100*(1-fid_opchance[13][3]),  100*(1-fid_opchance[14][3]), 100*(1-fid_opchance[15][3]), 100*(1-fid_opchance[16][3]), 100*(1-fid_opchance[17][3]), 100*(1-fid_opchance[18][3]), 
           fid_opchance[0][4], 100*fid_opchance[4][4]))
    
    print("\nNo extra die available:")
    print("Cast/Dispel\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\t17\t18\t19\t\tAVG\tOP")
    print("1D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (0, 100*(1-onedie[2][3]), 100*(1-onedie[3][3]), 100*(1-onedie[4][3]), 100*(1-onedie[5][3]), 100*(1-onedie[6][3]), 
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
           onedie[0][4], 0))
    print("2D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-twodice[1][3]),   100*(1-twodice[2][3]),  100*(1-twodice[3][3]),  100*(1-twodice[4][3]),  100*(1-twodice[5][3]),  100*(1-twodice[6][3] ), 
           100*(1-twodice[7][3]),   100*(1-twodice[8][3]),  100*(1-twodice[9][3]),  100*(1-twodice[10][3]), 100*(1-twodice[11][3]), 100*(1-twodice[12][3]), 
           100*(1-twodice[13][3]),  100*(1-twodice[14][3]), 100*(1-twodice[15][3]), 100*(1-twodice[16][3]), 100*(1-twodice[17][3]), 100*(1-twodice[18][3]), 
           twodice[0][4], 100*twd_opchance[4][4]))
    print("3D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-threedice[1][3]),   100*(1-threedice[2][3]),  100*(1-threedice[3][3]),  100*(1-threedice[4][3]),  100*(1-threedice[5][3]),  100*(1-threedice[6][3] ), 
           100*(1-threedice[7][3]),   100*(1-threedice[8][3]),  100*(1-threedice[9][3]),  100*(1-threedice[10][3]), 100*(1-threedice[11][3]), 100*(1-threedice[12][3]), 
           100*(1-threedice[13][3]),  100*(1-threedice[14][3]), 100*(1-threedice[15][3]), 100*(1-threedice[16][3]), 100*(1-threedice[17][3]), 100*(1-threedice[18][3]), 
           threedice[0][4], 100*thd_opchance[4][4]))
    print("4D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-fourdice[1][3]),   100*(1-fourdice[2][3]),  100*(1-fourdice[3][3]),  100*(1-fourdice[4][3]),  100*(1-fourdice[5][3]),  100*(1-fourdice[6][3] ), 
           100*(1-fourdice[7][3]),   100*(1-fourdice[8][3]),  100*(1-fourdice[9][3]),  100*(1-fourdice[10][3]), 100*(1-fourdice[11][3]), 100*(1-fourdice[12][3]), 
           100*(1-fourdice[13][3]),  100*(1-fourdice[14][3]), 100*(1-fourdice[15][3]), 100*(1-fourdice[16][3]), 100*(1-fourdice[17][3]), 100*(1-fourdice[18][3]), 
           fourdice[0][4], 100*fod_opchance[4][4]))
    print("5D6\t\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t%.1f%%\t\t%.1f\t%.1f%%" % 
          (100*(1-fivedice[1][3]),   100*(1-fivedice[2][3]),  100*(1-fivedice[3][3]),  100*(1-fivedice[4][3]),  100*(1-fivedice[5][3]),  100*(1-fivedice[6][3] ),
           100*(1-fivedice[7][3]),   100*(1-fivedice[8][3]),  100*(1-fivedice[9][3]),  100*(1-fivedice[10][3]), 100*(1-fivedice[11][3]), 100*(1-fivedice[12][3]), 
           100*(1-fivedice[13][3]),  100*(1-fivedice[14][3]), 100*(1-fivedice[15][3]), 100*(1-fivedice[16][3]), 100*(1-fivedice[17][3]), 100*(1-fivedice[18][3]), 
           fivedice[0][4], 100*fid_opchance[4][4]))
    
    print("\nMiscast/OP\tAmnesia\tCD\tBitV")
    print("1D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (0, 0, 0))
    print("2D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (0,       0,       0))
    print("3D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (thd_opchance[4][4]*100*1/3*0.5, 0,       0))
    print("4D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (fod_opchance[4][4]*100*2/3*0.5, fod_opchance[4][4]*100*1/3*0.5, 0))
    print("5D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (fid_opchance[4][4]*100*3/3*0.5, fid_opchance[4][4]*100*2/3*0.5, fid_opchance[4][4]*100*1/3*0.5))


    print("\nThaumaturgy")
    print("Miscast/OP\tAmnesia\tCD\tBitV")
    print("1D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (0, 0, 0))
    print("2D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (twd_opchance[4][4]*100*1/3*0.5, 0,       0))
    print("3D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (thd_opchance[4][4]*100*2/3*0.5, thd_opchance[4][4]*100*1/3*0.5, 0))
    print("4D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (fod_opchance[4][4]*100*3/3*0.5, fod_opchance[4][4]*100*2/3*0.5, fod_opchance[4][4]*100*1/3*0.5))
    print("5D6\t\t%.1f%%\t%.1f%%\t%.1f%%" % (fid_opchance[4][4]*100*3/3*0.5, fid_opchance[4][4]*100*2/3*0.5, fid_opchance[4][4]*100*1/3*0.5))xb

if __name__ == "__main__":
   main()
