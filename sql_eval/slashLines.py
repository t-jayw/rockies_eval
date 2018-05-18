import mysql.connector
import pandas as pd

slash_query = """
SELECT batter_id,
       CONCAT(CONCAT(name.name_last, ', '), name.name_first) AS batter_name,
       COUNT(1) AS PA, -- Every non-PA event is filtered in JOIN or WHERE 

       -- Filter out PA events that are not ABs
       SUM(IF(event_type NOT IN ('catcher_interf', 
                                   'hit_by_pitch', 
                                   'intent_walk', 
                                   'sac_bunt', 
                                   'sac_bunt_double_play', 
                                   'sac_fly', 
                                   'sac_fly_double_play', 
                                   'walk'), 1, 0)) AS AB,
       -- Hits
       SUM(IF(event_type IN ('single', 
                               'double', 
                               'triple', 
                               'home_run'), 1, 0)) AS hit,

       -- Hits / ABs
       SUM(IF(event_type IN ('single', 
                            'double', 
                            'triple', 
                            'home_run'), 1, 0))/
       SUM(IF(event_type NOT IN ('catcher_interf', 
                            'hit_by_pitch', 
                            'intent_walk', 
                            'sac_bunt', 
                            'sac_bunt_double_play', 
                            'sac_fly', 
                            'sac_fly_double_play', 
                            'walk'), 1, 0)) AS AVG,

       -- Reach base / AB + Walks + Sac Flies
       SUM(IF(event_type IN ('single', 
                            'double', 
                            'triple', 
                            'home_run', 
                            'walk', 
                            'intent_walk', 
                            'hit_by_pitch'), 1,0)) / 
       SUM(IF(event_type NOT IN ('catcher_interf', 
                                'sac_bunt', 
                                'sac_bunt_double_play'), 1,0)) AS OBP,

       -- (single * 1 + double * 2 + triple * 3 + hr * 4)/ABs
       SUM(CASE WHEN event_type = 'single' THEN 1 
                   WHEN event_type = 'double' THEN 2 
                   WHEN event_type = 'triple' THEN 3 
                   WHEN event_type = 'home_run' THEN 4 
                   ELSE 0 
                   END) / 
       SUM(IF(event_type NOT IN ('catcher_interf', 
                                'hit_by_pitch', 
                                'intent_walk', 
                                'sac_bunt', 
                                'sac_bunt_double_play', 
                                'sac_fly', 
                                'sac_fly_double_play', 
                                'walk'), 1, 0)) AS SLG
FROM mlb.pbp_play_by_play
LEFT JOIN mlb.player_master name ON batter_id = name.player_id
-- Primary filtering of non PA event_types
AND event_type NOT IN (
                       'fan_interference',
                       'runner_interference',
                       'error',
                       'other_out',
                       'cs_double_play',
                       'passed_ball',
                       'wild_pitch',
                       'other_advance',
                       'defensive_indiff',
                       'batter_interference',
                       'balk')
WHERE
    event_type NOT LIKE 'caught_stealing%' 
    AND event_type NOT LIKE 'pickoff%'
    AND event_type NOT LIKE 'stolen_base%'
GROUP BY batter_id
"""

# manage and utilize connection to mysql server
cnx = mysql.connector.connect(user='tyler_wood', password='GoRockies2018',
host="rockies-data-engineer.cxac4memkn4c.us-east-1.rds.amazonaws.com",
port=3306)
cursor = cnx.cursor()
cursor.execute(slash_query)
results = cursor.fetchall()
cnx.close()

# Load data to df, drop unneeded column, export to csv
# Would have been much easier to do this all in Pandas,
# but it was an SQL exercise
df = pd.DataFrame(results, 
					columns=['batter_id', 'name', 'PA', 'AB', 'HIT', 'AVG', 'OBP', 'SLG'])
df.drop(columns=['HIT'], inplace=True)
df.to_csv('mlb_player_2016_slashlines.csv')

