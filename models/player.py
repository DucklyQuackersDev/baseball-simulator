## RATINGS ##
class Ratings:
    """Influence probabilities in baserunning and hitting"""
    def __init__(self, contact, power, discipline, speed, gb_rate, fielding, arm_strength):
        self.contact = contact              #hit rate
        self.power = power                  #HR and XBH rate
        self.discipline = discipline        #BB and K rate
        self.speed = speed                  #Base running and infield hits
        self.gb_rate = gb_rate              #groundball vs flyball
        self.arm_strength = arm_strength    #for baserunning defense
        self.fielding = fielding            #for errors

class PitcherRatings:
    """Pitching attributes"""
    def __init__(self, stuff, control, stamina, gb_rate):
        self.stuff = stuff      #K rate
        self.control = control  #BB rate
        self.stamina = stamina  #How long can they pitch
        self.gb_rate = gb_rate  #groundball vs flyball

## Career Stats ##
class BattingStats:
    """Career hitting results - doesn't reset"""
    def __init__(self):
        self.games = 0
        self.at_bats = 0
        self.hits = 0
        self.singles = 0
        self.doubles = 0
        self.triples = 0
        self.homeruns = 0
        self.rbi = 0
        self.runs = 0
        self.walks = 0
        self.strikeouts = 0

    @property
    def avg(self):
        return self.hits / self.at_bats if self.at_bats > 0 else 0.000
    
    @property
    def obp(self):
        plate_appearances = self.at_bats + self.walks
        return (self.hits + self.walks) / plate_appearances if plate_appearances > 0 else 0.000
    
    @property
    def slg(self):
        total_bases = self.singles + (self.doubles * 2) + (self.triples * 3) + (self.homeruns * 4)
        return total_bases / self.at_bats if self.at_bats > 0 else 0.000
    
    @property
    def ops(self):
        return self.obp + self.slg
    
class PitchingStats:
    """Career pitching results - doesn't reset"""
    def __init__(self):
        self.games = 0
        self.innings_pitched = 0
        self.hits_allowed = 0
        self.runs_allowed = 0
        self.earned_runs = 0
        self.walks_allowed = 0
        self.strikeouts = 0
        self.homeruns_allowed = 0

    @property
    def era(self):
        return (self.earned_runs / self.innings_pitched) * 9 if self.innings_pitched > 0 else 0.000
    
    @property
    def whip(self):
        return (self.walks_allowed + self.hits_allowed) / self.innings_pitched if self.innings_pitched > 0 else 0.000
    
    @property
    def kp9(self):
        return (self.strikeouts / self.innings_pitched) * 9 if self.innings_pitched > 0 else 0.000
    
    @property
    def bb9(self):
        return (self.walks_allowed / self.innings_pitched) * 9 if self.innings_pitched > 0 else 0.000
    
## Game Stats ##
class BattingGameStats:
    """Single game batting results - resets every game"""
    def __init__(self):
        self.at_bats    = 0
        self.hits       = 0
        self.singles    = 0
        self.doubles    = 0
        self.triples    = 0
        self.homeruns  = 0
        self.rbi        = 0
        self.runs       = 0
        self.walks      = 0
        self.strikeouts = 0

    @property
    def avg(self):
        return self.hits / self.at_bats if self.at_bats > 0 else 0.000

    def reset(self):
        self.__init__()

class PitchingGameStats:
    """Single game pitching results - resets every game"""
    def __init__(self):
        self.innings_pitched   = 0.0
        self.hits_allowed      = 0
        self.runs_allowed      = 0
        self.earned_runs       = 0
        self.walks_allowed     = 0
        self.strikeouts        = 0
        self.homeruns_allowed = 0
        self.pitches           = 0

    @property
    def era(self):
        return (self.earned_runs / self.innings_pitched) * 9 if self.innings_pitched > 0 else 0.00

    def reset(self):
        self.__init__()

## Player ##
class Player:
    """Single player - holds ratings, position, and stats"""
    def __init__(self, first_name, last_name, position, ratings, pitching_ratings=None):
        self.first_name = first_name
        self.last_name = last_name
        self.position = position
        self.ratings = ratings
        self.pitching_ratings = pitching_ratings

        #career stats
        self.batting_stats = BattingStats()
        self.pitching_stats = PitchingStats() if pitching_ratings else None

        #single game stats
        self.game_batting_stats = BattingGameStats()
        self.game_pitching_stats = PitchingGameStats() if pitching_ratings else None

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def short_name(self):
        return f"{self.first_name[0]}. {self.last_name}"

    def is_pitcher(self):
        return self.position in ("SP", "RP")
    
    def record_at_bat(self, event, rbis=0):
        """Updates both career and game stats"""
        for stats in [self.batting_stats, self.game_batting_stats]:
            if event != "walk":
                stats.at_bats += 1
            
            match event:
                case "single":
                    stats.hits += 1
                    stats.singles += 1
                case "double":
                    stats.hits += 1
                    stats.doubles += 1
                case "triple":
                    stats.hits += 1
                    stats.triples += 1
                case "homerun":
                    stats.hits += 1
                    stats.homeruns += 1
                case "walk":
                    stats.walks += 1
                case "strikeout":
                    stats.strikeouts += 1

            stats.rbi = rbis

    def record_pitching(self, event, runs_scored, innings_pitched=0):
        for stats in [self.pitching_stats, self.game_pitching_stats]:
            match event:
                case "walk":
                    stats.walks_allowed += 1
                case "strikeout":
                    stats.strikeouts += 1
                case "homerun":
                    stats.homeruns_allowed += 1
                    stats.hits_allowed += 1
                case "single" | "double" | "triple":
                    stats.hits_allowed += 1
            
            stats.runs_allowed += runs_scored
            stats.earned_runs += runs_scored
            stats.innings_pitched += innings_pitched

    def record_run(self):
        """When the player scores"""
        self.batting_stats.runs += 1
        self.game_batting_stats.runs += 1

    def reset_game_stats(self):
        """reset before every game for single game stats"""
        self.game_batting_stats.reset()
        if self.game_pitching_stats:
            self.game_pitching_stats.reset()

    def print_game_batting_line(self):
        s = self.game_batting_stats
        print(f"{self.name:<15} | "
              f"{s.at_bats} AB   {s.hits} H   {s.doubles} 2B   {s.triples} 3B "
              f"{s.homeruns} HR   {s.rbi} RBI   {s.walks} BB   {s.strikeouts} K")
        
    def print_batting_line(self):
        s = self.batting_stats
        print(f"{self.name:<15} | "
              f"{s.at_bats} AB  {s.hits} H  {s.home_runs} HR  {s.rbi} RBI  | "
              f"AVG: {s.avg:.3f}  OBP: {s.obp:.3f}  SLG: {s.slg:.3f}  OPS: {s.ops:.3f}")
        
    def print_game_pitching_line(self):
        if not self.game_pitching_stats:
            return
        s = self.game_pitching_stats
        print(f"{self.name:<15} | "
              f"{s.innings_pitched} IP  {s.hits_allowed} H  "
              f"{s.earned_runs} ER  {s.walks_allowed} BB  {s.strikeouts} K  "
              f"{s.pitches} pitches")
        
    def print_pitching_line(self):
        if not self.pitching_stats:
            return
        s = self.pitching_stats
        print(f"{self.name:<15} | "
              f"{s.innings_pitched} IP  {s.hits_allowed} H  "
              f"{s.earned_runs} ER  {s.walks_allowed} BB  {s.strikeouts} K  | "
              f"ERA: {s.era:.2f}  WHIP: {s.whip:.2f}")