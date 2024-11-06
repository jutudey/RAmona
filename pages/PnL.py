import streamlit as st
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PIL import Image

app_name = functions.set_page_definitition()

st.title("⏳ P&L for Pets and Clients")


# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

if 'tl' not in st.session_state:
    st.session_state.tl = functions.build_tl()


tl = st.session_state.tl
st.dataframe(tl)

# Ensure tl_Revenue, tl_Cost, and tl_PetID are numeric
tl['tl_Revenue'] = pd.to_numeric(tl['tl_Revenue'], errors='coerce')
tl['tl_Cost'] = pd.to_numeric(tl['tl_Cost'], errors='coerce')
tl['tl_PetID'] = pd.to_numeric(tl['tl_PetID'], errors='coerce')

# Load pet details from external function
pet_details_df = functions.get_ezyvet_pet_details()

# Ensure Animal Code is numeric
pet_details_df['Animal Code'] = pd.to_numeric(pet_details_df['Animal Code'], errors='coerce')

# Merge pet details into tl DataFrame
tl = tl.merge(pet_details_df[['Animal Code', 'Animal Name', 'Owner Contact Code', 'Owner Last Name', 'Owner First Name']],
              how='left',
              left_on='tl_PetID',
              right_on='Animal Code')

# Rename columns to match expected output
tl.rename(columns={'Animal Name': 'tl_PetName', 'Owner Contact Code': 'tl_CustomerID', 'Owner Last Name': 'tl_CustomerLastName', 'Owner First Name': 'tl_CustomerFirstName'}, inplace=True)

# Group by tl_PetID and calculate sums for tl_Revenue and tl_Cost
tl_grouped = tl.groupby('tl_PetID').agg({
  'tl_PetName': 'first',
  'tl_CustomerID': 'first',
  'tl_CustomerLastName': 'first',
  'tl_CustomerFirstName': 'first',
  'tl_Revenue': 'sum',
  'tl_Cost': 'sum'
}).reset_index()

# Add a new column for revenue minus cost
tl_grouped['tl_Profit'] = tl_grouped['tl_Revenue'] - tl_grouped['tl_Cost']

# Display grouped tl DataFrame
st.subheader("Grouped tl DataFrame by tl_PetID")
st.dataframe(tl_grouped)
