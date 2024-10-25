import streamlit as st
import pandas as pd
from pyarrow import input_stream
import functions

functions.set_page_definitition()

file_list_in_data = functions.list_all_files_in_data_folder()
st.write(file_list_in_data)