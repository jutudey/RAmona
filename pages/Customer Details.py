import streamlit as st
import sqlite3
import pandas as pd
import functions


app_name = "RAmona v0.1"

# Enable wide mode and set light theme
st.set_page_config(layout="wide", page_title=app_name)

st.title("Customer Details")

# Create 3 columns for the filters
col1, col2, col3 = st.columns(3)

# Add filters in separate columns
with col1:
    # Create a text input to search by Contact Code
    contact_code = st.text_input('Enter Contact Code:', '')

with col2:
    # Add a search box for First Name
    first_name = st.text_input('Enter First Name:', '')

with col3:
    # Add a search box for Last Name
    last_name = st.text_input('Enter Last Name:', '')

# Function to get pet details by Contact Code


# def get_pet_details(contact_code):
#     conn = sqlite3.connect('ramona_db.db')
#     query = f'''
#       SELECT
#         "Animal_Code" as "Pet ID",
#         "Animal_Name" as "Name",
#         "Species",
#         "Breed",
#         "Animal_Record_Created_At" as "First registered at"
#         FROM eV_animals
#         WHERE "Owner_Contact_Code" = '{contact_code}'
#       '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df
#
#     # Function to get contact details by First Name and Last Name
#
#
# def get_contacts_by_name(first_name, last_name):
#     conn = sqlite3.connect('ramona_db.db')
#     conditions = []
#     if first_name:
#         conditions.append(f'"Contact First Name" LIKE "%{first_name}%"')
#     if last_name:
#         conditions.append(f'"Contact Last Name" LIKE "%{last_name}%"')
#     where_clause = ' AND '.join(conditions)
#     query = f'''
#         SELECT
#         "Contact Code",
#         "Contact First Name",
#         "Contact Last Name"
#         FROM eV_Contacts
#         WHERE {where_clause}
#         '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df
#
#     # Display contacts if First Name or Last Name is provided

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
                st.write("No details found for this Contact Code.")

    else:
        st.write("No contacts found with the given name(s).")

    # Function to get contact details by Contact Code


# def get_contact_details(contact_code):
#     conn = sqlite3.connect('ramona_db.db')
#     query = f'''
#         SELECT
#         "Contact Code",
#         "Contact First Name",
#         "Contact Last Name"
#         FROM eV_Contacts
#         WHERE "Contact Code" = {contact_code}
#         '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# Get pet details and display in a table

# Collect Pet details
pet_data = functions.get_pet_details(contact_code)
if not pet_data.empty:
    st.write("### Pet Details:")
    st.markdown(pet_data.to_markdown(index=False), unsafe_allow_html=True)
    selected_pet_id = st.radio("Select Pet ID:", pet_data['Pet ID'])

    selected_pet_name = pet_data.loc[pet_data['Pet ID'] == selected_pet_id, 'Name'].values[0]
    st.write(f"### Invoices for {selected_pet_name}")

    incl_subsc = st.radio("Include Subscription invoices", ("No", "Yes"))

    if incl_subsc == "No":
        payg_invoices = functions.get_invoices_wo_subsc(selected_pet_id)
        if not payg_invoices.empty:
            # selected_pet_name = pet_data.loc[pet_data['Pet ID'] == selected_pet_id, 'Name'].values[0]
            st.markdown(payg_invoices.to_markdown(index=False), unsafe_allow_html=True)
        else:
            st.write("All invoices are Subscription invoices.")

    if incl_subsc == "Yes":
        all_invoices = functions.get_invoices(selected_pet_id)
        if not all_invoices.empty:
            st.markdown(all_invoices.to_markdown(index=False), unsafe_allow_html=True)
        else:
            st.write("No invoices found for the selected pet.")
else:
    st.write("No pets found for this customer.")

