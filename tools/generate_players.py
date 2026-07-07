import json
import random

## Name Pools

FIRST_NAMES = [
    "Marcus", "Dante", "Leon", "Caleb", "Owen", "Jared", "Troy", "Reid", "Seth",
    "Felix", "Nolan", "Grant", "Bryce", "Cole", "Miles", "Ryder", "Drew", "Blake",
    "Tanner", "Eli", "Gavin", "Wyatt", "Chase", "Wade", "Zane", "Kurt", "Damon",
    "Jace", "Luca", "Aaron", "Shane", "Cody", "Brett", "Lance", "Nash", "Holt",
    "Cruz", "Hugo", "Percy", "Vance", "Knox", "Flynn", "Beau", "Clark", "Ross",
    "Gage", "Rhett", "Ward", "Dean", "Blaine", "Clay", "Reed", "Mack", "Jack",
    "Colt", "Reef", "Tate", "Hal", "Silas", "Preston", "Walt", "Finn", "Wes",
    "Zack", "Dex", "Gus", "Kent", "Jonah", "Alec", "Bo", "Roy", "Hugh", "Nate",
    "Luke", "Sam", "Art", "Evan", "Ian", "Glen", "Earl", "Ray", "Tom", "Dirk",
    "Vic", "Brock", "Jay", "Ned", "Al", "Bert", "Cliff", "Karl", "Saul", "Amos",
    "Lyle", "Gil", "Mel", "Cy", "Hank", "Lew", "Ike", "Otis", "Rex", "Curt",
    "Norm", "Ace", "Buck", "Slim", "Rafe", "Dario", "Cord", "Penn", "Alton",
    "Kieran", "Brant", "Clint", "Grady", "Thad", "Wynn", "Whit", "Chet", "Moss",
    "Dade", "Zeb", "Jeb", "Slade", "Huck", "Dash", "Vern", "Spence", "Monty",
    "Tex", "Flint", "Remy", "Seb", "Trace", "Lem", "Bart", "Dalt", "Pip", "Skip",
    "Chip", "Jud", "Bix", "Spud", "Tug", "Bud", "Chub", "Stub", "Rip", "Bub"
]

LAST_NAMES = [
    "Vega", "Rourke", "Ashby", "Strom", "Merritt", "Finch", "Navarro", "Calloway",
    "Dillard", "Harmon", "Prieto", "Weston", "Lowman", "Beckett", "Thornton",
    "Malone", "Kessler", "Sutton", "Cross", "Drummond", "Okafor", "Boone",
    "Delgado", "Ingram", "Hollis", "Pavia", "Reyes", "Whitfield", "Ferrell",
    "Quill", "Paxton", "Lamont", "Alonzo", "Dupree", "Colby", "Avery",
    "Mendenhall", "Santana", "Holt", "Pemberton", "Bauer", "Garrett", "Callahan",
    "Hensley", "Dunbar", "Whitmore", "Connelly", "Easton", "Stafford", "Rockwell",
    "Voss", "Fontaine", "Tully", "Norwood", "Waverly", "Langston", "Greer",
    "Mercer", "Hale", "Decker", "Radley", "Aldridge", "Thornley", "Raines",
    "Tillman", "Holloway", "Wren", "Burnham", "Hartwell", "Pickett", "Mackay",
    "Covington", "Branson", "Elwood", "Quinlan", "Crosby", "Mackey", "Tanner",
    "Moss", "Dunmore", "Hadley", "Shelton", "Landry", "Haines", "Colton",
    "Galvin", "Fenn", "Crowell", "Nolan", "Sweeney", "Kimball", "Penfield",
    "Ashford", "Ramsey", "Fogarty", "Whitten", "Grover", "Bancroft", "Davenport",
    "Sherwood", "Whitford", "Kirby", "Morrow", "Shelby", "Holden", "Flemming",
    "Wilder", "Stanton", "Vance", "Wolfe", "Drake", "Easley", "Archer", "Corbin",
    "Crane", "Dunbar", "Winslow", "Halsey", "Cranston", "Fenwick", "Gault",
    "Alcott", "Ridley", "Stokes", "Ponder", "Norris", "Langford", "Dolan",
    "Winfield", "Vickers", "Haggerty", "Doyle", "Wakefield", "Quigley",
    "Sheridan", "Holloway", "Denton", "Mallory", "Galloway", "Holton", "Prentiss",
    "Lacey", "Danforth", "Fielding", "Whitley", "Radley", "Colby", "Wren"
]

POSITIONS = ["CF", "RF", "LF", "1B", "2B", "3B", "SS", "C", "DH"]


## Generate Ratings

