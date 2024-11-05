import numpy as np
import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import re
import os
import datetime

def set_page_definitition():
    app_name = "RAmona v0.1"

    # Loading Image using PIL
    icon = Image.open('content/Subsidiary Salmon Logo.png')

    # Enable wide mode and set light theme and add tab icon
    st.set_page_config(layout="wide", page_title=app_name, page_icon=icon, initial_sidebar_state="expanded")
    # st.set_page_config(layout="wide", page_title=app_name, page_icon=":material/sound_detection_dog_barking:", initial_sidebar_state="expanded")

    return app_name

def get_date_range(selected_option, custom_start=None, custom_end=None):
    today = datetime.date.today()

    if selected_option == "Today":
        start_date = today
        end_date = today
    elif selected_option == "This Week":
        start_date = today - datetime.timedelta(days=today.weekday())  # Start of the week (Monday)
        end_date = today
    elif selected_option == "This Week-to-date":
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = today
    elif selected_option == "This Month":
        start_date = today.replace(day=1)  # First day of this month
        end_date = today
    elif selected_option == "This Month-to-date":
        start_date = today.replace(day=1)
        end_date = today
    elif selected_option == "This Quarter":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = today
    elif selected_option == "This Quarter-to-date":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = today
    elif selected_option == "This Year":
        start_date = today.replace(month=1, day=1)  # First day of this year
        end_date = today
    elif selected_option == "This Year-to-date":
        start_date = today.replace(month=1, day=1)
        end_date = today
    elif selected_option == "This Year-to-last-month":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=today.month - 1, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Yesterday":
        start_date = today - datetime.timedelta(days=1)
        end_date = today - datetime.timedelta(days=1)
    elif selected_option == "Recent":
        start_date = today - datetime.timedelta(days=7)
        end_date = today
    elif selected_option == "Last Week":
        start_date = today - datetime.timedelta(days=today.weekday() + 7)
        end_date = start_date + datetime.timedelta(days=6)
    elif selected_option == "Last Week-to-date":
        start_date = today - datetime.timedelta(days=today.weekday() + 7)
        end_date = today - datetime.timedelta(days=today.weekday() + 1)
    elif selected_option == "Last Month":
        first_day_of_this_month = today.replace(day=1)
        start_date = first_day_of_this_month - datetime.timedelta(days=1)  # Last day of the previous month
        start_date = start_date.replace(day=1)  # First day of the previous month
        end_date = first_day_of_this_month - datetime.timedelta(days=1)
    elif selected_option == "Last Month-to-date":
        first_day_of_this_month = today.replace(day=1)
        start_date = first_day_of_this_month - datetime.timedelta(days=1)
        start_date = start_date.replace(day=1)
        end_date = today - datetime.timedelta(days=today.day)
    elif selected_option == "Last Quarter":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
        start_date = start_date.replace(month=start_date.month - 2, day=1)
        end_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Last Quarter-to-date":
        current_month = today.month
        quarter_start_month = current_month - (current_month - 1) % 3
        start_date = today.replace(month=quarter_start_month, day=1) - datetime.timedelta(days=1)
        start_date = start_date.replace(month=start_date.month - 2, day=1)
        end_date = today
    elif selected_option == "Last Year":
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(year=today.year - 1, month=12, day=31)
    elif selected_option == "Last Year-to-date":
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(year=today.year - 1, month=today.month, day=today.day)
    elif selected_option == "Since 30 Days Ago":
        start_date = today - datetime.timedelta(days=30)
        end_date = today
    elif selected_option == "Since 60 Days Ago":
        start_date = today - datetime.timedelta(days=60)
        end_date = today
    elif selected_option == "Since 90 Days Ago":
        start_date = today - datetime.timedelta(days=90)
        end_date = today
    elif selected_option == "Since 365 Days Ago":
        start_date = today - datetime.timedelta(days=365)
        end_date = today
    elif selected_option == "Next Week":
        start_date = today + datetime.timedelta(days=(7 - today.weekday()))
        end_date = start_date + datetime.timedelta(days=6)
    elif selected_option == "Next 4 Weeks":
        start_date = today
        end_date = today + datetime.timedelta(weeks=4)
    elif selected_option == "Next Month":
        start_date = today.replace(day=1) + datetime.timedelta(days=32)
        start_date = start_date.replace(day=1)
        end_date = start_date.replace(month=start_date.month + 1, day=1) - datetime.timedelta(days=1)
    elif selected_option == "Next Quarter":
        current_month = today.month
        next_quarter_start_month = ((current_month - 1) // 3 + 1) * 3 + 1
        if next_quarter_start_month > 12:
            next_quarter_start_month = 1
            start_date = today.replace(year=today.year + 1, month=next_quarter_start_month, day=1)
        else:
            start_date = today.replace(month=next_quarter_start_month, day=1)
        end_date = start_date + datetime.timedelta(days=90)
    elif selected_option == "Next Year":
        start_date = today.replace(year=today.year + 1, month=1, day=1)
        end_date = today.replace(year=today.year + 1, month=12, day=31)
    elif selected_option == "Custom Range":
        if custom_start and custom_end:
            start_date = custom_start
            end_date = custom_end
        else:
            raise ValueError("Custom start and end dates must be provided for 'Custom Range'")



    return start_date, end_date

#----------------------------------------------------
# Old SQL functions
#----------------------------------------------------

def get_contacts_by_name(first_name, last_name):
    conn = sqlite3.connect('ramona_db.db')
    conditions = []
    if first_name:
        conditions.append(f'"Contact First Name" LIKE "%{first_name}%"')
    if last_name:
        conditions.append(f'"Contact Last Name" LIKE "%{last_name}%"')
    where_clause = ' AND '.join(conditions)
    query = f'''
        SELECT 
        "Contact Code", 
        "Contact First Name", 
        "Contact Last Name"
        FROM eV_Contacts
        WHERE {where_clause}
        '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_contacts_by_name_v2(first_name=None, last_name=None):
    # Load the DataFrame from session state
    df = st.session_state.get('ss_petcare_plans')

    # If df is not in session state, generate it
    if df is None:
        df = load_petcare_plans()

    # Apply filter for first name if provided
    if first_name:
        df = df[df['OwnerFirstName'].str.contains(first_name, case=False, na=False)]

    # Apply filter for last name if provided
    if last_name:
        df = df[df['OwnerLastName'].str.contains(last_name, case=False, na=False)]

    # Select relevant columns and remove duplicates based on EvCustomerID
    filtered_df = df[['EvCustomerID', 'OwnerFirstName', 'OwnerLastName']].drop_duplicates(subset='EvCustomerID')

    return filtered_df



def get_contact_details(contact_code):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
        SELECT 
        "Contact Code",
        "Contact First Name", 
        "Contact Last Name"
        FROM eV_Contacts
        WHERE "Contact Code" = {contact_code}
        '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_contact_details_v2(customer_id):
    # Load the DataFrame from session state
    df = st.session_state.get('ss_petcare_plans')

    # if df is not in sessions state, generate it
    if df is None:
        df = load_petcare_plans()

    # Start with the main dataframe and apply filters based on provided names
    filtered_df = df

    # Apply filter for first name if provided

    filtered_df = filtered_df[filtered_df['EvCustomerID'] == customer_id]

    # Select relevant columns
    return filtered_df[['EvCustomerID', 'OwnerFirstName', 'OwnerLastName']]

def get_pet_details(contact_code):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
      SELECT 
        "Animal Code" as "Pet ID", 
        "Animal Name" as "Name", 
        "Species", 
        "Breed", 
        "Animal Record Created At" as "First registered at"
        FROM eV_animals
        WHERE "Owner Contact Code" = '{contact_code}'
      '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_contact_details_v2(customer_id):
    # Load the DataFrame from session state
    df = st.session_state.get('ss_petcare_plans')

    # if df is not in sessions state, generate it
    if df is None:
        df = load_petcare_plans()

    # Start with the main dataframe and apply filters based on provided names
    filtered_df = df

    # Apply filter for first name if provided

    filtered_df = filtered_df[filtered_df['EvCustomerID'] == customer_id]

    # Select relevant columns
    return filtered_df[['EvCustomerID', 'OwnerFirstName', 'OwnerLastName']]



def get_PaymentLinkDetails(customer_id, pet_id):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
    SELECT
	paymentLink as "Payment Link",
    status as "Payment Status",
    merchantReference as "Merchant Reference",
    ROUND(CAST(REPLACE(amount, 'GBP ', '') AS REAL), 2) AS "Amount",
    creationDate,
	createdBy,
    shopperEmail,

    CASE

        WHEN merchantReference LIKE '%:%-%-%' THEN
            SUBSTR(
                merchantReference,
                INSTR(merchantReference, ':') + 1,
                INSTR(SUBSTR(merchantReference, INSTR(merchantReference, '-') + 1), '-') + INSTR(merchantReference, '-') - INSTR(merchantReference, ':') - 1
            )

        WHEN merchantReference NOT LIKE '%:%' THEN 'No invoice reference'
        ELSE NULL
    END AS invoiceReference

FROM adyen_PaymentLinks
WHERE
    amount NOT IN ('GBP 0.01', 'GBP 1.00', 'GBP 0.10')
    AND LENGTH("merchantReference") > 24
    AND (merchantReference LIKE '%{pet_id}%' OR merchantReference LIKE '%{customer_id}%')

        '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_invoice_name(invoice_number):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
    SELECT 
    "First Name", 
    "Last Name", 
    "Animal Name",
    "Invoice Date",
    "Invoice Line Date: Created"
    "Client Contact Code",
    "Animal Code",
    "Invoice #"
    FROM eV_InvoiceLines i 
    WHERE "Invoice #" = {invoice_number}
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:
        return (df.iloc[0]['First Name'],
                df.iloc[0]['Last Name'],
                df.iloc[0]['Animal Name'],
                df.iloc[0]['Invoice Date'],
                df.iloc[0]['Client Contact Code'],
                df.iloc[0]['Animal Code'],
                df.iloc[0]['Invoice #']
                )
    else:
        return None, None, None, None, None, None

def get_invoiceDetails(invoice_id):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
SELECT     
	i."Invoice Line ID",
	i."Product Name",
	i."Standard Price(incl)",
	i.DiscountPercentage,
	i."DiscountValue",
	i."Total Invoiced (incl)", 
	i."Discount Name" 
FROM
eV_InvoiceLines i
WHERE
i."Type" = 'Item'
AND i."Product Name" IS Not "Subscription Fee"
AND i."Product Name" IS Not "Cancellation Fee"
AND (i."Discount Name" not like "% - all"
OR i."Discount Name" is NULL)
AND i."Invoice #" = {invoice_id};
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Collect Invoices

def get_invoices(pet_id):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
    Select     
    i."Invoice #",
    i."Invoice Date",
    i."Client Contact Code",
    i."First Name",
    i."Last Name",
    i."Animal Code",
    i."Animal Name",
	SUM(i."Standard Price(incl)") AS "Total Standard Price(incl)",
    SUM(i.DiscountPercentage) AS "Total Discount Percentage",
    SUM(i."DiscountValue") AS "Total Discount Value",
    SUM(i."Total Invoiced (incl)") AS "Total Invoiced (incl)"
    FROM
    eV_InvoiceLines i
    WHERE
    i."Type" = 'Item'
    -- AND i."Product Name" IS Not "Subscription Fee"
    -- AND i."Product Name" IS Not "Cancellation Fee"
    -- AND (i."Discount Name" not like "% - all"
    -- OR i."Discount Name" is NULL)
	AND i."Animal Code" like {pet_id}
	GROUP BY 
	    i."Invoice #";
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_invoices_wo_subsc(pet_id):
    conn = sqlite3.connect('ramona_db.db')
    query = f'''
    Select     
    i."Invoice #",
    i."Invoice Date",
    i."Client Contact Code",
    i."First Name",
    i."Last Name",
    i."Animal Code",
    i."Animal Name",
	SUM(i."Standard Price(incl)") AS "Total Standard Price(incl)",
    SUM(i.DiscountPercentage) AS "Total Discount Percentage",
    SUM(i."DiscountValue") AS "Total Discount Value",
    SUM(i."Total Invoiced (incl)") AS "Total Invoiced (incl)"
    FROM
    eV_InvoiceLines i
    WHERE
    i."Type" = 'Item'
    AND i."Product Name" IS Not "Subscription Fee"
    AND i."Product Name" IS Not "Cancellation Fee"
    -- AND (i."Discount Name" not like "% - all"
    -- OR i."Discount Name" is NULL)
	AND i."Animal Code" like {pet_id}
	GROUP BY 
	    i."Invoice #";


    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


#----------------------------------------------------
# File management
#----------------------------------------------------

def list_all_files_in_data_folder():
    folder_path = "data"
    try:
        files = sorted(os.listdir(folder_path))
        file_list = [file for file in files if not (file.startswith("~") or file.startswith("."))]
        return file_list
    except FileNotFoundError:
        return [f"The folder '{folder_path}' does not exist."]
    except Exception as e:
        return [f"An error occurred: {e}"]

def load_newest_file(filename_prefix):
    folder_path = "data"
    try:
        files = os.listdir(folder_path)
        invoice_files = [file for file in files if file.startswith(filename_prefix)]
        if invoice_files:
            highest_file = max(invoice_files)
            print(highest_file)
            file_path = os.path.join(folder_path, highest_file)
            if highest_file.endswith(".csv"):
                df = pd.read_csv(file_path, low_memory=False)
                return df
            elif highest_file.endswith(".xlsx"):
                df = pd.read_excel(file_path)
                return df
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

#----------------------------------------------------
# Load data (ETL)
#----------------------------------------------------

def load_petcare_plans():
    filename_prefix = "pet-care-plans-"

    # load data into df
    df = load_newest_file(filename_prefix)

    df['EvPetId'] = df['EvPetId'].astype(str).fillna('')
    df['EvPetId'] = df['EvPetId'].astype(str).str.replace('\.0$', '', regex=True).fillna('')

    # Apply prefix based on the length of EvPetId
    def format_evpetid(id_value):
        if len(id_value) == 3:
            return f"100{id_value}"
        elif len(id_value) == 4:
            return f"10{id_value}"
        elif len(id_value) == 2:
            return f"1000{id_value}"
        else:
            return id_value

    df['EvPetId'] = df['EvPetId'].apply(format_evpetid)
    # formatting datatypes
    # Replace "v1" with "V1" in all cells of ActualEvWp
    df['ActualEvWp'] = df['ActualEvWp'].str.replace('v1', 'V1', regex=False)

    # Map specific ProductCode values to their new values
    df['ProductCode'] = df['ProductCode'].replace({
        "D1": "D1V1", "D2": "D2V2", "D3": "D3V1",
        "C1": "C1V1", "C2": "C2V2", "C3": "C3V3"
    })

    # Specifically change "C3V1 Cat-Senior" to "C3V1-Cat-Senior"
    df['ActualEvWp'] = df['ActualEvWp'].replace("C3V1 Cat-Senior", "C3V1-Cat-Senior")

    # Extract text before the first hyphen in ActualEvWp
    df['EvWPcode'] = df['ActualEvWp'].str.split('-').str[0]

    # Apply conditional changes to EvWPcode based on Species
    df['EvWPcode'] = df.apply(lambda x: "PCAV1-DOG" if x['EvWPcode'] == "PCAV1" and x['Species'] == "Dog" else (
        "PCAV1-CAT" if x['EvWPcode'] == "PCAV1" else x['EvWPcode']), axis=1)

    # Map specific ProductCode values to their new values
    df['EvWPcode'] = df['EvWPcode'].replace({
        "D1": "D1V1", "D2": "D2V2", "D3": "D3V1",
        "C1": "C1V1", "C2": "C2V2", "C3": "C3V3"
    })

    # Strip spaces and standardize case before comparing
    import numpy as np

    # Set VeraEvDiff to True when ProductCode and EvWPcode are the same, and False when they differ
    df['VeraEvDiff'] = np.where(df['EvWPcode'].isna(), False,
                                df['EvWPcode'].str.strip().str.upper() == df['ProductCode'].str.strip().str.upper())


    # Load ezyvet data to extract the customer id which is missing the Vera extract
    df2 = load_ezyvet_customers()

    df2['Animal Code'] = df2['Animal Code'].astype(str)
    df2['Owner Contact Code'] = df2['Owner Contact Code'].astype(str)

    # Assuming df2 contains 'Animal Code' and 'Owner Contact Code' columns
    df = df.merge(df2[['Animal Code', 'Owner Contact Code']], how='left', left_on='EvPetId', right_on='Animal Code')

    # Rename the merged 'Owner Contact Code' to 'EvCustomerID' and drop 'Animal Code' from the merged dataframe
    df = df.rename(columns={'Owner Contact Code': 'EvCustomerID'}).drop(columns=['Animal Code'])

    # Push the filtered DataFrame to session state
    st.session_state['ss_petcare_plans'] = df

    return df

def load_ezyvet_customers(customer_id=None):
    filename_prefix = "Animals Report-"

    # load data into df
    df = load_newest_file(filename_prefix)

    if customer_id == None:
        return df
    else:
        filt = (df['Owner Contact Code'] == customer_id)
        df = df[filt]
        return df

def get_pet_data(file_path):
    df = pd.read_csv(file_path, index_col=0)
    return df

def load_adyen_links(file_path):
  df = pd.read_csv(file_path, index_col=0)
  df.drop(columns=['description', 'store', 'reusable'], inplace=True)
  df.rename(columns={"status": "Adyen Status"}, inplace=True)

  # identifies VERA Toolbox links as PAYG
  def set_link_type(row):
      if row['amount'] == "GBP 0.01":
          return 'Card detail change'
      if row['amount'] == "GBP 1.00":
          return 'Test entry'
      if row['amount'] == "GBP 0.10":
          return 'Ignored'
      if pd.notna(row['createdBy']):
          return 'PAYG - Vera Adyen'
      if (isinstance(row['merchantReference'], str)
              and re.search(r"[ _-]", row['merchantReference'])):
          return 'PAYG - Vera Toolbox'

      return None

  # Apply the function to create the "Link Type" column
  df['Link Type'] = df.apply(set_link_type, axis=1)

  # Tag Failed Subscriptions payments
  df['Link Type'] = df['Link Type'].fillna('Failed Subscription')

  # Add customer ID and pet ID by extracting all strings of 6 numbers from 'merchantReference'
  def extract_six_numbers(merchant_reference):
      matches = re.findall(r'\d{6}', merchant_reference)
      customer_ids = []
      pet_ids = []
      for match in matches:
          if match.startswith('20'):
              customer_ids.append(match)
          elif match.startswith('10'):
              pet_ids.append(match)
      return customer_ids, pet_ids

  df[['Customer ID', 'Pet ID']] = df['merchantReference'].apply(
      lambda x: pd.Series(extract_six_numbers(x))
  )

  # Convert lists to comma-separated strings
  df['Customer ID'] = df['Customer ID'].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)
  df['Pet ID'] = df['Pet ID'].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)

  # Add invoice number (placeholder for future implementation)
  def extract_invoice_reference(merchant_reference):
      if re.search(r':.*-.*-', merchant_reference):
          try:
              colon_index = merchant_reference.index(':') + 1
              first_dash_index = merchant_reference.index('-', colon_index) + 1
              second_dash_index = merchant_reference.index('-', first_dash_index)
              return merchant_reference[colon_index:second_dash_index]
          except ValueError:
              return None
      elif ':' not in merchant_reference:
          return 'No invoice reference'
      else:
          return None

  df[['Invoice ID']] = df['merchantReference'].apply(
      lambda x: pd.Series(extract_invoice_reference(x))
  )

  return df

