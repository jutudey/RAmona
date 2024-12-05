import streamlit as st
import functions


app_name = functions.set_page_definitition()

if not functions.check_password():
    st.stop()  # Do not continue if check_password is not True.


# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

with st.spinner('Loading and preparing data...'):
    print('Initialising Session state...')
    functions.initialize_session_state()
    print('Session state initialised')

if st.button("Process all files"):
    with st.spinner('Loading and preparing data...'):
    # st.session_state.tl = None
    # st.session_state.all_invoice_lines = None
    # st.session_state.adyenlinks = None
        st.session_state.tl = functions.build_tl()
        st.session_state.adyenlinks = functions.load_adyen_links()
        st.session_state.all_invoice_lines = functions.get_ev_invoice_lines()
        functions.initialize_session_state()

invoice_lines = st.session_state.all_invoice_lines
adyenlinks = st.session_state.adyenlinks
selected_invoice_no = st.session_state.selected_invoice_no

# ----------------------------------------------------
# Menu Structure
# ----------------------------------------------------


topPage = "Case Details by Invoice No."
page1 = "PAYG Invoice Lines"
page3 = "Adyen Links"


pages = [topPage, page1, page3]

# Streamlit app with sidebar navigation
st.sidebar.title(app_name)
page = st.sidebar.radio("Go to", pages)



# ----------------------------------------------------
# Individual Pages
# ----------------------------------------------------



# Case Details by Invoice ID
if page == topPage:
    st.title(topPage)

    # Create 3 columns
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        case_invoice_no = st.text_input('Invoice number', selected_invoice_no)


    if case_invoice_no:

        st.session_state.selected_invoice_no = case_invoice_no
          # collect invoice data
        invoice_lines = invoice_lines[(invoice_lines['Invoice #'] == case_invoice_no)]
        # st.dataframe(invoice_lines_from_pandas)
        invoice_lines.reset_index(drop=True, inplace=True)
        first_name = invoice_lines.loc[0, 'First Name']
        last_name = invoice_lines.loc[0, 'Last Name']
        pet_name = invoice_lines.loc[0, 'Animal Name']
        invoice_date = invoice_lines.loc[0, 'Invoice Date']
        customer_id = invoice_lines.loc[0, 'Client Contact Code']
        pet_id = invoice_lines.loc[0, 'Animal Code']
        invoice_no = invoice_lines.loc[0, 'Invoice #']

        if first_name and last_name:
            st.header(f"{first_name} {last_name} - {pet_name}")

            with col3:
                st.markdown(f"**Invoice Date:** {invoice_date}")
                st.markdown(f"**Customer ID:** {customer_id}")
                st.markdown(f"**Pet ID:** {pet_id}")
                st.markdown(f"**Invoice ID:** {invoice_no}")


            # Set height dynamically based on the number of rows
            num_rows = len(invoice_lines)
            height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown("#### Invoice Lines:")

            invoice_lines.reset_index(drop=True, inplace=True)
            invoice_lines_from_pandas_display = invoice_lines[['Invoice Line ID', 'Product Name', 'Standard Price(incl)', 'Discount(%)', 'Discount(£)', 'Total Invoiced (incl)', 'Discount Name']]
            st.markdown(invoice_lines_from_pandas_display.to_markdown(index=False), unsafe_allow_html=True)


            # Collect Payment Links Detaiils
            adyenlinks_from_pandas_display = adyenlinks[adyenlinks["Customer ID"] == customer_id]
            # st.dataframe(adyenlinks_from_pandas_display)
            adyenlinks_from_pandas_display = adyenlinks_from_pandas_display[['paymentLink', 'Adyen Status', 'merchantReference', 'Invoice ID', 'amount', 'creationDate', 'createdBy', 'shopperEmail', 'Link Type']]

            # st.dataframe(adyenlinks_from_pandas_display)


            # Set height dynamically based on the number of rows
            num_rows = len(adyenlinks)
            height = min(40 * num_rows + 50, 400)  # Adjust height: 40px per row, max height 400px for 10 rows

            # Display the filtered results in a scrollable dataframe, remove index column
            st.markdown(f"#### Adyen Links associated with this client:""")


            adyenlinks_from_pandas_display['paymentLink'] = adyenlinks_from_pandas_display['paymentLink'].apply(lambda x: f'[Link]({x})')
            st.markdown(adyenlinks_from_pandas_display.to_markdown(index=False), unsafe_allow_html=True)




        else:
            st.header("Invoice not found")

# Page: PAYG Invoice Lines
elif page == page1:
    st.title(page1)

    # Create 3 columns for the filters
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        selected_invoice_no = st.text_input('Filter by Invoice #', selected_invoice_no)

    with col2:
        client_filter = st.text_input('Filter by Client Contact Code', '')

    with col3:
        animal_filter = st.text_input('Filter by Animal Code', '')

    # Apply filters on the data dynamically
    if selected_invoice_no:
        st.session_state.selected_invoice_no = selected_invoice_no
        invoice_lines = invoice_lines[invoice_lines['Invoice #'].astype(str).str.contains(selected_invoice_no)]
    if client_filter:
        invoice_lines = invoice_lines[invoice_lines['Client Contact Code'].astype(str).str.contains(client_filter)]
    if animal_filter:
        invoice_lines = invoice_lines[invoice_lines['Animal Code'].astype(str).str.contains(animal_filter)]

    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results:")
    st.dataframe(invoice_lines.reset_index(drop=True), height=400)  # Removed index and compact height of 400px


    # Export filtered data to CSV
    csv = invoice_lines.to_csv(index=False).encode('utf-8')

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

    # Create 3 columns for the filters
    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        merchant_ref_filter = st.text_input('Search inside the Merchant Reference', '')


    # Apply filters on the data dynamically
    if merchant_ref_filter:
        adyenlinks = adyenlinks[adyenlinks["merchantReference"].astype(str).str.contains(merchant_ref_filter)]

    # Display the filtered results in a scrollable dataframe, remove index column
    st.write("Displaying filtered results test:")
    # st.dataframe(data.reset_index(drop=True), height=400)  # Removed index and compact height of 400px
    st.dataframe(adyenlinks.reset_index(drop=True), height=400)  # Removed index and compact height of 400px




