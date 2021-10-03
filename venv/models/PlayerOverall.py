import os
import re
import datetime
import pandas as pd

file_list = os.listdir()

date_pattern = re.compile(r'\b(\d{2})-(\d{2})-(\d{4})\b')

# Extracting date for getting the file with the latest date
def get_date(filename):
    matched = date_pattern.search(filename)
    if not matched:
        return None
    m, d, y = map(int, matched.groups())
    return datetime.date(y, m, d)

dates = (get_date(fn) for fn in file_list)
dates = (d for d in dates if d is not None)
last_date = max(dates) #Getting the latest date
last_date = last_date.strftime('%m-%d-%Y')
latest_file = [fn for fn in file_list if last_date in fn] #Getting the file name with the latest date

print(latest_file[0])

workbook = pd.read_csv(latest_file[0])

workbook.fillna(0, inplace=True)

#Cleaning for Ball Control and Dribbling
workbook = workbook[~workbook.BallControl.str.contains("BallControl",)]
workbook = workbook[~workbook.Dribbling.str.contains("Dribbling")]

new_workbook = pd.DataFrame()
new_workbook['Ball_Skills'] = (workbook['BallControl'].astype(int) + workbook['Dribbling'].astype(int))/2


new_workbook['Defence'] = (workbook['SlideTackle'].astype(int) + workbook['StandTackle'].astype(int) +
                           workbook['Marking'].astype(int))/3



#Cleaning for Acceleration,Stamina,Strength,Balance,SprintSpeed,Agility,Jumping
workbook = workbook[~workbook.Acceleration.str.contains("Acceleration")]
workbook = workbook[~workbook.Stamina.str.contains("Stamina")]
workbook = workbook[~workbook.Strength.str.contains("Strength")]
workbook = workbook[~workbook.SprintSpeed.str.contains("SprintSpeed")]

new_workbook['Physical'] = (
                            workbook['Acceleration'].astype(int) + workbook['Stamina'].astype(int) +
                            workbook['Strength'].astype(int) + workbook['Balance'].astype(int) +
                            workbook['SprintSpeed'].astype(int) + workbook['Agility'].astype(int) +
                            workbook['Jumping'].astype(int)
                            )/7

#Cleaning for Heading,ShotPower,Finishing,LongShots,Curve,FKAcc,Penalties,Volleys
workbook = workbook[~workbook.Heading.str.contains("Heading")]
workbook = workbook[~workbook.ShotPower.str.contains("ShotPower")]
workbook = workbook[~workbook.Finishing.str.contains("Finishing")]
workbook = workbook[~workbook.LongShots.str.contains("LongShots")]
workbook = workbook[~workbook.FKAcc.str.contains("FKAcc")]
workbook = workbook[~workbook.Penalties.str.contains("Penalties", na=False)]
workbook = workbook[~workbook.Volleys.str.contains("Volleys", na=False)]

new_workbook['Shooting'] =(
                            workbook['Heading'].astype(int) + workbook['ShotPower'].astype(int) +
                            workbook['Finishing'].astype(int) + workbook['LongShots'].astype(int) +
                            workbook['Curve'].astype(int) + workbook['FKAcc'].astype(int) +
                            workbook['Penalties'].astype(int) + workbook['Volleys'].astype(int)
                            )/8


#Cleaning for Aggression,Reactions,AttPosition,Interceptions,Vision,Composure
workbook = workbook[~workbook.Aggression.str.contains("Aggression")]
workbook = workbook[~workbook.Reactions.str.contains("Reactions")]
workbook = workbook[~workbook.AttPosition.str.contains("AttPosition", na=False)]
workbook = workbook[~workbook.Interceptions.str.contains("Interceptions", na=False)]
workbook = workbook[~workbook.Vision.str.contains("Vision", na=False)]
workbook = workbook[~workbook.Composure.str.contains("Composure", na=False)]

new_workbook['Mental'] =(
                            workbook['Aggression'].astype(int) + workbook['Reactions'].astype(int) +
                            workbook['AttPosition'].astype(int) + workbook['Interceptions'].astype(int) +
                            workbook['Vision'].astype(int) + workbook['Composure'].astype(int)
                        )/6

#Cleaning for Crossing,Short Pass,Long Pass
workbook = workbook[~workbook.Crossing.str.contains("Crossing")]
workbook = workbook[~workbook.ShortPass.str.contains("ShortPass")]
workbook = workbook[~workbook.LongPass.str.contains("LongPass")]

new_workbook['Passing'] =  (
                            workbook['Crossing'].astype(int) + workbook['ShortPass'].astype(int) +
                            workbook['LongPass'].astype(int)

                        )/3

#Cleaning for GKPositioning,GKDiving GKHandling,GKKicking,GKReflexes
workbook = workbook[~workbook.Crossing.str.contains("GKPositioning")]
workbook = workbook[~workbook.ShortPass.str.contains("GKDiving")]
workbook = workbook[~workbook.LongPass.str.contains("GKHandling")]
workbook = workbook[~workbook.Crossing.str.contains("GKKicking")]
workbook = workbook[~workbook.ShortPass.str.contains("GKReflexes")]

new_workbook['Goalkeeper'] =  (
                            workbook['GKPositioning'].astype(int) + workbook['GKDiving'].astype(int) +
                            workbook['GKHandling'].astype(int) + workbook['GKKicking'].astype(int) +
                            workbook['GKReflexes'].astype(int)
                        )/5

new_workbook['Specialities'] = workbook['Specialities']


print(new_workbook.head())
print(new_workbook.info())