def extract_six_numbers(merchant_reference):
    matches = re.findall(r'\d{6}', merchant_reference)
    if matches:
        return ', '.join(matches)
    return None

def load_xero_PAYGrec_report(file_path):
    df = pd.read_excel(file_path, skiprows=4, header=0).drop([0, 1])
    df = df[~df['Date'].isin(["Total PetCare Advanced PAYG", "Total PAYG Income", "Total", "PetCare Advanced PAYG"])]
    df = df.dropna(how='all')

    # Cleaning up the ref ID
    # Define a helper function
    def process_reference(value):
        if isinstance(value, str) and value.startswith('PL:'):
            return value[3:]
        else:
            return np.nan

    # Apply the helper function to the "Reference" column to create the new column
    df['Adyen Ref ID'] = df['Reference'].apply(process_reference)

    # add VAT to the amount
    df['Amount (incl VAT)'] = (df['Credit (Source)'] * 1.20).round(2)

    # add payment status from AR report


    return df

def load_xero_AR_report(file_path):
    df = pd.read_excel(file_path, skiprows=5, header=0).drop([0, 1])
    # df.set_index("Invoice Number", inplace=True)
    df = df[~df['Invoice Date'].isin(
        ["Total PAYG Client", "Percentage of total", "Total", "PetCare Advanced PAYG"])]
    df = df.dropna(how='any', subset="Invoice Date")
    # df.drop(columns=["Contact Account Number"], inplace=True)
    df.drop(columns=["Due Date"], inplace=True)
    # Convert a Date column to datetime and format it to 'YYYY-MM-DD'
    df['Invoice Date'] = pd.to_datetime(df['Invoice Date']).dt.strftime('%Y-%m-%d')
    # Round all numeric columns to 2 decimal places
    df = df.round(2)
    # Apply formatting for all relevant columns to ensure 2 decimal places
    df["< 1 Month"] = df["< 1 Month"].round(2)
    df["1 Month"] = df["1 Month"].round(2)
    df["2 Months"] = df["2 Months"].round(2)
    df["3 Months"] = df["3 Months"].round(2)
    df["Older"] = df["Older"].round(2)
    df["Total"] = df["Total"].round(2)

    # Force all columns to display 2 decimals
    # df[["< 1 Month", "1 Month", "2 Months", "3 Months", "Older", "Total"]] = df[
    #     ["< 1 Month", "1 Month", "2 Months", "3 Months", "Older", "Total"]].apply(lambda x: f'{x:,.2f}')

    # Cleaning up the ref ID
    # Define a helper function
    def process_reference(value):
        if isinstance(value, str) and value.startswith('PL:'):
            return value[3:]
        else:
            return np.nan

    # Apply the helper function to the "Reference" column to create the new column
    df['Invoice Reference'] = df['Invoice Reference'].apply(process_reference)
    df = df[df['Total'] != 0.01]

    return df


