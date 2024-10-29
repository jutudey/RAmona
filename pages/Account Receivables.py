import streamlit as st
import functions

app_name=functions.set_page_definitition()

#----------------------------------------------------
# filepaths
#----------------------------------------------------
PaymentLinks = "data/paymentLinks-2024-10-29.csv"
XeroARreport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_AR_Report_for_Ramona.xlsx"
XeroPAYGrecReport = "data/Education___Clinical_Research___Innovation_Group_Limited_-_PAYG_Reconciliation.xlsx"
eV_animals = "data/Animals-2024-10-23-13-51-41.csv"

#----------------------------------------------------
# Import Adyen links - df1
#----------------------------------------------------

df1 = functions.load_adyen_links(PaymentLinks)

# Filter only PAYG links
df1 = df1[df1['Link Type'].str.contains('PAYG', na=True)]

# st.subheader("Adyen PAYG Payment Links - df1")
# st.write("Payment links related to failed subscription payments have been disregarded")
# st.dataframe(df1)
# st.write(len(df1))

#----------------------------------------------------
# Import Xero AR data - df3
#----------------------------------------------------

df3 = functions.load_xero_AR_report(XeroARreport)

# st.dataframe(df3)

# Merge df2 into df3 based on matching columns
df3 = df3.merge(df1, left_on='Invoice Reference', right_on='id', how='left').set_index(df3.index)

# If you don't need the 'id' column from df2 in df3, you can drop it
# df3.drop('id', axis=1, inplace=True)

# st.dataframe(df3)
# st.dataframe(df3[['Invoice ID', 'Invoice Date','< 1 Month', '1 Month', '2 Months', '3 Months', 'Older', 'Total', "Adyen Status"]])
# ])
# st.write(len(df3))

#----------------------------------------------------
# Import Xll Xero PAYG invoices - df2
#----------------------------------------------------

# st.subheader("All Xero PAYG invoices - df2")

df2 = functions.load_xero_PAYGrec_report(XeroPAYGrecReport)



# Use df3.index instead of df3['Invoice Number']
df2.loc[df2['Invoice Number'].isin(df3.index), 'Status'] = 'Unpaid'

# Use df3.index instead of df3['Invoice Number']
df2.loc[~df2['Invoice Number'].isin(df3.index), 'Status'] = 'Paid'


# st.dataframe(df2)
# st.write(len(df2))




#----------------------------------------------------
# Merging tables (PAYG details into Adyen Links table)
#----------------------------------------------------

# All PAYG links that are in both
in_both = df1.merge(df2, how='inner', left_on='id', right_on='Adyen Ref ID')
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

