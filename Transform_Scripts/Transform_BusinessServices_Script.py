"""
File Name: Transform_BusinessServices_Scripts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Transform_BusinessServices_Scripts to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading Business Services Pipeline Excel Sheet
df_BusinessServices = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/BusinessServices.xlsx', engine = 'openpyxl')



# Assume df is your DataFrame and these are the 5 columns you're checking:
columns_to_check = ['2014A EBITDA', '2015A EBITDA', '2016A EBITDA', '2017A/E EBITDA', '2018E EBITDA']


# Creating a function to find the currency in the rows
def find_currency(row):
    for col in columns_to_check:
        val = str(row[col]).strip().upper()

        if 'CAD' in val or val.startswith('C$') or val.startswith('C'): #If record has a C in the begining, the mark the new column with CAD
            return 'CAD'
        elif any(char.isdigit() for char in val):  # check for number
            return 'USD'
    
    return ''  # no match


df_BusinessServices['Currency'] = df_BusinessServices.apply(find_currency, axis=1)


# Creating a function to check if certain columns have LTM in the records
def extract_ltm(row):
    ltm_value = None

    # Check if '2016A EBITDA' has 'LTM'
    if isinstance(row['2016A EBITDA'], str) and 'LTM' in row['2016A EBITDA']:
        ltm_value = row['2016A EBITDA']
        row['2016A EBITDA'] = None  # clear original

    # Check if '2017A/E EBITDA' has 'LTM'
    elif isinstance(row['2017A/E EBITDA'], str) and 'LTM' in row['2017A/E EBITDA']:
        ltm_value = row['2017A/E EBITDA']
        row['2017A/E EBITDA'] = None  # clear original

    row['LTM EBITDA'] = ltm_value # moves the value to the ltm column
    return row

# Apply to each row
df_BusinessServices = df_BusinessServices.apply(extract_ltm, axis=1)



# Convert to datetime
df_BusinessServices['Date Added'] = pd.to_datetime(df_BusinessServices['Date Added'], format='%b-%y', errors='coerce').fillna(
    pd.to_datetime(df_BusinessServices['Date Added'], errors='coerce')
)



# Creating a function to convert to String and extarct unwanted characters
def format_to_string(column):
    df_BusinessServices[column] = df_BusinessServices[column].astype(str).str.extract(r'([\d]+\.?\d*)')

format_to_string('LTM EBITDA')
format_to_string('2014A EBITDA')
format_to_string('2015A EBITDA')
format_to_string('2016A EBITDA')
format_to_string('2017A/E EBITDA')
format_to_string('Enterprise Value')
format_to_string('Equity Investment Est.')


#df_BusinessServices['LTM EBITDA'] = df_BusinessServices['LTM EBITDA'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['2014A EBITDA'] = df_BusinessServices['2014A EBITDA'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['2015A EBITDA'] = df_BusinessServices['2015A EBITDA'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['2016A EBITDA'] = df_BusinessServices['2016A EBITDA'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['2017A/E EBITDA'] = df_BusinessServices['2017A/E EBITDA'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['Enterprise Value'] = df_BusinessServices['Enterprise Value'].astype(str).str.extract(r'([\d]+\.?\d*)')
#df_BusinessServices['Equity Investment Est.'] = df_BusinessServices['Equity Investment Est.'].astype(str).str.extract(r'([\d]+\.?\d*)')

# Creating a function to convert back to Numeric
def format_back_to_numeric(column):
    df_BusinessServices[column] = pd.to_numeric(df_BusinessServices[column])

format_back_to_numeric('LTM EBITDA')
format_back_to_numeric('2014A EBITDA')
format_back_to_numeric('2015A EBITDA')
format_back_to_numeric('2016A EBITDA')
format_back_to_numeric('2017A/E EBITDA')
format_back_to_numeric('Enterprise Value')
format_back_to_numeric('Equity Investment Est.')



# Step 1: Replace / with a consistent separator
df_BusinessServices['Invest. Bank'] = df_BusinessServices['Invest. Bank'].str.replace('/', ',',).str.strip()

# Step 2: Split each entry into a list
df_BusinessServices['Invest. Bank'] = df_BusinessServices['Invest. Bank'].str.split(',')

# Step 3: Explode into separate rows
df_BusinessServices = df_BusinessServices.explode('Invest. Bank')

# Step 4: Strip extra spaces
df_BusinessServices['Invest. Bank'] = df_BusinessServices['Invest. Bank'].str.strip()





df_BusinessServices.to_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/BusinessServices.xlsx', index=False)