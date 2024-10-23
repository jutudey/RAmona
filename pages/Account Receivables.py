import streamlit as st
import sqlite3
import pandas as pd
import functions
from PIL import Image
import numpy as np
import re

app_name=functions.set_page_definitition()

#----------------------------------------------------
# filepaths
#----------------------------------------------------
PaymentLinks = "data/paymentLinks-2024-10-22.csv"
XeroARreport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_Aged_Receivables_Detail.xlsx"
XeroPAYGrecReport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_PAYG_Reconciliation.xlsx"
eV_animals = "data/Animals-2024-10-23-13-51-41.csv"


#----------------------------------------------------
# Import Adyen links
#----------------------------------------------------

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
df3 = functions.load_xero_AR_report(XeroARreport)
st.dataframe(df3)
st.write(len(df3))

st.subheader("All Xero PAYG invoices - df2")

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
# Search for invoice details
#----------------------------------------------------


st.sidebar.subheader("Find invoice details")

# Create a text input to search by invoice id
# ar_invoice = st.sidebar.text_input('Enter Invoice ID:', '')
ar_invoice = "INV-7648"
st.sidebar.subheader(ar_invoice)
# Create a text input to search by Contact Code
contact_code = st.sidebar.text_input('Enter Contact Code:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('Enter Last Name:', '')


#----------------------------------------------------
# Present all info for individual invoice
#----------------------------------------------------

if ar_invoice:
    # Payment link data
    ar_xero_status = df2.loc[df2['Invoice Number'] == ar_invoice, 'Status'].iloc[0]
    st.write("Xero status: " + ar_xero_status)

    ar_amount = df1.loc[df1['Invoice ID'] == ar_invoice, 'amount'].iloc[0]
    st.write("Outstanding amount: " + ar_amount)

    ar_link_date = df1.loc[df1['Invoice ID'] == ar_invoice, 'creationDate'].iloc[0]
    st.write("Link creation date: " + ar_link_date)

    ar_customer_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Customer ID'].iloc[0]
    st.write("Customer ID: " + ar_customer_id)

    ar_paymentLink = df1.loc[df1['Invoice ID'] == ar_invoice, 'paymentLink'].iloc[0]
    st.write("Payment Link: " + ar_paymentLink)

    ar_link_status = df1.loc[df1['Invoice ID'] == ar_invoice, 'status'].iloc[0]
    st.write("Adyen status: " + ar_link_status)

    ar_pet_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Pet ID'].iloc[0]
    st.write("Pet ID: " + ar_pet_id)

    # collect customer details
    contact_data = functions.get_contact_details(ar_customer_id)
    st.dataframe(contact_data)
    # st.write("### Customer Details:")
    # st.write(f"Customer ID: {contact_data.iloc[0]['Contact Code']}")
    # st.write(f"First Name: {contact_data.iloc[0]['Contact First Name']}")
    # st.write(f"Last Name: {contact_data.iloc[0]['Contact Last Name']}")

    pet_data = functions.get_pet_data(eV_animals)

    # Ensure both 'Animal Code' column and 'ar_pet_id' are of the same type
    pet_data['Animal Code'] = pet_data['Animal Code'].astype(str)
    ar_pet_id = str(ar_pet_id)

    # Now perform the lookup
    pet_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name'].iloc[0]

    # pet_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name'].iloc[0]
    st.write(pet_name)

    ar_invoices = functions.get_invoices(ar_pet_id)
    st.dataframe(ar_invoices)
    st.markdown(ar_invoices.to_markdown(index=False), unsafe_allow_html=True)

    if len(ar_invoices)>1:
        selected_invoice_id = st.radio("Select Invoice ID:", ar_invoices['Invoice #'], horizontal=True)
    else:
        selected_invoice_id = ar_invoices['Invoice #'].values[0]

    st.write(f"### Details for Invoice no.: {selected_invoice_id}")


    ar_invoice_lines = functions.get_invoiceDetails(selected_invoice_id)
    st.dataframe(ar_invoice_lines)

