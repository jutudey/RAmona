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
with left_column:
    st.header("Files in Data Folder")
    file_df = list_files()
    selected_file = None
    if file_df is not None:
        try:
            selected_file = functions.multi_selectbox(file_df, 'File Name', height=650)
        except IndexError:
            pass
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
        if st.button("Refresh Filelist"):
            st.rerun()
        if st.button("Process new files"):
            st.session_state.tl = None
            st.session_state.all_invoice_lines = None
            st.session_state.adyenlinks = None
            functions.initialize_session_state()


if 'rerun_trigger' in st.session_state:
    del st.session_state['rerun_trigger']

# File Delete Functionality
with right_column:
    st.divider()
    if selected_file:
        st.header("Delete Files")
        if st.button("Delete " + selected_file):
            os.remove(os.path.join(data_folder, selected_file))
            st.success(f"File '{selected_file}' deleted successfully!")
            time.sleep(1)

with right_column:
    st.header('Required Files')
    st.write('In order to work Ramona needs as up to date versions of the following files:')
    st.subheader('ezyVet Invoice Lines')


