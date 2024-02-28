import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from pytube import YouTube
import os
from streamlit_player import st_player
import re
import shutil
import random

__version__ = "0.0.1"
__author__ = "lukas.calmbach@bs.ch"
SAVE_DIR = "./output/"
MP3_DIR = "./mp3/"

# demo urls
url_list = {
    "https://youtu.be/cfLrQZVpNWg?si=8wSsJQ26_SrNWwk0": "Die Sanität Basel im Info-Talk.m4a",
    "https://youtu.be/3rQWzPHi7-Y?si=zth7GypUAHlY_58o": "Georges-Simon Ulrich erklärt das Konzept： 17 Videoteaser à 17 Sekunden zu den 17 SDG.m4a",
    "https://youtu.be/vsZW2gUATG8?si=3dZn0tSPWKu8lSo1": "ÖREB-Kataster Basel-Stadt： Informationsveranstaltung für die kantonalen Rechtsdienste.m4a",
    "https://youtu.be/6GvkveUZzbI?si=DxFJXeiGgkwmG4G3": "Open Innovation Day «make open data – welche Daten dürfen es sein？».m4a",
}


def clean_filename(filename):
    cleaned_filename = filename.replace(" ", "-")
    cleaned_filename = re.sub(r'[\/\\:*?"<>|\']', "", cleaned_filename)
    return cleaned_filename


def delete_all_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)  # Delete the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def copy_files():
    delete_all_files_in_folder(SAVE_DIR)
    if st.session_state["url"] in list(url_list.keys()):
        shutil.copyfile(
            os.path.join(MP3_DIR, url_list[st.session_state["url"]]),
            os.path.join(SAVE_DIR, url_list[st.session_state["url"]]),
        )


if "url" not in st.session_state:
    st.session_state["url"] = random.choice(list(url_list.keys()))
    st.session_state["text"] = None
    st.session_state["txt_file_name"] = None
url = st.text_input("Gib eine Youtube Video URL ein", st.session_state["url"])
if url != st.session_state["url"]:
    st.session_state["url"] = url
    st.session_state["text"] = None
if st.session_state["url"] is not None:
    yt = YouTube(st.session_state["url"])
    st_player(st.session_state["url"])
    st.write(yt.title)

if st.button("Transkribiere Video"):
    with st.spinner(f'Transcribing "{yt.title}"...'):
        # make sure the file is copied to the save directory folder because in the cloud, downloading files form youtube does not
        # seem to work. this is a workaround for demo purpose, the productive version only works on local installations
        copy_files()
        loader = GenericLoader(
            YoutubeAudioLoader([url], SAVE_DIR), OpenAIWhisperParser()
        )
        try:
            docs = loader.load()
            st.session_state["text"] = " ".join([page.page_content for page in docs])
            st.session_state["txt_file_name"] = os.path.join(
                SAVE_DIR, clean_filename(yt.title) + ".txt"
            )
            with open(st.session_state["txt_file_name"], "w", encoding="utf8") as file:
                file.write(st.session_state["text"])
            st.success(f'Transkription für "{yt.title}" ist komplett.')
        except Exception as ex:
            st.warning(f'Video "{yt.title}" kann nicht geladen werden: {ex}.')

if st.session_state["text"] is not None:
    dummy = st.text_area("Output", value=st.session_state["text"], height=800)
    st.download_button(
        "Datei herunterladen",
        st.session_state["text"],
        st.session_state["txt_file_name"],
    )
