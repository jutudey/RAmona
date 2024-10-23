import streamlit as st
import functions

functions.set_page_definitition()

# def get_PaymentLinkDetails(customer_id, pet_id):
#     conn = sqlite3.connect('ramona_db.db')
#     query = f'''
#     SELECT
# 	paymentLink as "Payment Link",
#     status as "Payment Status",
#     merchantReference as "Merchant Reference",
#     ROUND(CAST(REPLACE(amount, 'GBP ', '') AS REAL), 2) AS "Amount",
#     creationDate,
# 	createdBy,
#     shopperEmail,
#
#     CASE
#
#         WHEN merchantReference LIKE '%:%-%-%' THEN
#             SUBSTR(
#                 merchantReference,
#                 INSTR(merchantReference, ':') + 1,
#                 INSTR(SUBSTR(merchantReference, INSTR(merchantReference, '-') + 1), '-') + INSTR(merchantReference, '-') - INSTR(merchantReference, ':') - 1
#             )
#
#         WHEN merchantReference NOT LIKE '%:%' THEN 'No invoice reference'
#         ELSE NULL
#     END AS invoiceReference
#
# FROM adyen_PaymentLinks
# WHERE
#     amount NOT IN ('GBP 0.01', 'GBP 1.00', 'GBP 0.10')
#     AND LENGTH("merchantReference") > 24
#     AND (merchantReference LIKE '%{pet_id}%' OR merchantReference LIKE '%{customer_id}%')
#
#         '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df


# Function to get First Name and Last Name for a specific Invoice #
# def get_invoice_name(invoice_number):
#     conn = sqlite3.connect('ramona_db.db')
#     query = f'''
#     SELECT
#     "First Name",
#     "Last Name",
#     "Animal Name",
#     "Invoice Date",
#     "Client Contact Code",
#     "Animal Code",
#     "Invoice #"
#     FROM eV_InvoiceLines i
#     WHERE "Invoice #" = {invoice_number}
#     '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#
#     if not df.empty:
#         return (df.iloc[0]['First Name'],
#                 df.iloc[0]['Last Name'],
#                 df.iloc[0]['Animal Name'],
#                 df.iloc[0]['Invoice Date'],
#                 df.iloc[0]['Client Contact Code'],
#                 df.iloc[0]['Animal Code'],
#                 df.iloc[0]['Invoice #']
#                 )
#     else:
#         return None, None, None, None, None, None


# Function to get invoice details

# def get_invoiceDetails(invoice_id):
#     conn = sqlite3.connect('ramona_db.db')
#     query = f'''
# SELECT
# 	i."Invoice Line ID",
# 	i."Product Name",
# 	i."Standard Price(incl)",
# 	i.DiscountPercentage,
# 	i."DiscountValue",
# 	i."Total Invoiced (incl)",
# 	i."Discount Name"
# FROM
# eV_InvoiceLines i
# WHERE
# i."Type" = 'Item'
# AND i."Product Name" IS Not "Subscription Fee"
# AND i."Product Name" IS Not "Cancellation Fee"
# AND (i."Discount Name" not like "% - all"
# OR i."Discount Name" is NULL)
# AND i."Invoice #" = {invoice_id};
#     '''
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df


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
     ) = functions.get_invoice_name(case_invoice_no)

    # Collect Invoice details
    data = functions.get_invoiceDetails(invoice_no)

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
        data2 = functions.get_PaymentLinkDetails(customer_id, pet_id)
        print(data2)
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

