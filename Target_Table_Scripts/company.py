"""
File Name: company.py
Author: Will Ronan

Modifications
[Project ID/Name]   - Creating company table
"""

import pandas as pd


# Loading from the Target Table Directory 
df_ConsumerRetail = pd.read_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/ConsumerRetail.xlsx', engine = 'openpyxl')
df_BusinessServices = pd.read_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/BusinessServices.xlsx', engine = 'openpyxl')
df_PEComps = pd.read_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/PEComps.xlsx', engine = 'openpyxl')



# CONCATING the Name columns from Consumer Retail df and Business Services and PE Companies df
df_company = pd.concat([
    df_ConsumerRetail['Company Name'],
    df_BusinessServices['Company Name'],
    df_PEComps['Company Name']
], ignore_index=True).to_frame(name='company_name')



# Remove Nulls
df_company = df_company[df_company['company_name'].notna()]

#Remove Duplicates
df_company = df_company.drop_duplicates(subset='company_name').reset_index(drop=True)

#remove line 218 & 268 Nomura Bank of America & N/A
df_company = df_company.drop([218, 268]).reset_index(drop=True)



# LEFT JOINGING Consumer Retail df
df_company = pd.merge(
    df_company, 
    df_ConsumerRetail[['Company Name', 'Vertical', 'Sub Vertical', 'Business Description', 'Current Owner', 'Portfolio Company Status']],
    left_on='company_name', 
    right_on='Company Name', 
    how='left'
)

# LEFT JOINGING Business Services df
df_company = pd.merge(
    df_company, 
    df_BusinessServices[['Company Name', 'Vertical', 'Sub Vertical', 'Business Description', 'Current Owner']],
    left_on='company_name', 
    right_on='Company Name', 
    how='left'
)


# Creating Function - Combine Columns to combine/merge the columns in the df
def combine_columns(columns, new_column_name):
    df_company[new_column_name] = df_company[columns].bfill(axis=1).iloc[:, 0]

combine_columns(['Vertical_x', 'Vertical_y'], 'vertical')
combine_columns(['Sub Vertical_x', 'Sub Vertical_y'], 'sub_vertical')
combine_columns(['Business Description_x', 'Business Description_y'], 'business_description')
combine_columns(['Current Owner_x', 'Current Owner_y'], 'current_owner')


# Creating Function - Drop Columns to drop/remove the columns in the df
def drop_columns(columns):
    df_company.drop(columns=columns, inplace=True)

drop_columns('Company Name_x')
drop_columns('Company Name_y')
drop_columns('Vertical_x')
drop_columns('Vertical_y')
drop_columns('Sub Vertical_x')
drop_columns('Sub Vertical_y')
drop_columns('Business Description_x')
drop_columns('Business Description_y')
drop_columns('Current Owner_x')
drop_columns('Current Owner_y')


# LEFT JOINGING PE Companies df
df_company = pd.merge(
    df_company, 
    df_PEComps[['Company Name', 'Priority', 'Website', 'AUM\n(Bns)', 'Sectors', 'Sample Portfolio Companies', 'Comments']],
    left_on='company_name', 
    right_on='Company Name', 
    how='left'
)

# Calling combine columns function
combine_columns(['Comments', 'business_description'], 'business_description')

# Calling Drop column functions
drop_columns('Comments')
drop_columns('Company Name')


# Renaming the columns for consistency 
df_company.rename(columns={
    'Portfolio Company Status': 'portfolio_company_status',
    'Priority': 'priority',
    'Website': 'website',
    'AUM\n(Bns)': 'AUM (Bns)',
    'Sectors': 'sectors',
    'Sample Portfolio Companies': 'sample_portfolio_companies'
}, inplace=True)


# Removing Duplicate rows
df_company = df_company.drop_duplicates()

# Indexing for the company ID column
df_company['company_id'] = range(1, len(df_company) + 1)


# Reordering the columns
new_col_order = ['company_id', 'company_name', 'website', 'AUM (Bns)', 'sectors', 'vertical', 'sub_vertical', 'business_description', 'current_owner', 'portfolio_company_status', 'sample_portfolio_companies', 'priority']
df_company = df_company[new_col_order]



print(df_company)
df_company.to_excel('/Users/ronanwill/DE_Assignment/Final_Tables/company.xlsx', index=False)

