import pytest
from unittest.mock import patch
from models.player import Player, Ratings, PitcherRatings
from engine.at_bat import SimulateAtBat, estimate_pitch_count

# Fixtures

@pytest.fixture
def average_batter():
    return Player(
        first_name = "John",
        last_name = "Doe",
        position = "RF",
        ratings = Ratings(
            contact = 0.5,
            power = 0.5,
            discipline = 0.5,
            speed = 0.5,
            gb_rate = 0.5,
            arm_strength = 0.5,
            fielding = 0.5
        )
    )

@pytest.fixture
def average_pitcher():
    return Player(
        first_name       = "Jane",
        last_name        = "Smith",
        position         = "SP",
        ratings          = Ratings(
            contact      = 0.15,
            power        = 0.10,
            discipline   = 0.20,
            speed        = 0.30,
            gb_rate  = 0.55,
            arm_strength = 0.70,
            fielding     = 0.50
        ),
        pitching_ratings = PitcherRatings(
            stuff       = 0.50,
            control     = 0.50,
            stamina     = 0.50,
            gb_rate = 0.50
        )
    ) 

@pytest.fixture
def elite_batter():
    return Player(
        first_name = "Aaron",
        last_name  = "Judge",
        position   = "RF",
        ratings    = Ratings(
            contact      = 0.95,
            power        = 0.95,
            discipline   = 0.95,
            speed        = 0.70,
            gb_rate  = 0.35,
            arm_strength = 0.90,
            fielding     = 0.88
        )
    )    

@pytest.fixture
def weak_batter():
    return Player(
        first_name = "Bench",
        last_name  = "Player",
        position   = "C",
        ratings    = Ratings(
            contact      = 0.10,
            power        = 0.10,
            discipline   = 0.10,
            speed        = 0.20,
            gb_rate  = 0.70,
            arm_strength = 0.40,
            fielding     = 0.50
        )
    )

@pytest.fixture
def elite_pitcher():
    return Player(
        first_name       = "Gerrit",
        last_name        = "Cole",
        position         = "SP",
        ratings          = Ratings(
            contact      = 0.15,
            power        = 0.10,
            discipline   = 0.20,
            speed        = 0.30,
            gb_rate  = 0.55,
            arm_strength = 0.70,
            fielding     = 0.50
        ),
        pitching_ratings = PitcherRatings(
            stuff       = 0.95,
            control     = 0.92,
            stamina     = 0.88,
            gb_rate = 0.42
        )
    )

@pytest.fixture
def weak_pitcher():
    return Player(
        first_name       = "Mop",
        last_name        = "Up",
        position         = "RP",
        ratings          = Ratings(
            contact      = 0.15,
            power        = 0.10,
            discipline   = 0.20,
            speed        = 0.30,
            gb_rate  = 0.55,
            arm_strength = 0.50,
            fielding     = 0.40
        ),
        pitching_ratings = PitcherRatings(
            stuff       = 0.10,
            control     = 0.10,
            stamina     = 0.30,
            gb_rate = 0.50
        )
    )

# Simulate At Bat Tests

VALID_EVENTS = {"walk", "strikeout", "homerun", "single", "double", "triple", "groundout", "flyout", "lineout"}

def test_at_bat_returns_valid_event(average_batter, average_pitcher):
    event, pitches = SimulateAtBat(average_batter, average_pitcher)
    assert event in VALID_EVENTS

def test_at_bat_returns_positive_pitch_count(average_batter, average_pitcher):
    event, pitches = SimulateAtBat(average_batter, average_pitcher)
    assert pitches > 0

def test_at_bat_returns_tuple(average_batter, average_pitcher):
    result = SimulateAtBat(average_batter, average_pitcher)
    assert isinstance(result, tuple)
    assert len(result) == 2

def test_elite_batter_hits_more_than_weak(elite_batter, weak_batter, average_pitcher):
    samples = 1000
    hit_events = {"single", "double", "triple", "homerun"}

    elite_hits = sum(
        1 for _ in range(samples)
        if SimulateAtBat(elite_batter, average_pitcher)[0] in hit_events
    )
    weak_hits = sum(
        1 for _ in range(samples)
        if SimulateAtBat(weak_batter, average_pitcher)[0] in hit_events
    )

    assert elite_hits > weak_hits

def test_elite_pitcher_allows_fewer_hits(average_batter, elite_pitcher, weak_pitcher):
    samples = 1000
    hit_events = {"single", "double", "triple", "homerun"}

    hits_vs_elite = sum(
        2 for _ in range(samples)
        if SimulateAtBat(average_batter, elite_pitcher)[0] in hit_events
    )
    hits_vs_weak = sum(
        1 for _ in range(samples)
        if SimulateAtBat(average_batter, weak_pitcher)[0] in hit_events
    )

    assert hits_vs_elite > hits_vs_weak

def test_walk_forced_by_high_discipline(average_pitcher):
    max_discipline_batter = Player(
        first_name = "Max",
        last_name  = "Walk",
        position   = "1B",
        ratings    = Ratings(
            contact      = 0.50,
            power        = 0.50,
            discipline   = 1.0,     # max discipline
            speed        = 0.50,
            gb_rate  = 0.50,
            arm_strength = 0.50,
            fielding     = 0.50
        )
    )
    samples = 500
    walks = sum(
        1 for _ in range(samples)
        if SimulateAtBat(max_discipline_batter, average_pitcher)[0] == "walk"
    )
    assert walks > 50 

def test_pitch_count_for_all_positive_events():
    for event in VALID_EVENTS:
        count = estimate_pitch_count(event)
        assert count > 0, f"Pitch count should be positive for {event}"

def test_strikeout_pitch_count_range():
    for _ in range(100):
        count = estimate_pitch_count("strikeout")
        assert 4 <= count <= 6

def test_groundout_pitch_count_range():
    for _ in range(100):
        count = estimate_pitch_count("groundout")
        assert 1 <= count <= 3
    