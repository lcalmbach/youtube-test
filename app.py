import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from pytube import YouTube
import os

save_dir="./docs/youtube/"
url = st.text_input("Enter the URL of the YouTube video")

if st.button("Transcribe"):
    yt = YouTube(url)
    with st.spinner(f"Transcribing '{yt.title}'..."):
        loader = GenericLoader(
            YoutubeAudioLoader([url], save_dir),
            OpenAIWhisperParser()
        )
        docs = loader.load()
        st.write(docs[0].page_content)
        text = ' '.join([page.page_content for page in docs])
        st.write(text)
        with open(os.path.join(save_dir, yt.title + '.txt'), "w") as file:
            file.write(text)
        st.success(f"Transcription of '{yt.title}' complete.")