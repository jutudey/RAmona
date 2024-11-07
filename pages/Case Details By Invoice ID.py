import streamlit as st
import functions

functions.set_page_definitition()

# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

functions.initialize_session_state()

invoice_lines = st.session_state.all_invoice_lines
adyenlinks = st.session_state.adyenlinks
selected_invoice_no = st.session_state.selected_invoice_no


# Create 3 columns
col1, col2, col3 = st.columns(3)

# Add filters in separate columns
with col1:
    case_invoice_no = st.text_input('Invoice number', selected_invoice_no)
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

