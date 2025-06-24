"""
File Name: deals.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating deals to reformat the data into a useable dataframe
"""

import pandas as pd

# Loading from the Target Table Directory 
df_ConsumerRetail = pd.read_excel('/Transformed_DataFiles/ConsumerRetail.xlsx', engine = 'openpyxl')
df_BusinessServices = pd.read_excel('/Transformed_DataFiles/BusinessServices.xlsx', engine = 'openpyxl')
df_company = pd.read_excel('/Final_Tables/company.xlsx', engine = 'openpyxl')


# CONCATING Both dfs - Consumer Retail & Business Servies
df_deals = pd.concat([df_BusinessServices, df_ConsumerRetail])


# Creating Function - Combine Columns to combine/merge the columns in the df
def combine_columns(columns, new_column_name):
    df_deals[new_column_name] = df_deals[columns].bfill(axis=1).iloc[:, 0]

combine_columns(['Est. Equity Investment', 'Equity Investment Est.'], 'est_equity_investment')


# Creating Function - Drop Columns to drop/remove the columns in the df
def drop_columns(columns):
    df_deals.drop(columns=columns, inplace=True)

drop_columns('Invest. Bank')
drop_columns('Banker')
drop_columns('Vertical')
drop_columns('Sub Vertical')
drop_columns('Current Owner')
drop_columns('Banker Email')
drop_columns('Banker Phone Number')
drop_columns('Portfolio Company Status')
drop_columns('Business Description')
drop_columns('Est. Equity Investment')
drop_columns('Equity Investment Est.')


# Renaming the columns for consistency 
df_deals.rename(columns={
    'Company Name': 'company_name',
    'Project Name': 'project_name',
    'Date Added': 'date_added',
    'Sourcing': 'sourcing',
    'Transaction Type': 'transaction_type',
    'LTM Revenue': 'ltm_revenue',
    'LTM EBITDA': 'ltm_ebitda',
    'Enterprise Value': 'enterprise_value',
    'Lead MD': 'lead_md',
    'Currency': 'currency',
    'Active Stage': 'active_stage',
    'Passed Rationale': 'passed_rationale',
    '2014A EBITDA': '2014a_ebitda',
    '2015A EBITDA': '2015a_ebitda',
    '2016A EBITDA': '2016a_ebitda',
    '2017A/E EBITDA': '2014ae_ebitda',
    '2018E EBITDA': '2018e_ebitda',
    'Status': 'status'
}, inplace=True)


# Remove Dups
df_deals = df_deals.drop_duplicates()

# Setting PK
df_deals['deal_id'] = range(1, len(df_deals) + 1)


# LEFT JOINGING comapny table
df_deals = pd.merge(
    df_deals, 
    df_company[['company_name', 'company_id']],
    on='company_name',
    how='left'
)

drop_columns('company_name')


# Reordering the columns
new_col_order = ['deal_id', 'company_id', 'project_name', 'transaction_type', 'sourcing', 'date_added', 'ltm_revenue', 'ltm_ebitda', '2014a_ebitda', '2015a_ebitda', '2016a_ebitda', '2014ae_ebitda', '2018e_ebitda', 'enterprise_value', 'est_equity_investment', 'status', 'active_stage', 'passed_rationale', 'lead_md']
df_deals = df_deals[new_col_order]

print(df_deals)
df_deals.to_excel('/Final_Tables/deals.xlsx', index=False)
