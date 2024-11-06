import streamlit as st
import sqlite3
import pandas as pd
import functions
from datetime import datetime

app_name = functions.set_page_definitition()

if 'tl' not in st.session_state:
    st.session_state.tl = ""
    st.session_state.tl = functions.build_tl()



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

# to be replaced by the panda function below
invoice_lines_from_pandas = functions.get_invoice_lines()

def get_PAYGinvoices():
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
    AND (i."Discount Name" not like "% - all"
    OR i."Discount Name" is NULL)
	GROUP BY 
	    i."Invoice #";


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
        return None, None, None, None, None, None, None


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

# to be replaced by pandas function below
adyenlinks_from_pandas = functions.load_adyen_links()

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


topPage = "Case Details by Invoice No."
page1 = "PAYG Invoice Lines"
page3 = "Adyen Links"
page4 = "Unpaid PAYG invoices?"
page5 = "Invoice Status"

pages = [topPage, page4, page1, page3, page5]

# Streamlit app with sidebar navigation
st.sidebar.title(app_name)
page = st.sidebar.radio("Go to", pages)

# Page: PAYG Invoice Lines
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


# Page: PAYG Invoice Lines
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

# Case Details by Invoice ID
elif page == topPage:
    # st.title(page2)

    # Create 3 columns
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        case_invoice_no = st.text_input('Invoice number', '')
        # case_invoice_no = 422642 # to force look during development

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

        if first_name and last_name:
            st.header(f"{first_name} {last_name} - {pet_name}")

            with col3:
                st.markdown(f"**Invoice Date:** {invoice_date}")
                st.markdown(f"**Customer ID:** {customer_id}")
                st.markdown(f"**Pet ID:** {pet_id}")
                st.markdown(f"**Invoice ID:** {invoice_no}")

            # Set height dynamically based on the number of rows
            num_rows = len(data)
            height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown("#### Invoice Lines:")

            # st.dataframe(data.reset_index(drop=True), height=height)  # Removed index and compact height of 400px
            st.markdown(data.to_markdown(index=False), unsafe_allow_html=True)

            # Collect Payment Links details
            data2 = get_PaymentLinkDetails(customer_id, pet_id)

            # Set height dynamically based on the number of rows
            num_rows = len(data)
            height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown(f"#### Adyen Links associated with this client:""")

            # st.dataframe(data2.reset_index(drop=True), height=height)  # Removed index and compact height of 400px
            data2['Payment Link'] = data2['Payment Link'].apply(lambda x: f'[Link]({x})')
            st.markdown(data2.to_markdown(index=False), unsafe_allow_html=True)


        else:
            st.header("Invoice #422642 not found")


# page: Adyen links
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


# page: PAYG Invoices
elif page == page4:
    st.title(page4)

    # Run the query automatically on page load
    data = get_PAYGinvoices()

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
