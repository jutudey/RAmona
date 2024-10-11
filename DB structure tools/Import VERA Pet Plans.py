import pandas as pd
import sqlite3
import os
import glob


# Define the folder to search in
folder_path = 'data'

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

    # Step 1: Load the CSV file into a pandas DataFrame with correct data types
    dtype_dict = {
        'EvPetId': 'str',  # Ensure EvPetId is treated as string
        'EvWpmId': 'str',  # Ensure EvWpmId is treated as string
        'ActualEvWpmId': 'str',  # Ensure ActualEvWpmId is treated as string
        # Add other fields if necessary
    }
    df = pd.read_csv(csv_file_path, header=0, dtype=dtype_dict)  # Explicitly specify data types

    # Step 2: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 3: Clear the table first to avoid replacing the table structure
    cursor.execute(f"DELETE FROM {table_name}")

    # Step 4: Insert the data into the table using the variable for table name
    df.to_sql(table_name, conn, if_exists='append', index=False)

    print(f"Data imported successfully into {table_name} table, excluding the header.")

    # Step 5: Execute the update query to transform EvPetId
    update_query = """
    UPDATE VeraPetCarePlans
    SET EvPetId = printf('%d', CAST(EvPetId AS INTEGER) + 100000)
    WHERE EvPetId IS NOT NULL;
    """

    # Step 6: Execute the query
    cursor.execute(update_query)

    # Step 7: Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("EvPetId values have been updated by adding 100000 and stored as text.")

else:
    print('Not imported')