import time

import streamlit as st
import os
import pandas as pd
from datetime import datetime
import functions

# Set page name or title
app_name = functions.set_page_definitition()

# Directory to store uploaded files
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Helper function to list files
def list_files():
    files = [f for f in os.listdir(data_folder) if f not in ['.DS_Store', '.ipynb_checkpoints'] and not f.endswith('.ipynb')]
    file_data = []
    for file in files:
        file_path = os.path.join(data_folder, file)
        if os.path.isfile(file_path):
            # num_lines = sum(1 for line in open(file_path)) if file.endswith(".csv") else 'N/A'
            upload_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            file_data.append((file, upload_time))
    return pd.DataFrame(file_data, columns=["File Name", "Upload Date"]) if file_data else None

# Two-column layout
left_column, right_column = st.columns([1, 1])

# List of Files in the left column
with right_column:
    st.header("Files in Data Folder")
    file_df = list_files()
    # selected_file = None
    if file_df is not None:
        file_df = file_df.sort_values(by="Upload Date", ascending=False)
        st.dataframe(file_df, height=500, use_container_width=True, hide_index=True)
        # try:
        #     selected_file = functions.multi_selectbox(file_df, 'File Name', height=650)
        # except IndexError:
        #     pass
    else:
        st.write("No files uploaded yet.")

    if st.button("Refresh Filelist"):
        selected_file = None
        st.rerun()


# File Upload in the right column
with right_column:
    st.header("Upload New File")
    uploaded_files = st.file_uploader("Choose CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(data_folder, uploaded_file.name)
            if os.path.exists(file_path):
                os.remove(file_path)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success("Files uploaded successfully!")
        # st.session_state['rerun_trigger'] = True
        if st.button("Refresh Ramona Filelist"):
            st.rerun()
        if st.button("Process new files"):
            st.session_state.tl = None
            st.session_state.all_invoice_lines = None
            st.session_state.adyenlinks = None
            functions.initialize_session_state()


if 'rerun_trigger' in st.session_state:
    del st.session_state['rerun_trigger']

# # File Delete Functionality
# with right_column:
#     st.divider()
#     if selected_file:
#         st.header("Delete Files")
#         if st.button("Delete " + selected_file):
#             os.remove(os.path.join(data_folder, selected_file))
#             st.success(f"File '{selected_file}' deleted successfully!")
#             time.sleep(1)

with left_column:
    st.header('Required Files')
    st.write('In order to work properly Ramona needs up-to-date versions of the following files:')

    st.subheader('ezyVet Invoice Lines')
    st.write('File name prefix: "Invoice Lines Report"')
    st.write('Newest file uploaded: ' + str(functions.get_newest_filename('Invoice Lines Report-')))
    with st.expander('Where to find the file', expanded=False):
        st.write('Go to ezyVet https://gvak.euw1.ezyvet.com/?recordclass=Reporting&recordid=0')
        st.write('and click on "Invoice Lines Report" in the File column')

    st.subheader('ezyVet Animals Report')
    st.write('File name prefix: "Animals Report"')
    st.write('Newest file uploaded: ' + str(functions.get_newest_filename('Animals Report-')))
    with st.expander('Where to find the file', expanded=False):
        st.write('Go to ezyVet https://gvak.euw1.ezyvet.com/?recordclass=Reporting&recordid=0')
        st.write('and click on "Animals Report" in the File column')

    st.subheader('ezyVet Wellness Plan Report')
    st.write('File name prefix: "WellnessPlanMembership_Export"')
    st.write('Newest file uploaded: ' + str(functions.get_newest_filename('WellnessPlanMembership_Export')))
    with st.expander('Where to find the file', expanded=False):
        st.write('Go to ezyVet https://gvak.euw1.ezyvet.com/#')
        st.write('- Click on the yellow "Dashboard" tab \n'
                 '- Click on the Records tab \n'
                 '- Under Saved Filters click on Global \n'
                 '- Choose "WellnessPlanMemberships - Recently Modified"  \n'
                 '- Click Show Records and scroll to the bottom \n'
                 '- Click on "All" \n'
                 '- Choose "Export - Wellness Memberships" and click Action \n'
                 '- Click Get CSV \n'
                 '- Upload the file here')

    st.subheader('VERA Payment History')
    st.write('File name prefix: "payment-history-"')
    st.write('Newest file uploaded: ' + str(functions.get_newest_filename('payment-history-')))
    with st.expander('Where to find the file', expanded=False):
        st.write('Go to VERA Toolbox https://app.gardenvets.com/adad4b9d-8ad5-4ef4-9f3f-7916b0850882/reports/report-list')
        st.write('and click on "Payment History" in the File column')

    st.subheader('VERA Adyen Payment Links')
    st.write('File name prefix: "payment-history-"')
    st.write('Newest file uploaded: ' + str(functions.get_newest_filename('payment-history-')))
    with st.expander('Where to find the file', expanded=False):
        st.write(
            'Go to VERA Toolbox https://app.gardenvets.com/adad4b9d-8ad5-4ef4-9f3f-7916b0850882/reports/report-list')
        st.write('and click on "Payment History" in the File column')