#----------------------------------------------------
# Prepare data for Client Timeline
#----------------------------------------------------

def extract_tl_Invoices():
    filename_prefix = "Invoice Lines-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["Invoice #"] = df["Invoice #"].astype(str)
    df["Animal Code"] = df["Animal Code"].astype(str).str.split('.').str[0]
    df["Client Contact Code"] = df["Client Contact Code"].astype(str)
    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], format="%d-%m-%Y")

    # Cleaning the data
    df = df[(df["Type"] != "Header") &
            (df["Product Name"] != "Subscription Fee") &
            (df["Product Name"] != "Cancellation Fee") &
            (df["Product Name"] != "Cancellation Fee") &
            ~df["First Name"].isin(["GVAK"])]

    # Grouping and adding sums, and renaming columns in one go
    df = df.assign(
        tl_ID=df["Invoice #"],
        tl_Date=df["Invoice Date"],
        tl_CustomerID=df["Client Contact Code"],
        tl_CustomerName=df["First Name"] + " " + df["Last Name"],
        tl_PetID=df["Animal Code"],
        tl_PetName=df["Animal Name"],
        tl_Cost=df.groupby("Invoice #")["Product Cost"].transform('sum').round(2),
        tl_Discount=df.groupby("Invoice #")["Discount(\u00a3)"].transform('sum').round(2),
        tl_Revenue=df.groupby("Invoice #")["Total Invoiced (incl)"].transform('sum').round(2),
        tl_Event="ezyVet Invoice"
    )

    # Reducing the DataFrame and grouping by "tl_ID"
    aggregated_invoices = df[[
        "tl_ID", "tl_Date", "tl_CustomerID", "tl_CustomerName", "tl_PetID",
        "tl_PetName", "tl_Cost", "tl_Discount", "tl_Revenue", "tl_Event"
    ]].groupby("tl_ID", as_index=False).agg({
        "tl_Date": "max",  # Latest date per group
        "tl_CustomerID": "first",  # Customer ID remains consistent within each invoice
        "tl_CustomerName": "first",  # Customer name remains consistent within each invoice
        "tl_PetID": "first",  # First Pet ID if multiple exist
        "tl_PetName": "first",  # First Pet Name
        "tl_Cost": "first",  # Sum of costs for each invoice
        "tl_Discount": "first",  # Sum of discounts for each invoice
        "tl_Revenue": "first",  # Sum of revenues for each invoice
        "tl_Event": "first"  # Event remains consistent within each invoice
    })

    # Update tl_Discount if tl_Revenue is less than tl_Cost
    aggregated_invoices.loc[aggregated_invoices["tl_Revenue"] < aggregated_invoices["tl_Cost"], "tl_Discount"] = (
        aggregated_invoices["tl_Cost"] - aggregated_invoices["tl_Revenue"]
    ).round(2)

    # Round the sums to 2 decimal places
    aggregated_invoices["tl_Cost"] = aggregated_invoices["tl_Cost"].round(2)
    aggregated_invoices["tl_Discount"] = aggregated_invoices["tl_Discount"].round(2)
    aggregated_invoices["tl_Revenue"] = aggregated_invoices["tl_Revenue"].round(2)

    # return the aggregated DataFrame
    return aggregated_invoices

