import random
from models.team import Team

def assign_players_to_teams(players, team_data):
    """Randomly distribute players across teams, each team gets balanced roster"""
    position_players = [p for p in players if not p.is_pitcher()]
    starters = [p for p in players if p.position == "SP"]
    relievers = [p for p in players if p.position == "RP"]

    random.shuffle(position_players)
    random.shuffle(starters)
    random.shuffle(relievers)

    num_teams = len(team_data)
    lineup_size = len(position_players) // num_teams
    rotation_size = len(starters) // num_teams
    bullpen_size = len(relievers) // num_teams

    assert lineup_size >= 9, f"Not enough position players for {num_teams} teams - need {num_teams * 9}"
    assert rotation_size >= 1, f"Not enough starters for {num_teams} teams"
    assert bullpen_size >= 1, f"Not enough relievers for {num_teams} teams"

    teams = []
    for i, t in enumerate(team_data):
        lineup = position_players[i * lineup_size : (i + 1) * lineup_size][:9]
        rotation = starters[i * rotation_size : (i + 1) * rotation_size]
        bullpen = relievers[i * bullpen_size : (i + 1) * bullpen_size]

        teams.append(Team(
            name = t["name"],
            city = t["city"],
            lineup = lineup,
            rotation = rotation,
            bullpen = bullpen
        ))

    return teams
