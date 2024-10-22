import streamlit as st
import sqlite3
import pandas as pd
import functions
from PIL import Image
import numpy as np
import re

app_name=functions.set_page_definitition()

#----------------------------------------------------
# Import Adyen links
#----------------------------------------------------

PaymentLinks = "data/paymentLinks-2024-10-22.csv"
df1 = functions.load_cvs_data(PaymentLinks)

# identifies links created in Adyen as PAYG
df1['Link Type'] = df1['createdBy'].apply(lambda x: 'PAYG - Adyen' if pd.notna(x) else None)

# identifes VERA Toolbox links as PAYG
def set_link_type(row):
    if pd.notna(row['createdBy']):
        return 'PAYG - Vera Toolbox'
    if isinstance(row['merchantReference'], str) and re.search(r"[ _-]", row['merchantReference']):
        return 'PAYG - Vera Toolbox'
    return None

# Apply the function to create the "Link Type" column
df1['Link Type'] = df1.apply(set_link_type, axis=1)

df1['Link Type'] = df1['Link Type'].fillna('Failed Subscription')


st.subheader("Adyen Payment Links")
st.dataframe(df1)
st.write(len(df1))



#----------------------------------------------------
# Import Xero PAYG invoices
#----------------------------------------------------

XeroInvoices = "data/Education___Clinical_Research___Innovation_Group_Limited_-_PAYG_Reconciliation.xlsx"
df2 = functions.load_xero_data(XeroInvoices)



# Cleaning up the ref ID
# Define a helper function
def process_reference(value):
    if isinstance(value, str) and value.startswith('PL:'):
        return value[3:]
    else:
        return np.nan

# Apply the helper function to the "Reference" column to create the new column
df2['Adyen Ref ID'] = df2['Reference'].apply(process_reference)

# add VAT to the amount
df2['Amount (incl VAT)'] = (df2['Credit (Source)'] * 1.20).round(2)

st.subheader("Xero PAYG invoices")
st.dataframe(df2)
st.write(len(df2))

# All invoices that are in both

in_both = df1.merge(df2, how='inner', left_on='id', right_on='Adyen Ref ID')
st.dataframe(in_both)
st.write(len(in_both))

st.subheader("Easily matched")

in_both_display = in_both[["Invoice Number", "status", "creationDate", "amount", "Description"]]
st.dataframe(in_both_display)
st.write(len(in_both_display))

st.subheader("Only in Adyen")

df_not_in_df2 = df1.merge(df2, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
st.dataframe(df_not_in_df2)
st.write(len(df_not_in_df2))
