"""
File Name: Format_Script.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Format_Script to reformat the data into a useable dataframe
"""

import pandas as pd



#    Loading all source files into dataframes (Including the multiple excel sheets in Contacts & Events file)
#        - Business Services Pipeline
#        - Consumer Retail and Healthcare Pipeline
#        - PE Comps
#        - Contacts (Tier 1's & Tier 2's)
#        - Events (Leaders and Partners Dinner & 2019 Market Re-Cap)


df_BusinessServices = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Business Services Pipeline.xlsx', engine = 'openpyxl')
df_ConsumerRetail = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Consumer Retail and Healthcare Pipeline.xlsx', engine = 'openpyxl')
df_PEComps = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/PE Comps.xlsx', engine = 'openpyxl')
df_Contacts_T1 = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Contacts.xlsx', sheet_name = "Tier 1's", engine = 'openpyxl')
df_Contacts_T2 = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Contacts.xlsx', sheet_name = "Tier 2's", engine = 'openpyxl')
df_Events_LPD = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Events.xlsx', sheet_name = "Leaders and Partners Dinner", engine = 'openpyxl')
df_Events_MRC = pd.read_excel('/Users/ronanwill/DE_Assignment/IntappDataEngineerAssessment/Events.xlsx', sheet_name = "2019 Market Re-Cap", engine = 'openpyxl')



# Creating a function to remove unwanted/Null rows
# Passing arguments df & rows_to_remove to input different dataframes and number of rows to remove
## After the rows ae removed the df will create a new index
def remove_rows_by_index(df, rows_to_remove):
    return df.drop(index=rows_to_remove).reset_index(drop=True)

df_BusinessServices = remove_rows_by_index(df_BusinessServices, [0, 1, 2, 3])
df_ConsumerRetail = remove_rows_by_index(df_ConsumerRetail, [0, 1, 2, 3, 4, 5, 6]) ## NEED TO REMOVE 1ST COLUMN
df_PEComps = remove_rows_by_index(df_PEComps, [0, 2])



# Removing all rows after index 190 for Consumer Retail
df_ConsumerRetail = df_ConsumerRetail.iloc[:192]



## Removing the first column in the Consumer Retail and Healthcare Pipeline df 
df_ConsumerRetail = df_ConsumerRetail.iloc[:, 1:]



def set_first_row_as_header(df):
    new_header = df.iloc[0]        # Get the first row
    df = df[1:].reset_index(drop=True)  # Drop the first row and reset index
    df.columns = new_header        # Set new column names
    return df

df_BusinessServices = set_first_row_as_header(df_BusinessServices)
df_ConsumerRetail = set_first_row_as_header(df_ConsumerRetail)
df_PEComps = set_first_row_as_header(df_PEComps)






#   Strating Analysis - Gather general information about the data

"""
# Getting the column names of each df
print(df_BusinessServices.columns)
print(df_ConsumerRetail.columns)
print(df_PEComps.columns)
print(df_Contacts_T1.columns)
print(df_Contacts_T2.columns)
print(df_Events_LPD.columns)
print(df_Events_MRC.columns)
"""


#print(df_BusinessServices.dtypes)
#print(df_ConsumerRetail.dtypes)
#print(df_PEComps.dtypes)
#print(df_Contacts_T1.dtypes)
#print(df_Contacts_T2.dtypes)
#print(df_Events_LPD.dtypes)
#print(df_Events_MRC.dtypes)



#print(df_BusinessServices.count())
#print(df_ConsumerRetail.count())
#print(df_PEComps.count())
#print(df_Contacts_T1.count())
#print(df_Contacts_T2.count())
#print(df_Events_LPD.count())
#print(df_Events_MRC.count())





def column_level_max_lengths(df):
    return df.astype(str).applymap(len).max()

#print(column_level_max_lengths(df_BusinessServices))
#print(column_level_max_lengths(df_ConsumerRetail))
#print(column_level_max_lengths(df_PEComps))
#print(column_level_max_lengths(df_Contacts_T1))
#print(column_level_max_lengths(df_Contacts_T2))
#print(column_level_max_lengths(df_Events_LPD))
#print(column_level_max_lengths(df_Events_MRC))



df_BusinessServices.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/BusinessServices.xlsx', index=False)
df_ConsumerRetail.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/ConsumerRetail.xlsx', index=False)
df_PEComps.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/PEComps.xlsx', index=False)
df_Contacts_T1.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/Contacts.xlsx', sheet_name="Tier 1's", index=False)
df_Contacts_T2.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/Contacts.xlsx', sheet_name="Tier 2's", index=False)
df_Events_LPD.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/Events.xlsx', sheet_name="Leaders and Partners Dinner", index=False)
df_Events_MRC.to_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/Events.xlsx', sheet_name="2019 Market Re-Cap", index=False)