import pandas as pd
import sqlite3
import openpyxl

# Load the Excel file into a pandas DataFrame
excel_file = 'Education___Clinical_Research___Innovation_Group_Limited_-_Approved__sent_and_paid.xlsx'
df = pd.read_excel(excel_file, skiprows=7)

# Connect to your SQLite database (or create one)
conn = sqlite3.connect('RA_for_GVAK.db')
cursor = conn.cursor()

# Write the DataFrame to SQLite as a table
df.to_sql('Xero', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
