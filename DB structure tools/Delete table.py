import sqlite3

# Path to your SQLite database
db_file_path = '../ramona_db.db'

# Define the table name to delete
table_name = 'eV_animals'

confirmation = input('Type Y if you are  sure you want to delete ' + table_name + " from " + db_file_path)

if confirmation == "Y":

    # Step 1: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 2: Execute the SQL command to delete the table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Step 3: Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Table '{table_name}' has been deleted successfully from the database.")

else:
    print("Not deleted")