def extract_tl_Payments_OLD():
    filename_prefix = "payment-history-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["ezyvetPetIDs"] = df["ezyvetPetIDs"].astype(str)
    df["ezyvetContactId"] = df["ezyvetContactId"].astype(str)
    df["cardDetails_lastFour"] = df["cardDetails_lastFour"].astype(str)
    df['amount'] = df['amount'].astype(float).round(2) / 100
    df["eventDate"] = pd.to_datetime(df["eventDate"], utc=True)
    df["eventDate"] = df["eventDate"].dt.strftime('%Y-%m-%d')

    # Grouping and adding sums, and renaming columns in one go
    df = df.assign(
        tl_ID=df["veraReference"],
        tl_Date=df["eventDate"],
        tl_CustomerID=df["ezyvetContactId"],
        tl_CustomerName="",
        tl_PetID=df["ezyvetPetIDs"],
        tl_PetName="",
        tl_Cost=0,
        tl_Discount=0,
        tl_Revenue=df["amount"],
        tl_Event=df["type"]
    )

    payments = df[[
        "tl_ID", "tl_Date", "tl_CustomerID", "tl_CustomerName", "tl_PetID",
        "tl_PetName", "tl_Cost", "tl_Discount", "tl_Revenue", "tl_Event"
    ]]
    # return the aggregated DataFrame
    return payments

