import streamlit as st
import yt_dlp
import os
import base64
import tempfile

def download_youtube_video(url):
    try:
        # Decode cookies file from environment variable
        cookies_base64 = os.getenv("YOUTUBE_COOKIES")
        cookies_path = None

        if cookies_base64:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                cookies_path = temp_file.name
                temp_file.write(base64.b64decode(cookies_base64))

        # yt-dlp options
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "%(title)s.%(ext)s",  # Save in the current directory
            "cookies": cookies_path if cookies_path else None,  # Use cookies if provided
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "Video")
            return f"{title}.mp4", title
    except Exception as e:
        return None, str(e)

# Streamlit App
st.title("YouTube Video Downloader")
st.write("Enter a YouTube video URL to download.")

url = st.text_input("YouTube Video URL:")

if st.button("Download"):
    if url:
        with st.spinner("Downloading video..."):
            video_path, message = download_youtube_video(url)
        if video_path:
            st.success(f"Downloaded: {message}")
            st.write("Video downloaded successfully.")
        else:
            st.error(f"Error: {message}")
    else:
        st.warning("Please enter a valid YouTube URL.")
