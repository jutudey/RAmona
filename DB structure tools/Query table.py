import sqlite3

# Path to your SQLite database
db_file_path = '../ramona_db.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Define the SQL query
query = """
SELECT p._id, p.PetName, a.Animal_Name, a.Breed, p.SubscriptionStartDate
FROM VeraPetCarePlans p
JOIN eV_animals a ON p.EvPetId = a.Animal_Code;
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results[:20]:
    print(row)

# Close the connection
conn.close()
