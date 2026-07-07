import json
from models.team import Team

def load_team_identities(filepath):
    """
    Load raw team identities from JSON
    Returns a flast list of team dicts - east division, then west
    teams[:8] = east, teams [8:] = west
    """
    with open(filepath) as f:
        data = json.load(f)

    east = data["divisions"]["east"]
    west = data["divisions"]["west"]

    if len(east) != 8 or len(west) != 8:
        raise ValueError(f"Each division must have exactly 8 teams - "
                         f"got {len(east)} and {len(west)}")
    
    print(f"Loaded {len(east) + len(west)} teams - "
          f"{len(east)} East, {len(west)} West")

    return east + west