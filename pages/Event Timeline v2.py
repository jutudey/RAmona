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

st.header('selected_pet_id : ' + str(st.session_state.selected_pet_id))
st.header('selected_customer_id : ' + str(st.session_state.selected_customer_id))

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
        st.write("### Customer Details:")
        st.write(f"Customer ID: {customer_data.iloc[0]['Contact Code']}")
        st.write(f"First Name: {customer_data.iloc[0]['Contact First Name']}")
        st.write(f"Last Name: {customer_data.iloc[0]['Contact Last Name']}")
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

    if len(pet_data) > 1:
        selected_pet_name = st.radio("Select Pet:", pet_data['Name'], index=pet_data['Name'].tolist().index(pet_data.loc[pet_data['Pet ID'] == st.session_state.selected_pet_id, 'Name'].values[0]) if st.session_state.selected_pet_id else 0, horizontal=True)
        if selected_pet_name:
            st.session_state.selected_pet_id = pet_data.loc[pet_data['Name'] == selected_pet_name, 'Pet ID'].values[0]
    else:
        st.session_state.selected_pet_id = str(pet_data['Pet ID'].values[0])

    # Print and display the selected pet details
    if st.session_state.selected_pet_id in pet_data['Pet ID'].values:
        selected_pet_name = pet_data.loc[pet_data['Pet ID'] == st.session_state.selected_pet_id, 'Name'].values[0]
        st.write(f"### Key events for {selected_pet_name}")

        # ----------------------------------------------------
        # Prepare data for Client Timeline
        # ----------------------------------------------------

        tl = st.session_state.tl

        # filter by pet ID
        filt = (tl["tl_PetID"] == str(st.session_state.selected_pet_id))
        tl_for_pet = tl[filt]

        # ----------------------------------------------------
        # show events for the selected pet in a table
        # ----------------------------------------------------

        if not tl_for_pet.empty:
            # Select specific columns and rename them
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

            # ----------------------------------------------------
            # Display visual timeline for the selected pet
            # ----------------------------------------------------

            # Ensure the tl_Date column is in datetime format
            tl_for_pet['tl_Date'] = pd.to_datetime(tl_for_pet['tl_Date'])

            # Extract relevant data and convert it to a list of dictionaries
            timeline_items = [
                {"Event": row['tl_Event'], "Date": row['tl_Date']} for _, row in tl_for_pet.iterrows()
            ]

            # Define a color map for each event type
            event_types = tl_for_pet['tl_Event'].unique()
            colors = plt.cm.get_cmap('tab10', len(event_types))  # Get a colormap with enough colors for each unique event type
            event_color_map = {event: colors(i) for i, event in enumerate(event_types)}

            # Plot the events on a horizontal line with markers
            fig, ax = plt.subplots(figsize=(12, 3))

            # Draw a horizontal line
            if not tl_for_pet['tl_Date'].empty:
                ax.hlines(y=0, xmin=min(tl_for_pet['tl_Date']), xmax=max(tl_for_pet['tl_Date']), color='grey', linewidth=0.5)

                # Add markers for each event with different colors
                for idx, row in tl_for_pet.iterrows():
                    ax.plot(row['tl_Date'], 0, "o", color=event_color_map[row['tl_Event']])

                # Annotate each event with event names
                for idx, row in tl_for_pet.iterrows():
                    ax.text(row['tl_Date'], 0.05, row['tl_Event'], ha="left", va="bottom", fontsize=7,
                            rotation=40)

                # Remove the frame (spines)
                for spine in ax.spines.values():
                    spine.set_visible(False)

                # Remove y-axis and adjust x-axis
                ax.get_yaxis().set_visible(False)
                ax.set_xlabel("Event Date")
                ax.tick_params(axis='x', which='both', pad=-5)  # Move tick labels closer by setting a negative pad value

                # Set x-tick label positions to bring them even closer to the line
                for tick in ax.get_xticklabels():
                    tick.set_y(-0.05)

                # Format x-axis labels as "Month Year" (e.g., "March 2024")
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%B %Y'))

                plt.xticks(fontsize=7, rotation=30, color='grey')

                # Set limits and labels
                ax.set_ylim(-0.1, 1)
                ax.set_yticks([])

                # Display the figure in Streamlit
                st.pyplot(fig)

        else:
            st.write("No events found for the selected pet.")

# ----------------------------------------------------
# Showing the full dataframe
# ----------------------------------------------------

# st.dataframe(tl_invoices)
