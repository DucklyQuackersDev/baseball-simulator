import pytest
from models.player import Player, Ratings
from engine.baserunning import (
    handle_walk, handle_single, handle_double,
    handle_triple, handle_homerun, handle_out,
    advance_bases, count_runners, score_runner,
    FIRST, SECOND, THIRD
)

# Helpers --------------------------------------------
def make_player(first="John", last="Doe", position="RF"):
    """Creates a minimal player for testing"""
    ratings = Ratings(
        contact      = 0.50,
        power        = 0.50,
        discipline   = 0.50,
        speed        = 0.50,
        gb_rate  = 0.50,
        arm_strength = 0.50,
        fielding     = 0.50
    )
    return Player(first, last, position, ratings)

# Fixtures --------------------------------------
@pytest.fixture
def batter():
    return make_player("Batter", "Test")

@pytest.fixture
def runner_a():
    return make_player("Runner", "A")

@pytest.fixture
def runner_b():
    return make_player("Runner", "B")

@pytest.fixture
def runner_c():
    return make_player("Runner", "C")

@pytest.fixture
def empty_bases():
    return [None, None, None]

@pytest.fixture
def bases_loaded(runner_a, runner_b, runner_c):
    return [runner_a, runner_b, runner_c]

@pytest.fixture
def runner_on_first(runner_a):
    return [runner_a, None, None]

@pytest.fixture
def runner_on_second(runner_a):
    return [None, runner_a, None]

@pytest.fixture
def runner_on_third(runner_a):
    return [None, None, runner_a]

@pytest.fixture
def runners_on_first_and_second(runner_a, runner_b):
    return [runner_a, runner_b, None]

@pytest.fixture
def runners_on_first_and_third(runner_a, runner_b):
    return [runner_a, None, runner_c]

# Count runners tests -----------------------------------------
def test_count_runners_empty(empty_bases):
    assert count_runners(empty_bases) == 0

def test_count_runners_one(runner_on_first):
    assert count_runners(runner_on_first) == 1

def test_count_runners_two(runners_on_first_and_second):
    assert count_runners(runners_on_first_and_second) == 2

def test_count_runners_three(bases_loaded):
    assert count_runners(bases_loaded) == 3

# Score Runners tests -------------------------------------------
def test_score_runner_increments_runs(runner_a):
    runs = score_runner(runner_a, 0)
    assert runs == 1

def test_score_runner_updates_player_stats(runner_a):
    score_runner(runner_a, 0)
    assert runner_a.batting_stats.runs == 1

def test_score_runner_updates_game_stats(runner_a):
    score_runner(runner_a, 0)
    assert runner_a.game_batting_stats.runs == 1

