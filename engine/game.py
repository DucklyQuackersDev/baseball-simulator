from engine.inning import SimulateInning

def should_pull_pitcher(pitcher, runs_allowed):
    pitches = pitcher.game_pitching_stats.pitches

    #Starter limits - Stamina rating
    if pitcher.position == "SP":
        pitch_limit = int(80 + pitcher.pitching_ratings.stamina * 40) # 80 - 120
        return pitches >= pitch_limit
    
    if pitcher.position == "RP":
        return pitches >= 30
    
    return False

def substitute_pitcher(defense):
    current = defense.current_pitcher
    print(f"  Pitching change - {current.short_name} is pulled "
          f"({current.game_pitching_stats.pitches} pitches)")
    
    #find next reliever
    available = [p for p in defense.bullpen
                 if p.game_pitching_stats.pitches == 0]
    
    if available:
        defense.current_pitcher = available[0]
        print(f"  {defense.current_pitcher.short_name} enters the game")
    else:
        print(f"  No Relievers available - {current.short_name} stays in")

def SimulateGame(home_team, away_team):
    home_runs = 0
    away_runs = 0

    home_team.reset()
    away_team.reset()

    for inning in range(1, 10):
        print(f"\n--- Inning {inning} ---")

        ##top of inning ##
        #check away pitcher
        if should_pull_pitcher(away_team.current_pitcher, away_runs):
            substitute_pitcher(away_team)

        print(f"\n-- Top {inning} | {away_team.name} batting --")
        away_runs += SimulateInning(away_team, home_team)
        print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")


        ##bottom of inning, skip if home is leading in 9th##
        #cheack home pitcher
        if should_pull_pitcher(home_team.current_pitcher, home_runs):
            substitute_pitcher(home_team)

        if inning == 9 and home_runs > away_runs:
            print("Bottom of 9th Skipped")
            break
        
        print(f"\n-- Bottom {inning} | {home_team.name} batting --")
        home_runs += SimulateInning(home_team, away_team)
        print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

    ##Extra innings
    extra = 10
    while home_runs == away_runs:
        print(f"\n--- Inning {extra} ---")
        print(f"\n-- Top {extra} | {away_team.name} batting --")
        away_runs += SimulateInning(away_team, home_team)

        print(f"\n-- Bottom {extra} | {home_team.name} batting --")
        home_runs += SimulateInning(home_team,away_team)
        print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

    winner = home_team.name if home_runs > away_runs else away_team.name
    print(f"\n Final")
    print(f"{away_team.name} {away_runs} - {home_team.name} {home_runs}")
    print(f"Winner: {winner}")

    return home_runs, away_runs