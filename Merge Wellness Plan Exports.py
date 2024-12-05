import os
import pandas as pd
from datetime import datetime

# Specify the directory where your CSV files are stored
directory = "data/WellnessPlanExports"

# Initialize an empty list to store individual DataFrames
dataframes = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        # Append the DataFrame to the list
        dataframes.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
merged_df = pd.concat(dataframes, ignore_index=True)

# Split out duplicates into a separate DataFrame
duplicates_df = merged_df[merged_df.duplicated(keep=False)]
merged_df = merged_df.drop_duplicates(keep=False)

# Get the current date stamp
date_stamp = datetime.now().strftime("%Y%m%d")

# Save the merged DataFrame and duplicates DataFrame to new CSV files
os.makedirs("data", exist_ok=True)
merged_df.to_csv(f"data/evWellnessPlans-{date_stamp}.csv", index=False)
duplicates_df.to_csv(f"data/evWellnessPlans_duplicates_{date_stamp}.csv", index=False)

print(f"CSV files merged successfully into 'data/evWellnessPlans-{date_stamp}.csv'")
print(f"Duplicates saved into 'data/evWellnessPlans_duplicates_{date_stamp}.csv'")