import pytest
from unittest.mock import patch, MagicMock
from models.player import Player, Ratings, PitcherRatings
from models.team import Team
from engine.inning import SimulateInning

# Helpers
def make_player(first, last, position, pitching=False):
    ratings = Ratings(0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50)
    pitcher_ratings = PitcherRatings(0.50, 0.50, 0.50, 0.50) if pitching else None
    return Player(first, last, position, ratings, pitcher_ratings)

def make_team():
    lineup = [make_player(f"Batter{i}", "Test", "RF") for i in range(9)]
    rotation = [make_player("Starter", "Test", "SP", pitching=True)]
    bullpen = [make_player("Reliever", "Test", "RP", pitching=True)]
    return Team("Test", "City", lineup, rotation, bullpen)

# Tests
def test_inning_ends_at_three_outs():
    batting = make_team()
    fielding = make_team()

    with patch("engine.inning.SimulateAtBat", return_value=("groundout", 3)):
        runs = SimulateInning(batting, fielding)

    assert runs == 0

def test_inning_returns_integer():
    batting = make_team()
    fielding = make_team()
    runs = SimulateInning(batting, fielding)
    assert isinstance(runs, int)

def test_inning_runs_never_negative():
    batting = make_team()
    fielding = make_team()
    for _ in range(50):
        batting.reset()
        fielding.reset()
        runs = SimulateInning(batting, fielding)
        assert runs >= 0

def test_lineup_advances_lineup():
    batting = make_team()
    fielding = make_team()

    with patch("engine.inning.SimulateAtBat", return_value=("strikeout", 4)):
        runs = SimulateInning(batting, fielding)

    assert runs == 0

def test_inning_three_homeruns():
    batting = make_team()
    fielding = make_team()

    events = [("homerun", 3), ("homerun", 3), ("homerun", 3), 
              ("groundout", 2), ("groundout", 2), ("groundout", 2)]
    
    with patch("engine.inning.SimulateAtBat", side_effect=events):
        runs = SimulateInning(batting, fielding)

    assert runs == 3