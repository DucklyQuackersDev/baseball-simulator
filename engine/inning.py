import random
from engine.at_bat import SimulateAtBat

## Constants
FIRST = 0
SECOND = 1
THIRD = 2

## Half Inning
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