# Walk tests -------------------------------------------------------
def test_walk_empty_bases(empty_bases, batter):
    bases, runs = handle_walk(empty_bases, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is None
    assert bases[THIRD] is None
    assert runs == 0

def test_walk_runner_on_first(runner_on_first, batter, runner_a):
    bases, runs = handle_walk(runner_on_first, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases[THIRD] is None
    assert runs == 0

def test_walk_runners_on_first_and_second(runners_on_first_and_second, batter, runner_a, runner_b):
    bases, runs = handle_walk(runners_on_first_and_second, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases[THIRD] is runner_b
    assert runs == 0

def test_walk_bases_loaded(bases_loaded, batter, runner_a, runner_b, runner_c):
    bases, runs = handle_walk(bases_loaded, 0, batter)
    assert runs == 1
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases[THIRD] is runner_b

def test_walk_runner_on_second(runner_on_second, batter, runner_a):
    bases, runs = handle_walk(runner_on_second, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases[THIRD] is None
    assert runs == 0

def test_walk_runner_on_third(runner_on_third, batter, runner_a):
    bases, runs = handle_walk(runner_on_third, 0, batter)
    assert bases[FIRST] is batter
    assert bases[THIRD] is runner_a
    assert runs == 0

def test_walk_bases_loaded_updates_scorer_stats(bases_loaded, batter, runner_c):
    handle_walk(bases_loaded, 0, batter)
    assert runner_c.batting_stats.runs == 1

# Single Tests ----------------------------------------------------------------------
def test_single_empty_bases(empty_bases, batter):
    bases, runs = handle_single(empty_bases, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is None
    assert bases[THIRD] is None
    assert runs == 0

def test_single_runner_on_first(runner_on_first, batter, runner_a):
    bases, runs = handle_single(runner_on_first, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases[THIRD] is None
    assert runs == 0

def test_single_runner_on_second(runner_on_second, batter, runner_a):
    bases, runs = handle_single(runner_on_second, 0, batter)
    assert bases[FIRST] is batter
    assert bases[SECOND] is None
    assert bases[THIRD] is runner_a
    assert runs == 0

def test_single_runner_on_third(runner_on_third, batter, runner_a):
    bases, runs = handle_single(runner_on_third, 0, batter)
    assert runs == 1
    assert bases[FIRST] is batter
    assert bases[SECOND] is None
    assert bases[THIRD] is None
    assert runner_a.batting_stats.runs == 1

def test_single_bases_loaded(bases_loaded, batter, runner_a, runner_b, runner_c):
    bases, runs = handle_single(bases_loaded, 0, batter)
    assert runs == 1
    assert bases[FIRST] is batter
    assert bases[SECOND] is runner_a
    assert bases [THIRD] is runner_b
    assert runner_c.batting_stats.runs == 1

def test_single_preserves_runner_identity(runner_on_first, batter, runner_a):
    bases, runs = handle_single(runner_on_first, 0, batter)
    assert bases[SECOND] is runner_a
    assert bases[SECOND] is not batter 

# Double Tests ----------------------------------------------------------------------
def test_double_bases_empty(empty_bases, batter):
    bases, runs = handle_double(empty_bases, 0, batter)
    assert bases[FIRST] is None
    assert bases[SECOND] is batter
    assert bases[THIRD] is None
    assert runs == 0

def test_double_runner_on_first(runner_on_first, batter, runner_a):
    bases, runs = handle_double(runner_on_first, 0, batter)
    assert bases[FIRST] is None
    assert bases[SECOND] is batter
    assert bases[THIRD] is runner_a
    assert runs == 0

def test_double_runner_on_second_scores(runner_on_second, batter, runner_a):
    bases, runs = handle_double(runner_on_second, 0 ,batter)
    assert runs == 1
    assert bases[FIRST] is None
    assert bases[SECOND] is batter
    assert bases[THIRD] is None
    assert runner_a.batting_stats.runs == 1

def test_double_runner_on_third_scores(runner_on_third, batter, runner_a):
    bases, runs = handle_double(runner_on_third, 0 , batter)
    assert runs == 1
    assert bases[FIRST] is None
    assert bases[SECOND] is batter
    assert bases[THIRD] is None
    assert runner_a.batting_stats.runs == 1

def test_double_bases_loaded(bases_loaded, batter, runner_a, runner_b, runner_c):
    bases, runs = handle_double(bases_loaded, 0, batter)
    assert runs == 2
    assert bases[FIRST] is None
    assert bases[SECOND] is batter
    assert bases[THIRD] is runner_a
    assert runner_b.batting_stats.runs == 1
    assert runner_c.batting_stats.runs == 1

# Triple Tests ----------------------------------------------------------------------
def test_triple_empty_bases(empty_bases, batter):
    bases, runs = handle_triple(empty_bases, 0 , batter)
    assert bases[FIRST] is None
    assert bases[SECOND] is None
    assert bases[THIRD] is batter
    assert runs == 0

def test_triple_scores_all(bases_loaded, batter, runner_a, runner_b, runner_c):
    bases, runs = handle_triple(bases_loaded, 0, batter)
    assert runs == 3
    assert bases[FIRST] is None
    assert bases[SECOND] is None
    assert bases[THIRD] is batter
    assert runner_a.batting_stats.runs == 1
    assert runner_b.batting_stats.runs == 1
    assert runner_c.batting_stats.runs == 1

def test_triple_one_on(runner_on_first, batter, runner_a):
    bases, runs = handle_triple(runner_on_first, 0, batter)
    assert runs == 1
    assert bases[FIRST] is None
    assert bases[SECOND] is None
    assert bases[THIRD] is batter
    assert runner_a.batting_stats.runs == 1

def test_triple_runner_on_third(runner_on_third, batter, runner_a):
    bases, runs = handle_triple(runner_on_third, 0, batter)
    assert bases[THIRD] is batter

# Homerun Tests ---------------------------------------------------------------------
def test_homerun_empty_bases(empty_bases, batter):
    bases, runs = handle_homerun(empty_bases, 0, batter)
    assert runs == 1
    assert bases == [None, None, None]
    assert batter.batting_stats.runs == 1

def test_homerun_bases_loaded_grand_slam(bases_loaded, batter, runner_a, runner_b, runner_c):
    bases, runs = handle_homerun(bases_loaded, 0, batter)
    assert runs == 4
    assert bases == [None, None, None]
    assert batter.batting_stats.runs  == 1
    assert runner_a.batting_stats.runs == 1
    assert runner_b.batting_stats.runs == 1
    assert runner_c.batting_stats.runs == 1

def test_homerun_clears_bases(runner_on_first, batter, runner_a):
    bases, runs = handle_homerun(runner_on_first, 0, batter)
    assert runs == 2
    assert bases == [None, None, None]

def test_homerun_updates_all_runner_stats(bases_loaded, batter, runner_a, runner_b, runner_c):
    handle_homerun(bases_loaded, 0, batter)
    for player in [batter, runner_a, runner_b, runner_c]:
        assert player.batting_stats.runs == 1
        assert player.game_batting_stats.runs == 1

# Out Tests -------------------------------------------------------------------------
def test_strikeout_increments_outs(empty_bases, batter):
    bases, outs = handle_out(empty_bases, 0, batter, "strikeout")
    assert outs == 1

def test_groundout_increments_outs(empty_bases, batter):
    bases, outs = handle_out(empty_bases, 0, batter, "groundout")
    assert outs == 1

def test_flyout_increments_outs(empty_bases, batter):
    bases, outs = handle_out(empty_bases, 0, batter, "flyout")
    assert outs == 1

def test_lineout_increments_outs(empty_bases, batter):
    bases, outs = handle_out(empty_bases, 0, batter, "lineout")
    assert outs == 1

def test_generic_out_increments_outs(empty_bases):
    bases, outs = handle_out(empty_bases, 0, batter)
    assert outs == 1

def test_out_does_not_clear_bases(runner_on_first, batter, runner_a):
    bases, outs = handle_out(runner_on_first, 0, batter, "groundout")
    assert bases[FIRST] is batter

# Advance Bases Tests ---------------------------------------------------------------
def test_advance_bases_returns_correct_structure(empty_bases, batter):
    result = advance_bases("single", empty_bases, 0, 0, batter)
    assert len(result) == 5 # bases, runs, outs, runs_Scored, rbis

def test_advance_bases_single_places_batter(empty_bases, batter):
    bases, runs, outs, runs_scored, rbis = advance_bases("single", empty_bases, 0, 0, batter)
    assert bases[FIRST] is batter

def test_advance_bases_returns_runs_scored(bases_loaded, batter):
    bases, runs, outs, runs_scored, rbis = advance_bases("single", bases_loaded, 0, 0, batter)
    assert runs_scored == 1
    assert runs == 1

def test_advance_bases_grand_slam(bases_loaded, batter):
    bases, runs, outs, runs_scored, rbis = advance_bases("homerun", bases_loaded, 0, 0, batter)
    assert runs_scored == 4
    assert runs == 4

def test_advance_bases_out_no_runs(empty_bases, batter):
    bases, runs, outs, runs_scored, rbis = advance_bases("strikeout", empty_bases, 0, 0, batter)
    assert runs_scored == 0
    assert outs == 1

def test_advance_bases_walk_no_runs_empty(empty_bases, batter):
    bases, runs, outs, runs_scored, rbis = advance_bases("walk", empty_bases, 0, 0, batter)
    assert runs_scored == 0
    assert bases[FIRST] is batter

def test_advance_bases_preserves_runner_identity(runner_on_first, batter, runner_a):
    """Runner objects should be preserved through base advancement"""
    bases, runs, outs, runs_scored, rbis = advance_bases("single", runner_on_first, 0, 0, batter)
    assert bases[FIRST]  is batter
    assert bases[SECOND] is runner_a

