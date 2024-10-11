import sqlite3

# Define variables for database name, table name, and the unique key field
database_name = 'RA_for_GVAK.db'  # Change this to your database file name
table_name = 'eV_agenda'           # Change this to your table name
unique_key_field = 'Animal Code'          # Change this to the field name you want to set as UNIQUE

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Create a table with a unique constraint on the specified field
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        name TEXT,
        {unique_key_field} TEXT UNIQUE
    )
'''
cursor.execute(create_table_query)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
