import random
from engine.at_bat import SimulateAtBat
from engine.baserunning import advance_bases

## Constants
FIRST = 0
SECOND = 1
THIRD = 2

## Half Inning
def SimulateInning(offense, defense):
    """Half inning simulation"""
    outs = 0
    runs = 0
    bases = [None, None, None] ##at bases[3] would be home, but we dont need that since no one can occupy home, a runner eaching index 3 that runner instead scores

    while outs < 3:
        batter = offense.get_current_batter()
        pitcher = defense.current_pitcher

        event, pitches = SimulateAtBat(batter, pitcher)
        offense.advance_lineup()
        
        pitcher.game_pitching_stats.pitches += pitches

        bases, runs, outs, runs_scored, rbis = advance_bases(event, bases, runs, outs, batter)

        batter.record_at_bat(event, rbis=rbis)
        pitcher.record_pitching(event, runs_scored)

        print(f"  {batter.short_name:<12} {event:<12} | "
              f"Bases: {bases} | Outs: {outs} | Runs: {runs}")
        
    defense.current_pitcher.record_pitching("", 0, innings_pitched=1)
            
    print(f"  End of inning - Runs scored: {runs}")
    return runs