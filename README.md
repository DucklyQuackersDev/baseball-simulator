# Baseball Simulation
Simple Baseball game simulation

## Getting Started
This project was built in python 3.14 and is required to run this file

## Installing and Running
Follow the steps below:

1. Download the zip files from this repository 

2. Unzip project files into a designated folder

3. Open terminal and navigate to file location

4. (Optional) Generate your own players by running "python tools/generate_players.py"

5. type "python main.py" in cmd to run
    - Default Mode is "Single Game" between New York and Boston
    - To simulate a full season: "python main.py season"
    - To simulate a series between two teams from the list: python main.py series "[team_name1]" "[team_name2]" [#games]
    - To simulate a season from a single team perspective chosen from the list: python main.py team [team_name]

## Current Features
- Simple game simulation with working base running mechanics and score tracking
- 16 teams with players assigned randomly at runtime, only the first 2 are used in the simulation
- Player stats affect hitting outcomes
- New player generator in /tools so you can generate your own random players
- Full season scheduler and simulation
- Multiple simulation modes: 
    - Single Game
    - 3 Game series
    - Full Season
    - Team Focused Season

# Teams List
**East Division**
- New York Americans
- Boston Red Eyes
- Toronto Blue Birds
- Tampa Bay Devils
- Baltimore Ushers
- Detroit Cars
- Cleveland Protectors
- Minnesota Brothers

**West Division**
- Los Angeles Dodgeballs
- San Francisco Davids
- San Diego Fathers
- Colorado Boulders
- Arizona Serpents
- Chicago Little Bears
- St. Louis Popes
- Milwaukee Decanters

## Upcoming Features
- fielding positions and stats
- more specific hit data (where was the ball hit? what positions we're involved in the fielding)
- errors
- better baserunning functionality (stolen bases, 1st to 3rd on singles, advance in a fielders choice)
- better pitching (wild pitches, hit by pitch etc., better timings on pulling pitcher)
- Post Season and World Series


## Built With
- [VS Code](https://code.visualstudio.com/) - text editor
- [Python 3.14](https://www.python.org/downloads/release/python-3140/)

## Versioning
Current version 2.2

## Authors
- **Duck** - *Main contributor* - [DucklyQuackersDev](https://github.com/DucklyQuackersDev)

## License
This project is licensed under the GNU GPL 3.0 License - see the [LICENSE.md](https://github.com/DucklyQuackersDev/baseball-simulator/blob/main/License) file for details
