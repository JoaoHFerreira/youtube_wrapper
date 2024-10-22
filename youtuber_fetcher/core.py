import re
import os
import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
import sqlite3
from pydub import AudioSegment
from pydub.playback import play




def save_audio(youtube_url, output_path="."):
    file_name = _download_audio(youtube_url)
    return _convert_mp3(file_name)


def _download_audio(youtube_url, output_path="."):
    temp_file = None
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        file_name = ydl.prepare_filename(info)

    return file_name


def _convert_mp3(file_name):

    if file_name and file_name.endswith(".webm"):
        audio = AudioSegment.from_file(file_name, format="webm")
        mp3_filename = file_name.replace(".webm", ".mp3")
        audio.export(mp3_filename, format="mp3")
        print(f"Audio converted to MP3: {mp3_filename}")

        os.remove(file_name)
        print(f"Temporary file removed: {file_name}")
        return mp3_filename

    if file_name and file_name.endswith(".m4a"):
        audio = AudioSegment.from_file(file_name, format="m4a")
        mp3_filename = file_name.replace(".m4a", ".mp3")
        audio.export(mp3_filename, format="mp3")
        print(f"Audio converted to MP3: {mp3_filename}")

        os.remove(file_name)
        print(f"Temporary file removed: {file_name}")
        return mp3_filename


def get_id(url):
    youtube_url_regex = (
        r"^(https?://)?(www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})$"
    )
    match = re.match(youtube_url_regex, url)

    if match:
        return match.group(3)
    return None


def get_transcript(video_id, title, ln="en"):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=[
                ln,
            ],
        )
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        file_name = safe_title


        transcript_dict_list = []
        for entry in transcript:
            entry["end"] = entry["start"] + entry["duration"]
            transcript_dict_list.append(entry)


        with open(f"{file_name}.json", "w") as outfile:
            json.dump(transcript_dict_list, outfile, indent=4)

        return file_name + ".json"

    except Exception as e:
        print(f"Error fetching transcript: {e}")


def slice_mp3_from_json(input_file, json_path, output_dir="sliced_data"):
    """Slices an MP3 file based on start and end times specified in a JSON file and saves
    the segments with a numbered pattern using pydub library.

    Args:
        input_file (str): Path to the input MP3 file.
        output_dir (str): Path to the output directory.
        json_data (list): List of dictionaries containing 'start' and 'end' values.
    """
    with open(json_path, "r") as f:
        json_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    sound = AudioSegment.from_mp3(input_file)
    
    # Process all elements except the last one
    for index in range(len(json_data) - 1):
        start_time = float(json_data[i]["start"]) * 1000
        end_time = float(json_data[i]["end"]) * 1000
        
        sliced_audio = sound[int(start_time):int(end_time)]
        output_file = os.path.join(output_dir, f"file_name_part{index}.mp3")
        sliced_audio.export(output_file, format="mp3")
    
    # Handle the last element separately
    if json_data:  # Check if the list is not empty
        last_idx = len(json_data) - 1
        start_time = float(json_data[last_idx]["start"]) * 1000
        end_time = len(sound)  # Use total duration for the last segment
        
        sliced_audio = sound[int(start_time):int(end_time)]
        output_file = os.path.join(output_dir, f"file_name_part{last_idx}.mp3")
        sliced_audio.export(output_file, format="mp3")
