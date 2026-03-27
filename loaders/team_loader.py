import json
from models.team import Team

def load_team_identities(filepath):
    """Load raw team name and city from JSON"""
    with open(filepath) as f:
        data = json.load(f)
    return data["teams"]