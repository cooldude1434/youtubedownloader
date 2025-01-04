import streamlit as st
import yt_dlp
import os
import tempfile

# Function to download YouTube Shorts video
def download_youtube_short(url, output_path):
    try:
        # yt-dlp options for downloading
        ydl_opts = {
            "format": "mp4",  # Desired format (MP4)
            "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),  # Save video with title as filename
        }

        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get("title", "Video")  # Get the title of the video

            # Return the file path and title for success message
            video_file_path = os.path.join(output_path, f"{title}.mp4")
            return video_file_path, title
    except Exception as e:
        return None, str(e)

# Streamlit App UI
st.title("YouTube Shorts Downloader (yt-dlp)")
st.write("Enter the URL of a YouTube Short to download it.")

# Input for YouTube Shorts URL
url = st.text_input("YouTube Shorts URL:")

# Button to trigger the download process
if st.button("Download"):
    if url:
        # Create a temporary directory for downloads
        with tempfile.TemporaryDirectory() as tmp_dir:
            with st.spinner("Downloading..."):  # Show a spinner while downloading
                # Call the download function
                video_path, message = download_youtube_short(url, tmp_dir)

            # Handle the response
            if video_path:
                st.success("Download complete!")  # Success message
                # Provide a download button for the user
                with open(video_path, "rb") as video_file:
                    st.download_button(
                        label="Download Video to Your Laptop", 
                        data=video_file,
                        file_name=os.path.basename(video_path),
                        mime="video/mp4"
                    )
            else:
                st.error(f"Error: {message}")  # Show error message if download fails
    else:
        st.warning("Please enter a valid URL.")  # Warning if no URL is provided
