from openai import OpenAI

import streamlit as st
from pytube import YouTube
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import os

MP4_DIR = './data/mp4/'
MP3_DIR = './data/mp3/'
TEXT_DIR = './data/text/'

def download_video(url, path):
    try:
        # Create YouTube object with the URL of the video
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        video_stream = yt.streams.get_highest_resolution()
        
        # Download the video to the specified path
        video_stream.download(output_path=path)
        print(f"Downloaded '{yt.title}' successfully.")
    except Exception as e:
        print(f"Failed to download video: {e}")
    return path + f'{yt.title}.mp4'

def extract_audio(mp4_file_path):
    mp4_dir_path, mp4_file_name = os.path.split(mp4_file_path)
    mp3_file_name = mp4_file_name.replace(".mp4", ".mp3")
    mp3_file_path = os.path.join(MP3_DIR, mp3_file_name)    
    try:
        video = VideoFileClip(mp4_file_path)
        video.audio.write_audiofile(mp3_file_path)
        print(f"Audio extracted successfully and saved as '{mp3_file_path}'.")
    except Exception as e:
        print(f"Failed to extract audio: {e}")
    return mp3_file_path

def convert2wav(mp3_file_path: str):
    wav_file_path = mp3_file_path.replace(".mp3", ".wav")
    
    try:
        audio = AudioSegment.from_mp3(mp3_file_path)
        st.write(audio)
        audio.export(wav_file_path, format="wav")
        print(f"Audio converted successfully and saved as '{wav_file_path}'.")
    except Exception as e:
        print(f"Failed to convert audio: {e}")
    return wav_file_path

def transcribe_audio(mp3_file_path: str):
    client = OpenAI()
    mp3_dir_path, mp3_file_name = os.path.split(mp3_file_path)
    text_file_name = mp3_file_name.replace(".mp3", ".txt")
    text_file_path = os.path.join(MP3_DIR, text_file_name)
    st.write(os.path.getsize(mp3_file_path))
    if os.path.getsize(mp3_file_path) > 25 * 1024 * 1024:
        st.write(mp3_file_path)
        full = AudioSegment.from_mp3(mp3_file_path)
        ten_minutes = 10 * 60 * 1000
        first_10_minutes = full[:ten_minutes]
        file_path = mp3_file_path.replace(".mp3", "_10.mp3")
        first_10_minutes.export(file_path, format="mp3")
        mp3_file_path = file_path

    audio_file = open(mp3_file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text"
    )
    with open(text_file_path, 'w') as file:
        file.write(transcript)


url = st.text_input('Enter the youtube video url')
if st.button('download video'):
    mp4_file_path = download_video(url, MP4_DIR)
    st.success(f'Download of {mp4_file_path} complete')

mp4_files = os.listdir(MP4_DIR)
sel_mp4 = st.selectbox('Select a video', mp4_files)
st.video(os.path.join(MP4_DIR, sel_mp4))
if st.button('convert to mp3'):
    mp3_path = extract_audio(os.path.join(MP4_DIR, sel_mp4))


mp3_files = os.listdir(MP3_DIR)
sel_mp3 = st.selectbox('Select a mp3', mp3_files)
st.audio(os.path.join(MP3_DIR, sel_mp3))
if st.button('Transcribe'):
    text_path = transcribe_audio(os.path.join(MP3_DIR, sel_mp3))
