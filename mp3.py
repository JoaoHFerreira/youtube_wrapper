import streamlit as st
import os
from pathlib import Path

def main():
    st.title("Simple MP3 Player")
    
    # Set your fixed path where MP3 files are stored
    mp3_folder = "sliced_data"  # Replace with your actual folder path
    
    # Check if folder exists
    if not os.path.exists(mp3_folder):
        st.error(f"Folder '{mp3_folder}' not found. Please create it and add MP3 files.")
        return
    
    # Get list of MP3 files
    mp3_files = [f for f in os.listdir(mp3_folder) if f.endswith('.mp3')]
    
    if not mp3_files:
        st.warning("No MP3 files found in the folder.")
        return
    
    # Create a selection box for choosing the MP3 file
    selected_file = st.selectbox(
        "Choose an audio file to play:",
        mp3_files
    )
    
    # Display audio player
    if selected_file:
        audio_path = os.path.join(mp3_folder, selected_file)
        try:
            with open(audio_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
            # Display some basic file information
            file_size = Path(audio_path).stat().st_size / (1024 * 1024)  # Convert to MB
            st.info(f"File size: {file_size:.2f} MB")
            
        except Exception as e:
            st.error(f"Error playing the audio file: {str(e)}")

if __name__ == "__main__":
    main()