import random
import calendar
from datetime import date, timedelta
from itertools import combinations
from models.game import Game

## Generate Dates
def generate_dates(num_games, start_date=None):
    """
    Spreads games across the season with rest days
    Rest days after 3 games
    """
    
    if start_date is None:
        start_date = date(2026, 4, 1)

    dates = []
    current = start_date

    while len(dates) < num_games:
        dates.append(current)
        if len(dates) % 3 == 0:
            current += timedelta(days=2)
        else:
            current += timedelta(days=1)

    return dates

## Division Schedule
def generate_division_schedule(teams, games_against_division=4, games_against_others=2):
    """
    Builds raw game tuples from divionsal rules
    16 teams - East[:8] and West[8:]
    Same divison opponents games_against_division
    Inter-division opponents games_against_others
    """
    if len(teams) != 16:
        raise ValueError(f"Expected 16 teams, got {len(teams)}")
    
    if games_against_division % 2 != 0:
        raise ValueError(f"games_against_division must be even - got {games_against_division}")
    
    if games_against_others % 2 != 0:
        raise ValueError(f"games_against_others must be even - got {games_against_others}")
    
    east = teams[:8]
    west = teams[8:]

    games = []

    # Same Division
    for division in [east, west]:
        for home, away in combinations(division, 2):
            for _ in range(games_against_division // 2):
                games.append((home, away))  #home games
                games.append((away, home))  #Away games

    # Inter Division
    for home in east:
        for away in west:
            for _ in range(games_against_others // 2):
                games.append((home, away))
                games.append((away, home))

    return games


def generate_season_schedule(teams, start_date=None, games_against_division=4, games_against_others=2):
    """
    Generates a full season 
    Returns: list of game objects
    """
    games = generate_division_schedule(teams, games_against_division, games_against_others)
    random.shuffle(games)
    dates = generate_dates(len(games), start_date)

    schedule = [
        Game(home_team=home, away_team=away, date=d)
        for (home,away), d in zip(games, dates)
    ]

    print(f"Generated {len(schedule)} game schedule - "
          f"starts {dates[0]} ends {dates[-1]}")
    
    return schedule

## Verify Schedule
def verify_schedule(teams, schedule, games_against_division=4, games_against_other=2):
    """
    Asserts every team plays the correct number of games
    """
    east = teams[:8]
    west = teams[8:]

    print("\nVerifying schedule...")
    errors = []

    for team in teams:
        division = east if team in east else west
        other_division = west if team in east else east

        #Check division opponents
        for opp in [t for t in division if t is not team]:
            count = sum(
                1 for g in schedule if
                (g.home_team is team and g.away_team is opp) or
                (g.away_team is team and g.home_team is opp)
            )
            if count != games_against_division:
                errors.append(f"{team.name} vs {opp.name} (div): "
                              f"expected {games_against_division} got {count}")
                
        #Check inter division opponents
        for opp in other_division:
            count = sum(
                1 for g in schedule if
                (g.home_team is team and g.away_team is opp) or
                (g.away_team is team and g.home_team is opp)
            )
            if count != games_against_other:
                errors.append(f"{team.name} vs {opp.name} (inter): "
                              f"expected {games_against_other} got {count}")
                
    if errors:
        print(f"    {len(errors)} schedule errors found:")
        for e in errors:
            print(f"    {e}")
    else:
        total = len(schedule)
        per_team = (games_against_division * 7) + (games_against_other * 8)
        print(f"    Schedule verified - {total} total games, {per_team} per team")

## Queries
def get_games_by_date(schedule, target_date):
    """Returns all games on specific date"""
    return [g for g in schedule if g.date == target_date]

def get_games_by_month(schedule, year, month):
    """Returns all games in specifc month"""
    return [g for g in schedule if g.date.year == year and g.date.mont == month]

def get_team_schedule(schedule, team):
    """Returns all games for a specific team"""
    return [g for g in schedule if g.home_team or g.away_team is team]

def get_division_schedule(schedule, teams, division="east"):
    """Returns all games where both teams are in the same division"""
    east = teams[:8]
    west = teams[8:]
    div = east if division == "east" else west
    return [g for g in schedule if g.home_team in div and g.away_team in div]

def get_inter_division_schedule(schedule, teams):
    """Returns all games between divisions"""
    east = teams[:8]
    west = teams[8:]
    return [g for g in schedule if
            (g.home_team in east and g.away_team in west) or
            (g.home_team in west and g.away_team in east)]

## Display
def print_schedule(schedule):
    """Prints readable schedule"""
    print(f"\nSchedule - {len(schedule)} games")
    for i, game in enumerate(schedule):
        print(f"    Game {i + 1:>3}: {game}")

def get_schedule_summary(teams, schedule):
    """Prints home, away, division, and inter-division game counts per team"""
    east = teams[:8]
    west = teams[8:]

    print("\nSchedule Summar:")
    print(f"    {'Team':<13} {'Div':<6} {'Total':>6} {'Home':>6} {"Away":>6} "
          f"{'Div G':>6} {'Inter':>6}")
    print(f"    {'-' * 52}")

    for team in teams:
        division = east if team in east else west
        other_div = west if team in east else east
        div_name = "East" if tem in east else "West"

        home_games = sum(1 for g in schedule if g.home_team is team)
        away_games = sum(1 for g in schedule if g.away_team is team)
        div_games = sum(1 for g in schedule if
                        (g.home_team is team or g.away_team is team) and
                        (g.home_team in division and g.away_team in division))
        inter_games = sum(1 for g in schedule if
                          (g.home_team is team or g.away_team is team) and
                          (g.home_team in other_div or g.away_team in other_div))
        total = home_games + away_games

        print(f"    {team.name:<14} {div_name:<6} {total:>6} {home_games:>6} "
              f"{away_games:>6} {div_games:>6} {inter_games:>6}")
        
def print_calendar(schedule, year, month):
    """"Prints a simple calendar view for a given month with game days marked"""
    games_this_month = get_games_by_month(schedule, year, month)

    print(f"\n{calendar.month_name[month]} {year}")
    print(f"  {'Mon':<6}{'Tue':<6}{'Wed':<6}{'Thu':<6}{'Fri':<6}{'Sat':<6}{'Sun':<6}")
    print(f"  {'-' * 42}")

    cal = calendar.monthcalendar(year, month)
    game_dates = {g.date.day for g in games_this_month}

    for week in cal:
        row = "  "
        for day in week:
            if day == 0:
                row += f"{'':6}"
            elif day in game_dates:
                row += f"{'*' + str(day):<6}"
            else:
                row += f"{day:<6}"
        print(row)
    print(f"\n  * = game day ({len(games_this_month)} games this month)")

def print_team_calendar(schedule, team, year, month):
    """Prints a calendar view for a specific team - shows home vs away"""
    games_this_month = [
        g for g in get_games_by_month(schedule, year, month)
        if g.home_team is team or g.away_team is team
    ]

    print(f"\n{team.name} - {calendar.month_name[month]} {year}")
    print(f"  {'Mon':<6}{'Tue':<6}{'Wed':<6}{'Thu':<6}{'Fri':<6}{'Sat':<6}{'Sun':<6}")
    print(f"  {'-' * 42}")

    cal = calendar.monthcalendar(year, month)

    # Map day to H (home) or A (away)
    game_map = {}
    for g in games_this_month:
        if g.home_team is team:
            game_map[g.date.day] = "H"
        else:
            game_map[g.date.day] = "A"

    for week in cal:
        row = "  "
        for day in week:
            if day == 0:
                row += f"{'':6}"
            elif day in game_map:
                row += f"{game_map[day] + str(day):<6}"
            else:
                row += f"{day:<6}"
        print(row)

    home_count = sum(1 for g in games_this_month if g.home_team is team)
    away_count = sum(1 for g in games_this_month if g.away_team is team)
    print(f"\n  H = home ({home_count})  A = away ({away_count})")
                    
