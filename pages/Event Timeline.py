import streamlit as st
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from PIL import Image

app_name = functions.set_page_definitition()

st.title("Event Timeline for Pet")
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

# st.header('selected_pet_id : ' + str(st.session_state.selected_pet_id))
# st.header('selected_customer_id : ' + str(st.session_state.selected_customer_id))

# ----------------------------------------------------
# Search for client details
# ----------------------------------------------------

st.sidebar.subheader("Search for client")

# Create a text input to search by Contact Code
customer_id = st.sidebar.text_input('Enter Customer ID:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('Enter Last Name:', '')

customer_data = pd.DataFrame()  # Initialize contact_data to avoid NameError

# Search by names
if first_name or last_name:
    contacts_data = functions.get_contacts_by_name(first_name, last_name)
    st.sidebar.write(contacts_data)
    if not contacts_data.empty:
        selected_contact = st.selectbox('Select a Contact:',
                                        contacts_data["Contact Code"].astype(str) + ' - ' + contacts_data[
                                            "Contact First Name"] + ' ' + contacts_data["Contact Last Name"])
        st.session_state.selected_customer_id = selected_contact.split(' - ')[0]
    else:
        st.write("No contacts found with the given name(s).")

# Display contact details if Contact Code is provided
if st.session_state.selected_customer_id:
    customer_data = functions.get_contact_details(st.session_state.selected_customer_id)
    if not customer_data.empty:
        pass
        # st.write("### Customer Details:")
        # st.write(f"Customer ID: {customer_data.iloc[0]['Contact Code']}")
        # st.write(f"First Name: {customer_data.iloc[0]['Contact First Name']}")
        # st.write(f"Last Name: {customer_data.iloc[0]['Contact Last Name']}")
    else:
        st.info("No details found for this Customer ID")

if not customer_data.empty:
    st.header(f" {customer_data.iloc[0]['Contact First Name']} {customer_data.iloc[0]['Contact Last Name']}")

# ----------------------------------------------------
# select Pet
# ----------------------------------------------------

pet_data = functions.get_pet_details(st.session_state.selected_customer_id)

if not pet_data.empty:
    st.write("### Pet Details:")
    st.markdown(pet_data.to_markdown(index=False), unsafe_allow_html=True)

    # If there are multiple pets, allow the user to select one
    if len(pet_data) > 1:
        selected_pet_name = st.radio(
            "Select Pet:",
            pet_data['Name'],
            index=pet_data['Name'].tolist().index(
                pet_data.loc[pet_data['Pet ID'] == st.session_state.selected_pet_id, 'Name'].values[0]
            ) if st.session_state.selected_pet_id in pet_data['Pet ID'].values else 0,
            horizontal=True
        )
    else:
        selected_pet_name = pet_data.loc[0, 'Name']

    st.session_state.selected_pet_id = pet_data.loc[pet_data['Name'] == selected_pet_name, 'Pet ID'].values[0]


    ############################################################
    # Display the selected pet details
    ############################################################

    if str(st.session_state.selected_pet_id) in str(pet_data['Pet ID']):
        selected_pet_name = pet_data.loc[pet_data['Pet ID'] == st.session_state.selected_pet_id, 'Name'].values[0]

        st.write(f"### Key events for {selected_pet_name}")

        # Prepare data for Client Timeline
        tl = st.session_state.tl
        filt = (tl["tl_PetID"] == str(st.session_state.selected_pet_id))
        tl_for_pet = tl[filt]

        # Show events for the selected pet in a table
        if not tl_for_pet.empty:
            tl_table = tl_for_pet[["tl_Date", "tl_Event", "tl_Cost", "tl_Revenue"]].rename(
                columns={
                    "tl_Date": "Event Date",
                    "tl_Event": "Event Description",
                    "tl_Cost": "Internal Cost",
                    "tl_Revenue": "Revenue"
                }
            )

            # Format the date to dd.mm.yyyy
            tl_table["Event Date"] = tl_table["Event Date"].dt.strftime('%d.%m.%Y')

            # Calculate sum of Revenue and Cost
            total_revenue = tl_table["Revenue"].sum()
            total_cost = tl_table["Internal Cost"].sum()

            # Determine P&L line values
            pnl_description = "**P&L for this pet**"
            pnl_revenue = total_revenue if total_revenue > total_cost else 0
            pnl_cost = total_cost if total_cost > total_revenue else 0

            # Create a DataFrame for the summary line
            summary_df = pd.DataFrame([{
                "Event Date": "",
                "Event Description": pnl_description,
                "Internal Cost": pnl_cost,
                "Revenue": pnl_revenue
            }])

            # Append the summary row to the main table
            tl_table = pd.concat([tl_table, summary_df], ignore_index=True)

            # Replace 0 values with an empty string in "Internal Cost" and "Revenue" columns
            tl_table["Internal Cost"] = tl_table["Internal Cost"].replace(0, "")
            tl_table["Revenue"] = tl_table["Revenue"].replace(0, "")

            # Display the DataFrame as markdown
            st.markdown(tl_table.to_markdown(index=False), unsafe_allow_html=True)

            ############################################################
            # Display the selected pet details
            ############################################################

            # Display visual timeline for the selected pet
            tl_for_pet['tl_Date'] = pd.to_datetime(tl_for_pet['tl_Date'])

            fig, ax = plt.subplots(figsize=(12, 3))

            if not tl_for_pet['tl_Date'].empty:
                ax.hlines(y=0, xmin=min(tl_for_pet['tl_Date']), xmax=max(tl_for_pet['tl_Date']), color='grey',
                          linewidth=0.5)

                # Ensure each event type has a unique color
                unique_events = tl_for_pet['tl_Event'].unique()
                event_color_map = {event: plt.cm.get_cmap('tab10')(i) for i, event in enumerate(unique_events)}

                for idx, row in tl_for_pet.iterrows():
                    ax.plot(row['tl_Date'], 0, "o", color=event_color_map[row['tl_Event']])

                for idx, row in tl_for_pet.iterrows():
                    ax.text(row['tl_Date'], 0.05, row['tl_Event'], ha="left", va="bottom", fontsize=7, rotation=40)

                for spine in ax.spines.values():
                    spine.set_visible(False)

                ax.get_yaxis().set_visible(False)
                ax.set_xlabel(f"Key events for {selected_pet_name}")
                ax.tick_params(axis='x', which='both', pad=-5)

                for tick in ax.get_xticklabels():
                    tick.set_y(-0.05)

                ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))

                plt.xticks(fontsize=7, rotation=30, color='grey')

                ax.set_ylim(-0.1, 1)
                ax.set_yticks([])

                st.pyplot(fig)

        else:
            st.write("No events found for the selected pet.")

# ----------------------------------------------------
# Showing the full dataframe
# ----------------------------------------------------

# st.dataframe(pet_data)
