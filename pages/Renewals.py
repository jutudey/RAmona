import streamlit as st
import pandas as pd
import functions
import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

from PIL import Image

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
initial_registration["tl_Date_day"] = initial_registration["tl_Date"].dt.date

# Group by `tl_Date_day` and count the number of rows per day
grouped_by_day = initial_registration.groupby("tl_Date_day").size().reset_index(name="Rows per day")

# Display the grouped data
st.dataframe(grouped_by_day)

# Add a date slider to filter the data
start_date = grouped_by_day["tl_Date_day"].min()
end_date = grouped_by_day["tl_Date_day"].max()
selected_dates = st.slider(
    "Select date range:",
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date)
)

# Filter the grouped data based on the selected date range
filtered_grouped_by_day = grouped_by_day[(grouped_by_day["tl_Date_day"] >= selected_dates[0]) & (grouped_by_day["tl_Date_day"] <= selected_dates[1])]

# Create a bar chart showing New Registrations per day
chart = alt.Chart(filtered_grouped_by_day).mark_bar().encode(
    x='tl_Date_day:T',
    y='Rows per day:Q',
    tooltip=['tl_Date_day', 'Rows per day']
).properties(
    title='New Registrations per Day'
)

st.altair_chart(chart, use_container_width=True)
