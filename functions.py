import numpy as np
import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import re

def set_page_definitition():
    app_name = "RAmona v0.1"

    # Loading Image using PIL
    icon = Image.open('content/Subsidiary Salmon Logo.png')

    # Enable wide mode and set light theme and add tab icon
    st.set_page_config(layout="wide", page_title=app_name, page_icon=icon, initial_sidebar_state="expanded")
    # st.set_page_config(layout="wide", page_title=app_name, page_icon=":material/sound_detection_dog_barking:", initial_sidebar_state="expanded")

    return app_name

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

    # Function to get contact details by First Name and Last Name

# Case Details Functions

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
# Load data (ETL)
#----------------------------------------------------

def get_pet_data(file_path):
    df = pd.read_csv(file_path, index_col=0)
    return df


def load_adyen_links(file_path):
  df = pd.read_csv(file_path, index_col=0)

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
    df = pd.read_excel(file_path, skiprows=7, header=0).drop([0, 1])
    df = df[~df['Contact Account Number'].isin(["Total PAYG Client", "Percentage of total", "Total", "PetCare Advanced PAYG"])]
    df = df.dropna(how='all')

    # # Cleaning up the ref ID
    # # Define a helper function
    # def process_reference(value):
    #     if isinstance(value, str) and value.startswith('PL:'):
    #         return value[3:]
    #     else:
    #         return np.nan
    #
    # # Apply the helper function to the "Reference" column to create the new column
    # df['Adyen Ref ID'] = df['Reference'].apply(process_reference)
    #
    # # add VAT to the amount
    # df['Amount (incl VAT)'] = (df['Credit (Source)'] * 1.20).round(2)

    return df
