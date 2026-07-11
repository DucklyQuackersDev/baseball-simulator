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
    - Default Mode is "Single Game"
    - To simulate a full season or series pass "season" or "series" as an argument, Ex: "python main.py season" 
    - To simulate a season from a single team perspective pass argument "team"

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

## Upcoming Features
- fielding positions and stats
- more specific hit data (where was the ball hit? what positions we're involved in the fielding)
- errors
- better baserunning functionality (stolen bases, 1st to 3rd on singles, advance in a fielders choice)
- better pitching (wild pitches, hit by pitch etc., better timings on pulling pitcher)
- Better Scheduling (currently only one game per day, need to update to multi games across different teams)
- Post Season and World Series


## Built With
- [VS Code](https://code.visualstudio.com/) - text editor
- [Python 3.14](https://www.python.org/downloads/release/python-3140/)

## Versioning
Current version 2.1

## Authors
- **Duck** - *Main contributor* - [DucklyQuackersDev](https://github.com/DucklyQuackersDev)

## License
This project is licensed under the GNU GPL 3.0 License - see the [LICENSE.md](https://github.com/DucklyQuackersDev/baseball-simulator/blob/main/License) file for details
