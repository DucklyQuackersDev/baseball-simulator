## Constants
FIRST = 0
SECOND = 1
THIRD = 2


def handle_out(bases, outs, event_type="generic"):

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
            # TODO: double play
            pass
        case "lineout":
            outs += 1
            # TODO: double play
            pass
        case _:
            outs += 1
    return bases, outs

def handle_walk(bases, runs):
    if bases[FIRST] and bases[SECOND] and bases[THIRD]: ##bases loaded
        runs+=1
    elif bases[FIRST] and bases[SECOND]: ##1st and 2nd
        bases[THIRD] = True
    elif bases[FIRST]: ##1st
        bases[SECOND] = True

    bases[FIRST] = True

    return bases, runs

def handle_single(bases, runs):
    if bases[THIRD]: ##Runner on third scores
        runs += 1
        bases[THIRD] = False

    if bases[SECOND]: ##Runner on second advances
        bases[THIRD] = True
        bases[SECOND] = False

    if bases[FIRST]: ##Runner on first advances
        bases[SECOND] = True
        bases[FIRST] = False

    bases[FIRST] = True ##batter takes 1st

    # TODO: 1st to third depending on speed and hit location
    return bases, runs

def handle_double(bases, runs):
    if bases[THIRD]: ##runner on third scores
        runs+=1
        bases[THIRD] = False

    if bases[SECOND]: ##runner on second scores
        runs+=1
        bases[SECOND] = False

    if bases[FIRST]: ##runner on 1st advances to 3rd
        bases[THIRD] = True
        bases[FIRST] = False

    bases[SECOND] = True ##batter takes second

    # TODO: 1st to score depending on speed and hit location
    return bases, runs

def handle_triple(bases, runs):
    runs += sum(bases)
    bases = [False, False, True] ##Runners empty, batter takes third

    return bases, runs

def handle_homerun(bases, runs):
    runs += sum(bases) + 1
    bases = [False, False, False]

    return bases, runs

def advance_bases(event, bases, runs, outs):
    match event:
        case "walk":
            bases, runs = handle_walk(bases, runs)
        case "single":
            bases, runs = handle_single(bases, runs)
        case "double":
            bases, runs = handle_double(bases, runs)
        case "triple":
            bases, runs = handle_triple(bases, runs)
        case "homerun": 
            bases, runs = handle_homerun(bases, runs)
        case "strikeout":
            bases, outs = handle_out(bases, outs, "strikeout")
        case "flyout":
            bases, outs = handle_out(bases, outs, "flyout")
        case "groundout":
            bases, outs = handle_out(bases, outs, "groundout")
        case "lineout":
            bases, outs = handle_out(bases, outs, "lineout")
        case _:
            outs += 1


    return bases, runs, outs