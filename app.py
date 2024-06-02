import time
import requests
import streamlit as st
from backend.lang_options import language_dict, language_list


st.title("AutoSTTop")
st.write("Transcribe WAV audio files with MMS-STT")


# === USER INPUT ===
option_lang = st.selectbox(
    "What language would you like to transcribe?",
    ([x for x in language_list]))

file_uploader = st.file_uploader("Select an audio file", type=["wav"])


# === INTERPRETING VALUES ===
language_code = language_dict.get(option_lang, "eng")


# === REQUEST TO STT ENDPOINT ===
if file_uploader:
    start = time.time()

    with st.spinner('Loading...'):
        url = f"http://localhost:8000/stt?lang_code={language_code}"
        files = {"wav_file": file_uploader}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        transcription_results = response.json()["transcription"]
    
        conversation = " "
        for result in transcription_results:
            conversation += result

        st.success("Transcription successful!")
        st.write(conversation)

        end = time.time()
        st.write("Time taken:", end-start)
            
    else:
        st.write("Error:", response.text)