def extract_tl_Payments():
    filename_prefix = "payment-history-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["ezyvetPetIDs"] = df["ezyvetPetIDs"].astype(str)
    df["ezyvetContactId"] = df["ezyvetContactId"].astype(str)
    df["cardDetails_lastFour"] = df["cardDetails_lastFour"].astype(str)
    df['amount'] = df['amount'].astype(float).round(2) / 100
    df["eventDate"] = pd.to_datetime(df["eventDate"], utc=True)
    df["eventDate"] = df["eventDate"].dt.strftime('%Y-%m-%d')

    # st.header('pre-split DF')
    # st.dataframe(df)

    # splitting multipet payments
    # Add new column 'PetsInSubscription' with the number of pet IDs in 'ezyvetPetIDs'
    df['PetsInSubscription'] = df['ezyvetPetIDs'].apply(lambda x: x.count(',') + 1)

    # Split rows with multiple pet IDs into separate rows
    df['ezyvetPetIDs'] = df['ezyvetPetIDs'].str.split(',')
    df = df.explode('ezyvetPetIDs')

    # st.header('post-split DF')
    # st.dataframe(df)

    # Identifying number of failed payments in a row
    # Create a subset where status is 'Refused'
    df_refused = df[df['status'] == 'Refused']

    # Sort df_refused by 'ezyvetPetIDs' and 'eventDate'
    df_refused = df_refused.sort_values(by=['ezyvetPetIDs', 'eventDate']).reset_index(drop=True)

    # Add new column 'MissedPayments' with the sequence number for each 'ezyvetPetIDs'
    def assign_sequence(df):
        sequence = []
        current_seq = 1
        for i in range(len(df)):
            if i == 0:
                sequence.append(current_seq)
            else:
                if df['ezyvetPetIDs'][i] == df['ezyvetPetIDs'][i - 1] and pd.to_datetime(
                        df['eventDate'][i]) == pd.to_datetime(df['eventDate'][i - 1]) + pd.Timedelta(days=1):
                    current_seq += 1
                else:
                    current_seq = 1
                sequence.append(current_seq)
        return sequence

    # Sort the dataframe by 'ezyvetPetIDs' and 'eventDate'
    df_refused = df_refused.sort_values(by=['ezyvetPetIDs', 'eventDate']).reset_index(drop=True)

    df_refused['MissedPayments'] = assign_sequence(df_refused)

    # st.title("Sorted payments with label")
    # st.dataframe(df_refused)


    # Update 'type' column based on 'MissedPayments'
    df_refused['type'] = df_refused.apply(lambda row: 'SUSPENDED ACCOUNT' if row['MissedPayments'] >= 8 else
    f"Missed Payment {row['MissedPayments']} - £{row['amount']}" if 1 <= row['MissedPayments'] < 8 else None, axis=1)
    df_refused['amount'] = 0

    # st.header('refused with sequence number')
    # st.dataframe(df_refused)

    # Drop duplicate 'adyenReference' in df_refused
    df_refused = df_refused.drop_duplicates(subset='adyenReference')

    # Merge df with df_refused to update 'type' and 'amount'
    df = df.merge(df_refused[['adyenReference', 'type', 'amount']], on='adyenReference', how='left',
                  suffixes=('', '_refused'))

    # Update 'type' and 'amount' only where there are values from df_refused
    df['type'] = df['type_refused'].combine_first(df['type'])
    df['amount'] = df['amount_refused'].combine_first(df['amount'])

    # Drop the temporary columns
    df = df.drop(columns=['type_refused', 'amount_refused'])

    # st.header('Merged df - are amounts 0')
    # st.dataframe(df)

    df.loc[df['adyenEvent'] == 'REFUND', 'amount'] *= -1

    # Grouping and adding sums, and renaming columns in one go
    df = df.assign(
        tl_ID=df["veraReference"],
        tl_Date=df["eventDate"],
        tl_CustomerID=df["ezyvetContactId"],
        tl_CustomerName="",
        tl_PetID=df["ezyvetPetIDs"],
        tl_PetName="",
        tl_Cost=0,
        tl_Discount=0,
        tl_Revenue=df["amount"],
        tl_Event=df["type"],
        tl_Comment=""
    )

    payments = df[[
        "tl_ID", "tl_Date", "tl_CustomerID", "tl_CustomerName", "tl_PetID",
        "tl_PetName", "tl_Cost", "tl_Discount", "tl_Revenue", "tl_Event","tl_Comment"
    ]]

    # st.header('output DF')
    # st.dataframe(payments)

    # return the aggregated DataFrame
    return payments



