import streamlit as st
import sqlite3
import pandas as pd
import functions
from PIL import Image
import numpy as np

app_name=functions.set_page_definitition()

# Import Adyen links

PaymentLinks = "data/paymentLinks-2024-10-22.csv"
df1 = functions.load_cvs_data(PaymentLinks)

st.subheader("Adyen Payment Links")
st.dataframe(df1)
st.write(len(df1))

# Import Xero PAYG invoices

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

df_not_in_df2 = df1.merge(df2, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
st.dataframe(df_not_in_df2)
st.write(len(df_not_in_df2))
