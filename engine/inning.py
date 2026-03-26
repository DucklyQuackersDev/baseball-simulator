import random
from engine.at_bat import SimulateAtBat
from engine.baserunning import advance_bases

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
        
        bases, runs, outs = advance_bases(event, bases, runs, outs)

        print(f"Event: {event} | Bases: {bases} | Outs: {outs} | Runs: {runs}")
            
    print("End of Inning")
    print("runs:", runs)
    return runs