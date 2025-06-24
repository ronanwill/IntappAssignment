"""
File Name: Transform_PEComps_Scripts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Transform_PEComps_Scripts to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading PE Comps Excel Sheet
df_PEComps = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/PEComps.xlsx', engine = 'openpyxl')


# Formatting the Sectors, Sample Portfolio Companies & Comments columns to remove the - and space. It will also replace the new line with a comma
df_PEComps['Sectors'] = df_PEComps['Sectors'].str.replace(r'- ', '', regex=True).str.replace(r'\n', ', ', regex=True).str.strip()
df_PEComps['Sample Portfolio Companies'] = df_PEComps['Sample Portfolio Companies'].str.replace(r'- ', '', regex=True).str.replace(r'\n', ', ', regex=True).str.strip()
df_PEComps['Comments'] = df_PEComps['Comments'].str.replace(r'- ', '', regex=True).str.replace(r'\n', ', ', regex=True).str.strip()


# Transforming the Contact Name 1 and Contact 2 Columns

# Step 1: Replacing every , with a new line. This way the data is at least seperated on a new line (Name, Title, Email, and Phone Number)
df_PEComps['Contact Name 1'] = df_PEComps['Contact Name 1'].str.replace(',', '\n')
# Contact 2 is already in this format

# Fixing Index 0 Contact Name 1. The name had a comma in it so I replacing the only fist new line back to comma
df_PEComps.at[0, 'Contact Name 1'] = df_PEComps.at[0, 'Contact Name 1'].replace('\n', ', ', 1)


# Creating a function to tarnsform the Contact Name 1 and Contact 2 columns
def parse_contact(data):
    if not isinstance(data, str): # Checks if the data is a string string
        return pd.Series(['', '', '', '']) # If not it will return a series of strings. Cannot process non text value

    lines = data.strip().split('\n') # Strinps the data of whitespaces and splits the data into individual lines
    
    # Initializing fields
    name = ""
    title = ""
    phone = ""
    email = ""
    
    for line in lines:
        line = line.strip() # Strips each line of whitespaces
        if "@" in line:
            email = line # If the line has an @ then move it to the email field
        elif any(char.isdigit() for char in line) and len(line) >= 10:
            phone = line # If the line has numbers equal to or less then 10 digits then move it the the phone field 
        elif name == "":
            name = line # Takes the first line of the record and moves it to the phone field
        else:
            title = line # Anything else remaining, move it to the Title field
            
    return pd.Series([name, title, phone, email]) # Wraps the 4 fields into a comma sperated series

# Calling the parse_contact function
df_PEComps[['Name 1', 'Title 1', 'Contact Phone 1', 'Contact Email 1']] = df_PEComps['Contact Name 1'].apply(parse_contact) # Creating new columns in the data frame to place the series data after the column is ran through the function
df_PEComps[['Name 2', 'Title 2', 'Contact Phone 2', 'Contact Email 2']] = df_PEComps['Contact 2'].apply(parse_contact) # Creating new columns in the data frame to place the series data after the column is ran through the function


# Removeing the spaces and unwated characters in the Contact Phone 1 & Contact Phone 2 columns
df_PEComps['Contact Phone 1'] = df_PEComps['Contact Phone 1'].str.replace(r"[()\-\s\.]", "", regex=True) # Removes the ( ) - and spaces
df_PEComps['Contact Phone 2'] = df_PEComps['Contact Phone 2'].str.replace(r"[()\-\s\.]", "", regex=True) # Removes the ( ) - and spaces

# Replacing any record in the Contact Phone 2 column that has an extension to # instead of ext
df_PEComps['Contact Phone 2'] = df_PEComps['Contact Phone 2'].str.replace('ext', '#')


# Adding +1 infort of the Phone & Secondary Phone numbers that do not have it
df_PEComps['Contact Phone 1'] = df_PEComps['Contact Phone 1'].apply(
    lambda x: '' if pd.isna(x) or str(x).strip().lower() in ['', 'nan'] else ('+1' + str(x).lstrip('+1').strip()) # IF the vlue is NULL then return an empty string OR check if the value is just a blank space. ELSE add +1 to the value and strip it for blank spaces 
)

df_PEComps['Contact Phone 2'] = df_PEComps['Contact Phone 2'].apply(
    lambda x: '' if pd.isna(x) or str(x).strip().lower() in ['', 'nan'] else ('+1' + str(x).lstrip('+1').strip()) # IF the vlue is NULL then return an empty string OR check if the value is just a blank space. ELSE add +1 to the value and strip it for blank spaces 
)


# Dropping Origion Contact Name 1 and Contact 2 columns
df_PEComps = df_PEComps.drop('Contact Name 1', axis=1)
df_PEComps = df_PEComps.drop('Contact 2', axis=1)

# Adding Tier Status of 2 to all records that have a corresponding name for both Name 1 & Name 2
df_PEComps['Tier status 1'] = df_PEComps['Name 1'].apply(lambda x: 2 if pd.notna(x) and str(x).strip() != '' else '')
df_PEComps['Tier status 2'] = df_PEComps['Name 2'].apply(lambda x: 2 if pd.notna(x) and str(x).strip() != '' else '')

df_PEComps.to_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/PEComps.xlsx', index=False)