import random
from engine.at_bat import SimulateAtBat
from engine.baserunning import advance_bases

## Constants
FIRST = 0
SECOND = 1
THIRD = 2

## Half Inning
def SimulateInning(batting_team, fielding_team, silent=False):
    outs  = 0
    runs  = 0
    bases = [None, None, None]

    while outs < 3:
        batter  = batting_team.get_current_batter()
        pitcher = fielding_team.current_pitcher

        event, pitches = SimulateAtBat(batter, pitcher)
        batting_team.advance_lineup()

        pitcher.game_pitching_stats.pitches += pitches

        bases, runs, outs, runs_scored, rbis = advance_bases(event, bases, runs, outs, batter)

        batter.record_at_bat(event, rbis=rbis)
        pitcher.record_pitching(event, runs_scored)

        if not silent:
            print(f"  {batter.short_name:<12} {event:<12} | "
                  f"Bases: {[b.last_name if b else None for b in bases]} | "
                  f"Outs: {outs} | Runs: {runs}")

    fielding_team.current_pitcher.record_pitching("", 0, innings_pitched=1)

    if not silent:
        print(f"  End of inning — Runs scored: {runs}")

    return runs