import os

# Path to the database file
db_file_path = '/Users/arnejohaneriksen/Python/Python Apps/GVAK_RA/ramona_db.db'


confirmation = input('Type Y if you are  sure you want to delete ' + db_file_path + " ? ")

if confirmation == "Y":
    # Check if the file exists before attempting to delete it
    if os.path.exists(db_file_path):
        # Delete the file
        os.remove(db_file_path)
        print(f"{db_file_path} has been deleted successfully.")
    else:
        print(f"{db_file_path} does not exist.")

else:
    print('not deleted')
