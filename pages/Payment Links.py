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
df1 = functions.load_adyen_links(PaymentLinks)

# Filter only PAYG links
df1 = df1[df1['Link Type'].str.contains('PAYG', na=True)]

st.subheader("Adyen PAYG Payment Links - df1")
st.write("Payment links related to failed subscription payments have been disregarded")
st.dataframe(df1)
st.write(len(df1))

#----------------------------------------------------
# Import Xero PAYG data
#----------------------------------------------------

st.subheader("Xero Accounts Receivables report - df3")
XeroARreport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_Aged_Receivables_Detail.xlsx"
df3 = functions.load_xero_AR_report(XeroARreport)
st.dataframe(df3)
st.write(len(df3))

st.subheader("All Xero PAYG invoices - df2")

XeroPAYGrecReport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_PAYG_Reconciliation.xlsx"
df2 = functions.load_xero_PAYGrec_report(XeroPAYGrecReport)

# Update Status in df2 where Invoice Number exists in df3
df2.loc[df2['Invoice Number'].isin(df3['Invoice Number']), 'Status'] = 'Unpaid'


st.dataframe(df2)
st.write(len(df2))






#----------------------------------------------------
# Merging tables
#----------------------------------------------------

# All PAYG links that are in both
in_both = df1.merge(df2, how='inner', left_on='id', right_on='Adyen Ref ID')
st.subheader("merged data")
st.dataframe(in_both)
st.write(len(in_both))

st.subheader("Easily matched (using payment link ID")

in_both_display = in_both[["Invoice Number",
                           "status", "Status", "Link Type", "creationDate",
                           "amount", "Description", "Customer ID", "Pet ID"]]
st.dataframe(in_both_display)
st.write(len(in_both_display))

# st.subheader("Only in Adyen")

df_not_in_df2 = df1.merge(df2, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
# st.dataframe(df_not_in_df2)
# st.write(len(df_not_in_df2))


#----------------------------------------------------
# investigate individual invoice
#----------------------------------------------------


st.sidebar.subheader("Find invoice details")

# Create a text input to search by invoice id
# ar_invoice = st.sidebar.text_input('Enter Invoice ID:', '')
ar_invoice = "INV-8830"
st.sidebar.subheader("INV-8830")
# Create a text input to search by Contact Code
contact_code = st.sidebar.text_input('Enter Contact Code:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('Enter Last Name:', '')

# Collect Payment Link status
if ar_invoice:
    ar_customer_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Customer ID'].iloc[0]
    st.write("Customer ID: " + ar_customer_id)
    ar_pet_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Pet ID'].iloc[0]
    st.write("Pet ID: " + ar_pet_id)

