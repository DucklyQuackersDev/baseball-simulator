from dataclasses import dataclass, field
from datetime import date
from models.team import Team

@dataclass
class Game:
    """Represents a single game, can be scheduled or completed"""
    home_team: object
    away_team: object
    date: date
    played: bool = False

    # Results
    home_runs = 0
    away_runs = 0

    def __str__(self):
        if self.played:
            return (f"{self.date} | {self.away_team.name} {self.away_runs} "
                    f"@ {self.home_team.name} {self.home_runs}")
        return f"{self.date} | {self.away_team.name} @ {self.home_team.name}"
    
    @property
    def winner(self):
        if not self.played:
            return None
        return self.home_team if self.home_runs > self.away_runs else self.away_team
