from engine.game import SimulateGame

## Standings
def initialize_standings(teams):
    """
    Creates a standings dictionary for all teams
    W = Wins, L = Losses, RS = Runs Scored, RA = Runs Against
    """
    return {
        team: {"W": 0, "L": 0, "RS": 0, "RA": 0}
        for team in teams
    }

def update_standings(standings, home_team, away_team, home_runs, away_runs):
    """Updates standings after a game"""
    standings[home_team]["RS"] += home_runs
    standings[home_team]["RA"] += away_runs

    standings[away_team]["RS"] += away_runs
    standings[away_team]["RA"] += home_runs
    
    if home_runs > away_runs:
        standings[home_team]["W"] += 1
        standings[away_team]["L"] += 1
    else:
        standings[home_team]["L"] += 1
        standings[away_team]["W"] += 1

def print_standings(standings, teams):
    """Prints standings split by division and sorted by wins"""
    east = teams[:8]
    west = teams[8:]

    for div_name, division in [("East", east), ("West", west)]:
        print(f"\n  {div_name} Division")
        print(f"  {'Team':<14} {'W':>4} {'L':>4} {'PCT':>6} {'GB':>5} {'RS':>5} {'RA':>5} {'DIFF':>6}")
        print(f"  {'-' * 56}")

        sorted_teams = sorted(
            division,
            key=lambda t: standings[t]["W"],
            reverse=True
        )

        leader_wins = standings[sorted_teams[0]]["W"]
        leader_loss = standings[sorted_teams[0]]["L"]

        for team in sorted_teams:
            w = standings[team]["W"]
            l = standings[team]["L"]
            rs = standings[team]["RS"]
            ra = standings[team]["RA"]
            diff = rs - ra
            pct = w / (w + l) if (w + l) > 0 else 0.000
            gb = ((leader_wins - w) + (l - leader_loss)) / 2
            gb_str = "-" if gb == 0 else f"{gb:.1f}"

            print(f"    {team.name:>14} {w:>4} {l:>4} {pct:>6.3f} {gb_str:>5} "
                  f"{rs:>5} {ra:>5} {diff:>+6}")
            

## Season Simulator
def SimulateSeason(teams, schedule, verbose=False):
    """
    Simulates a full season from a schedule of Game objects
    verbose=True prints every game result
    verbose=False prints progress and standings at end
    """
    standings = initialize_standings(teams)
    total = len(schedule)

    print(f"\nSimulating {total} game season...")

    for i, game in enumerate(schedule):
        home_runs, away_runs = SimulateGame(
            game.home_team,
            game.away_team,
            silent=True
        )

        #update game object with results
        game.home_runs = home_runs 
        game.away_runs = away_runs
        game.played = True

        update_standings(standings, game.home_team, game.away_team, home_runs, away_runs)

        if verbose:
            winner = game.home_team.name if home_runs > away_runs else game.away_team.name
            print(f"  Game {i + 1:>3} {game.date} | "
                  f"{game.away_team.name:<14} {away_runs} @ "
                  f"{game.home_team.name:<14} {home_runs} | "
                  f"W: {winner}")
            
        #print progress at every 1/10th season marker
        if (i + 1) % max(1, total // 10) == 0:
            pct = (i + 1) / total * 100
            print(f"    {i + 1}/{total} games complete ({pct:.0f}%)...")

    print(f"\n{'=' * 60}")
    print(f"Final Standings")
    print(f"{'=' * 60}")
    print_standings(standings, teams)

    return standings