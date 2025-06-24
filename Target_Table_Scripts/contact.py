"""
File Name: contacts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating contacts to reformat the data into a useable dataframe
"""

import pandas as pd

# Loading from the Target Table Directory 
df_Contacts_old= pd.read_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/Contacts.xlsx', engine = 'openpyxl')
df_PEComps = pd.read_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/PEComps.xlsx', engine = 'openpyxl')
df_company = pd.read_excel('/Users/ronanwill/DE_Assignment/Final_Tables/company.xlsx', engine = 'openpyxl')


# CONCATING the Name columns from Contacts df and the PE Companies df
df_contacts = pd.concat([
    df_Contacts_old['Name'],
    df_PEComps['Name 1'],
    df_PEComps['Name 2'],
], ignore_index=True).to_frame(name='contact_name')


#Remove Nulls
df_contacts = df_contacts[df_contacts['contact_name'].notna()]


# LEFT JOINGING Contacts df
df_contacts = pd.merge(
    df_contacts, 
    df_Contacts_old[['Name', 'Firm', 'Title', 'City', 'E-mail', 'Phone', 'Secondary Phone', 'Birthday', 'Coverage Person', 'Preferred Contact Method', 'Tier Status']],
    left_on='contact_name',
    right_on='Name',
    how='left'
)

# LEFT JOINGING PE Companies df
df_contacts = pd.merge(
    df_contacts, 
    df_PEComps[['Name 1', 'Company Name', 'Title 1', 'Contact Phone 1',	'Contact Email 1', 'Tier status 1']],
    left_on='contact_name',
    right_on='Name 1',
    how='left'
)

# LEFT JOINGING PE Companies df
df_contacts = pd.merge(
    df_contacts, 
    df_PEComps[['Name 2', 'Company Name', 'Title 2', 'Contact Phone 2',	'Contact Email 2', 'Tier status 2']],
    left_on='contact_name',
    right_on='Name 2',
    how='left'
)


# Creating Function - Combine Columns to combine/merge the columns in the df
def combine_columns(columns, new_column_name):
    df_contacts[new_column_name] = df_contacts[columns].bfill(axis=1).iloc[:, 0]

combine_columns(['Name 1', 'Name 2'], 'name_z')
combine_columns(['Company Name_x', 'Company Name_y'], 'company_name_z')
combine_columns(['Title 1', 'Title 2'], 'title_z')
combine_columns(['Contact Phone 1', 'Contact Phone 2'], 'phone_z')
combine_columns(['Contact Email 1', 'Contact Email 2'], 'email_z')
combine_columns(['Tier status 1', 'Tier status 2'], 'tier_z')


# Creating Function - Drop Columns to drop/remove the columns in the df
def drop_columns(columns):
    df_contacts.drop(columns=columns, inplace=True)

drop_columns('Name 1')
drop_columns('Name 2')
drop_columns('Company Name_x')
drop_columns('Company Name_y')
drop_columns('Title 1')
drop_columns('Title 2')
drop_columns('Contact Phone 1')
drop_columns('Contact Phone 2')
drop_columns('Contact Email 1')
drop_columns('Contact Email 2')
drop_columns('Tier status 1')
drop_columns('Tier status 2')

# Calling combine columns function
combine_columns(['contact_name', 'name_z'], 'contact_name_w')
combine_columns(['Firm', 'company_name_z'], 'company_name')
combine_columns(['Title', 'title_z'], 'title')
combine_columns(['Phone', 'phone_z'], 'primary_phone')
combine_columns(['E-mail', 'email_z'], 'email')
combine_columns(['Tier Status', 'tier_z'], 'tier_status')

# Calling drop columns function
drop_columns('contact_name')
drop_columns('name_z')
drop_columns('Firm')
drop_columns('company_name_z')
drop_columns('Title')
drop_columns('title_z')
drop_columns('Phone')
drop_columns('phone_z')
drop_columns('E-mail')
drop_columns('email_z')
drop_columns('Tier Status')
drop_columns('tier_z')
drop_columns('Name')

# Renaming the columns for consistency 
df_contacts.rename(columns={
    'City': 'city',
    'Secondary Phone': 'secondary_phone',
    'Birthday': 'birthday',
    'Coverage Person': 'coverage_person',
    'Preferred Contact Method': 'preferred_contact_method',
    'contact_name_w': 'name',
}, inplace=True)


# LEFT JOINGING comapny table
df_contacts = pd.merge(
    df_contacts, 
    df_company[['company_name', 'company_id']],
    on='company_name',
    how='left'
)

# Calling drop columns function
drop_columns('company_name')


# Removing Duplicate rows
df_contacts = df_contacts.drop_duplicates()

# Indexing for the contact ID column
df_contacts['contact_id'] = range(1, len(df_contacts) + 1)


# Reordering the columns
new_col_order = ['contact_id', 'company_id', 'name', 'title', 'city', 'email', 'primary_phone', 'secondary_phone', 'birthday', 'coverage_person', 'preferred_contact_method', 'tier_status']
df_contacts = df_contacts[new_col_order]


print(df_contacts)
df_contacts.to_excel('/Users/ronanwill/DE_Assignment/Final_Tables/contacts.xlsx', index=False)