df_not_in_df2 = df1.merge(df2, left_on='id', right_on='Adyen Ref ID', how='left', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
# st.dataframe(df_not_in_df2)
# st.write(len(df_not_in_df2))


#----------------------------------------------------
# Present AR report to user and select invoice to investigate
#----------------------------------------------------

st.header("Xero Aged Receivables")
st.info("This table shows all unsettled debt in Xero where the Adyen link is either still active or has expired. This debt is likely to not have been settled. "
        "For cases where Xero is not correctly updated and is not aware of debt having been paid, please click [here](http://localhost:8501/Xero_not_up_to_date)'.")

link_still_active = (df3['Adyen Status'] != "completed")

df3 = df3[link_still_active]
# st.dataframe(df3)
ar_invoice_id = ()
selection = st.dataframe(df3[['Invoice Number','Invoice ID', 'Invoice Date',
                                  '< 1 Month', '1 Month', '2 Months',
                                  '3 Months', 'Older', 'Total', "Adyen Status", "Customer ID", "Pet ID"]],
                             on_select="rerun", selection_mode="single-row")
# Display the selected row(s)
if selection:
    # st.write("Selected rows:", selection)
    # Extract the selected row indices
    selected_rows = selection["selection"]["rows"]
    # st.write(selected_rows)
    # Extract the Invoice # from the selected rows
    selected_invoices = df3.iloc[selected_rows]["Invoice Number"].values

    # Print each selected invoice
    for selected_invoice in selected_invoices:
        # st.write("Selected Invoice #:", selected_invoice)
        ar_invoice_id = selected_invoice
        print('extracted from selection table' + ar_invoice_id)


#----------------------------------------------------
# Present all info for individual invoice
#----------------------------------------------------
if selection:
    if ar_invoice_id:
        try:
            # Attempt to retrieve Customer ID from df3
            ar_customer_id = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'Customer ID'].iloc[0]
            print("Customer Id is found " + ar_customer_id)
        except IndexError:
            # If no match is found, set Customer ID to an empty string
            print("Customer id is NOT found")
            ar_customer_id = ""

        # Check if Customer ID is empty
        if ar_customer_id == "":
            ar_merchant_reference = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'merchantReference'].iloc[0]
            print(ar_merchant_reference)
            print("Requesting Customer ID in GUI")
            ar_pet_id = st.text_input("The description in the Adyen Payment Link is not enough to enable us to identify the Customer and Pet. Please check the description that was provided and see if you can add the Pet ID manually. " + ar_merchant_reference)

            # Stop execution until the input is provided
            if not ar_pet_id:
                # st.warning("Please provide a Pet ID to proceed.")
                st.stop()


        # Payment link data
        ar_xero_status = "Unpaid"
        # st.write("Xero status: " + ar_xero_status)

        ar_amount = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'amount'].iloc[0]
        # st.write("Outstanding amount: " + ar_amount)

        ar_link_date = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'creationDate'].iloc[0]
        # st.write("Link creation date: " + ar_link_date)

        ar_paymentLink = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'paymentLink'].iloc[0]
        # st.write("Payment Link: " + ar_paymentLink)

        ar_link_status = df3.loc[df3['Invoice ID'] == ar_invoice_id, 'Adyen Status'].iloc[0]
        if ar_link_status == "completed":
            ar_link_status = "Paid"
        else:
            ar_link_status = f"Unpaid ({ar_link_status})"

        print("Adyen status: " + ar_link_status)
        print("invoice id: " + ar_invoice_id)




        ar_pet_id = df1.loc[df1['Invoice ID'] == ar_invoice_id, 'Pet ID'].iloc[0]
        print("Pet Id: " + ar_pet_id)


        try:
            # Attempt to retrieve Customer ID from df1
            ar_pet_id = df1.loc[df1['Invoice ID'] == ar_invoice_id, 'Pet ID'].iloc[0]
        except IndexError:
            # If no match is found, set Pet ID to an empty string
            ar_pet_id = ""

        # Check if Customer ID is empty
        if not ar_pet_id:

            # Prompt user to enter the Customer ID manually
            # st.sidebar.write(f"You also have to enter the Pet ID")

            ar_pet_id_newish = st.sidebar.text_input("Please enter an ezyVet Pet Id", key='customer_id_input')


        pet_data = functions.get_pet_data(eV_animals)

        # Ensure both 'Animal Code' column and 'ar_pet_id' are of the same type
        pet_data['Animal Code'] = pet_data['Animal Code'].astype(str)
        ar_pet_id = str(ar_pet_id)

        # Now perform the lookups
        result = pet_data.loc[pet_data['Animal Code'] == ar_pet_id, 'Animal Name']
        if not result.empty:
            ar_pet_name = result.iloc[0]
        else:
            ar_pet_name = None
            st.info(f"Pet with Pet ID {ar_pet_id} not found in ezyVet data")# or assign a default value, e.g., 'Unknown'

        # st.write(ar_pet_name)

        # st.write(ar_pet_id)
        try:
            ar_invoices = functions.get_invoices(ar_pet_id)

            ar_first_name = ar_invoices.loc[ar_invoices['Animal Code'] == ar_pet_id, 'First Name'].iloc[0]
            ar_last_name = ar_invoices.loc[ar_invoices['Animal Code'] == ar_pet_id, 'Last Name'].iloc[0]


        except IndexError:
            # If no match is found, set Customer ID to an empty string
            print("No invoice is NOT found")
            st.warning("No invoice is found for this pet. Please ensure that you have the latest version of the Invoice export from ezyVet")

        # st.dataframe(ar_invoices)

        # st.write(ar_first_name)
        # st.write(ar_last_name)


        st.header(f"{ar_invoice_id}: {ar_first_name} {ar_last_name} - {ar_pet_name}")

        col1, col2, col3 = st.columns(3)

        # Add filters in separate columns
        with col1:
            st.markdown("##### Outstanding amount: " + ar_amount)
            st.markdown("##### Customer ID: " + ar_customer_id)
            st.markdown("##### Pet ID: " + ar_pet_id)


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
            st.markdown("##### All ezyVet invoices for " + ar_pet_name)
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






