import streamlit as st
import functions
import pandas as pd

app_name=functions.set_page_definitition()

# ----------------------------------------------------
# defining session states
# ----------------------------------------------------

functions.initialize_session_state()

selected_invoice_no = st.session_state.selected_invoice_no


#----------------------------------------------------
# Import Adyen links with
# extracted pet ID, Customer Id and
# Invoice ID where possible-               adyen_links
#----------------------------------------------------

adyen_links = functions.load_adyen_links()

# Filter only PAYG links
adyen_links = adyen_links[adyen_links['Link Type'].str.contains('PAYG', na=True)]

# st.subheader("Adyen PAYG Payment Links - adyen_links")
# st.write("Payment links related to failed subscription payments have been disregarded")
# st.dataframe(adyen_links)
# st.write(len(adyen_links))

#----------------------------------------------------
# Import Xero AR data plus Adyen link details
# merged in from adyen_links above-                    xero_ar_data
#----------------------------------------------------

xero_ar_data, ar_date = functions.load_xero_AR_report()

# st.dataframe(xero_ar_data)
# st.write(len(xero_ar_data))

# Merge xero_payg_invoices into xero_ar_data based on matching columns
xero_ar_data = xero_ar_data.merge(adyen_links, left_on='Invoice Reference', right_on='id', how='left').set_index(xero_ar_data.index)

# st.subheader("Xero AR Report for RAmona - xero_ar_data")
# st.dataframe(xero_ar_data)
# st.dataframe(xero_ar_data[['Invoice ID', 'Invoice Date','< 1 Month', '1 Month', '2 Months', '3 Months', 'Older', 'Total', "Adyen Status"]])
# st.write(len(xero_ar_data))

#----------------------------------------------------
# Import Xll Xero PAYG invoices - xero_payg_invoices
#----------------------------------------------------

xero_payg_invoices = functions.load_xero_PAYGrec_report()

# Use xero_ar_data.index instead of xero_ar_data['Invoice Number']
xero_payg_invoices.loc[xero_payg_invoices['Invoice Number'].isin(xero_ar_data.index), 'Status'] = 'Unpaid'

# Use xero_ar_data.index instead of xero_ar_data['Invoice Number']
xero_payg_invoices.loc[~xero_payg_invoices['Invoice Number'].isin(xero_ar_data.index), 'Status'] = 'Paid'

# st.subheader("Import Xll Xero PAYG invoices - xero_payg_invoices")
# st.dataframe(xero_payg_invoices)
# st.write(len(xero_payg_invoices))




#----------------------------------------------------
# Merging tables (PAYG details into Adyen Links table)
#----------------------------------------------------

# All PAYG links that are in both
in_both = adyen_links.merge(xero_payg_invoices, how='inner', left_on='id', right_on='Adyen Ref ID')


# st.subheader("merged data")
# st.dataframe(in_both)
# st.write(len(in_both))

# st.subheader("Easily matched (using payment link ID")

in_both_display = in_both[["Invoice Number",
                           "Adyen Status", "Status", "Link Type", "creationDate",
                           "amount", "Description", "Customer ID", "Pet ID"]]
# st.dataframe(in_both_display)
# st.write(len(in_both_display))

# st.subheader("Only in Adyen")

df_not_in_xero_payg_invoices = adyen_links.merge(xero_payg_invoices, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
# st.dataframe(df_not_in_xero_payg_invoices)
# st.write(len(df_not_in_xero_payg_invoices))


#----------------------------------------------------
# Present AR report to user and select invoice to investigate
#----------------------------------------------------

st.header(f"Xero Aged Receivables ({ar_date})")
st.info("This table shows all unsettled debt in Xero where the Adyen link is either still active or has expired. This debt is likely to not have been settled. "
        "For cases where Xero is not correctly updated and is not aware of debt having been paid, go to the Xero not up to Date page.")

link_still_active = (xero_ar_data['Adyen Status'] != "completed")

xero_ar_data = xero_ar_data[link_still_active]
# st.dataframe(xero_ar_data)
ar_invoice_id = ()
selection = st.dataframe(xero_ar_data[['Invoice Number', 'Invoice ID', 'Invoice Date',
                                  '< 1 Month', '1 Month', '2 Months',
                                  '3 Months', 'Older', 'Total', "Adyen Status", "Customer ID", "Pet ID"]],
                         on_select="rerun", selection_mode="single-row")
# Display the selected row(s)
if selection:
    # st.write("Selected rows:", selection)
    # Extract the selected row indices
    selected_row = selection["selection"]["rows"]
    # st.write(selected_row)

    # Extract data from the selected rows
    selected_invoices = xero_ar_data.iloc[selected_row]["Invoice Number"].values[0]
    ar_invoice_id = selected_invoices
    st.session_state.selected_invoices = selected_invoices
    ar_customer_id = xero_ar_data.iloc[selected_row]["Customer ID"].values[0]
    ar_pet_id = xero_ar_data.iloc[selected_row]["Pet ID"].values[0]


    st.header(ar_invoice_id)
    st.header(ar_customer_id)
    st.header(ar_pet_id)

    if pd.isna(ar_customer_id):
        st.header("No Customer ID")
        st.warning("Please choose an invoice where the Customer ID is not empty")
        ar_merchant_reference = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'merchantReference'].iloc[0]
        ar_customer_id = st.text_input(
        "Please enter a Customer ID manually " + ar_merchant_reference)

    elif ar_customer_id == "":
        st.header("No Customer ID")
        st.warning("Please choose an invoice where the Customer ID is not empty")
        ar_merchant_reference = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'merchantReference'].iloc[0]
        ar_customer_id = st.text_input(
        "Please enter a Customer ID manually " + ar_merchant_reference)

    else:
        ar_invoice_id = selected_invoices

