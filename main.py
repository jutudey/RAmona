import streamlit as st
import sqlite3
import pandas as pd
import tabulate

app_name = "RAmona v0.1"

# Enable wide mode and set light theme
st.set_page_config(layout="wide", page_title=app_name)


# Function to query the database
def get_PAYGinvoiceLines():
    conn = sqlite3.connect('ramona_db.db')
    query = '''
    Select     
    i."Invoice #",
    i."Invoice Date",
    i."Client Contact Code",
    i."First Name",
    i."Last Name",
    i."Animal Code",
    i."Animal Name",
    i."Product Name",
    i."Invoice Line ID",
    i."Standard Price(incl)",
    i.DiscountPercentage,
    i."DiscountValue",
    i."Discount Name",
    i."Total Invoiced (incl)" 
    FROM
    eV_InvoiceLines i
    WHERE
    i."Type" = 'Item'
    AND i."Product Name" IS Not "Subscription Fee"
    AND i."Product Name" IS Not "Cancellation Fee"
    AND (i."Discount Name" not like "% - all"
    OR i."Discount Name" is NULL)
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Function to get invoice details
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

# Function to get First Name and Last Name for a specific Invoice #
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
    FROM eV_InvoiceLines
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

# Function to get Adyen Payment links with IDs
def get_PaymentLinks():
    conn = sqlite3.connect('ramona_db.db')
    query = '''
    SELECT
    id as "Identifier",
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
    END AS invoiceReference,

    CASE

        WHEN SUBSTR(merchantReference, INSTR(merchantReference, '10'), 6) LIKE '10____'
             AND SUBSTR(merchantReference, INSTR(merchantReference, '10') + 5, 1) != '-' THEN
            SUBSTR(merchantReference, INSTR(merchantReference, '10'), 6)
        ELSE NULL
    END AS PetID,

    CASE

        WHEN SUBSTR(merchantReference, INSTR(merchantReference, '20'), 6) LIKE '20____'
             AND SUBSTR(merchantReference, INSTR(merchantReference, '20') + 5, 1) != '-' THEN
            SUBSTR(merchantReference, INSTR(merchantReference, '20'), 6)
        ELSE NULL
    END AS CustomerID


FROM adyen_PaymentLinks
WHERE
    amount NOT IN ('GBP 0.01', 'GBP 1.00', 'GBP 0.10')
    AND LENGTH("merchantReference") > 24
        '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

page1 = "PAYG Invoice Lines"
page2 = "Case Details by Invoice"
page3 = "Adyen Links"

pages = [page2, page1, page3]

# Streamlit app with sidebar navigation
st.sidebar.title(app_name)
page = st.sidebar.radio("Go to", pages)

# First page: Data Viewer
if page == page1:
    st.title(page1)

    # Run the query automatically on page load
    data = get_PAYGinvoiceLines()

    # Create 3 columns for the filters
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        invoice_filter = st.text_input('Filter by Invoice #', '')

    with col2:
        client_filter = st.text_input('Filter by Client Contact Code', '')

    with col3:
        animal_filter = st.text_input('Filter by Animal Code', '')

    # Apply filters on the data dynamically
    if invoice_filter:
        data = data[data['Invoice #'].astype(str).str.contains(invoice_filter)]
    if client_filter:
        data = data[data['Client Contact Code'].astype(str).str.contains(client_filter)]
    if animal_filter:
        data = data[data['Animal Code'].astype(str).str.contains(animal_filter)]

    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results:")
    st.dataframe(data.reset_index(drop=True), height=400)  # Removed index and compact height of 400px

    # Export filtered data to CSV
    csv = data.to_csv(index=False).encode('utf-8')

    # Create export button
    st.download_button(
        label="Export filtered data to CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

# Second page: Hello
elif page == page2:
    st.title(page2)

    # Create 3 columns
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        case_invoice_no = st.text_input('Invoice number', '')
        # case_invoice_no = 422642 # to force look during development

    # with col2:
    #     client_filter = st.text_input('Filter by Client Contact Code', '')
    #
    # with col3:
    #     animal_filter = st.text_input('Filter by Animal Code', '')

    if case_invoice_no:
        # Fetch the first and last name for the defined Invoice number
        (first_name,
         last_name,
         pet_name,
         invoice_date,
         customer_id,
         pet_id,
         invoice_no
         ) = get_invoice_name(case_invoice_no)

        # Collect Invoice details
        data = get_invoiceDetails(invoice_no)

        # Collect Payment Links details



        if first_name and last_name:
            st.subheader(f"Customer: {first_name} {last_name}")
            st.subheader(f"Pet: {pet_name}")
            st.markdown(f"**Invoice Date:** {invoice_date}")
            st.markdown(f"**Customer ID:** {customer_id}")
            st.markdown(f"**Pet ID:** {pet_id}")
            st.markdown(f"**Invoice ID:** {invoice_no}")



            # Set height dynamically based on the number of rows
            num_rows = len(data)
            height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.write("Displaying filtered results:")
            st.dataframe(data.reset_index(drop=True), height=height)  # Removed index and compact height of 400px

        else:
            st.header("Invoice #422642 not found")

    st.write("Made by AJ")

# third page: Adyen links
elif page == page3:
    st.title(page3)

   # Run the query automatically on page load
    data = get_PaymentLinks()

    # Create 3 columns for the filters
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        merchant_ref_filter = st.text_input('Search inside the Merchant Reference', '')

    # with col2:
    #     # client_filter = st.text_input('Filter by Client Contact Code', '')
    #
    # with col3:
    #     # animal_filter = st.text_input('Filter by Animal Code', '')

    # Apply filters on the data dynamically
    if merchant_ref_filter:
        data = data[data["Merchant Reference"].astype(str).str.contains(merchant_ref_filter)]
    # if client_filter:
    #     data = data[data['Client Contact Code'].astype(str).str.contains(client_filter)]
    # if animal_filter:
    #     data = data[data['Animal Code'].astype(str).str.contains(animal_filter)]



    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results test:")
    st.dataframe(data.reset_index(drop=True), height=400)  # Removed index and compact height of 400px

    # Export filtered data to CSV
    csv = data.to_csv(index=False).encode('utf-8')

    # Create export button
    st.download_button(
        label="Export filtered data to CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )