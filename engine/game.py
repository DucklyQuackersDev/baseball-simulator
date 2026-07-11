from engine.inning import SimulateInning

def should_pull_pitcher(pitcher, runs_allowed):
    pitches = pitcher.game_pitching_stats.pitches

    #Starter limits - Stamina rating
    if pitcher.position == "SP":
        pitch_limit = int(60 + pitcher.pitching_ratings.stamina * 40) # 60 - 100
        return pitches >= pitch_limit
    
    if pitcher.position == "RP":
        return pitches >= 30
    
    return False

def substitute_pitcher(defense, silent=False):
    """Pulls current pitcher and brings in next available reliever"""
    current = defense.current_pitcher

    if not silent:
        print(f"  Pitching change — {current.short_name} is pulled "
              f"({current.game_pitching_stats.pitches} pitches)")

    available = [p for p in defense.bullpen
                 if p.game_pitching_stats.pitches == 0]

    if available:
        defense.current_pitcher = available[0]
        if not silent:
            print(f"  {defense.current_pitcher.short_name} enters the game")
    else:
        if not silent:
            print(f"  No relievers available — {current.short_name} stays in")

def SimulateGame(home_team, away_team, silent=False):
    """Simulates a full 9 inning game — returns final score as (home_runs, away_runs)"""
    home_runs = 0
    away_runs = 0

    home_team.reset()
    away_team.reset()

    for inning in range(1, 10):
        if not silent:
            print(f"\n{'=' * 40}")
            print(f"Inning {inning}")
            print(f"{'=' * 40}")

        # ── Top of inning — away bats ─────────────────────────────────────────
        if should_pull_pitcher(home_team.current_pitcher, home_runs):
            substitute_pitcher(home_team, silent)

        if not silent:
            print(f"\n-- Top {inning} | {away_team.name} batting --")

        away_runs += SimulateInning(away_team, home_team, silent)

        if not silent:
            print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

        # ── Walk off check ────────────────────────────────────────────────────
        if inning == 9 and home_runs > away_runs:
            if not silent:
                print("Walk off — game over")
            break

        # ── Bottom of inning — home bats ──────────────────────────────────────
        if should_pull_pitcher(away_team.current_pitcher, away_runs):
            substitute_pitcher(away_team, silent)

        if not silent:
            print(f"\n-- Bottom {inning} | {home_team.name} batting --")

        home_runs += SimulateInning(home_team, away_team, silent)

        if not silent:
            print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

    # ── Extra innings ─────────────────────────────────────────────────────────
    extra = 10
    while home_runs == away_runs:
        if not silent:
            print(f"\n{'=' * 40}")
            print(f"Extra Inning {extra}")
            print(f"{'=' * 40}")

        if should_pull_pitcher(home_team.current_pitcher, home_runs):
            substitute_pitcher(home_team, silent)

        if not silent:
            print(f"\n-- Top {extra} | {away_team.name} batting --")

        away_runs += SimulateInning(away_team, home_team, silent)

        if not silent:
            print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

        if should_pull_pitcher(away_team.current_pitcher, away_runs):
            substitute_pitcher(away_team, silent)

        if not silent:
            print(f"\n-- Bottom {extra} | {home_team.name} batting --")

        home_runs += SimulateInning(home_team, away_team, silent)

        if not silent:
            print(f"Score: {away_team.name} {away_runs} - {home_team.name} {home_runs}")

        extra += 1
        assert extra < 30, "Extra innings loop — something is wrong"

    # ── Final ─────────────────────────────────────────────────────────────────
    winner = home_team.name if home_runs > away_runs else away_team.name

    if not silent:
        print(f"\n{'=' * 40}")
        print(f"Final")
        print(f"{'=' * 40}")
        print(f"{away_team.name:<14} {away_runs}")
        print(f"{home_team.name:<14} {home_runs}")
        print(f"Winner: {winner}")

    return home_runs, away_runs