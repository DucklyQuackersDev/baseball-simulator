from engine.inning import SimulateInning

def SimulateGame():
    home_runs = 0
    away_runs = 0

    for inning in range(1, 10):
        print(f"--- Inning {inning} ---")

        ##top of inning
        print("Top of inning")
        away_runs += SimulateInning()

        ##bottom of inning, skip if home is leading in 9th
        if inning == 9 and home_runs > away_runs:
            print("Bottom of 9th Skipped")
            break
        
        print("Bottom of inning")
        home_runs += SimulateInning()

    ##Extra innings
    extra = 10
    while home_runs == away_runs:
        print(f"--- Inning {extra} ---")
        print("Top of inning")
        away_runs += SimulateInning()
        print("Bottom of inning")
        home_runs += SimulateInning()

    print(f"Final: Away {away_runs} - Home {home_runs}")
    return home_runs, away_runs