import pandas as pd
import sqlite3
import openpyxl

# Load the Excel file into a pandas DataFrame
csv_file = 'Agenda.csv'
df = pd.read_csv(csv_file)

# Connect to your SQLite database (or create one)
conn = sqlite3.connect('RA_for_GVAK.db')
cursor = conn.cursor()

# Write the DataFrame to SQLite as a table
df.to_sql('eV_agenda', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