def extract_tl_pet_data_death():
    filename_prefix = "Animals Report-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["Animal Record Created At"] = pd.to_datetime(df["Animal Record Created At"], format="%Y-%m-%d %H:%M:%S")
    df["Date of Passing"] = pd.to_datetime(df["Date of Passing"], format="%d-%m-%Y")
    df["Animal Code"] = df["Animal Code"].astype(str).str.split('.').str[0]
    df["Owner Contact Code"] = df["Owner Contact Code"].astype(str)

    # filtering the data
    df = df[(df["Has Passed Away"] == "Yes")]


    # adding new columns
    df = df.assign(
        tl_ID=df["Animal Code"],
        tl_Date=df["Date of Passing"],
        tl_CustomerID=df["Owner Contact Code"],
        tl_CustomerName=df["Owner First Name"] + " " + df["Owner Last Name"],
        tl_PetID=df["Animal Code"],
        tl_PetName=df["Animal Name"],
        tl_Cost=0,
        tl_Discount=0,
        tl_Revenue=0,
        tl_Event="Pet passed away"
    )

    # Reducing the DataFrame and grouping by "tl_ID"
    dead_pets = df[["tl_ID",
                    "tl_Date",
                    "tl_CustomerID",
                    "tl_CustomerName",
                    "tl_PetID",
                    "tl_PetName",
                    "tl_Cost",
                    "tl_Discount",
                    "tl_Revenue",
                    "tl_Event"
                    ]]


    # return the aggregated DataFrame
    return dead_pets

