import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('ramona_db.db')

# Create a cursor object
cursor = conn.cursor()

# SQL query to create the table
create_table_query = '''

SELECT COUNT(*) AS total_entries
FROM VeraPetCarePlans;


'''

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

