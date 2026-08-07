import sys
from loaders.player_loader    import load_players
from loaders.team_loader      import load_team_identities
from loaders.roster_builder   import assign_players_to_teams
from loaders.schedule_builder import (
    generate_season_schedule,
    verify_schedule,
    verify_stretches,
    get_schedule_summary,
    print_schedule,
    print_calendar,
    print_team_calendar,
    get_team_schedule
)
from engine.game   import SimulateGame
from engine.season import SimulateSeason
from datetime import date

def load_data():
    """Loads and assembles all teams - shared across all modes"""
    players = load_players("data/players.json")
    team_data = load_team_identities("data/teams.json")
    teams = assign_players_to_teams(players, team_data)
    return teams

##Modes

def mode_game(teams):
    """Simulates and prints a single game with full play by play"""
    for team in teams[:2]:
        team.print_lineup()

    home_runs, away_runs = SimulateGame(teams[0], teams[1], silent=False)

    teams[0].print_box_score()
    teams[1].print_box_score()


def mode_series(teams):
    """
    Simulates a short series between two specific teams
    argv[2] = home team
    argv[3] = away team
    argv[4] = series length
    Ex: python main.py series "Americans" "Red Eyes"
    """
    if len(sys.argv) < 4:
        print("Usage: python main.py series <home team> <away team> <games>")
        print(f"Available teams: {', '.join(t.name for t in teams)}")
        return

    home_name     = sys.argv[2]
    away_name     = sys.argv[3]
    series_length = int(sys.argv[4]) if len(sys.argv) > 4 else 3

    home = next((t for t in teams if t.name.lower() == home_name.lower()), None)
    away = next((t for t in teams if t.name.lower() == away_name.lower()), None)

    if home is None:
        print(f"Home team '{home_name}' not found")
        print(f"Available teams: {', '.join(t.name for t in teams)}")
        return

    if away is None:
        print(f"Away team '{away_name}' not found")
        print(f"Available teams: {', '.join(t.name for t in teams)}")
        return

    results = {"home": 0, "away": 0}

    print(f"\n{away.name} @ {home.name} — {series_length} game series")
    print(f"{'=' * 40}")

    for game_num in range(1, series_length + 1):
        print(f"\nGame {game_num}")
        home_runs, away_runs = SimulateGame(home, away, silent=False)

        if home_runs > away_runs:
            results["home"] += 1
        else:
            results["away"] += 1

        print(f"Series: {away.name} {results['away']} - {home.name} {results['home']}")

    print(f"\n{'=' * 40}")
    print(f"Series Final: {away.name} {results['away']} - {home.name} {results['home']}")
    winner = home.name if results["home"] > results["away"] else away.name
    print(f"Series Winner: {winner}")


def mode_season(teams):
    """Simulate a full season and prints standings"""
    schedule = generate_season_schedule(
        teams,
        games_against_division = 4,
        games_against_others = 2,
        start_date = date(2026, 4, 1),
        max_stretch = 3
    )

    #debug
    print(f"First game: {min(g.date for g in schedule)}")
    print(f"Last game:  {max(g.date for g in schedule)}")
    print(f"Games in April 2026: {len([g for g in schedule if g.date.month == 4 and g.date.year == 2026])}")

    verify_schedule(teams, schedule)
    verify_stretches(schedule, teams)
    get_schedule_summary(teams, schedule)

    SimulateSeason(teams, schedule, verbose=False)

    # print first team's calendar as a sample
    print_team_calendar(schedule, teams[0], 2026, 4)


def mode_schedule(teams):
    """Generates and displays a schedule without simulating"""
    schedule = generate_season_schedule(
        teams,
        games_against_division = 4,
        games_against_others    = 2,
        start_date             = date(2026, 4, 1)
    )

    verify_schedule(teams, schedule)
    verify_stretches(schedule, teams)
    get_schedule_summary(teams, schedule)
    print_schedule(schedule)
    print_team_calendar(schedule, teams[0], 2026, 4)    


def mode_team(teams):
    """Simulates a full season then prints a specific team's results"""
    team_name = sys.argv[2] if len(sys.argv) > 2 else teams[0].name
    team      = next((t for t in teams if t.name.lower() == team_name.lower()), None)

    if team is None:
        print(f"Team '{team_name}' not found")
        print(f"Available teams: {', '.join(t.name for t in teams)}")
        return

    schedule = generate_season_schedule(
        teams,
        games_against_division = 4,
        games_against_others   = 2,
        start_date             = date(2026, 4, 1)
    )

    # simulate the full season first
    SimulateSeason(teams, schedule, verbose=False)

    # then show the team's results
    team_schedule = get_team_schedule(schedule, team)

    wins   = sum(1 for g in team_schedule if g.played and
                 ((g.home_team is team and g.home_runs > g.away_runs) or
                  (g.away_team is team and g.away_runs > g.home_runs)))
    losses = sum(1 for g in team_schedule if g.played and
                 ((g.home_team is team and g.home_runs < g.away_runs) or
                  (g.away_team is team and g.away_runs < g.home_runs)))

    print(f"\n{team.city} {team.name} — {wins}W {losses}L")
    print_team_calendar(schedule, team, 2026, 4)

    print(f"\n  {'Date':<12} {'Opponent':<16} {'H/A':<5} {'Result'}")
    print(f"  {'-' * 46}")

    for game in team_schedule:
        is_home  = game.home_team is team
        opponent = game.away_team.name if is_home else game.home_team.name
        ha       = "Home" if is_home else "Away"

        team_score = game.home_runs if is_home else game.away_runs
        opp_score  = game.away_runs if is_home else game.home_runs
        result     = "W" if team_score > opp_score else "L"
        score      = f"{result} {team_score}-{opp_score}"

        print(f"  {str(game.date):<12} {opponent:<16} {ha:<5} {score}")


 ## MAIN ───────────────────────────────────────────────────────────────

MODES = {
    "game":     mode_game,
    "series":   mode_series,
    "season":   mode_season,
    "schedule": mode_schedule,
    "team":     mode_team,
}

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "game"
    teams = load_data()

    if mode not in MODES:
        print(f"Unknown mode: '{mode}'")
        print(f"Available modes: {', '.join(MODES.keys())}")
        return
    
    MODES[mode](teams)


if __name__ == "__main__":
    main()