def extract_tl_pet_data_registration():
    filename_prefix = "Animals Report-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["Animal Record Created At"] = pd.to_datetime(df["Animal Record Created At"], format="%Y-%m-%d %H:%M:%S")
    df["Date of Passing"] = pd.to_datetime(df["Date of Passing"], format="%d-%m-%Y")
    df["Animal Code"] = df["Animal Code"].astype(str).str.split('.').str[0]
    df["Owner Contact Code"] = df["Owner Contact Code"].astype(str)

    # filtering the data
    df = df[(df["Owner Contact Code"] != "ezyVet")
            & (df["Owner First Name"] != "GVAK")
            & (df["Animal Record Created At"] > "2023-11-17 19:10:22")
            ]

    # adding new columns
    df = df.assign(
        tl_ID=df["Animal Code"],
        tl_Date=df["Animal Record Created At"],
        tl_CustomerID=df["Owner Contact Code"],
        tl_CustomerName=df["Owner First Name"] + " " + df["Owner Last Name"],
        tl_PetID=df["Animal Code"],
        tl_PetName=df["Animal Name"],
        tl_Cost=0,
        tl_Discount=0,
        tl_Revenue=0,
        tl_Event="Initial registration"
    )

    # Reducing the DataFrame and grouping by "tl_ID"
    initial_registration = df[["tl_ID",
                               "tl_Date",
                               "tl_CustomerID",
                               "tl_CustomerName",
                               "tl_PetID",
                               "tl_PetName",
                               "tl_Cost",
                               "tl_Discount",
                               "tl_Revenue",
                               "tl_Event"]]

    # return the aggregated DataFrame
    return initial_registration

