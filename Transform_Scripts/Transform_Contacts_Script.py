"""
File Name: Transform_Contacts_Scripts.py
Author: Will Ronan

Modifications
[Project ID/Name]    June 12, 2025   Creating Transform_Contacts_Scripts to reformat the data into a useable dataframe
"""

import pandas as pd


# Loading Both Contact Excel Sheets (Tier 1's & Tier 2's)
df_Contacts_T1 = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/ContactsT1.xlsx', engine = 'openpyxl')
df_Contacts_T2 = pd.read_excel('/Users/ronanwill/DE_Assignment/Clean_DataFiles/ContactsT2.xlsx', engine = 'openpyxl')



# Removeing the spaces and unwated characters in the Phone & Secondary Phone columns
df_Contacts_T1['Phone'] = df_Contacts_T1['Phone'].str.replace(r"[()\-\s]", "", regex=True) # Removes the ( ) - and spaces
df_Contacts_T1['Secondary Phone'] = df_Contacts_T1['Secondary Phone'].str.replace(r"[()\-\s]", "", regex=True) # Removes the ( ) - and spaces

df_Contacts_T2['Phone'] = df_Contacts_T1['Phone'].str.replace(r"[()\-\s]", "", regex=True) # Removes the ( ) - and spaces
df_Contacts_T2['Secondary Phone'] = df_Contacts_T1['Secondary Phone'].str.replace(r"[()\-\s]", "", regex=True) # Removes the ( ) - and spaces


# Adding +1 infort of the Phone & Secondary Phone numbers that do not have it
df_Contacts_T1['Phone'] = df_Contacts_T1['Phone'].apply(
    lambda x: x if pd.isna(x) else (x if str(x).startswith('+') else '+1' + str(x)) #IF the records is NULL then leave it, IF the record starts with + then leave it, ELSE +1
)

df_Contacts_T1['Secondary Phone'] = df_Contacts_T1['Secondary Phone'].apply(
    lambda x: x if pd.isna(x) else (x if str(x).startswith('+') else '+1' + str(x)) #IF the records is NULL then leave it, IF the record starts with + then leave it, ELSE +1
)

df_Contacts_T2['Phone'] = df_Contacts_T2['Phone'].apply(
    lambda x: x if pd.isna(x) else (x if str(x).startswith('+') else '+1' + str(x)) #IF the records is NULL then leave it, IF the record starts with + then leave it, ELSE +1
)

df_Contacts_T2['Secondary Phone'] = df_Contacts_T2['Secondary Phone'].apply(
    lambda x: x if pd.isna(x) else (x if str(x).startswith('+') else '+1' + str(x)) #IF the records is NULL then leave it, IF the record starts with + then leave it, ELSE +1
)


# Modifying the Data Added column data type to datetime
df_Contacts_T1['Birthday'] = pd.to_datetime(df_Contacts_T1['Birthday'], format='%m/%d/%Y')
df_Contacts_T2['Birthday'] = pd.to_datetime(df_Contacts_T1['Birthday'], format='%m/%d/%Y')


# Added a new column to the dataframe called Tier Status and giving all the columns a value of 1 from the Tier's 1 list. And the value of 2 for the Tier's 2 list
df_Contacts_T1['Tier Status'] = 1
df_Contacts_T2['Tier Status'] = 2


# Contact T2 Secondary Phone number is NULL ~ A NULL row is return data type float64. Chaning it to object
df_Contacts_T2['Secondary Phone'] = df_Contacts_T2['Secondary Phone'].astype('object')



# Joining both Data Frames
df_Contacts = pd.concat([df_Contacts_T1, df_Contacts_T2], ignore_index=True)


df_Contacts.to_excel('/Users/ronanwill/DE_Assignment/Transformed_DataFiles/Contacts.xlsx', index=False)
