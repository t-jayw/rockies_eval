import sys, argparse, os, requests, json

import pandas as pd

from datetime import datetime as dt


DATE_FORMAT = '%Y-%m-%d'
BASE_URL="https://gd2.mlb.com/components/"+ \
          "game/mlb/year_%s/month_%s/day_%s/grid.json"
wanted_cols = ['away_code','away_file_code', 'away_name_abbrev',
      'away_score', 'away_team_id', 'away_team_name', 'calendar_event_id',
      'double_header_sw', 'event_time', 'game_nbr', 'game_pk', 'game_type',
      'gameday_sw', 'group', 'home_code', 'home_file_code', 'home_name_abbrev',
      'home_score', 'home_team_id', 'home_team_name', 'id', 'ind', 'inning',
      'media_state', 'series', 'series_num', 'status', 'tbd_flag', 'top_inning',
      'venue', 'venue_id',]
records_dir = 'daily_games_records'
help_string = """
Please run this script with the following command
\n>> rip_script.py yyyy-mm-dd\n
Where the date is formated 'yyyy-mm-dd'
More info in readme.txt"""

def establish_directory(directory_name=records_dir):
  if not os.path.exists(directory_name):
    os.makedirs(directory_name)
    print(directory_name)

def print_help():
  print(help_string)
  exit()

def validate_date(date_arg):
    try:
      date = dt.strptime(date_arg, DATE_FORMAT)
    except ValueError:
      return False
    return date_arg

def format_request(date):
  date = date.split('-')
  y, m, d = date[0], date[1], date[2]
  url = BASE_URL%(y, m, d)
  return url

def request_data(url):
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
  drop = list(set(df.columns) - set(wanted_cols))
  df = df.drop(columns = drop)
  return df

def write_to_csv(df, date):
  filename = 'game_records_%s.csv'%(date)
  path = os.path.join(records_dir, filename)
  df.to_csv(path)
  print "csv written to "+"path"


if __name__ == "__main__":
  establish_directory()

  args = sys.argv
  
  if len(args) <> 2:
    print_help()

  date = sys.argv[1]

  date = validate_date(date)

  if not date:
    print("""Incorrectly formatted date argument.""")
    print_help()
  
  url = format_request(date)
  data = request_data(url)
  df = create_df(data)
  df = drop_unwanted_columns(df, wanted_cols)
  write_to_csv(df, date)






