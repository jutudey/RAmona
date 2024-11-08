import sqlite3

# Path to your SQLite database
db_file_path = '/Users/arnejohaneriksen/Python/Python Apps/GVAK_RA/ramona_db.db'

# Define the table name to clear
table_name = 'VeraPetCarePlans'

confirmation = input('Type Y if you are sure you want to delete all entries from ' + table_name + " in " + db_file_path + ": ")

if confirmation == "Y":
    # Step 1: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 2: Execute the SQL command to delete all entries from the table
    cursor.execute(f"DELETE FROM {table_name}")

    # Optional: Reset the auto-incrementing primary key if applicable (usually used with INTEGER PRIMARY KEY)
    # cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

    # Step 3: Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"All entries from table '{table_name}' have been deleted successfully from the database.")

else:
    print("No action taken.")