def make_batting_ratings(tier):
    """
    Generate ratings based on tier
    tier 1 = elite, tier 2 = good, tier 3 = average, tier 4 = bench
    """

    ranges = {
        1: (0.80, 0.96),
        2: (0.68, 0.82),
        3: (0.55, 0.70),
        4: (0.40, 0.58)
    }
    lo, hi = ranges[tier]

    return {
        "contact":      round(random.uniform(lo, hi), 2),
        "power":        round(random.uniform(lo, hi), 2),
        "discipline":   round(random.uniform(lo, hi), 2),
        "speed":        round(random.uniform(lo, hi), 2),
        "gb_rate":      round(random.uniform(0.38, 0.62), 2),
        "arm_strength": round(random.uniform(lo, hi), 2),
        "fielding":     round(random.uniform(lo, hi), 2),
    }

def make_pitching_ratings(tier):
    """
    Generate pitching ratings based on tier
    tier 1 = elite, tier 2 = good, tier 3 = avg, tier 4 = replaceable
    """

    ranges = {
        1: (0.85, 0.96),
        2: (0.74, 0.86),
        3: (0.62, 0.76),
        4: (0.50, 0.64)
    }
    lo, hi = ranges[tier]

    return {
        "stuff":       round(random.uniform(lo, hi), 2),
        "control":     round(random.uniform(lo, hi), 2),
        "stamina":     round(random.uniform(lo, hi), 2),
        "gb_rate": round(random.uniform(0.38, 0.56), 2)
    }

def make_pitcher_batting_ratings():
    """Pitchers are weak batters"""
    return {
        "contact":      round(random.uniform(0.10, 0.18), 2),
        "power":        round(random.uniform(0.06, 0.14), 2),
        "discipline":   round(random.uniform(0.12, 0.22), 2),
        "speed":        round(random.uniform(0.20, 0.32), 2),
        "gb_rate":      round(random.uniform(0.48, 0.62), 2),
        "arm_strength": round(random.uniform(0.44, 0.72), 2),
        "fielding":     round(random.uniform(0.44, 0.56), 2)
    }


## Player Generate

def generate_position_players(num_teams, players_per_team=9):
    """
    Generate pool of players across the 4 tiers
    Guarantees every team will have 1 of each position
    """
    #one of each position per team
    position_slots = POSITIONS * num_teams
    random.shuffle(position_slots)

    players = []
    used_names = set()

    #tier distribution
    total = len(position_slots)
    tiers = (
        [1] * (total // 6) +
        [2] * (total // 3) +
        [3] * (total // 3) +
        [4] * (total - (total // 6) - (total // 3) - (total // 3))
    )
    random.shuffle(tiers)

    for i, (position, tier) in enumerate(zip(position_slots, tiers)):
        attempts = 0
        while True:
            first = random.choice(FIRST_NAMES)
            last  = random.choice(LAST_NAMES)
            name  = f"{first} {last}"
            if name not in used_names:
                used_names.add(name)
                break
            attempts += 1
            if attempts > 100:
                last = last + str(i)
                break

        players.append({
            "first_name":       first,
            "last_name":        last,
            "position":         position,
            "ratings":          make_batting_ratings(tier),
            "pitching_ratings": None
        })

    return players


def generate_pitchers(count, position):
    """
    Generate pool of pitchers (SP or RP) across 4 tiers
    """

    pitchers = []
    used_names = set()

    tiers = (
        [1] * (count // 6) +
        [2] * (count // 3) +
        [3] * (count // 3) +
        [4] * (count - (count // 6) - (count // 3) - (count // 3))
    )
    random.shuffle(tiers)

    for i, tier in enumerate(tiers):
        attempts = 0
        while True:
            first = random.choice(FIRST_NAMES)
            last  = random.choice(LAST_NAMES)
            name  = f"{first} {last}"
            if name not in used_names:
                used_names.add(name)
                break
            attempts += 1
            if attempts > 100:
                last = last + str(i)
                break

        pitchers.append({
            "first_name":       first,
            "last_name":        last,
            "position":         position,
            "ratings":          make_pitcher_batting_ratings(),
            "pitching_ratings": make_pitching_ratings(tier)
        })

    return pitchers


## Main
def generate(num_teams=16, starters_per_team=2, relievers_per_team=2,
             output_path="data/players.json"):
    
    total_starters = num_teams * starters_per_team
    total_relievers = num_teams * relievers_per_team

    print(f"Generating {num_teams * 9} position players, "
          f"{total_starters} starters, {total_relievers} relievers...")

    position_players = generate_position_players(num_teams)
    starters = generate_pitchers(total_starters, "SP")
    relievers = generate_pitchers(total_relievers, "RP")

    all_players = position_players + starters + relievers
    random.shuffle(all_players) #Shuffle so json doesn't imply team

    data = {"players": all_players}

    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Written to {output_path}")
    print(f"  {len(position_players)} position players")
    print(f"  {len(starters)} starters")
    print(f"  {len(relievers)} relievers")
    print(f"  {len(all_players)} total")

if __name__ == "__main__":
    generate()

