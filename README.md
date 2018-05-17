# rockies_eval
Evaluation exercises for Rockies R+D

### Programming Exercise
* script executable from bash command line
* accepts date argument as '2018-05-16'
* pulls game data from Gameday API and outputs a CSV with specified columns

***
### README.txt
All following information is additionally included in a file README.txt, per specifications. 

#### Using this script
* From a command line, navigate to the directory containing the script `scrapeGamesByDate.py`
* Run the command `>> python scrapeGamesByDate.py [DATE]` where `[DATE]` is a string representation of a date of form YYYY-MM-DD
* If for some reason the date is misformatted, the date is in the future, or no games were played on the given date, the script will alert and exit.
* The script with create a new directory `daily_games_records` if it does not exist where output CSVs will be stored
* Required packages not from the standard library are found in requirements.txt. 
* If you have Pip installed (which you should) you can run `>>pip install -r requirements.txt`
* This script works with Python 2 and 3


