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

# Update dates before "2023-12-04" to "2023-12-04"
initial_registration.loc[initial_registration["tl_Date"] < pd.Timestamp("2023-12-04"), "tl_Date"] = pd.Timestamp("2023-12-04")

# Display the updated DataFrame
st.dataframe(initial_registration)

# Convert `tl_Date` to datetime if it isn't already
initial_registration["tl_Date"] = pd.to_datetime(initial_registration["tl_Date"])

# Extract the date part only (year, month, day) to group all entries from the same day together
initial_registration["tl_Date"] = initial_registration["tl_Date"].dt.date

# Group by `tl_Date` and count the number of rows per day
grouped_by_day = initial_registration.groupby("tl_Date").size().reset_index(name="Rows per day")

# Function to get date range based on selected option
def get_date_range(selected_option, custom_start=None, custom_end=None):
    today = datetime.date.today()

    if selected_option == "Today":
        start_date = today
        end_date = today
    elif selected_option == "This Week":
        start_date = today - datetime.timedelta(days=today.weekday())  # Start of the week (Monday)
        end_date = today
    elif selected_option == "This Week-to-date":
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = today
    elif selected_option == "This Month":
        start_date = today.replace(day=1)  # First day of this month
        end_date = today
    elif selected_option == "This Month-to-date":
        start_date = today.replace(day=1)
        end_date = today
    elif selected_option == "This Quarter":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = today
    elif selected_option == "This Quarter-to-date":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = today
    elif selected_option == "This Year":
        start_date = today.replace(month=1, day=1)  # First day of this year
        end_date = today
    elif selected_option == "This Year-to-date":
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif selected_option == "This Year-to-last-month":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=today.month - 1, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Yesterday":
        start_date = today - datetime.timedelta(days=1)
        end_date = today - datetime.timedelta(days=1)
    elif selected_option == "Recent":
        start_date = today - datetime.timedelta(days=7)
        end_date = today
    elif selected_option == "Last Week":
        start_date = today - datetime.timedelta(days=today.weekday() + 7)
        end_date = start_date + datetime.timedelta(days=6)
    elif selected_option == "Last Week-to-date":
        start_date = today - datetime.timedelta(days=today.weekday() + 7)
        end_date = today - datetime.timedelta(days=today.weekday() + 1)
    elif selected_option == "Last Month":
        first_day_of_this_month = today.replace(day=1)
        start_date = first_day_of_this_month - datetime.timedelta(days=1)  # Last day of the previous month
        start_date = start_date.replace(day=1)  # First day of the previous month
        end_date = first_day_of_this_month - datetime.timedelta(days=1)
    elif selected_option == "Last Month-to-date":
        first_day_of_this_month = today.replace(day=1)
        start_date = first_day_of_this_month - datetime.timedelta(days=1)
        start_date = start_date.replace(day=1)
        end_date = today - datetime.timedelta(days=today.day)
    elif selected_option == "Last Quarter":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
        start_date = start_date.replace(month=start_date.month - 2, day=1)
        end_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Last Quarter-to-date":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
        start_date = start_date.replace(month=start_date.month - 2, day=1)
        end_date = today
    elif selected_option == "Last Year":
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(year=today.year - 1, month=12, day=31)
    elif selected_option == "Last Year-to-date":
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(year=today.year - 1, month=today.month, day=today.day)
    elif selected_option == "Since 30 Days Ago":
        start_date = today - datetime.timedelta(days=30)
        end_date = today
    elif selected_option == "Since 60 Days Ago":
        start_date = today - datetime.timedelta(days=60)
        end_date = today
    elif selected_option == "Since 90 Days Ago":
        start_date = today - datetime.timedelta(days=90)
        end_date = today
    elif selected_option == "Since 365 Days Ago":
        start_date = today - datetime.timedelta(days=365)
        end_date = today
    elif selected_option == "Next Week":
        start_date = today + datetime.timedelta(days=(7 - today.weekday()))
        end_date = start_date + datetime.timedelta(days=6)
    elif selected_option == "Next 4 Weeks":
        start_date = today
        end_date = today + datetime.timedelta(weeks=4)
    elif selected_option == "Next Month":
        start_date = today.replace(day=1) + datetime.timedelta(days=32)
        start_date = start_date.replace(day=1)
        end_date = start_date.replace(month=start_date.month + 1, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Next Quarter":
        current_month = today.month
        next_quarter_start_month = ((current_month - 1) // 3 + 1) * 3 + 1
        if next_quarter_start_month > 12:
            next_quarter_start_month = 1
            start_date = today.replace(year=today.year + 1, month=next_quarter_start_month, day=1)
        else:
            start_date = today.replace(month=next_quarter_start_month, day=1)
        end_date = start_date + datetime.timedelta(days=90)
    elif selected_option == "Next Year":
        start_date = today.replace(year=today.year + 1, month=1, day=1)
        end_date = today.replace(year=today.year + 1, month=12, day=31)
    elif selected_option == "Custom Range":
        if custom_start and custom_end:
            start_date = custom_start
            end_date = custom_end
        else:
            raise ValueError("Custom start and end dates must be provided for 'Custom Range'")

    return start_date, end_date

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
    start_date = grouped_by_day["tl_Date"].min()
    end_date = grouped_by_day["tl_Date"].max()
    custom_start, custom_end = st.slider(
        "Select the custom date range:",
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date)
    )

    # Use the selected custom range
    start_date, end_date = get_date_range(selected_option, custom_start, custom_end)
else:
    # Get the date range based on the selected option
    start_date, end_date = get_date_range(selected_option)

# Convert start_date and end_date to pandas Timestamps
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the grouped data based on the selected date range
filtered_grouped_by_day = grouped_by_day[
    (grouped_by_day["tl_Date"] >= start_date.date()) &
    (grouped_by_day["tl_Date"] <= end_date.date())
]

# Create a bar chart showing New Registrations per day using Plotly
fig = px.bar(
    filtered_grouped_by_day,
    x='tl_Date',
    y='Rows per day',
    title='New Registrations per Day',
    labels={'tl_Date': 'Date', 'Rows per day': 'Number of Registrations'},
    hover_data=['tl_Date', 'Rows per day']
)

# Display the Plotly chart with interactivity using PlotlyState
selected_points = plotly_events(fig, click_event=True, select_event=False)

# If a bar is clicked, show the selected date and detailed registrations
if selected_points:
    selected_day = filtered_grouped_by_day.iloc[selected_points[0]["pointIndex"]]["tl_Date"]
    st.header(f"Selected Date: {selected_day}")
    filtered_data = initial_registration[initial_registration["tl_Date"] == selected_day]
    st.write(f"Registrations for {selected_day}:")
    st.dataframe(filtered_data[["tl_CustomerName", "tl_PetName"]])
