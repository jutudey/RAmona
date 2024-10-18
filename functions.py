import streamlit as st
import sqlite3
import pandas as pd


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