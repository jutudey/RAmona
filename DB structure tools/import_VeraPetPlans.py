import pandas as pd
import sqlite3
import os
import glob


# Define the folder to search in
folder_path = 'Data'

# Pattern to match files starting with 'pet-summary-' and ending with '.csv'
file_pattern = os.path.join(folder_path, 'pet-summary-*.csv')

# Find all matching files
matching_files = glob.glob(file_pattern)

# Check if there are any matching files
if matching_files:
    # Sort files by their modification time (most recent first)
    most_recent_file = max(matching_files, key=os.path.getmtime)

    # Output the most recent file path
    print(f"The most recently added CSV file is: {most_recent_file}")
else:
    print("No files matching the pattern 'pet-summary-*.csv' were found.")


# Path to your CSV file and SQLite database
csv_file_path = most_recent_file
db_file_path = 'ramona_db.db'

# Define the table name as a variable
table_name = 'VeraPetCarePlans'

confirmation = input('Type Y if you want to import ' + most_recent_file + " into " + table_name + " in " + db_file_path + " ?  ")

if confirmation == "Y":
    # Step 1: Load the CSV file into a pandas DataFrame, excluding the header (first row)
    df = pd.read_csv(csv_file_path, header=0)  # The `header=0` argument ensures the first line is treated as column names

    # Step 2: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 3: Insert the data into the table using the variable for table name
    df.to_sql(table_name, conn, if_exists='append', index=False)

    # Step 4: Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Data imported successfully into {table_name} table, excluding the header.")

else:
    print('not imported')