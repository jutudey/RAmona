import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('ramona_db.db')

# Create a cursor object
cursor = conn.cursor()

# SQL query to create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS VeraPetCarePlans (
    _id TEXT,  -- Likely a unique identifier, string type
    Age TEXT,  -- Age should be an integer
    Breed TEXT,  -- Breed is a text field
    Email TEXT,  -- Email is text
    InitialHealthCheckComplete BOOLEAN,  -- True/False values, likely boolean
    MonthlySubscriptionPrice REAL,  -- For monetary values
    MonthlySubscriptionPriceWithoutDiscount REAL,  -- For monetary values
    OwnerFirstName TEXT,  -- Text field for the owner's first name
    OwnerLastName TEXT,  -- Text field for the owner's last name
    OwnerUserID TEXT,  -- User ID, likely a string identifier
    PetID TEXT,  -- Pet ID, string
    PetLastUpdatedTime DATETIME,
    PetName TEXT, 
    PetPlan TEXT,
    ProductCode TEXT,  -- Product code, a short string
    Species TEXT,  -- Species (e.g., Dog, Cat)
    SubID TEXT,  -- Subscription ID, string
    SubscriptionStartDate DATETIME,  -- Subscription start date as text, can convert to DATE or DATETIME later
    SubscriptionStatus INTEGER,  -- Status, possibly a numeric code
    EvPetId TEXT,  -- Pet ID, likely numeric
    EvWpmId TEXT,  -- Possibly numeric
    ActualEvWpmId TEXT,  -- Possibly numeric
    ActualEvWp TEXT  -- Descriptive code
);
'''

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Table 'VeraPetCarePlans' created successfully.")
