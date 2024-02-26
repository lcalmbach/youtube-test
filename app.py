import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from pytube import YouTube
import os
from streamlit_player import st_player

__version__ = '0.0.1'
__author__ = 'lukas.calmbach@bs.ch'

SAVE_DIR = './docs/youtube/'
if 'url' not in st.session_state:
    st.session_state['url'] = 'https://youtu.be/cfLrQZVpNWg?si=8wSsJQ26_SrNWwk0'
    st.session_state['text'] = None
url = st.text_input('Gib eine Youtube Video URL ein', st.session_state['url'])
if url != st.session_state['url']:
    st.session_state['url'] = url
    st.session_state['text'] = None
if st.session_state['url'] is not None:
    yt = YouTube(st.session_state['url'])
    st_player(st.session_state['url'])

if st.button('Transkribiere Video'):
    with st.spinner(f'Transcribing "{yt.title}"...'):
        loader = GenericLoader(
            YoutubeAudioLoader([url], SAVE_DIR),
            OpenAIWhisperParser()
        )
        docs = loader.load()
        st.session_state['text'] = ' '.join([page.page_content for page in docs])
        with open(os.path.join(SAVE_DIR, yt.title + '.txt'), 'w', encoding='utf8') as file:
            file.write(st.session_state['text'])
        st.success(f'Transkription für "{yt.title}" ist komplett.')

if st.session_state['text'] is not None:
    st.write(st.session_state['text'])
    st.download_button('Datei herunterladen', st.session_state['text'], f'{yt.title}.txt')