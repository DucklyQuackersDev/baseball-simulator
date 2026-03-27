import json
from models.player import Player, Ratings, PitcherRatings

def load_ratings(data):
    """Builds rating object from JSON"""
    return Ratings(
        contact = data["contact"],
        power = data["power"],
        discipline = data["discipline"],
        speed = data["speed"],
        gb_rate = data["gb_rate"],
        arm_strength = data["arm_strength"],
        fielding = data["fielding"]
    )

def load_pitching_ratings(data):
    """Builds Pitching Ratings from JSON"""
    return PitcherRatings(
        stuff = data["stuff"],
        control = data["control"],
        stamina = data["stamina"],
        gb_rate = data["gb_rate"]
    )

def load_player(data):
    """Build a single player"""
    ratings = load_ratings(data["ratings"])
    pitching_ratings = load_pitching_ratings(data["pitching_ratings"]) if data["pitching_ratings"] else None

    return Player(
        first_name = data["first_name"],
        last_name = data["last_name"],
        position = data["position"],
        ratings = ratings,
        pitching_ratings = pitching_ratings
    )

def load_players(filepath):
    """Load all players from JSON files - returns a list of player objects"""
    with open(filepath) as f:
        data = json.load(f)

    players = [load_players(p) for p in data["players"]]

    print(f"Loaded {len(players)} players from {filepath}")
    return players