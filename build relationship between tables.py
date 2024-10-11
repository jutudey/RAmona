import sqlite3

# Define the database path
database_name = 'RA_for_GVAK.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_name)
cursor = conn.cursor()

# Enable foreign key support (important in SQLite)
cursor.execute('PRAGMA foreign_keys = ON')

# Create the 'VeraPetCarePlans' table with a primary key (NormalisedEvPetID)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS VeraPetCarePlans (
        NormalisedEvPetID INTEGER PRIMARY KEY,
        plan_name TEXT,
        plan_description TEXT
    )
''')

# Create the 'eV_agenda' table with a foreign key referencing 'VeraPetCarePlans'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS eV_agenda (
        agenda_id INTEGER PRIMARY KEY,
        Animal_Code TEXT,
        agenda_details TEXT,
        NormalisedEvPetID TEXT,
        FOREIGN KEY (NormalisedEvPetID) REFERENCES VeraPetCarePlans(NormalisedEvPetID)
    )
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Tables created and foreign key relationship established successfully.")
