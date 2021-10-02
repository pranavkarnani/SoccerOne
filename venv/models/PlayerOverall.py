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
workbook = workbook[~workbook.BallControl.str.contains("BallControl")]
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

print(new_workbook.head())