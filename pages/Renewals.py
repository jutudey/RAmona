import streamlit as st
import pandas as pd
import functions
import plotly.express as px
from streamlit_plotly_events import plotly_events
import datetime

app_name = functions.set_page_definitition()
st.title("Subscription Renewals")


# ----------------------------------------------------
# Collect data
# ----------------------------------------------------

initial_registration = functions.extract_tl_pet_data_registration()
tl = st.session_state.tl

# Update dates before "2023-12-04" to "2023-12-04"
initial_registration.loc[initial_registration["tl_Date"] < pd.Timestamp("2023-12-04"), "tl_Date"] = pd.Timestamp(
    "2023-12-04")

# Display the updated DataFrame
# st.dataframe(initial_registration)

# Convert `tl_Date` to datetime if it isn't already
initial_registration["tl_Date"] = pd.to_datetime(initial_registration["tl_Date"])

# Extract the date part only (year, month, day) to group all entries from the same day together
initial_registration["tl_Date"] = initial_registration["tl_Date"].dt.date

# Group by `tl_Date` and count the number of rows per day
# Add tl_PetID to the grouped data
grouped_by_day = initial_registration.groupby("tl_Date").agg({"tl_PetID": "count"}).reset_index()
# grouped_by_day.rename(columns={"tl_PetId": "Rows per day"}, inplace=True)

# ----------------------------------------------------
# Select Date Range
# ----------------------------------------------------

# Sidebar for selecting date filters
st.sidebar.subheader("Select a date filter")

date_options = [
    "Custom Range", "Today", "This Week", "This Week-to-date", "This Month", "This Month-to-date",
    "This Quarter", "This Quarter-to-date", "This Year", "This Year-to-date", "This Year-to-last-month",
    "Yesterday", "Recent", "Last Week", "Last Week-to-date", "Last Month", "Last Month-to-date",
    "Last Quarter", "Last Quarter-to-date", "Last Year", "Last Year-to-date",
    "Since 30 Days Ago", "Since 60 Days Ago", "Since 90 Days Ago", "Since 365 Days Ago",
    "Next Week", "Next 4 Weeks", "Next Month", "Next Quarter", "Next Year"
]
selected_option = st.sidebar.selectbox("Pick a date range", date_options)

# Set the custom date range if 'Custom Range' is selected
custom_start = custom_end = None
if selected_option == "Custom Range":
    # Add a date slider to filter the data if 'Custom Range' is selected
    if 'custom_start' not in st.session_state or 'custom_end' not in st.session_state:
        st.session_state.custom_start = grouped_by_day["tl_Date"].min()
        st.session_state.custom_end = grouped_by_day["tl_Date"].max()

    custom_start, custom_end = st.slider(
        "Select the custom date range:",
        min_value=grouped_by_day["tl_Date"].min(),
        max_value=grouped_by_day["tl_Date"].max(),
        value=(st.session_state.custom_start, st.session_state.custom_end)
    )

    # Store the selected custom range in session state
    st.session_state.custom_start = custom_start
    st.session_state.custom_end = custom_end

    # Use the selected custom range
    start_date, end_date = functions.get_date_range(selected_option, custom_start, custom_end)
    start_date, end_date = functions.get_date_range(selected_option, custom_start, custom_end)
else:
    # Get the date range based on the selected option
    start_date, end_date = functions.get_date_range(selected_option)

# Convert start_date and end_date to pandas Timestamps
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the grouped data based on the selected date range
filtered_grouped_by_day = grouped_by_day[
    (grouped_by_day["tl_Date"] >= start_date.date()) &
    (grouped_by_day["tl_Date"] <= end_date.date())
    ]

# ----------------------------------------------------
# Create graph
# ----------------------------------------------------

fig = px.bar(
    filtered_grouped_by_day,
    x='tl_Date',
    y='tl_PetID',
    title='New Registrations per Day',
    labels={'tl_Date': 'Date', 'tl_PetID': 'Number of Registrations'},
    hover_data=['tl_Date', 'tl_PetID']
)

# Display the Plotly chart with interactivity using PlotlyState
selected_points = plotly_events(fig, click_event=True, select_event=False)

# ----------------------------------------------------
# Show pet details for the selected day
# ----------------------------------------------------

# # If a bar is clicked, show the selected date and detailed registrations
# if selected_points:
#     selected_day = filtered_grouped_by_day.iloc[selected_points[0]["pointIndex"]]["tl_Date"]
#     st.header(f"Selected Date: {selected_day}")
#     filtered_data = initial_registration[initial_registration["tl_Date"] == selected_day]
#     st.write(f"Registrations for {selected_day}:")
#     # Create a table with customer name, pet name, and pet id
#     st.dataframe(filtered_data[["tl_CustomerName", "tl_PetName", "tl_PetID"]])


# If a bar is clicked, show the selected date and detailed registrations
if selected_points:
    selected_day = filtered_grouped_by_day.iloc[selected_points[0]["pointIndex"]]["tl_Date"]
    st.header(f"Selected Date: {selected_day}")
    filtered_data = initial_registration[initial_registration["tl_Date"] == selected_day]
    st.write(f"Registrations for {selected_day}:")

    # Create a clickable link for each Pet ID
    def create_pet_id_link(pet_id):
        return f'<a href="/Event_Timeline?selected_pet_id={pet_id}" target="_self">{pet_id}</a>'

    # Add clickable links to the DataFrame
    filtered_data["tl_PetID_Link"] = filtered_data["tl_PetID"].apply(create_pet_id_link)

    # Display the DataFrame with clickable Pet IDs
    st.write(filtered_data.to_html(columns=["tl_CustomerName", "tl_PetName", "tl_PetID_Link"], escape=False), unsafe_allow_html=True)