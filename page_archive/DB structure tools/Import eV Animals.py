import pandas as pd
import sqlite3
import os
import glob


# Define the folder to search in
folder_path = 'data'

# # Pattern to match files starting with 'Animals-' and ending with '.csv'
# file_pattern = os.path.join(folder_path, 'Animals-*.csv')
#
# # Find all matching files
# matching_files = glob.glob(file_pattern)
#
# # Check if there are any matching files
# if matching_files:
#     # Sort files by their modification time (most recent first)
#     most_recent_file = max(matching_files, key=os.path.getmtime)
#
#     # Output the most recent file path
#     print(f"The most recently added CSV file is: {most_recent_file}")
# else:
#     print("No files matching the pattern 'Animals-*.csv' were found.")
#

# Path to your CSV file and SQLite database
csv_file_path = '../data/Animals-2024-10-10-12-53-27.csv'
db_file_path = '../ramona_db.db'
most_recent_file = csv_file_path

# Define the table name as a variable
table_name = 'eV_animals'

# confirmation = input('Type Y if you want to import ' + most_recent_file + " into " + table_name + " in " + db_file_path + " ?  ")
confirmation = "Y"

if confirmation == "Y":

    # Step 1: Load the CSV file into a pandas DataFrame with correct data types
    # dtype_dict = {
    #     'EvPetId': 'str',  # Ensure EvPetId is treated as string
    #     'EvWpmId': 'str',  # Ensure EvWpmId is treated as string
    #     'ActualEvWpmId': 'str',  # Ensure ActualEvWpmId is treated as string
    #     # Add other fields if necessary
    # }
    # df = pd.read_csv(csv_file_path, header=0, dtype=dtype_dict)  # backup of line from VERA script
    df = pd.read_csv(csv_file_path, header=0)  # Explicitly specify data types

    # Replace spaces with underscores in the column names
    df.columns = df.columns.str.replace('Physical Address Suburb/Neighborhood', 'Physical_Address_Suburb_Neighborhood')
    df.columns = df.columns.str.replace('Postal Address Suburb/Neighborhood', 'Postal_Address_Suburb_Neighborhood')
    df.columns = df.columns.str.replace('Postal Address Suburb/Neighborhood', 'General_Reminder')
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('(kg)', 'Kg')
    df.columns = df.columns.str.replace('.', '')


    print(df.columns)
    # exit()


    # Step 2: Connect to the SQLite database
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Step 3: Clear the table first to avoid replacing the table structure
    cursor.execute(f"DELETE FROM {table_name}")

    # Step 4: Insert the data into the table using the variable for table name
    df.to_sql(table_name, conn, if_exists='append', index=False)

    print(f"Data imported successfully into {table_name} table, excluding the header.")



    # Step 7: Commit the changes and close the connection
    conn.commit()
    conn.close()


else:
    print('Not imported')