#----------------------------------------------------
# Present all info for individual invoice
#----------------------------------------------------

    st.dataframe(xero_ar_data)

    if ar_invoice_id:

        # ----------------------------------------------------
        # Prepare all details for the selected AR invoice
        # ----------------------------------------------------

        ar_merchant_reference = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'merchantReference'].iloc[0]

        # Payment link data
        ar_xero_status = "Unpaid"
        # st.write("Xero status: " + ar_xero_status)

        ar_amount = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'amount'].iloc[0]
        # st.write("Outstanding amount: " + ar_amount)

        ar_link_date = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'creationDate'].iloc[0]
        # st.write("Link creation date: " + ar_link_date)

        ar_paymentLink = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'paymentLink'].iloc[0]
        # st.write("Payment Link: " + ar_paymentLink)

        ar_link_status = xero_ar_data.loc[xero_ar_data['Invoice ID'] == ar_invoice_id, 'Adyen Status'].iloc[0]
        if ar_link_status == "completed":
            ar_link_status = "Paid"
        else:
            ar_link_status = f"Unpaid ({ar_link_status})"

        ar_pet_id = str(ar_pet_id)

        # Collect data about the pet from eV
        pet_data = functions.get_ezyvet_pet_details(ar_pet_id)
        # st.dataframe(pet_data)

        # Now perform the lookups
        ar_pet_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name'].iloc[0]
        ar_first_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Owner First Name'].iloc[0]
        ar_last_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Owner Last Name'].iloc[0]

        st.header(f"{ar_invoice_id}: {ar_first_name} {ar_last_name} - {ar_pet_name}")

        col1, col2, col3 = st.columns(3)

        # Add filters in separate columns
        with col1:
            st.markdown("##### Outstanding amount: " + ar_amount)
            st.markdown("##### Customer ID: " + ar_customer_id)
            st.markdown("##### Pet ID: " + ar_pet_id)

        with col2:
            st.markdown("##### Adyen Link: " + ar_paymentLink)

        with col3:
            if ar_xero_status == "Unpaid" and ar_link_status == "Paid":
                ar_xero_status_formatted = f"<span style='color:red; font-weight:bold;'>{ar_xero_status}</span>"
                st.markdown("##### Xero status:    " + ar_xero_status_formatted, unsafe_allow_html=True)
                st.markdown("##### Adyen status: " + ar_link_status)
                notification = "Xero is not correctly updated"
                st.info(notification)
                st.button("Do something about it")
            else:
                ar_xero_status_formatted = ar_xero_status
                st.markdown("##### Xero status: " + ar_xero_status_formatted, unsafe_allow_html=True)
                st.markdown("##### Adyen status: " + ar_link_status)

        st.markdown("---")

        st.markdown("##### All ezyVet invoices for " + ar_pet_name)

        selected_invoices = functions.extract_tl_Invoices(pet_id=ar_pet_id)
        functions.rename_tl_columns(selected_invoices)
        st.dataframe(selected_invoices)



        #
        # # Define a function to convert the Invoice ID to a hyperlink
        # def create_hyperlink(invoice_id):
        #     # Use only the last 5 characters of the Invoice ID in the link
        #     record_id = invoice_id[-5:]
        #     # Generate the hyperlink
        #     return f"[{invoice_id}](https://gvak.euw1.ezyvet.com/?recordclass=Invoice&recordid={record_id})"


        # # Create a new column with hyperlinks for the Invoice ID
        # ar_invoices['Invoice Link'] = ar_invoices['Invoice ID'].apply(create_hyperlink)

        # Select specific columns for the output, including both original and hyperlink versions of the Invoice ID
        selected_columns = [
            'Invoice ID',  # Original Invoice ID with all 6 characters
            # 'Invoice Link',  # New hyperlink version of Invoice ID
            'Invoice Date',
            'Total Amount'
        ]

        # Create a new DataFrame with only the selected columns
        ar_invoices_subset = ar_invoices[selected_columns]
        st.markdown(ar_invoices_subset.to_markdown(index=False), unsafe_allow_html=True)


        with col2:
            if len(ar_invoices)>1:
                st.markdown("##### Select Invoice ID ")
                selected_invoice_id = st.radio("", ar_invoices['Invoice ID'], horizontal=False)
            else:
                selected_invoice_id = ar_invoices['Invoice ID'].values[0]

        st.markdown("---")

        st.write(f"### Details for Invoice no.: {selected_invoice_id}")


        ar_invoice_lines = functions.get_invoiceDetails(selected_invoice_id)

        ar_invoice_lines.rename(columns={
            'Invoice Line ID': 'Line ID',
            'Product Name': 'Product',
            'Standard Price(incl)': 'Price',
            'DiscountPercentage': 'Discount [%]',
            'DiscountValue': 'Discount [£]',
            'Total Invoiced (incl)': 'Total Amount',
            'Discount Name': 'Discount description'
        }, inplace=True)


        st.markdown(ar_invoice_lines.to_markdown(index=False), unsafe_allow_html=True)






