import streamlit as st
import sqlite3
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt

from PIL import Image

app_name=functions.set_page_definitition()

st.title("Client Timeline for Pet")


#----------------------------------------------------
# Search for client details
#----------------------------------------------------


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

#----------------------------------------------------
# select Pet
#----------------------------------------------------

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

    # ----------------------------------------------------
    # Prepare data for Client Timeline
    # ----------------------------------------------------

    # import data for TimeLine
    tl_invoices = functions.extract_tl_Invoices()
    tl_change_plan = functions.extract_tl_Cancellations()

    # Concatenate the DataFrames
    merged_df = pd.concat([tl_invoices, tl_change_plan], ignore_index=True)

    # Sort the merged DataFrame by the 'date' column
    tl = merged_df.sort_values(by='tl_Date',
                                             ascending=True)  # Set ascending=False if you want descending order

    # Display the sorted DataFrame
    st.dataframe(tl)


    # filter by pet ID
    filt = (tl["tl_PetID"] == selected_pet_id)
    tl_for_pet = tl[filt]

    # ----------------------------------------------------
    # show events on the timeline data for the selected pet
    # ----------------------------------------------------

    st.dataframe(tl_for_pet)

    # ----------------------------------------------------
    # Display visual timeline for the selected pet
    # ----------------------------------------------------

    # Ensure the tl_Date column is in datetime format
    tl_for_pet['tl_Date'] = pd.to_datetime(tl_for_pet['tl_Date'])

    # Extract relevant data and convert it to a list of dictionaries
    timeline_items = [
        {"Event": row['tl_Event'], "Date": row['tl_Date']} for _, row in tl_for_pet.iterrows()
    ]

    # Plot the events on a horizontal line with markers
    fig, ax = plt.subplots(figsize=(12, 2))

    # Draw a horizontal line
    ax.hlines(y=0, xmin=min(tl_for_pet['tl_Date']), xmax=max(tl_for_pet['tl_Date']), color='black', linewidth=1)

    # Add markers for each event
    ax.plot(tl_for_pet['tl_Date'], [0] * len(tl_for_pet), "o", color='blue')

    # Annotate each event with event names
    for idx, row in tl_for_pet.iterrows():
        ax.text(row['tl_Date'], 0.1, row['tl_Event'], ha="center", va="bottom", fontsize=9, rotation=45)

    # Remove y-axis and adjust x-axis
    ax.get_yaxis().set_visible(False)
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)

    # Set limits and labels
    ax.set_ylim(-0.5, 1)
    ax.set_yticks([])

    # Display the figure in Streamlit
    st.pyplot(fig)

    # ----------------------------------------------------
    # Showing the full dataframe
    # ----------------------------------------------------


    st.dataframe(tl_invoices)
