from engine.game import SimulateGame
from loaders.player_loader import load_players
from loaders.team_loader import load_team_identities
from loaders.roster_builder import assign_players_to_teams

players = load_players("data/players.json")
team_data = load_team_identities("data/teams.json")
teams = assign_players_to_teams(players, team_data)

## Print Lineups

## Simulate 1 game
SimulateGame()

## Print Box Scores after game
