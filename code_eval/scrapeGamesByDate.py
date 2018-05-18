import sys, argparse, os, requests, json

import pandas as pd

from datetime import datetime as dt

### Constants for use later
DATE_FORMAT = '%Y-%m-%d' 
BASE_URL="https://gd2.mlb.com/components/"+ \
          "game/mlb/year_%s/month_%s/day_%s/grid.json"
WANTED_COLS = ['away_code','away_file_code', 'away_name_abbrev',
      'away_score', 'away_team_id', 'away_team_name', 'calendar_event_id',
      'double_header_sw', 'event_time', 'game_nbr', 'game_pk', 'game_type',
      'gameday_sw', 'group', 'home_code', 'home_file_code', 'home_name_abbrev',
      'home_score', 'home_team_id', 'home_team_name', 'id', 'ind', 'inning',
      'media_state', 'series', 'series_num', 'status', 'tbd_flag', 'top_inning',
      'venue', 'venue_id',]
RECORDS_DIR = 'daily_games_records'
HELP_STRING = """
  Please run this script with the following command
  \n>> rip_script.py yyyy-mm-dd\n
  Where the date is formated 'yyyy-mm-dd'
  More info in readme.txt
"""

def establish_directory(directory_name=RECORDS_DIR):
  """specs require an output directory for csv. This
  function checks if directory defined in constants exists
  or else creates it"""
  if not os.path.exists(directory_name):
    os.makedirs(directory_name)
    print(directory_name)

def print_help():
  """Print help info if things break"""
  print(HELP_STRING)
  exit()

def validate_date(date_arg):
  """Ensures date arg is a date of proper format"""
  try:
    date = dt.strptime(date_arg, DATE_FORMAT)
  except ValueError:
    return False
  return date_arg

def format_request(date):
  """Generate the formatted request URL for date"""
  date = date.split('-')
  y, m, d = date[0], date[1], date[2]
  url = BASE_URL%(y, m, d)
  return url

def request_data(url):
  """Fetches the data from formatted URL. 
  Will exit with error message if date is in future,
  or no games were played on specified date"""
  r = requests.get(url).content
  try:
    j = json.loads(r)
    try:
      data = j['data']['games']['game']
      return data
    except KeyError:
      print("No games played on this date")
      exit()
  except ValueError:
    print("No accessible records for provided date")
    exit()

def create_df(data):
  df = pd.DataFrame(data)
  return df

def drop_unwanted_columns(df, wanted_cols):
  """returns a df with only the WANTED_COLS columns"""
  drop = list(set(df.columns) - set(wanted_cols))
  df = df.drop(columns = drop)
  return df

def write_to_csv(df, date):
  filename = 'game_records_%s.csv'%(date)
  path = os.path.join(RECORDS_DIR, filename)
  df.to_csv(path)
  print("csv written to "+path)


if __name__ == "__main__":
  establish_directory()

  ### Process the sys args and check that there are 2
  ### (script name and date), and that the date is
  ### properly formatted
  args = sys.argv
  if len(args)!= 2:
    print_help()
  date = sys.argv[1]
  date = validate_date(date)
  if not date:
    print("""Incorrectly formatted date argument.""")
    print_help()
 
  ### Step by step execution of descriptively named functions
  url = format_request(date)
  data = request_data(url)
  df = create_df(data)
  df = drop_unwanted_columns(df, WANTED_COLS)
  write_to_csv(df, date)

