import pandas as pd
import numpy as np


df = pd.read_csv("../data/SCMS_Delivery_History_Dataset.csv")

#Preprocessing
def null_values(df, feature):
    match feature:
        case 'Line Item Insurance (USD)':
            df[feature] = df[feature].fillna(df['Line Item Insurance (USD)'].median())
            return df
        case 'Shipment Mode':
            df[feature]=df[feature].fillna("Other")
            return df
        case _:
            print('Error')

null_values(df, 'Line Item Insurance (USD)')
null_values(df, 'Shipment Mode')

def replace_strings(df, feature):
    match feature:
        case 'Freight Cost (USD)':
            df[feature]=df[feature].replace("Freight Included in Commodity Cost",0)
            df.loc[df[feature].str.contains('See', na=False), feature] = 'test'
            df[feature] = df[feature].replace('test', 0)
            return df
        case 'Weight (Kilograms)':
            df[feature] = df[feature].replace('Weight Captured Separately', 0)
            df.loc[df[feature].str.contains('See', na=False), feature] = 'test'
            df[feature] = df[feature].replace('test', 0)
            return df
        case 'PO / SO #':
            df.loc[df[feature].str.contains('SCMS', na=False), feature] = 'SCMS'
            df.loc[df[feature].str.contains('SO', na=False), feature] = 'SO'
            return df
        case 'ASN/DN #':
            df.loc[df[feature].str.contains('ASN', na=False), feature] = 'ASN'
            df.loc[df[feature].str.contains('DN', na=False), feature] = 'DN'
        case _:
            print('Error')

replace_strings(df, 'Freight Cost (USD)')
replace_strings(df, 'Weight (Kilograms)')
replace_strings(df, 'PO / SO #')
replace_strings(df, 'ASN/DN #')

df = df[df["PO / SO #"] != 'DSCM-10090']
df=df[(df["Freight Cost (USD)"]!='Invoiced Separately')]

df['Freight Cost (USD)'] = df['Freight Cost (USD)'].astype('float')
df['Weight (Kilograms)'] = df['Weight (Kilograms)'].astype('float')

df['Scheduled Delivery Date'] = pd.to_datetime(df['Scheduled Delivery Date'])
df['Delivery Recorded Date'] = pd.to_datetime(df['Delivery Recorded Date'])

df['Delay'] = df['Delivery Recorded Date'] - df['Scheduled Delivery Date']
df['Delay'] = df['Delay'].dt.days.astype('int64')

df.drop(['ID', 'PQ #','Project Code',  'PQ First Sent to Client Date', 'PO Sent to Vendor Date',
       'Scheduled Delivery Date', 'Delivered to Client Date',
       'Delivery Recorded Date',
       'Vendor', 'Item Description', 'Molecule/Test Type', 'Brand', 'Dosage',
       'Dosage Form', 'Unit of Measure (Per Pack)', 'Line Item Quantity',
       'Line Item Value', 'Pack Price', 'Unit Price', 'Manufacturing Site'], axis=1, inplace=True)

df['PO / SO #'] = pd.get_dummies(df['PO / SO #'], drop_first=True)
df['ASN/DN #'] = pd.get_dummies(df['ASN/DN #'], drop_first=True)

df['Fulfill Via'] = pd.get_dummies(df['Fulfill Via'], drop_first=True)
df['First Line Designation'] = pd.get_dummies(df['First Line Designation'], drop_first=True)