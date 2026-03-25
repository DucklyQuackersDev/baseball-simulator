import random

FIRST = 0
SECOND = 1
THIRD = 2

##single pitch simulation
def SimulatePitch():
    pitchRoll = random.randrange(0, 1000)
    
    if pitchRoll < 250:
        outcome = "ball"
    elif pitchRoll > 600:
        outcome = "strike"
    else:
        outcome = "contact"

    return outcome

##Full At Bat
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
                outcome = "out"                
                break
                
    if strikes == 3:
        outcome = "strike out"
    
    if balls == 4:
        outcome = "walk"
    
    ##print(outcome)
    return outcome

def SimulateInning():
    outs = 0
    runs = 0

    bases = [False, False, False] ##at bases[3] would be home, but we dont need that since no one can occupy home, a runner eaching index 3 that runner instead scores

    while outs < 3:
        event = SimulateAtBat()
        ## Baserunning and out logic
        match event:
            case "out":
                type = "ground out"
                outs+=1
                # TODO: add double plays and sac fly

            case "strike out":
                type = "strike"
                outs+=1

            case "walk":
                if bases[FIRST] and bases[SECOND] and bases[THIRD]: ##bases loaded
                    runs+=1
                elif bases[FIRST] and bases[SECOND]: ##1st and 2nd
                    bases[THIRD] = True
                elif bases[FIRST]: ##1st
                    bases[SECOND] = True

                bases[FIRST] = True
                
            case "single":
                if bases[THIRD]: ##Runner on third scores
                    runs += 1
                    bases[THIRD] = False

                if bases[SECOND]: ##Runner on second advances
                    bases[THIRD] = True
                    bases[SECOND] = False

                if bases[FIRST]: ##Runner on first advances
                    bases[SECOND] = True
                    bases[FIRST] = False

                bases[FIRST] = True ##batter takes 1st

                # TODO: 1st to third depending on speed and hit location

            case "double":
                if bases[THIRD]: ##runner on third scores
                    runs+=1
                    bases[THIRD] = False

                if bases[SECOND]: ##runner on second scores
                    runs+=1
                    bases[SECOND] = False

                if bases[FIRST]: ##runner on 1st advances to 3rd
                    bases[THIRD] = True
                    bases[FIRST] = False

                bases[SECOND] = True ##batter takes second

                # TODO: 1st to score depending on speed and hit location

            case "triple":
                runs += sum(bases)
                bases = [False, False, True] ##Runners empty, batter takes third

            case "homerun":
                runs += sum(bases) + 1
                bases = [False, False, False]
        print(f"Event: {event} | Bases: {bases} | Outs: {outs} | Runs: {runs}")
            
    print("End of Inning")
    print("runs:", runs)
    return runs

def SimulateGame():
    home_runs = 0
    away_runs = 0

    for inning in range(1, 10):
        print(f"--- Inning {inning} ---")

        ##top of inning
        print("Top of inning")
        away_runs += SimulateInning()

        ##bottom of inning, skip if home is leading in 9th
        if inning == 9 and home_runs > away_runs:
            print("Bottom of 9th Skipped")
            break
        
        print("Bottom of inning")
        home_runs += SimulateInning()

    ##Extra innings
    extra = 10
    while home_runs == away_runs:
        print(f"--- Inning {extra} ---")
        print("Top of inning")
        away_runs += SimulateInning()
        print("Bottom of inning")
        home_runs += SimulateInning()

    print(f"Final: Away {away_runs} - Home {home_runs}")
    return home_runs, away_runs


SimulateGame()

                
                

