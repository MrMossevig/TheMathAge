# TheMathAge
Statistical tools for The Ninth Age (T9A).

## TheMathAge_ana.py
Python code for calculating the roll probability analytically (e.g. loops through all possible outcomes) and determines the probability based on that.

### TMA_example_output_ana.txt
Example output from running TheMathAge_ana.py.

### TMA_example_output_ana_w_doce.txt
Example output from running TheMathAge_ana.py with verbose (-v).

## TheMathAge_stat.py
Doing the same as TheMathAge_ana.py but using statisical average over simulations.

### TMA_example_output_stat.txt
Example output from running TheMathAge_stat.py.


## TheMathAge_combat.py
Gives probabilites for the number of wounds given an attacker and a target. Basically doing the same thing as http://tools.druchii.net/9th-Combat-Calculator.php but can take D3/D3+1/D6/2D6 as inputs for number of attacks and multiple wounds. Can also calculate probabilities given "Multiple Wounds on Lethal Strike" and "Extra Attacks on Unsaved Wound".
Inputs are either target/attacker name and kit, character stats, hit/wound/AS/WS rolls or a combination of these.
-v is verbose.

### Example Usage:
#### Duke with Might and Dragon Lance charging a Stygiosaur:
    python TheMathAge_combat.py -tname eos-stank -aname koe-duke -kit might dragonlance

#### Breath Weapon S3, AP6 vs a Steam Tank:
    python TheMathAge_combat.py -tname eos-stank -tohit 1 -armourroll 7 -aa 2D6

#### If you rather do all the character inputs yourself:
    python TheMathAge_combat.py -tws 3 -tt 6 -tas 1 -twa 7 -aws 5 -as 4 -aa 5 -als 1 -amw D3+1

#### Or if you just want to input the die-rolls directly:
    python TheMathAge_combat.py -tohit 2 -wowound 3 rro -armourroll 4 -wardroll 6 -aa 10

#### DO NOT USE:
2D6 attacks combined with D3/D6 multiple wounds. It will crash and burn. Unless you're using a supercomputer.

## Further work
* Clean up code to avoid the usage of global variables
* Get data/stats from an online repository
* Add multi-profile attacks, so you can add multiple profiles (e.g. horses, grail knights, duke and breath weapon)
