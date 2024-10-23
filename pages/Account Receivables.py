import streamlit as st
import functions


app_name=functions.set_page_definitition()

#----------------------------------------------------
# filepaths
#----------------------------------------------------
PaymentLinks = "data/paymentLinks-2024-10-22.csv"
XeroARreport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_Aged_Receivables_Detail.xlsx"
XeroPAYGrecReport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_PAYG_Reconciliation.xlsx"
eV_animals = "data/Animals-2024-10-23-13-51-41.csv"


#----------------------------------------------------
# Import Adyen links
#----------------------------------------------------

df1 = functions.load_adyen_links(PaymentLinks)

# Filter only PAYG links
df1 = df1[df1['Link Type'].str.contains('PAYG', na=True)]

# st.subheader("Adyen PAYG Payment Links - df1")
# st.write("Payment links related to failed subscription payments have been disregarded")
# st.dataframe(df1)
# st.write(len(df1))

#----------------------------------------------------
# Import Xero PAYG data
#----------------------------------------------------

st.subheader("Xero Accounts Receivables report")
df3 = functions.load_xero_AR_report(XeroARreport)
st.dataframe(df3)
# st.write(len(df3))

# st.subheader("All Xero PAYG invoices - df2")

df2 = functions.load_xero_PAYGrec_report(XeroPAYGrecReport)

# Update Status in df2 where Invoice Number exists in df3
df2.loc[df2['Invoice Number'].isin(df3['Invoice Number']), 'Status'] = 'Unpaid'

# Set Status to 'Paid' for rows where Invoice Number is not found in df3
df2.loc[~df2['Invoice Number'].isin(df3['Invoice Number']), 'Status'] = 'Paid'

# st.dataframe(df2)
# st.write(len(df2))






#----------------------------------------------------
# Merging tables
#----------------------------------------------------

# All PAYG links that are in both
in_both = df1.merge(df2, how='inner', left_on='id', right_on='Adyen Ref ID')
# st.subheader("merged data")
# st.dataframe(in_both)
# st.write(len(in_both))

# st.subheader("Easily matched (using payment link ID")

in_both_display = in_both[["Invoice Number",
                           "status", "Status", "Link Type", "creationDate",
                           "amount", "Description", "Customer ID", "Pet ID"]]
# st.dataframe(in_both_display)
# st.write(len(in_both_display))

# st.subheader("Only in Adyen")

df_not_in_df2 = df1.merge(df2, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
# st.dataframe(df_not_in_df2)
# st.write(len(df_not_in_df2))


#----------------------------------------------------
# Search for invoice details
#----------------------------------------------------


st.sidebar.subheader("Select an invoice")

# Create a text input to search by invoice id
# ar_invoice = st.sidebar.text_input('Enter Invoice ID:', '')

selected_ar_invoice = st.sidebar.selectbox('',
                                        df3["Invoice Number"].astype(str))
selected_contact_code = selected_ar_invoice.split(' - ')[0]
ar_invoice = selected_ar_invoice

# ar_invoice = "INV-6149"
# st.sidebar.subheader(ar_invoice)

# # Create a text input to search by Contact Code
# contact_code = st.sidebar.text_input('Enter Contact Code:', '')
#
# # Add a search box for First Name
# first_name = st.sidebar.text_input('Enter First Name:', '')
#
# # Add a search box for Last Name
# last_name = st.sidebar.text_input('Enter Last Name:', '')


#----------------------------------------------------
# Present all info for individual invoice
#----------------------------------------------------

if ar_invoice:
    # Payment link data
    ar_xero_status = df2.loc[df2['Invoice Number'] == ar_invoice, 'Status'].iloc[0]
    # st.write("Xero status: " + ar_xero_status)

    ar_amount = df1.loc[df1['Invoice ID'] == ar_invoice, 'amount'].iloc[0]
    # st.write("Outstanding amount: " + ar_amount)

    ar_link_date = df1.loc[df1['Invoice ID'] == ar_invoice, 'creationDate'].iloc[0]
    # st.write("Link creation date: " + ar_link_date)

    ar_customer_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Customer ID'].iloc[0]
    # st.write("Customer ID: " + ar_customer_id)

    ar_paymentLink = df1.loc[df1['Invoice ID'] == ar_invoice, 'paymentLink'].iloc[0]
    # st.write("Payment Link: " + ar_paymentLink)

    ar_link_status = df1.loc[df1['Invoice ID'] == ar_invoice, 'status'].iloc[0]
    if ar_link_status == "completed":
        ar_link_status = "Paid"
    else:
        ar_link_status = f"Unpaid ({ar_link_status})"

    # st.write("Adyen status: " + ar_link_status)

    ar_pet_id = df1.loc[df1['Invoice ID'] == ar_invoice, 'Pet ID'].iloc[0]
    # st.write("Pet ID: " + ar_pet_id)

    pet_data = functions.get_pet_data(eV_animals)

    # Ensure both 'Animal Code' column and 'ar_pet_id' are of the same type
    pet_data['Animal Code'] = pet_data['Animal Code'].astype(str)
    ar_pet_id = str(ar_pet_id)

    # Now perform the lookups
    pet_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name'].iloc[0]

    # pet_name = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name'].iloc[0]
    # st.write(pet_name)


    ar_invoices = functions.get_invoices(ar_pet_id)
    # st.dataframe(ar_invoices)

    ar_first_name = ar_invoices.loc[ar_invoices['Animal Code'] == ar_pet_id, 'First Name'].iloc[0]
    ar_last_name = ar_invoices.loc[ar_invoices['Animal Code'] == ar_pet_id, 'Last Name'].iloc[0]

    # st.write(ar_first_name)
    # st.write(ar_last_name)


    st.header(f"{ar_invoice}: {ar_first_name} {ar_last_name} - {pet_name}")

    col1, col2, col3 = st.columns(3)

    # Add filters in separate columns
    with col1:
        st.markdown("##### Outstanding amount: " + ar_amount)


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




    with col2:
        st.markdown("##### Adyen Link: " + ar_paymentLink)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("##### All ezyVet invoices for " + pet_name)
        ar_invoices = ar_invoices.rename(columns={
            'Invoice #': 'Invoice ID',
            'Invoice Date': 'Invoice Date',
            'Client Contact Code': 'Customer ID',
            'First Name': 'First',
            'Last Name': 'Last',
            'Animal Code': 'Animal ID',
            'Animal Name': 'Animal',
            'Total Standard Price(incl)': 'Standard Price',
            'Total Discount Percentage': 'Discount (%)',
            'Total Discount Value': 'Discount Value',
            'Total Invoiced (incl)': 'Total Amount'
            })


        # Define a function to convert the Invoice ID to a hyperlink
        def create_hyperlink(invoice_id):
            # Use only the last 5 characters of the Invoice ID in the link
            record_id = invoice_id[-5:]
            # Generate the hyperlink
            return f"[{invoice_id}](https://gvak.euw1.ezyvet.com/?recordclass=Invoice&recordid={record_id})"


        # Create a new column with hyperlinks for the Invoice ID
        ar_invoices['Invoice Link'] = ar_invoices['Invoice ID'].apply(create_hyperlink)

        # Select specific columns for the output, including both original and hyperlink versions of the Invoice ID
        selected_columns = [
            # 'Invoice ID',  # Original Invoice ID with all 6 characters
            'Invoice Link',  # New hyperlink version of Invoice ID
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
            selected_invoice_id = ar_invoices['Invoice #'].values[0]

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






