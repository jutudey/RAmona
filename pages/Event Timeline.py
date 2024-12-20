import datetime
import streamlit as st
import pandas as pd
import functions
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from streamlit_timeline import timeline
import json
from PIL import Image

app_name = functions.set_page_definitition()

st.title("⏳   Event Timeline for Pet")
#
# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

functions.initialize_session_state()


invoice_lines = st.session_state.all_invoice_lines
adyenlinks = st.session_state.adyenlinks
print("1 TL Session state invoice id: " + st.session_state.selected_invoice_no)
print("1 TL Session state customer id: " + st.session_state.selected_customer_id)
print("1 TL Session state pet id: ")
print(st.session_state.selected_pet_id)

# st.header('selected_pet_id : ' + str(st.session_state.selected_pet_id))
# st.header('selected_customer_id : ' + str(st.session_state.selected_customer_id))

# ----------------------------------------------------
# Search for client details
# ----------------------------------------------------

st.sidebar.subheader("Search")

# Create a text input to search by EvCustomerID
customer_id = st.sidebar.text_input('🆔 Enter Customer ID:', '')

# Add a search box for First Name
first_name = st.sidebar.text_input('👤 Enter First Name:', '')

# Add a search box for Last Name
last_name = st.sidebar.text_input('👤 Enter Last Name:', '')

# Add a search box for Pet Name
pet_name = st.sidebar.text_input('🐶 Enter Pet Name:', '')

customer_data = pd.DataFrame()  # Initialize contact_data to avoid NameError

# Button to clear all input boxes and session states
if st.sidebar.button('Clear All'):
    customer_id = ''
    first_name = ''
    last_name = ''
    pet_name = ''
    st.session_state.selected_invoice_no = ''
    st.session_state.selected_customer_id = ''
    st.session_state.selected_pet_id = ''
    st.rerun()

# search by customer id:
if customer_id:
    st.session_state.selected_customer_id = customer_id

    # st.warning(st.session_state.selected_customer_id)

# Search by names
if first_name or last_name or pet_name:
    contacts_data = functions.get_contacts_by_name_v2(first_name=first_name,
                                                      last_name=last_name,
                                                      pet_name=pet_name)
    # print(contacts_data)

    if not contacts_data.empty:
        if pet_name:
            selected_contact = st.selectbox('Select a Contact:',
                                            contacts_data["EvCustomerID"].astype(str) + ' - ' + contacts_data[
                                                "OwnerFirstName"] + ' ' + contacts_data["OwnerLastName"] + ' - ' + contacts_data["PetName"])
            st.session_state.selected_customer_id = selected_contact.split(' - ')[0]
        else:
            selected_contact = st.selectbox('Select a Contact:',
                                            contacts_data["EvCustomerID"].astype(str) + ' - ' + contacts_data[
                                                "OwnerFirstName"] + ' ' + contacts_data["OwnerLastName"])
            st.session_state.selected_customer_id = selected_contact.split(' - ')[0]
    else:
        st.warning("No contacts found with the given name(s).")

# if pet_name:
#     contacts_data = functions.get_contacts_by_name_v2(pet_name=pet_name)
#     if not contacts_data.empty:
#         selected_contact = st.selectbox('Select a Pet:',
#                                     contacts_data["EvCustomerID"].astype(str) + ' - ' + contacts_data[
#                                         "OwnerFirstName"] + ' ' + contacts_data["OwnerLastName"] + ' - ' + contacts_data["PetName"])
#         st.session_state.selected_customer_id = selected_contact.split(' - ')[0]
#     else:
#         st.warning("No pets found with the given name.")

print("2 TL Session state invoice id: " + st.session_state.selected_invoice_no)
print("2 TL Session state customer id: " + st.session_state.selected_customer_id)
print("2 TL Session state pet id: ")
print(st.session_state.selected_pet_id)

# Display contact details if EvCustomerID is provided
if st.session_state.selected_customer_id:
    customer_data = functions.get_contact_details_v2(st.session_state.selected_customer_id)
    if not customer_data.empty:

        st.write("### Customer Details:")
        st.write(f"Customer ID: {customer_data.iloc[0]['EvCustomerID']}")
        st.write(f"First Name: {customer_data.iloc[0]['OwnerFirstName']}")
        st.write(f"Last Name: {customer_data.iloc[0]['OwnerLastName']}")
        pass
    else:
        st.info("No details found for this Customer ID")

if not customer_data.empty:
    st.header(f"👤   {customer_data.iloc[0]['OwnerFirstName'].title()} "
              f"{customer_data.iloc[0]['OwnerLastName'].title()} ({customer_data.iloc[0]['EvCustomerID'].title()})")

# ----------------------------------------------------
# select Pet
# ----------------------------------------------------

