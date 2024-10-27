import streamlit as st
import sqlite3
import pandas as pd
import functions
from PIL import Image

app_name=functions.set_page_definitition()

st.title("Client Timeline for Pet")

# Streamlit app with sidebar navigation
# st.sidebar.title(app_name)

st.sidebar.subheader("Search for client")

# Create a text input to search by Contact Code
contact_code = st.sidebar.text_input('Enter Customer ID:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('Enter Last Name:', '')



# Search by names
if first_name or last_name:
    contacts_data = functions.get_contacts_by_name(first_name, last_name)
    if not contacts_data.empty:
        selected_contact = st.selectbox('Select a Contact:',
                                        contacts_data["Contact Code"].astype(str) + ' - ' + contacts_data[
                                            "Contact First Name"] + ' ' + contacts_data["Contact Last Name"])
        selected_contact_code = selected_contact.split(' - ')[0]
        contact_code = selected_contact_code

        # Display contact details if Contact Code is provided
        if contact_code:
            contact_data = functions.get_contact_details(contact_code)
            if not contact_data.empty:
                st.write("### Customer Details:")
                st.write(f"Customer ID: {contact_data.iloc[0]['Contact Code']}")
                st.write(f"First Name: {contact_data.iloc[0]['Contact First Name']}")
                st.write(f"Last Name: {contact_data.iloc[0]['Contact Last Name']}")
            else:
                st.info("No details found for this Customer ID")

    else:
        st.write("No contacts found with the given name(s).")

st.header(f" {contact_data.iloc[0]['Contact First Name']} {contact_data.iloc[0]['Contact Last Name']}")

# Collect Pet ID
pet_data = functions.get_pet_details(contact_code)
print(pet_data)

if not pet_data.empty:
    st.write("### Pet Details:")
    st.markdown(pet_data.to_markdown(index=False), unsafe_allow_html=True)

    if len(pet_data) > 1:
        # Show only names in the radio button
        selected_pet_name = st.radio("Select Pet:", pet_data['Name'], horizontal=True)

        # Retrieve the corresponding pet ID for the selected name
        selected_pet_id = pet_data.loc[pet_data['Name'] == selected_pet_name, 'Pet ID'].values[0]
        selected_pet_id = str(selected_pet_id)  # Convert to string
    else:
        selected_pet_id = str(pet_data['Pet ID'].values[0])  # Convert directly to string

    # Select pet name based on the string `selected_pet_id`
    selected_pet_name = pet_data.loc[pet_data['Pet ID'].astype(str) == selected_pet_id, 'Name'].values[0]

    # Print and display the selected pet details
    print(selected_pet_name)
    print(selected_pet_id)
    st.write(f"### Selected pet : {selected_pet_name}")

    # import data for TimeLine
    tl_invoices = functions.extract_tl_Invoices()

    # filter by pet ID
    filt = (tl_invoices["tl_PetID"] == selected_pet_id)
    tl_for_pet = tl_invoices[filt]

    # show timeline data for selected pet

    st.dataframe(tl_for_pet)


    st.dataframe(tl_invoices)

