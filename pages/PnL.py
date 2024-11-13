import streamlit as st
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PIL import Image

app_name = functions.set_page_definitition()

st.title("⚖️ P&L for Pets and Clients")

# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

functions.initialize_session_state()


invoice_lines = st.session_state.all_invoice_lines
adyenlinks = st.session_state.adyenlinks
selected_invoice_no = st.session_state.selected_invoice_no
tl = st.session_state.tl
# st.dataframe(tl)
print("1 P&L Session state invoice id: " + st.session_state.selected_invoice_no)
print("1 P&L Session state customer id: " + st.session_state.selected_customer_id)
print("1 P&L Session state pet id: ")
print(st.session_state.selected_pet_id)
# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

MostProfitablePet, MostExpensivePet, MostContributingOwner, MostExpensiveOwner = st.tabs(["Most Profitable Pets",
                                                                                          "Most Expensive Pet",
                                                                                          "Most Contributing Owners",
                                                                                          "Most Expensive Owners"])

# Group by tl_PetID and calculate sums for tl_Revenue and tl_Cost
tl_grouped = tl.groupby('tl_PetID').agg({
  'tl_PetName': 'first',
  'tl_CustomerID': 'first',
  'tl_CustomerName': 'first',
  'tl_Revenue': 'sum',
  'tl_Cost': 'sum'
}).reset_index()

# Add a new column for revenue minus cost
tl_grouped['tl_Profit'] = tl_grouped['tl_Revenue'] - tl_grouped['tl_Cost']

# Rename columns
tl_grouped.rename(columns={
    'tl_PetName': 'Pet Name',
    'tl_PetID': 'Pet eV ID',
    'tl_CustomerID': 'Customer eV ID',
    'tl_CustomerName': 'Customer Name',
    'tl_Revenue': 'Revenue',
    'tl_Cost': 'Cost',
    'tl_Profit': 'P&L',
    'tl_Comment': 'Comment'}, inplace=True)

with MostProfitablePet:
    # Show the top 20 entries with the highest P&L
    st.subheader("📈   Top 20 most profitable pets")
    top_20_pl = tl_grouped.nlargest(20, 'P&L')
    # st.dataframe(top_20_pl)
    try:
        selected_pet_id, selected_customer_id = functions.multi_selectbox(top_20_pl, "Pet eV ID", 'Customer eV ID')
        st.session_state.selected_pet_id = selected_pet_id
        st.session_state.selected_customer_id = selected_customer_id
        print("2 P&L Session state invoice id: " + st.session_state.selected_invoice_no)
        print("2 P&L Session state customer id: " + st.session_state.selected_customer_id)
        print("2P&L Session state pet id: ")
        print(st.session_state.selected_pet_id)
    except IndexError:
        pass

with MostExpensivePet:

    # Show the top 20 entries with the lowest P&L
    st.subheader("📉   Top 20 most expensive pets")
    top_20_lowest_pl = tl_grouped.nsmallest(20, 'P&L')
    st.dataframe(top_20_lowest_pl)

# Group by tl_PetID and calculate sums for tl_Revenue and tl_Cost
    tl_grouped = tl.groupby('tl_CustomerID').agg({
        'tl_CustomerName': 'first',
        'tl_Revenue': 'sum',
        'tl_Cost': 'sum'
    }).reset_index()

    # Add a new column for revenue minus cost
    tl_grouped['tl_Profit'] = tl_grouped['tl_Revenue'] - tl_grouped['tl_Cost']

    # Rename columns
    tl_grouped.rename(columns={
        'tl_PetName': 'Pet Name',
        'tl_PetID': 'Pet eV ID',
        'tl_CustomerID': 'Customer eV ID',
        'tl_CustomerName': 'Customer Name',
        'tl_Revenue': 'Revenue',
        'tl_Cost': 'Cost',
        'tl_Profit': 'P&L',
        'tl_Comment': 'Comment'}, inplace=True)

with MostContributingOwner:
    # Show the top 20 entries with the highest P&L
    st.subheader("📈  Top 20 most contributing Owners")
    top_20_pl = tl_grouped.nlargest(20, 'P&L')
    st.dataframe(top_20_pl)

with MostExpensiveOwner:
    # Show the top 20 entries with the lowest P&L
    st.subheader("📉  Top 20 most leaching Owners")
    top_20_lowest_pl = tl_grouped.nsmallest(20, 'P&L')
    st.dataframe(top_20_lowest_pl)

# # Display grouped tl DataFrame
# st.subheader("P&L for all pets")
# st.dataframe(tl_grouped)
