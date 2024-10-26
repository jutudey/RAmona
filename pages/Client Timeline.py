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

st.header(contact_code)

# Collect Pet details
pet_data = functions.get_pet_details(contact_code)
print(pet_data)

if not pet_data.empty:
    st.write("### Pet Details:")
    st.markdown(pet_data.to_markdown(index=False), unsafe_allow_html=True)
    if len(pet_data)>1:
        selected_pet_id = st.radio("Select Pet ID:", pet_data['Pet ID'], horizontal=True)
    else:
        selected_pet_id = pet_data['Pet ID'].values[0]

    selected_pet_name = pet_data.loc[pet_data['Pet ID'] == selected_pet_id, 'Name'].values[0]
    print(selected_pet_name)
    print(selected_pet_id)
    st.write(f"### Selected pet : {selected_pet_name}")

    # incl_subsc = st.radio("Include Subscription invoices", ("No", "Yes"))
    #
    # if incl_subsc == "No":
    #     payg_invoices = functions.get_invoices_wo_subsc(selected_pet_id)
    #     if not payg_invoices.empty:
    #         # selected_pet_name = pet_data.loc[pet_data['Pet ID'] == selected_pet_id, 'Name'].values[0]
    #         st.markdown(payg_invoices.to_markdown(index=False), unsafe_allow_html=True)
    #     else:
    #         st.write("All invoices are Subscription invoices.")
    #
    # if incl_subsc == "Yes":
    #     all_invoices = functions.get_invoices(selected_pet_id)
    #     if not all_invoices.empty:
    #         st.markdown(all_invoices.to_markdown(index=False), unsafe_allow_html=True)
    #     else:
    #         st.write("No invoices found for the selected pet.")
    # else:
    #     st.write("No pets found for this customer.")