def extract_tl_Cancellations():

# ----------------------------------------------------
# NOTE - Zero priced Cancellation Fees in ezyVet indicates
# a change of Wellness Plan
# ----------------------------------------------------


    filename_prefix = "Invoice Lines-"

    # load data into df
    df = load_newest_file(filename_prefix)

    # formatting datatypes
    df["Invoice #"] = df["Invoice #"].astype(str)
    df["Animal Code"] = df["Animal Code"].astype(str).str.split('.').str[0]
    df["Client Contact Code"] = df["Client Contact Code"].astype(str)
    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"], format="%d-%m-%Y")
    df["Invoice Line Date: Created"] = pd.to_datetime(df["Invoice Line Date: Created"], format="%d-%m-%Y")

    # Cleaning the data
    df = df[(df["Type"] != "Header") &
            (df["Product Name"] == "Cancellation Fee") &
            (df["Total Invoiced (incl)"] == 0)]

    # Grouping and adding sums, and renaming columns in one go
    df = df.assign(
        tl_ID=df["Invoice #"],
        tl_Date=df["Invoice Line Date: Created"],
        tl_CustomerID=df["Client Contact Code"],
        tl_CustomerName=df["First Name"] + " " + df["Last Name"],
        tl_PetID=df["Animal Code"],
        tl_PetName=df["Animal Name"],
        tl_Cost=df.groupby("Invoice #")["Product Cost"].transform('sum').round(2),
        tl_Discount=df.groupby("Invoice #")["Discount(\u00a3)"].transform('sum').round(2),
        tl_Revenue=df.groupby("Invoice #")["Total Invoiced (incl)"].transform('sum').round(2),
        tl_Event="Changed PetCare Plan in ezyVet"
        )

    # Reducing the DataFrame and grouping by "tl_ID"
    cancellations = df[[
        "tl_ID", "tl_Date", "tl_CustomerID", "tl_CustomerName", "tl_PetID",
        "tl_PetName", "tl_Cost", "tl_Discount", "tl_Revenue", "tl_Event"
    ]].groupby("tl_ID", as_index=False).agg({
        "tl_Date": "max",  # Latest date per group
        "tl_CustomerID": "first",  # Customer ID remains consistent within each invoice
        "tl_CustomerName": "first",  # Customer name remains consistent within each invoice
        "tl_PetID": "first",  # First Pet ID if multiple exist
        "tl_PetName": "first",  # First Pet Name
        "tl_Cost": "sum",  # Sum of costs for each invoice
        "tl_Discount": "sum",  # Sum of discounts for each invoice
        "tl_Revenue": "sum",  # Sum of revenues for each invoice
        "tl_Event": "first"  # Event remains consistent within each invoice
    })

    # Round the sums to 2 decimal places
    cancellations["tl_Cost"] = cancellations["tl_Cost"].round(2)
    cancellations["tl_Discount"] = cancellations["tl_Discount"].round(2)
    cancellations["tl_Revenue"] = cancellations["tl_Revenue"].round(2)

    # return the aggregated DataFrame
    return cancellations

def build_tl():
    # import data for TimeLine
    tl_invoices = extract_tl_Invoices()
    tl_change_plan = extract_tl_Cancellations()
    tl_pet_data = extract_tl_pet_data_death()
    tl_initial_registration = extract_tl_pet_data_registration()
    tl_payments = extract_tl_Payments()

    # Concatenate the DataFrames
    merged_df = pd.concat([tl_invoices, tl_change_plan, tl_pet_data, tl_initial_registration, tl_payments], ignore_index=True)

    merged_df["tl_Date"] = pd.to_datetime(merged_df["tl_Date"])

    # Sort the merged DataFrame by the 'date' column
    tl = merged_df.sort_values(by='tl_Date', ascending=True)  # Set ascending=False if you want descending order



    if 'tl' not in st.session_state:
        st.session_state.tl = 'tl'

    return tl













