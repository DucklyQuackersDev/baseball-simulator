import random

def estimate_pitch_count(event):
    """Estimate pitches thrown in at bat"""
    match event:
        case "strikeout":
            return random.randint(4, 6)   # deep counts on strikeouts
        case "walk":
            return random.randint(4, 6)   # walks also run deep
        case "homerun":
            return random.randint(1, 4)
        case "single":
            return random.randint(1, 4)
        case "double":
            return random.randint(1, 4)
        case "triple":
            return random.randint(1, 4)
        case "groundout":
            return random.randint(1, 3)   # quick contact outs
        case "flyout":
            return random.randint(1, 3)
        case "lineout":
            return random.randint(1, 3)
        case _:
            return 1

## Full At Bat
def SimulateAtBat(batter, pitcher):
    """Simualte a single at bat - returns event and pitch count"""

    # Base Rates
    base_bb_rate = 0.085
    base_k_rate = 0.225
    base_hr_rate = 0.034
    base_hit_rate = 0.240

    # Rating Modifiers
    bb_rate  = base_bb_rate  + (batter.ratings.discipline - 0.50)          * 0.05 \
                             + (0.50 - pitcher.pitching_ratings.control)    * 0.05
    
    k_rate   = base_k_rate   + (0.50 - batter.ratings.discipline)          * 0.08 \
                             + (pitcher.pitching_ratings.stuff - 0.50)      * 0.08
    
    hr_rate  = base_hr_rate  + (batter.ratings.power - 0.50)               * 0.04 \
                             + (0.50 - pitcher.pitching_ratings.stuff)      * 0.02
    
    hit_rate = base_hit_rate + (batter.ratings.contact - 0.50)             * 0.08 \
                             + (0.50 - pitcher.pitching_ratings.stuff)      * 0.04
    
    # Prevent negatives or values greater than 1
    bb_rate = max(0.01, min(bb_rate, 0.20))
    k_rate = max(0.05, min(k_rate, 0.45))
    hr_rate = max(0.00, min(hr_rate, 0.40))

    # Roll
    roll = random.random()

    if roll < bb_rate:
        event = "walk"
    elif roll < bb_rate + k_rate:
        event = "strikeout"
    elif roll < bb_rate + k_rate + hr_rate:
        event = "homerun"
    elif roll < bb_rate + k_rate + hr_rate + hit_rate:
        hit_roll = random.random()
        if hit_roll < 0.60:
            event = "single"
        elif hit_roll < 0.85:
            event = "double"
        else:
            event = "triple"
    else:
        if random.random() < batter.ratings.gb_rate:
            event = "groundout"
        else:
            event = "flyout"
    
    pitches = estimate_pitch_count(event)
    return event, pitches
    