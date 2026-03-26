import random

outTypes = ["groundout", "flyout", "lineout"]

## Single pitch simulation
def SimulatePitch():
    pitchRoll = random.randrange(0, 1000)
    
    if pitchRoll < 250:
        outcome = "ball"
    elif pitchRoll > 600:
        outcome = "strike"
    else:
        outcome = "contact"

    return outcome

## Full At Bat
def SimulateAtBat():
    n = 0 ##Pitch Count
    strikes = 0
    balls = 0

    while strikes < 3 and balls < 4:
        pitch = SimulatePitch() ##what is pitch
    

        if pitch == "ball":
            balls+=1
        elif pitch == "strike":
            strikes+=1
        else:
            contactOutcome = random.randrange(0,1000)

            if contactOutcome < 200:
                if strikes != 2:
                    strikes+=1
            elif contactOutcome >= 200 and contactOutcome < 520:
                hitType = random.randrange(0,1338)
        
                if hitType < 872:
                    outcome = "single"
                elif hitType > 871 and hitType < 1130:
                    outcome = "double"
                elif hitType > 1129 and hitType < 1151:
                    outcome = "triple"
                elif hitType > 1150:
                    outcome = "homerun"
                break
            else:
                outcome = random.choice(outTypes)             
                break
                
    if strikes == 3:
        outcome = "strike out"
    
    if balls == 4:
        outcome = "walk"
    
    ##print(outcome)
    return outcome