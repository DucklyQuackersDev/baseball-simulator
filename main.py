from engine.game import SimulateGame
from loaders.player_loader import load_players
from loaders.team_loader import load_team_identities
from loaders.roster_builder import assign_players_to_teams

def main():
    # Load Data 
    players = load_players("data/players.json")
    team_data = load_team_identities("data/teams.json")
    teams = assign_players_to_teams(players, team_data)

    # Lineups
    for team in teams[:2]:
        team.print_lineup()

    # Simulate 1 game
    home = teams[0]
    away = teams[1]

    home_runs, away_runs = SimulateGame(home, away)

    # Print Box Scores after game
    home.print_box_score()
    away.print_box_score()

if __name__ == "__main__":
    main()