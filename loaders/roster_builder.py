import random
from models.team import Team
from itertools import groupby

def assign_players_to_teams(players, team_data):
    """
    Randomly distribute players across teams, each team guaranteed one of each position
    """
    position_players = [p for p in players if not p.is_pitcher()]
    starters = [p for p in players if p.position == "SP"]
    relievers = [p for p in players if p.position == "RP"]

    num_teams = len(team_data)

    ##Shuffle position group
    by_position = {}
    for p in position_players:
        by_position.setdefault(p.position, []).append(p)

    for pos in by_position:
        random.shuffle(by_position[pos])


    ##Build lineups
    lineups = [[] for _ in range(num_teams)]
    for pos, pool in by_position.items():
        for i, player in enumerate(pool[:num_teams]):
            lineups[i].append(player)

    ##Shuffle lineup for more unique batting orders
    for lineup in lineups:
        random.shuffle(lineup)

    ##Distribute pitchers
    rotation_size = len(starters) // num_teams
    bullpen_size = len(relievers) // num_teams
    
    assert all(len(l) == 9 for l in lineups), "Not all lineups have 9 players"
    assert rotation_size >= 1, f"Not enough starters for {num_teams} teams"
    assert bullpen_size >= 1, f"Not enough relievers for {num_teams} teams"

    teams = []
    for i, t in enumerate(team_data):
        rotation = starters[i * rotation_size : (i + 1) * rotation_size]
        bullpen = relievers[i * bullpen_size : (i + 1) * bullpen_size]

        teams.append(Team(
            name = t["name"],
            city = t["city"],
            lineup = lineups[i],
            rotation = rotation,
            bullpen = bullpen
        ))

    return teams
