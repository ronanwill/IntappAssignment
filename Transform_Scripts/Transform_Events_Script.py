"""
File Name: Transform_BusinessServices_Scripts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Transform_BusinessServices_Scripts to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading Both Events Excel Sheets (Tier 1's & Tier 2's)
df_Events_LPD = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/EventsLPD.xlsx', engine = 'openpyxl')
df_Events_MRC = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/EventsMRC.xlsx', engine = 'openpyxl')



# Adding a new column called Events and I will populate that column with Leaders and Partner Dinners
df_Events_LPD['Event'] = 'Leaders and Partner Dinners'


# Adding a new column called Events and I will populate that column with 2019 Market Re-Cap
df_Events_MRC['Event'] = '2019 Market Re-Cap'


# Joining both Data Frames
df_Events = pd.concat([df_Events_LPD, df_Events_MRC], ignore_index=True)


df_Events['Tier Status'] = 2


df_Events.to_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/Events.xlsx', index=False)

print(df_Events)
