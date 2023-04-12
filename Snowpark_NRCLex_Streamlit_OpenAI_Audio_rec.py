# Snowpark for Python Developer Guide: https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html
# Streamlit docs: https://docs.streamlit.io/
# OpenAI: https://openai.com/

import pandas as pd
from snowflake.snowpark.session import Session
import streamlit as st
import openai
import os
import uuid
import config
from nrclex import NRCLex        
# Retrieve OpenAI key from environment variable
openai.api_key = config.OPENAI_API_KEY

# Streamlit config
st.set_page_config(
    page_title="Speech Emotion Recognition app in Snowflake",
    layout='wide',
    page_icon="musical_note",
    menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "The source code for this application can be accessed on GitHub <URL>"
     }
)


# Set page title, header and links to docs
st.header("🗣 Speech Recognition app in Snowflake using Snowpark Python, NRCLex, Streamlit and OpenAI✨")
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
st.subheader("Upload The Audio File Below")
uploaded_file = st.file_uploader("Choose an image file", accept_multiple_files=False, label_visibility='hidden')

if uploaded_file is not None:
    file_name = uploaded_file.name
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path,file_name),"wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Processing Audio ... 💫"):
        #UPLOADING AUDIO FILE ON SNOWFLAKE STAGE
        session.file.put("file://"+upload_path+file_name, "@raw_data_set/audios/",auto_compress =False, overwrite = True)
        
        #GENERATING TRANSCRIPTS AND TRANSCRIBES FOR THE AUDIO FILE WHICH WE HAVE UPLOADED
        audio_file = open(upload_path+file_name, "rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        txt_transcript = transcript.text
        audio_file1 = open(upload_path+file_name, "rb")
        transcribe = openai.Audio.transcribe("whisper-1", audio_file1)
        txt_transcribe = transcribe.text
        st.title("Generated Transcript 📜")
        st.write(txt_transcript)
        st.title("Generated Original Audio Text 🔊")
        st.write(txt_transcribe)

        #USING NRCLex TO EXTRACT THE EMOTIONS FROM THE AUDIO FILE
        emotion = NRCLex(txt_transcript)
        df = pd.DataFrame(emotion.top_emotions,columns=["Sentiment", "Score"])
        st.title("Emotion/Sentiment Analysis From Audio File 🙂")
        st.dataframe(df)

        #USING SNOWPARK PYTHON TO LOAD THE DATA INTO SNOWFLAKE TABLE
        clean_file_name = file_name.replace(".","_").replace(" ","_")
        rec_uuid = clean_file_name+'_'+ str(uuid.uuid4())
        json_sentiment_score = df.to_json(orient="records")
        load_df = pd.DataFrame({"UUID":[rec_uuid],"FILE_NAME":[file_name],"AUDIO_TRANSCRIPT":[txt_transcript],"AUDIO_TRANSCRIBE":[txt_transcribe],"SENTIMENT_SCORE":[json_sentiment_score]})
        session.write_pandas(load_df, "TB_CUSTOMER_AUDIO_SENTIMENTS")
    
    st.markdown("""---""")
    st.write("Audio File Loaded on Snowflake...")
    st.write("Audio Analysis Uploaded on Snowflake...")
    sf_refresh_directory = session.sql('ALTER STAGE RAW_DATA_SET REFRESH;').collect()
    sf_exec_q = session.sql(f"select get_presigned_url(@raw_data_set, 'audios/{file_name}',604800);").collect()
    st.title("Get the Snowflake Audio URL Link - [Click]("+sf_exec_q[0][0]+")")