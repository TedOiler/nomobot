import streamlit as st
from nomobot_test import run_selenium_cycle
import pandas as pd
from datetime import datetime


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


st.set_page_config(
    page_title="Nomobot",
    page_icon='⚖️'
)

st.write(
    '<img width=100 src="https://em-content.zobj.net/thumbs/240/apple/325/robot_1f916.png" style="margin-left: 5px; brightness(1);">',
    unsafe_allow_html=True)
st.title("Nomobot")

if 'df' not in st.session_state:
    df = pd.DataFrame([])

data_expander = st.expander('Submitted Data', expanded=True)
data_expander_input, data_expander_output = data_expander.tabs(["Input Data", "Output Data"])

data_form_input = data_expander_input.form(key='input')
with data_form_input:
    uploaded_file = data_form_input.file_uploader("Upload data", type=['xlsx', 'csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=[0])
        except:
            df = pd.read_csv(uploaded_file, header=[0])
    else:
        df = None

submit_data_btn = data_form_input.form_submit_button("✅ Submit")

if submit_data_btn:
    data_expander_input.table(df)
    data_expander_input.download_button(label="📥 Export input data to CSV", data=convert_df(df),
                                        file_name=f'Input_data_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.csv',
                                        mime='text/csv')
    with st.spinner("Downloading Data"):
        data_out = run_selenium_cycle(data=df)
        data_expander_input.success("Data successfully scraped. \nCheck 'Output' tab.")

    data_expander_output.table(data_out)
    data_expander_output.download_button(label="📥 Export data to CSV", data=convert_df(data_out),
                                         file_name=f'Output_data_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.csv',
                                         mime='text/csv')
