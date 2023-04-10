# Snowpark for Python Developer Guide: https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html
# Streamlit docs: https://docs.streamlit.io/
# OpenAI: https://openai.com/

import pandas as pd
from snowflake.snowpark.session import Session
import streamlit as st
import base64
import openai
import os
import uuid
import config

# Retrieve OpenAI key from environment variable
openai.api_key = config.OPENAI_API_KEY

# Streamlit config
st.set_page_config(
    page_title="Speech Emotion Recognition app in Snowflake",
    layout='wide',
    menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "The source code for this application can be accessed on GitHub <URL>"
     }
)


# Set page title, header and links to docs
st.header("Speech Recognition app in Snowflake using Snowpark Python, NRCLex, Streamlit and OpenAI")
st.caption(f"App developed by [Divyansh](https://www.linkedin.com/in/divyanshsaxena/)")
st.write("[Resources: [Snowpark for Python Developer Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html)   |   [Streamlit](https://docs.streamlit.io/)   |   [OpenAI](https://openai.com/)]")

# Function to create new or get existing Snowpark session
def create_session():
    if "snowpark_session" not in st.session_state:
        session = Session.builder.configs(config.sf_conn_config).create()
        st.session_state['snowpark_session'] = session
    else:
        session = st.session_state['snowpark_session']
    return session

# Call function to create new or get existing Snowpark session to connect to Snowflake
session = create_session()
upload_path = "upload_path/"

st.markdown("""---""")
uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, label_visibility='hidden')


if uploaded_file is not None:
    file_name = uploaded_file.name
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path,file_name),"wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Processing Audio ... 💫"):
        session.file.put("file://"+upload_path+file_name, "@raw_data_set/audios/",auto_compress =False, overwrite = True)
        import os
        import openai
        audio_file = open(upload_path+file_name, "rb")
        audio_file1 = open(upload_path+file_name, "rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        transcribe = openai.Audio.transcribe("whisper-1", audio_file1)
        st.write(transcript.text)
        st.write(transcribe.text)
    st.write("File Loaded on Snowflake ")
