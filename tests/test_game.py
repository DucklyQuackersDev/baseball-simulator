import pytest
from unittest.mock import patch
from models.player import Player, Ratings, PitcherRatings
from models.team import Team
from engine.game import SimulateGame, should_pull_pitcher, substitute_pitcher

# Helpers
def make_player(first, last, position, pitching=False, stamina=0.50):
    ratings = Ratings(0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50)
    pitching_ratings = PitcherRatings(0.50, 0.50, stamina, 0.50) if pitching else None
    return Player(first, last, position, ratings, pitching_ratings)

def make_team(name="Home"):
    lineup   = [make_player(f"Batter{i}", "Test", "RF") for i in range(9)]
    rotation = [make_player("Starter", "Test", "SP", pitching=True)]
    bullpen  = [make_player("Reliever", "Test", "RP", pitching=True)]
    return Team(name, "City", lineup, rotation, bullpen)

# Simulate Game Tests
def test_game_returns_two_scores():
    home = make_team("Home")
    away = make_team("Away")
    result = SimulateGame(home, away)
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_game_scores_never_negative():
    for _ in range(10):
        home = make_team("Home")
        away = make_team("Away")
        home_runs, away_runs = SimulateGame(home, away)
        assert home_runs >= 0
        assert away_runs >= 0

def test_game_has_a_winner():
    for _ in range(20):
        home = make_team("Home")
        away = make_team("Away")
        home_runs, away_runs = SimulateGame(home, away)
        assert home_runs != away_runs

def test_game_resets_team():
    home = make_team("Home")
    away = make_team("Away")

    SimulateGame(home, away)
    first_index = home.lineup_index

    SimulateGame(home, away)
    assert home.lineup_index != 9

# Should Pull Pitcher tests
def test_starter_not_pulled_under_limit():
    pitcher = make_player("Fresh", "Arm", "SP", pitching=True, stamina=0.50)
    pitcher.game_pitching_stats.pitches = 50
    assert should_pull_pitcher(pitcher, 0) == False

def test_starter_pulled_over_limit():
    pitcher = make_player("Tired", "Arm", "SP", pitching=True, stamina=0.50)
    pitcher.game_pitching_stats.pitches = 105   # over 80 + 0.50 * 40 = 100
    assert should_pull_pitcher(pitcher, 0) == True

def test_reliever_pulled_over_30():
    pitcher = make_player("Short", "Relief", "RP", pitching=True)
    pitcher.game_pitching_stats.pitches = 31
    assert should_pull_pitcher(pitcher, 0) == True

def test_reliever_not_pulled_under_30():
    pitcher = make_player("Fresh", "Relief", "RP", pitching=True)
    pitcher.game_pitching_stats.pitches = 20
    assert should_pull_pitcher(pitcher, 0) == False

def test_high_stamina_pitcher_has_higher_limit():
    high_stamina = make_player("Iron", "Man", "SP", pitching=True, stamina=1.0)
    low_stamina  = make_player("Glass", "Arm", "SP", pitching=True, stamina=0.0)

    high_stamina.game_pitching_stats.pitches = 100
    low_stamina.game_pitching_stats.pitches  = 100

    # high stamina should survive 100 pitches, low stamina should not
    assert should_pull_pitcher(high_stamina, 0) == False
    assert should_pull_pitcher(low_stamina,  0) == True
