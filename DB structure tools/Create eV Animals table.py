import sqlite3

# Path to your SQLite database
db_file_path = '../ramona_db.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Step 1: Create the SQL query to create the new table with all fields as TEXT
create_table_query = """
CREATE TABLE IF NOT EXISTS eV_animals (
    Animal_ID TEXT,
    Division TEXT,
    Animal_Name TEXT,
    Animal_Weight_kg REAL,
    Date_Of_Birth DATE,
    DOB_Is_Estimated TEXT,
    Sex TEXT,
    Has_Passed_Away TEXT,
    Date_Of_Passing TEXT,
    Cause_Of_Death TEXT,
    Caution_Status TEXT,
    Species TEXT,
    Breed TEXT,
    AnimalColour TEXT,
    Animal_Notes TEXT,
    Microchip_Number TEXT,
    Last_Vaccination_Date DATE,
    Last_Vaccination_Name TEXT,
    Next_Vaccination_Due DATE,
    Next_Vaccination_Name TEXT,
    Master_Problems TEXT,
    Last_Visit DATE,
    Next_Appointment DATE,
    Animal_Record_Created_At DATE,
    Animal_Record_Created_By TEXT,
    Animal_Record_Last_Modified_At DATE,
    Animal_Code TEXT,
    Age TEXT,
    Owner_Business_Name TEXT,
    Owner_Title TEXT,
    Owner_First_Name TEXT,
    Owner_Last_Name TEXT,
    Owner_Contact_Code TEXT,
    Is_Business TEXT,
    Physical_Address_Street_1 TEXT,
    Physical_Address_Street_2 TEXT,
    Physical_Address_Suburb_Neighborhood TEXT,
    Physical_Address_City TEXT,
    Physical_Address_Postcode TEXT,
    Physical_Address_State TEXT,
    Physical_Address_Country TEXT,
    Postal_Address_Street_1 TEXT,
    Postal_Address_Street_2 TEXT,
    Postal_Address_Suburb_Neighborhood TEXT,
    Postal_Address_City TEXT,
    Postal_Address_Postcode TEXT,
    Postal_Address_State TEXT,
    Postal_Address_Country TEXT,
    GUID TEXT,
    Opt_Out_Of_Electronic_Marketing TEXT,
    Insurance_Supplier TEXT,
    Insurance_Number TEXT,
    Referring_Clinic TEXT,
    Referring_Vet TEXT,
    Active TEXT,
    SOC_Due_Next_Month TEXT,
    Latest_BCS TEXT,
    Latest_DS TEXT,
    Latest_Temp TEXT,
    Email_Addresses TEXT,
    Home_Email_Address TEXT,
    Business_Email_Address TEXT,
    Accounts_Email_Address TEXT,
    Fax_Numbers TEXT,
    Mobile_Numbers TEXT,
    Phone_Numbers TEXT,
    General TEXT,
    Reminder TEXT
);
"""

# Step 2: Execute the query to create the table
cursor.execute(create_table_query)

# Step 3: Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'eV_animals' created successfully with all fields as TEXT.")
