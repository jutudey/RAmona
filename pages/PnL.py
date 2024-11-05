import streamlit as st
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PIL import Image

app_name = functions.set_page_definitition()

st.title("⏳ P&L for Pets and Clients")
#

# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

if 'tl' not in st.session_state:
    st.session_state.tl = functions.build_tl()

if 'selected_pet_id' not in st.session_state:
    st.session_state.selected_pet_id = ''

if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = ''

tl = st.session_state.tl

st.dataframe(tl)
# Ensure tl_Revenue and tl_Cost are numeric
tl['tl_Revenue'] = pd.to_numeric(tl['tl_Revenue'], errors='coerce')
tl['tl_Cost'] = pd.to_numeric(tl['tl_Cost'], errors='coerce')

# Group by tl_PetID and calculate total revenue, total cost, and add customer and pet names
grouped_df = tl.groupby('tl_PetID').agg(
    total_revenue=('tl_Revenue', 'sum'),
    total_cost=('tl_Cost', 'sum'),
    tl_CustomerName=('tl_CustomerName', 'first')
).reset_index()

# Handle tl_PetName by selecting the first non-empty value
grouped_df['tl_PetName'] = tl.groupby('tl_PetID')['tl_PetName'].apply(lambda x: x[x != ''].iloc[0] if any(x != '') else '')

# Calculate total P&L for each tl_PetID
grouped_df['total_pnl'] = grouped_df['total_revenue'] - grouped_df['total_cost']

st.dataframe(grouped_df)

