## Constants
FIRST = 0
SECOND = 1
THIRD = 2

# HELPERS
def count_runners(bases):
    return sum(1 for b in bases if b is not None)

def score_runner(runner, runs):
    runner.record_run()
    runs += 1
    return runs

def calculate_rbis(event, bases_before, runs_scored):
    """Calculate RBIs for batter, not every run is an rbi"""
    match event:
        case "homerun":
            return runs_scored
        case "single" | "double" | "triple":
            return runs_scored
        case "walk":
            runner_on_first  = bases_before[FIRST]  is not None
            runner_on_second = bases_before[SECOND] is not None
            runner_on_third  = bases_before[THIRD]  is not None
            if runner_on_first and runner_on_second and runner_on_third:
                return 1
            return 0
        case "groundout" | "flyout" | "lineout":
            # TODO: sac fly and fielders choice
            return 0
        case "strikeout":
            return 0
        case _:
            return 0

# Outs
def handle_out(bases, outs, batter, event_type="generic"):
    """Batter is out unless groundout, then lead runner"""
    match event_type:
        case "strikeout": ## Runners don't move
            outs += 1
            pass
        case "flyout":
            outs += 1
            # TODO: sac fly
            pass
        case "groundout":
            outs += 1
            if bases[FIRST] and bases[SECOND] and bases[THIRD]: # Runner on 1st, 2nd, and 3rd
                bases[THIRD] = bases[SECOND]
                bases[SECOND] = bases[FIRST]
                bases[FIRST] = batter
            elif bases[FIRST] and bases[SECOND]: # Runner on first and second
                bases[SECOND] = bases[FIRST]
                bases[FIRST] = batter
            elif bases[FIRST]: # Runner on First
                bases[FIRST] = batter

            # TODO: double plays
            pass
        case "lineout":
            outs += 1
            # TODO: double play
            pass
        case _:
            outs += 1
    return bases, outs

# Walk
def handle_walk(bases, runs, batter):
    if bases[FIRST] and bases[SECOND] and bases[THIRD]: ##bases loaded
        runs = score_runner(bases[THIRD], runs)
        bases[THIRD] = bases[SECOND]
        bases[SECOND] = bases[FIRST]
    elif bases[FIRST] and bases[SECOND]: ##1st and 2nd
        bases[THIRD] = bases[SECOND]
        bases[SECOND] = bases[FIRST]
    elif bases[FIRST]: ##1st
        bases[SECOND] = bases[FIRST]

    bases[FIRST] = batter

    return bases, runs

# Single
def handle_single(bases, runs, batter):
    if bases[THIRD]: ##Runner on third scores
        runs = score_runner(bases[THIRD], runs)
        bases[THIRD] = None

    if bases[SECOND]: ##Runner on second advances
        bases[THIRD] = bases[SECOND]
        bases[SECOND] = None

    if bases[FIRST]: ##Runner on first advances
        bases[SECOND] = bases[FIRST]
        bases[FIRST] = None

    bases[FIRST] = batter ##batter takes 1st

    # TODO: 1st to third depending on speed and hit location
    return bases, runs

# Double
def handle_double(bases, runs, batter):
    if bases[THIRD]: ##runner on third scores
        runs = score_runner(bases[THIRD], runs)
        bases[THIRD] = None

    if bases[SECOND]: ##runner on second scores
        runs = score_runner(bases[SECOND], runs)
        bases[SECOND] = None

    if bases[FIRST]: ##runner on 1st advances to 3rd
        bases[THIRD] = bases[FIRST]
        bases[FIRST] = None

    bases[SECOND] = batter ##batter takes second

    # TODO: 1st to score depending on speed and hit location
    return bases, runs

# Triple
def handle_triple(bases, runs, batter):
    for runner in bases:
        if runner is not None:
            runs = score_runner(runner, runs)
    
    bases = [None, None, None]
    bases[THIRD] = batter

    return bases, runs

# Homerun
def handle_homerun(bases, runs, batter):
    for runner in bases:
        if runner is not None:
            runs = score_runner(runner, runs)

    batter.record_run()
    runs += 1
    bases = [None, None, None]

    return bases, runs

# Handler
def advance_bases(event, bases, runs, outs, batter):
    runs_before = runs
    bases_before = [b for b in bases]

    match event:
        case "walk":
            bases, runs = handle_walk(bases, runs, batter)
        case "single":
            bases, runs = handle_single(bases, runs, batter)
        case "double":
            bases, runs = handle_double(bases, runs, batter)
        case "triple":
            bases, runs = handle_triple(bases, runs, batter)
        case "homerun": 
            bases, runs = handle_homerun(bases, runs, batter)
        case "strikeout":
            bases, outs = handle_out(bases, outs, batter, "strikeout")
        case "flyout":
            bases, outs = handle_out(bases, outs, batter, "flyout")
        case "groundout":
            bases, outs = handle_out(bases, outs, batter, "groundout")
        case "lineout":
            bases, outs = handle_out(bases, outs, batter, "lineout")
        case _:
            outs += 1

    runs_scored = runs - runs_before
    rbis = calculate_rbis(event, bases_before, runs_scored)
    return bases, runs, outs, runs_scored, rbis