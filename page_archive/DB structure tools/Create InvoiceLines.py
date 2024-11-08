import pandas as pd
import sqlite3

# Path to your SQLite database
db_file_path = '../ramona_db.db'

# Path to your CSV file
csv_file_path = '/Users/arnejohaneriksen/Python/Python Apps/GVAK_RA/data/Invoice+Lines.csv'  # Update this with the actual CSV file path

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Clean the column names by replacing spaces and removing special characters
df.columns = df.columns.str.replace('[^A-Za-z0-9]+', '', regex=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create the SQL query to create the new table without foreign key
create_table_query = """
CREATE TABLE IF NOT EXISTS InvoiceLines (
    Invoice_Num TEXT PRIMARY KEY,  -- Using Invoice# as the primary key (renamed Invoice_Num for safety)
    -- Add all other columns from the CSV with cleaned names (set as TEXT)
"""

# Add all the columns from the DataFrame as TEXT, skipping Invoice_Num since it's already defined
for col in df.columns:
    if col != 'Invoice_Num':  # Ensure you don't add 'Invoice_Num' twice
        create_table_query += f"{col} TEXT, "

# Remove the trailing comma and close the statement
create_table_query = create_table_query.rstrip(", ") + ");"

# Execute the query to create the new table
cursor.execute(create_table_query)

# Insert the data into the table
df.to_sql('InvoiceLines', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'InvoiceLines' created successfully and data inserted.")
