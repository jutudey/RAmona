import pandas as pd
import sqlite3

# Path to your SQLite database
db_file_path = '../ramona_db.db'

# Path to your CSV file
csv_file_path = '/Users/arnejohaneriksen/Python/Python Apps/GVAK_RA/data/Invoice+Lines.csv'  # Update with actual file path

# Load the CSV file, ignoring the first row (headers) and without using any header names
df = pd.read_csv(csv_file_path, header=None, skiprows=1)

# Define the column names (if they are not provided or ignored in the file)
# Assuming you know the structure/order of the columns in the file, you can assign column names like below:
df.columns = ['InvoiceNumber', 'InvoiceDate', 'Type', 'ParentLineID', 'InvoiceLineDateCreated', 'InvoiceLineTimeCreated',
              'CreatedBy', 'InvoiceLineDateLastModified', 'InvoiceLineTimeLastModified', 'LastModifiedBy',
              'InvoiceLineDate', 'InvoiceLineTime', 'DepartmentID', 'Department', 'InventoryLocation',
              'ClientContactCode', 'BusinessName', 'FirstName', 'LastName', 'Email', 'AnimalCode', 'AnimalName',
              'Species', 'Breed', 'InvoiceLineID', 'InvoiceLineReference', 'ProductCode', 'ProductName',
              'ProductDescription', 'Account', 'ProductCost', 'ProductGroup', 'StaffMemberID', 'StaffMember',
              'SalespersonisVet', 'ConsultID', 'ConsultNumber', 'CaseOwner', 'Qty', 'StandardPriceincl',
              'DiscountPercentage', 'DiscountValue', 'UserReason', 'SurchargeAdjustment', 'SurchargeName',
              'DiscountAdjustment', 'DiscountName', 'RoundingAdjustment', 'RoundingName', 'PriceAfterDiscountexcl',
              'TaxperQtyAfterDiscount', 'PriceAfterDiscountincl', 'TotalInvoicedexcl', 'TotalTaxAmount',
              'TotalInvoicedincl', 'TotalEarnedexcl', 'TotalEarnedincl', 'PaymentTerms']

# Specify the data types to enforce the fields as TEXT
dtype_dict = {
    'InvoiceNumber': 'str',
    'ClientContactCode': 'str',
    'AnimalCode': 'str',
    'InvoiceLineID': 'str',
    'ProductCode': 'str',
    'ConsultID': 'str',
    'ConsultNumber': 'str'
}

# Apply the specified data types to the DataFrame
df = df.astype(dtype_dict)

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Step 1: Delete the existing data in the InvoiceLines table to replace it
cursor.execute("DELETE FROM InvoiceLines")

# Step 2: Insert the data from the DataFrame into the SQLite table
df.to_sql('InvoiceLines', conn, if_exists='append', index=False)

# Commit and close the connection
conn.commit()
conn.close()

print("Data imported successfully, replacing existing data in the 'InvoiceLines' table.")
