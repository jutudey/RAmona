import streamlit as st
import sqlite3
import pandas as pd
import functions
from PIL import Image

app_name=functions.set_page_definitition()

st.title("Customer Details")


# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

if 'selected_pet_id' not in st.session_state:
    st.session_state.selected_pet_id = ''
    selected_pet_id = st.session_state.selected_pet_id

if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = ''
    selected_customer_id = st.session_state.selected_customer_id

# st.header('selected_pet_id : ' + str(st.session_state.selected_pet_id))
# st.header('selected_customer_id : ' + str(st.session_state.selected_customer_id))




#----------------------------------------------------
# Select data in sidebar
#----------------------------------------------------

st.sidebar.subheader("Search for client")

# Create a text input to search by Contact Code
customer_id = st.sidebar.text_input('Enter Customer ID:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('Enter Last Name:', '')

#----------------------------------------------------
# Extract Customer and Pet data
#----------------------------------------------------

# Search by names
if first_name or last_name:
    contacts_data = functions.get_contacts_by_name(first_name, last_name)
    if not contacts_data.empty:
        selected_contact = st.selectbox('Select a Contact:',
                                        contacts_data["Contact Code"].astype(str) + ' - ' + contacts_data[
                                            "Contact First Name"] + ' ' + contacts_data["Contact Last Name"])
        st.session_state.selected_customer_id = selected_contact.split(' - ')[0]
        # customer_id = selected_customer_id
        # st.session_state.selected_customer_id = selected_customer_id


        # Display contact details if Contact Code is provided
        if st.session_state.selected_customer_id:
            contact_data = functions.get_contact_details(st.session_state.selected_customer_id)
            if not contact_data.empty:
                st.write("### Customer Details:")
                st.write(f"Customer ID: {contact_data.iloc[0]['Contact Code']}")
                st.write(f"First Name: {contact_data.iloc[0]['Contact First Name']}")
                st.write(f"Last Name: {contact_data.iloc[0]['Contact Last Name']}")
            else:
                st.info("No details found for this Customer ID")

    else:
        st.write("No contacts found with the given name(s).")



# Collect Pet details
print('starting to collect pet data')

pet_data = functions.get_pet_details(st.session_state.selected_customer_id)
print(pet_data)
# print(pet_data.iloc[0, 0])
# st.session_state.selected_pet_id = (pet_data.iloc[0, 0])
print("value in session state for customer: " + str(st.session_state.selected_customer_id))
print("value in session state for pet: " + str(st.session_state.selected_pet_id))
if not pet_data.empty:
    st.write("### Pet Details:")
    st.markdown(pet_data.to_markdown(index=False), unsafe_allow_html=True)
    if len(pet_data)>1:
        st.session_state.selected_pet_id = st.radio("Select Pet ID:", pet_data['Pet ID'], horizontal=True)

    else:
        st.session_state.selected_pet_id = pet_data['Pet ID'].values[0]

    print("value in session state for customer after radio button: " + str(st.session_state.selected_customer_id))
    print("value in session state for pet after radio button: " + str(st.session_state.selected_pet_id))

    selected_pet_name = pet_data.loc[pet_data['Pet ID'] == st.session_state.selected_pet_id, 'Name'].values[0]
    st.write(f"### Invoices for {selected_pet_name}")

    # st.header(st.session_state.selected_pet_id)
    # selected_pet_id = str(selected_pet_id)
    all_invoices = functions.extract_tl_Invoices()
    filt = (all_invoices["tl_PetID"] == str(st.session_state.selected_pet_id))
    all_invoices = all_invoices[filt]
    # st.dataframe(all_invoices)
    if not all_invoices.empty:
        filt = (all_invoices["tl_PetID"] == str(st.session_state.selected_pet_id))
        all_invoices = all_invoices[filt]
        st.markdown(all_invoices.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.write("No invoices found for the selected pet.")


