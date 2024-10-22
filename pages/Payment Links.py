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
df2['Amount (incl VAT)'] = df2['Credit (Source)'] * 1.20

st.subheader("Xero PAYG invoices")
st.dataframe(df2)
st.write(len(df2))

# All invoices that are in both

result = df1.merge(df2, how='inner', left_on='id', right_on='Adyen Ref ID')
st.dataframe(result)
st.write(len(result))
