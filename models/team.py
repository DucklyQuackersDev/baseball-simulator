class Team:
    """Roster and tracks lineup positions and pitchers"""
    def __init__(self, name, city, lineup, rotation, bullpen):
        self.name = name
        self.city = city
        self.lineup = lineup                #batting order
        self.rotation = rotation            #list of starting pitchers
        self.bullpen = bullpen              #list of relief pitchers
        self.lineup_index = 0               #who is up to bat
        self.current_pitcher = rotation[0]  #Starting pitcher starts

    def get_current_batter(self):
        return self.lineup[self.lineup_index]
    
    def advance_lineup(self):
        self.lineup_index = (self.lineup_index + 1) % 9

    def reset(self):
        self.lineup_index = 0
        self.current_pitcher = self.rotation[0]
        for player in self.all_players():
            player.reset_game_stats()

    def all_players(self):
        return self.lineup + self.rotation + self.bullpen
    
    def print_lineup(self):
        print(f"\n{self.city} {self.name} Lineup:")
        for i, player in enumerate(self.lineup):
            print(f"  {i + 1}. {player.name:<15} {player.position}")
        print(f"  SP: {self.current_pitcher}")

    def print_box_score(self):
        print(f"\n{self.city} {self.name} Box Score:")
        for player in self.lineup:
            player.print_game_batting_line()
        print()
        for pitcher in self.rotation + self.bullpen:
            if pitcher.game_pitching_stats.pitches > 0:
                pitcher.print_game_pitching_line()
        