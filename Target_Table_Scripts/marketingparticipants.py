"""
File Name: firm.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating pe_firm to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading from the Target Table Directory 
df_Contacts_Old= pd.read_excel('/Transformed_DataFiles/Contacts.xlsx', engine = 'openpyxl')
df_ConsumerRetail = pd.read_excel('/Transformed_DataFiles/ConsumerRetail.xlsx', engine = 'openpyxl')
df_BusinessServices = pd.read_excel('/Transformed_DataFiles/BusinessServices.xlsx', engine = 'openpyxl')
df_Events = pd.read_excel('/Transformed_DataFiles/Events.xlsx', engine = 'openpyxl')
df_company = pd.read_excel('/Finial_DataFile/company.xlsx', engine = 'openpyxl')
df_contacts = pd.read_excel('/Finial_DataFile/contacts.xlsx', engine = 'openpyxl')


# CONCATING the Name columns from Consumer Retail df and Business Services
df_vert = pd.concat([
    df_BusinessServices[['Invest. Bank', 'Company Name', 'Banker']], 
    df_ConsumerRetail[['Invest. Bank', 'Company Name', 'Banker', 'Banker Email', 'Banker Phone Number']]
])

# Remove Nulls
df_vert = df_vert.dropna()

#Remove Duplicates
df_vert.drop_duplicates(inplace=True)


# Creating a new df
df_marketpart = pd.DataFrame({
    'attendee_status': df_Events['Attendee Status'],
    'email': df_Events['E-mail'],
    'event_name': df_Events['Event']
})


# LEFT JOINGING Contacts df
df_marketpart = pd.merge(
    df_marketpart, 
    df_Contacts_Old[['E-mail', 'Firm', 'Group']],
    left_on= 'email',
    right_on='E-mail', 
    how='left'
)


# LEFT JOINGING vert df
df_marketpart = pd.merge(
    df_marketpart, 
    df_vert[['Invest. Bank', 'Company Name', 'Banker', 'Banker Email', 'Banker Phone Number']],
    left_on= 'Firm',
    right_on='Invest. Bank', 
    how='left'
)


# LEFT JOINGING contacts table
df_marketpart = pd.merge(
    df_marketpart, 
    df_contacts[['email', 'contact_id']],
    on= 'email', 
    how='left'
)


# LEFT JOINGING company table
df_marketpart = pd.merge(
    df_marketpart, 
    df_company[['company_name', 'company_id']],
    left_on= 'Company Name',
    right_on= 'company_name',
    how='left'
)


# Creating Function - Drop Columns to drop/remove the columns in the df
def drop_columns(columns):
    df_marketpart.drop(columns=columns, inplace=True)

drop_columns('Invest. Bank')
drop_columns('email')
drop_columns('E-mail')
drop_columns('Company Name')
drop_columns('company_name')


# Renaming the columns for consistency 
df_marketpart.rename(columns={
    'Firm': 'investment_bank',
    'Group': 'group',
    'Banker': 'banker_name',
    'Banker Email': 'banker_email',
    'Banker Phone Number': 'banker_phone'
}, inplace=True)


# Remove Dups
df_marketpart = df_marketpart.drop_duplicates()

# Setting PK
df_marketpart['participants_id'] = range(1, len(df_marketpart) + 1)


# Reordering the columns
new_col_order = ['participants_id', 'contact_id', 'company_id', 'event_name', 'attendee_status', 'investment_bank', 'group', 'banker_name', 'banker_email', 'banker_phone']
df_marketpart = df_marketpart[new_col_order]


print(df_marketpart)
df_marketpart.to_excel('/Final_Tables/marketing_participants.xlsx', index=False)

