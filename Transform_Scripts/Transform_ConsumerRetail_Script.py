"""
File Name: Transform_ConsumerRetail_Scripts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Transform_ConsumerRetail_Scripts to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading Consumer Retail and Healthcare Pipeline Excel Sheet
df_ConsumerRetail = pd.read_excel('/Clean_DataFiles/ConsumerRetail.xlsx', engine = 'openpyxl')



# Modifying the Banker Emial column to remove the unwanted spaces
df_ConsumerRetail['Banker Email'] = df_ConsumerRetail['Banker Email'].str.replace(' ', '', regex=False)


# Removeing the spaces and unwated characters in the Banker Phone Number column
df_ConsumerRetail['Banker Phone Number'] = df_ConsumerRetail['Banker Phone Number'].str.replace(r"[()\-\s]", "", regex=True) # Removes the ( ) - and spaces


# Adding +1 infort of the Banker Phone Number that do not have it
df_ConsumerRetail['Banker Phone Number'] = df_ConsumerRetail['Banker Phone Number'].apply(
    lambda x: x if pd.isna(x) else (x if str(x).startswith('+') else '+1' + str(x)) #IF the records is NULL then leave it, IF the record starts with + then leave it, ELSE +1
)


# Removing Hidden/Non-Formatted characters from the Company Name
df_ConsumerRetail['Company Name'] = df_ConsumerRetail['Company Name'].str.encode('ascii', 'ignore').str.decode('ascii')


# Replacing the : and ; in the Banker column with a ,
df_ConsumerRetail['Banker'] = df_ConsumerRetail['Banker'].str.replace(r'[:;]', ',', regex=True)



# Manually modifing 3 banks with incorrect bank names
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.replace('Nomura Bank of America', 'Nomura, Bank of America')
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.replace('Houlihan Lokey UBS', 'Houlihan Lokey, UBS')
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.replace('Barclays Goldman Sachs', 'Barclays, Goldman Sachs')


# Stringping the column and replace nulle strings with actual nulls
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.strip()
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].replace('N/A', pd.NA)



# Step 1: Replace ; and , with a consistent separator
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.replace(';', ',',).str.replace('\n', '').str.strip()

# Step 2: Split each entry into a list
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.split(',')

# Step 3: Explode into separate rows
df_ConsumerRetail = df_ConsumerRetail.explode('Invest. Bank')

# Step 4: Strip extra spaces
df_ConsumerRetail['Invest. Bank'] = df_ConsumerRetail['Invest. Bank'].str.strip()

# Filing Null columns with actual null values
df_ConsumerRetail['Banker'] = df_ConsumerRetail['Banker'].fillna('')


# Formatting the Banker column
df_ConsumerRetail['Banker'] = df_ConsumerRetail.apply(
    lambda row: ', '.join( # Joins the filtered names back into a single string seperated by columns
        [name for name in row['Banker'].split(', ') if name.endswith(f"({row['Invest. Bank']})")] # This keeps only names that end in the investment bank’s name in parentheses.
    ) if pd.notna(row['Banker']) and any(name.endswith(f"({row['Invest. Bank']})") for name in row['Banker'].split(', ')) else row['Banker'], # Only does the filtering if "Banker" is not null and at least one name matches the filter.
    axis=1
)


# Step 2: Split each entry into a list
df_ConsumerRetail['Banker'] = df_ConsumerRetail['Banker'].str.split(',')

# Step 3: Explode into separate rows
df_ConsumerRetail = df_ConsumerRetail.explode('Banker')

# Step 4: Strip extra spaces
df_ConsumerRetail['Banker'] = df_ConsumerRetail['Banker'].str.strip()

# Remove the (Bank Names)
df_ConsumerRetail['Banker'] = df_ConsumerRetail['Banker'].str.replace(r'\s*\([^)]*\)', '', regex=True)



def make_email(row):
    name = row['Banker']
    bank = row['Invest. Bank']

    # Check if name is a valid string with at least one space
    if isinstance(name, str) and ' ' in name:
        first_name, last_name = name.split(' ', 1)
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = f"{first_name}.{last_name}@{bank}.com"
    else:
        # fallback email if name invalid
        email = None

    return email

df_ConsumerRetail['Banker Email'] = df_ConsumerRetail.apply(make_email, axis=1)

df_ConsumerRetail['Banker Email'] = df_ConsumerRetail['Banker Email'].str.replace(' ', '', regex=False)



df_ConsumerRetail.to_excel('/Transformed_DataFiles/ConsumerRetail.xlsx', index=False)