pet_data = functions.load_ezyvet_customers(st.session_state.selected_customer_id)
# print("pet_data:")
# print(pet_data)
if not pet_data.empty:
    st.write("### Pet Details:")
    pet_data_display = pet_data[['Animal Code', 'Animal Name','Animal Record Created At', 'Has Passed Away', "Active", "Last Visit"]]
    # st.markdown(pet_data_display.to_markdown(index=False), unsafe_allow_html=True)

    # If there are multiple pets, allow the user to select one
    if len(pet_data) > 1:
        try:
            selected_pet_id, selected_pet_name = functions.multi_selectbox(pet_data_display, 'Animal Code', "Animal Name")
            st.session_state.selected_pet_id = str(selected_pet_id)
            st.session_state.selected_pet_name = str(selected_pet_name)
        except IndexError:
            pass
    else:
        selected_pet_name = pet_data_display['Animal Name'].iloc[0]
        st.session_state.selected_pet_id = pet_data.loc[pet_data['Animal Name'] == selected_pet_name, 'Animal Code'].astype(str).values[0]    # st.header(st.session_state.selected_pet_id)

    ############################################################
    # Display the selected pet details
    ############################################################

    if str(st.session_state.selected_pet_id) in str(pet_data['Animal Code']):
        try:
            selected_pet_name = pet_data.loc[pet_data['Animal Code'] == st.session_state.selected_pet_id, 'Animal Name'].values[0]
            selected_pet_species = pet_data.loc[pet_data['Animal Code'] == st.session_state.selected_pet_id, 'Species'].values[0]

            if selected_pet_species == "Canine":
                st.write(f"### 🐕  {selected_pet_name}  ({st.session_state.selected_pet_id}) - Key Events")
            elif selected_pet_species == "Feline":
                st.write(f"### 🐈  {selected_pet_name} - Key Events")
            else:
                st.write(f"### 🐁  {selected_pet_name} - Key Events")

        except IndexError:
            pass

        # Prepare data for Client Timeline
        tl = st.session_state.tl
        # st.dataframe(tl)
        # st.write(st.session_state.selected_pet_id)

        tl_for_pet = tl[tl["tl_PetID"] == st.session_state.selected_pet_id]
        # Replace any NaN with an empty string in tl_Comment
        tl_for_pet['tl_Comment'] = tl_for_pet['tl_Comment'].fillna('')
        # st.dataframe(tl_for_pet)

        # Show events for the selected pet in a table
        if not tl_for_pet.empty:
            tl_table = tl_for_pet[["tl_Date", "tl_Event", "tl_Cost", "tl_Revenue", "tl_Comment"]].rename(
                columns={
                    "tl_Date": "Event Date",
                    "tl_Event": "Event Description",
                    "tl_Cost": "Internal Cost",
                    "tl_Revenue": "Revenue",
                    "tl_Comment": "Remark"
                }
            )

            # Format the date to dd.mm.yyyy
            tl_table["Event Date"] = tl_table["Event Date"].dt.strftime('%d.%m.%Y')

            # Calculate sum of Revenue and Cost
            total_revenue = tl_table["Revenue"].sum()
            # st.write(total_revenue)
            total_cost = tl_table["Internal Cost"].sum()
            # st.write(total_cost)
            total_pnl = round(total_revenue - total_cost, 2)

            # Determine P&L line values
            pnl_description = "**P&L for this pet**"
            pnl_revenue = total_pnl if total_revenue > total_cost else 0
            pnl_cost = total_pnl if total_cost > total_revenue else 0

            # Create a DataFrame for the summary line
            summary_df = pd.DataFrame([{
                "Event Date": "",
                "Event Description": pnl_description,
                "Internal Cost": pnl_cost,
                "Revenue": pnl_revenue,
                'Remark': ""
            }])

            # Append the summary row to the main table
            tl_table = pd.concat([tl_table, summary_df], ignore_index=True)

            # Replace 0 values with an empty string in "Internal Cost" and "Revenue" columns
            tl_table["Internal Cost"] = tl_table["Internal Cost"].replace(0, "")
            tl_table["Revenue"] = tl_table["Revenue"].replace(0, "")

            # Display the DataFrame as markdown
            st.markdown(tl_table.to_markdown(index=False), unsafe_allow_html=True)

            ############################################################
            # Display timeline with plotly
            ############################################################

            # Display visual timeline for the selected pet
            tl_for_pet['tl_Date'] = pd.to_datetime(tl_for_pet['tl_Date'])

            fig, ax = plt.subplots(figsize=(12, 3))

            if not tl_for_pet['tl_Date'].empty:
                # ax.hlines(y=0, xmin=min(tl_for_pet['tl_Date']), xmax=max(tl_for_pet['tl_Date']), color='grey',
                #           linewidth=0.5)
                #
                # # Ensure each event type has a unique color
                # unique_events = tl_for_pet['tl_Event'].unique()
                # event_color_map = {event: plt.cm.get_cmap('tab10')(i) for i, event in enumerate(unique_events)}
                #
                # for idx, row in tl_for_pet.iterrows():
                #     ax.plot(row['tl_Date'], 0, "o", color=event_color_map[row['tl_Event']])
                #
                # for idx, row in tl_for_pet.iterrows():
                #     ax.text(row['tl_Date'], 0.05, row['tl_Event'], ha="left", va="bottom", fontsize=7, rotation=40)
                #
                # for spine in ax.spines.values():
                #     spine.set_visible(False)
                #
                # ax.get_yaxis().set_visible(False)
                # ax.set_xlabel(f"Key events for {selected_pet_name}")
                # ax.tick_params(axis='x', which='both', pad=-5)
                #
                # for tick in ax.get_xticklabels():
                #     tick.set_y(-0.05)
                #
                # ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))
                #
                # plt.xticks(fontsize=7, rotation=30, color='grey')
                #
                # ax.set_ylim(-0.1, 1)
                # ax.set_yticks([])

                # st.pyplot(fig)

                ############################################################
                # Display timeline with Timeline component
                ############################################################

                # Ensure the 'tl_Date' column is in datetime format
                tl_for_pet['tl_Date'] = pd.to_datetime(tl_for_pet['tl_Date'])

                # Create new columns for year, month, day, hour, minute, and second
                tl_for_pet['Year'] = tl_for_pet['tl_Date'].dt.year
                tl_for_pet['Month'] = tl_for_pet['tl_Date'].dt.month
                tl_for_pet['Day'] = tl_for_pet['tl_Date'].dt.day
                tl_for_pet['Hour'] = tl_for_pet['tl_Date'].dt.hour
                tl_for_pet['Minute'] = tl_for_pet['tl_Date'].dt.minute
                tl_for_pet['Second'] = tl_for_pet['tl_Date'].dt.second

                data = {
                    "title": {
                        "text": {
                            "headline": f"Key Events for {selected_pet_name}",
                            "text": "Timeline </p>"
                        }
                    },
                    "events": [
                        {
                            "start_date": {
                                "year": row['Year'],
                                "month": row['Month'],
                                "day": row['Day'],
                                "hour": row['Hour'],
                                "minute": row['Minute'],
                                "second": row['Second'],
                                "display_date": row['tl_Date'].strftime('%d-%m-%Y'),
                            "group": row['tl_Group']
                            },
                            "text": {
                                "headline": row['tl_Event'],
                                "text": row['tl_Comment']
                            }
                        } for idx, row in tl_for_pet.iterrows()
                    ]
                }




                # ----------------------------------------------------
                # Manually add event
                # ----------------------------------------------------

                # Initialize or load the DataFrame
                if 'events_df' not in st.session_state:
                    st.session_state['events_df'] = pd.DataFrame(
                        columns=["tl_Date",
                                 'tl_CustomerID',
                                 'tl_CustomerName',
                                 'tl_PetID',
                                 'tl_PetName',
                                 "tl_Cost",
                                 "tl_Revenue",
                                 "tl_Event",
                                 "tl_Comment"])

                # st.dataframe(tl_for_pet)



                ############################################################
                # Manually add event
                ############################################################

                # Define the dialog function
                @st.dialog("Enter Event Details")
                def enter_event_manually():
                    with st.form("enter_event_manually"):
                        event_date = st.date_input('Enter Event Date:')
                        event_cost = st.number_input("Enter Cost:", min_value=0.0, step=1.0, key='event_cost')
                        event_revenue = st.number_input("Enter Revenue:", min_value=0.0, step=1.0, key='event_revenue')
                        event_type = st.text_input("Which kind of event?")
                        event_comment = st.text_input("Add a comment or additional info")
                        event_creator = st.text_input("Enter your name")
                        submitted = st.form_submit_button("Submit")


                        if submitted:
                            date_stamp = datetime.datetime.now().strftime("%Y%m%d")
                            new_event = pd.DataFrame([{
                                "tl_Date": event_date,
                                "tl_CustomerID": st.session_state.selected_customer_id,
                                "tl_CustomerName": st.session_state.selected_customer_id,
                                "tl_PetID": st.session_state.selected_pet_id,
                                "tl_PetName": selected_pet_name,
                                "tl_Cost": event_cost,
                                "tl_Revenue": event_revenue,
                                "tl_Event": event_type,
                                "tl_Comment": event_comment + " - " + " [" + event_creator + " - " + date_stamp + "]",

                            }])

                            # Use pd.concat to add the new row to the DataFrame
                            st.session_state['events_df'] = pd.concat([st.session_state['events_df'], new_event], ignore_index=True)

                            # Save the updated DataFrame to CSV
                            csv_path = "reference_data/manually_entered_events.csv"
                            st.session_state['events_df'].to_csv(csv_path, index=False)

                            # Reload the data
                            tl_manually_entered = functions.get_manually_entered_tl_events()
                            st.session_state.tl = pd.concat([st.session_state.tl, tl_manually_entered], ignore_index=True)

                            st.rerun()  # Close the dialog after submission


                # # Button to open the modal dialog
                # if st.button("Create Event Manually"):
                #     enter_event_manually()



                # Display the updated DataFrame
                # st.write(st.session_state['events_df'])

                timeline(data, height=400)

# ----------------------------------------------------
# Showing the full dataframe
# ----------------------------------------------------

# st.dataframe(pet_data)


            else:
                st.write("No events found for the selected pet.")