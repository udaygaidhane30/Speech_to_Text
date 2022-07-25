# Libraries to be used ------------------------------------------------------------

import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="Speech to Text Transcription App", page_icon="🗣️")

st.text("")

st.title("Speech to text transcription app")

st.write(
    """  
-   Upload a wav file, transcribe it, then export it to a text file!
	"""
)

st.text("")

c1, c2, c3 = st.columns([1, 4, 1])

with c2:
    with st.form(key="my_form"):
        f = st.file_uploader("", type=[".wav"])

        st.info(
            f"""
                    👆 Upload a .wav file.
                    """
        )

        submit_button = st.form_submit_button(label="Transcribe")

if f is not None:
    st.audio(f, format="wav")
    path_in = f.name
    old_file_position = f.tell()
    f.seek(0, os.SEEK_END)
    getsize = f.tell()
    f.seek(old_file_position, os.SEEK_SET)
    getsize = round((getsize / 1000000), 1)

    if getsize < 5:  # File more than 5 MB
        # To read file as bytes:
        bytes_data = f.getvalue()

        # Load your API key from an environment variable
        api_token = st.secrets["api_token"]

        # endregion API key
        headers = {"Authorization": f"Bearer {api_token}"}
        API_URL = (
            "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
        )


        def query(data):
            response = requests.request("POST", API_URL, headers=headers, data=data)
            return json.loads(response.content.decode("utf-8"))


        # st.audio(f, format="wav")
        data = query(bytes_data)

        values_view = data.values()
        value_iterator = iter(values_view)
        text_value = next(value_iterator)
        text_value = text_value.lower()

        st.info(text_value)

        c0, c1 = st.columns([2, 2])

        with c0:
            st.download_button(
                "Download the transcription",
                text_value,
                file_name=None,
                mime=None,
                key=None,
                help=None,
                on_click=None,
                args=None,
                kwargs=None,
            )

    else:
        st.warning(
            "🚨 We've limited to 5MB files. Please upload a smaller file."
        )
        st.stop()


else:
    path_in = None
    st.stop()
