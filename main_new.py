import streamlit as st
import sqlite3
import pandas as pd
import functions
from datetime import datetime

app_name = functions.set_page_definitition()


# ----------------------------------------------------
# defining session states
# ----------------------------------------------------



if 'tl' not in st.session_state:
    st.session_state.tl = ""
    st.session_state.tl = functions.build_tl()



# Collect Invoice Lines
invoice_lines_from_pandas = functions.get_invoice_lines()

# Collect Adyen Links
adyenlinks_from_pandas = functions.load_adyen_links()


topPage = "Case Details by Invoice No."
page1 = "PAYG Invoice Lines"
page3 = "Adyen Links"


pages = [topPage, page1, page3]

# Streamlit app with sidebar navigation
st.sidebar.title(app_name)
page = st.sidebar.radio("Go to", pages)



# Case Details by Invoice ID
if page == topPage:
    st.title(topPage)

    # Create 3 columns
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        case_invoice_no = st.text_input('Invoice number', '')


    if case_invoice_no:
        # # OLD Fetch the first and last name for the defined Invoice number
        # (first_name,
        #  last_name,
        #  pet_name,
        #  invoice_date,
        #  customer_id,
        #  pet_id,
        #  invoice_no
        #  ) = get_invoice_name(case_invoice_no)

        # collect invoice data
        invoice_lines_from_pandas = invoice_lines_from_pandas[(invoice_lines_from_pandas['Invoice #'] == case_invoice_no)]
        # st.dataframe(invoice_lines_from_pandas)
        invoice_lines_from_pandas.reset_index(drop=True, inplace=True)
        _first_name = invoice_lines_from_pandas.loc[0, 'First Name']
        _last_name = invoice_lines_from_pandas.loc[0, 'Last Name']
        _pet_name = invoice_lines_from_pandas.loc[0, 'Animal Name']
        _invoice_date = invoice_lines_from_pandas.loc[0, 'Invoice Date']
        _customer_id = invoice_lines_from_pandas.loc[0, 'Client Contact Code']
        _pet_id = invoice_lines_from_pandas.loc[0, 'Animal Code']
        _invoice_no = invoice_lines_from_pandas.loc[0, 'Invoice #']
        # OLD Collect Invoice details
        # data = get_invoiceDetails(invoice_no)

        if _first_name and _last_name:
            st.header(f"{_first_name} {_last_name} - {_pet_name}")

            with col3:
                st.markdown(f"**Invoice Date:** {_invoice_date}")
                st.markdown(f"**Customer ID:** {_customer_id}")
                st.markdown(f"**Pet ID:** {_pet_id}")
                st.markdown(f"**Invoice ID:** {_invoice_no}")

            # # OLD Set height dynamically based on the number of rows
            # num_rows = len(data)
            # height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # NEW Set height dynamically based on the number of rows
            _num_rows = len(invoice_lines_from_pandas)
            _height = min(40 * _num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown("#### Invoice Lines:")

            # st.markdown(data.to_markdown(index=False), unsafe_allow_html=True)

            # NEW
            invoice_lines_from_pandas.reset_index(drop=True, inplace=True)
            invoice_lines_from_pandas_display = invoice_lines_from_pandas[['Invoice Line ID', 'Product Name', 'Standard Price(incl)', 'Discount(%)', 'Discount(£)', 'Total Invoiced (incl)', 'Discount Name' ]]
            st.markdown(invoice_lines_from_pandas_display.to_markdown(index=False), unsafe_allow_html=True)

            # OLD Collect Payment Links details
            # data2 = get_PaymentLinkDetails(customer_id, pet_id)

            # Collect Payment Links Detaiils
            adyenlinks_from_pandas_display = adyenlinks_from_pandas[adyenlinks_from_pandas["Customer ID"] == _customer_id]
            # st.dataframe(adyenlinks_from_pandas_display)
            adyenlinks_from_pandas_display = adyenlinks_from_pandas_display[['paymentLink', 'Adyen Status', 'merchantReference', 'Invoice ID', 'amount', 'creationDate', 'createdBy', 'shopperEmail', 'Link Type']]

            # st.dataframe(adyenlinks_from_pandas_display)

            # # OLD Set height dynamically based on the number of rows
            # num_rows = len(data)
            # height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Set height dynamically based on the number of rows
            _num_rows = len(adyenlinks_from_pandas)
            _height = min(40 * _num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown(f"#### Adyen Links associated with this client:""")

            # data2['Payment Link'] = data2['Payment Link'].apply(lambda x: f'[Link]({x})')
            # st.markdown(data2.to_markdown(index=False), unsafe_allow_html=True)

            adyenlinks_from_pandas_display['paymentLink'] = adyenlinks_from_pandas_display['paymentLink'].apply(lambda x: f'[Link]({x})')
            st.markdown(adyenlinks_from_pandas_display.to_markdown(index=False), unsafe_allow_html=True)




        else:
            st.header("Invoice not found")

# Page: PAYG Invoice Lines
elif page == page1:
    st.title(page1)

    # Run the query automatically on page load
    # data = get_PAYGinvoiceLines()

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
        invoice_lines_from_pandas = invoice_lines_from_pandas[invoice_lines_from_pandas['Invoice #'].astype(str).str.contains(invoice_filter)]
    if client_filter:
        invoice_lines_from_pandas = invoice_lines_from_pandas[invoice_lines_from_pandas['Client Contact Code'].astype(str).str.contains(client_filter)]
    if animal_filter:
        invoice_lines_from_pandas = invoice_lines_from_pandas[invoice_lines_from_pandas['Animal Code'].astype(str).str.contains(animal_filter)]

    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results:")
    st.dataframe(invoice_lines_from_pandas.reset_index(drop=True), height=400)  # Removed index and compact height of 400px


    # Export filtered data to CSV
    csv = invoice_lines_from_pandas.to_csv(index=False).encode('utf-8')

    # Create export button
    st.download_button(
        label="Export filtered data to CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )

# page: Adyen links
elif page == page3:
    st.title(page3)

    # Run the query automatically on page load
    # data = get_PaymentLinks()

    # Create 3 columns for the filters
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        merchant_ref_filter = st.text_input('Search inside the Merchant Reference', '')


    # Apply filters on the data dynamically
    if merchant_ref_filter:
        # data = data[data["Merchant Reference"].astype(str).str.contains(merchant_ref_filter)]
        adyenlinks_from_pandas = adyenlinks_from_pandas[adyenlinks_from_pandas["merchantReference"].astype(str).str.contains(merchant_ref_filter)]
    # if client_filter:
    #     data = data[data['Client Contact Code'].astype(str).str.contains(client_filter)]
    # if animal_filter:
    #     data = data[data['Animal Code'].astype(str).str.contains(animal_filter)]

    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results test:")
    # st.dataframe(data.reset_index(drop=True), height=400)  # Removed index and compact height of 400px
    st.dataframe(adyenlinks_from_pandas.reset_index(drop=True), height=400)  # Removed index and compact height of 400px




