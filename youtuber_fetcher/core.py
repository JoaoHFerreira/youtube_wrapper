import re
import os
import yt_dlp
from pydub import AudioSegment
from youtube_transcript_api import YouTubeTranscriptApi
import json


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

        with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(f"{entry['start']:.2f}s: {entry['text']}\n")

        parsed_data = _get_transcript_list_dict(file_name)

        with open(f"{file_name}.json", "w") as outfile:
            json.dump(parsed_data, outfile, indent=4)  # Add indentation for readability

        return file_name + ".json"

    except Exception as e:
        print(f"Error fetching transcript: {e}")


def _get_transcript_list_dict(transcript_name):
    """
    Parses a transcript file, extracts speech segments with start and end times,
    and saves the data as JSON.

    Args:
        transcript_name (str): Name of the transcript file (without extension).
        output_filename (str, optional): Name of the output JSON file. Defaults to "transcript_data.json".
    """
    transcript_name = transcript_name.split(".")[0]
    parsed_data = []
    with open(f"{transcript_name}.txt", "r") as file:
        lines = list(filter(None, file.read().split("\n")))

    for i in range(len(lines) - 1):
        init_time, phrase = lines[i].split("s: ")
        next_init_time, _ = lines[i + 1].split("s: ")
        parsed_data.append(
            {
                "init_time": init_time.strip(),
                "final_time": next_init_time.strip(),
                "phrase": phrase.strip(),
            }
        )

    init_time, phrase = lines[-1].split("s: ")
    parsed_data.append(
        {"init_time": init_time.strip(), "final_time": None, "phrase": phrase.strip()}
    )
    return parsed_data


def slice_mp3_from_json(input_file, json_path, output_dir="sliced_data"):
    """Slices an MP3 file based on start and end times specified in a JSON file and saves
    the segments with a numbered pattern using pydub library.

    Args:
        input_file (str): Path to the input MP3 file.
        output_dir (str): Path to the output directory.
        json_data (list): List of dictionaries containing 'init_time' and 'final_time' values.
    """

    with open(json_path, "r") as f:
        json_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    sound = AudioSegment.from_mp3(input_file)

    # Iterate over the JSON data and slice the audio
    for i, data in enumerate(json_data):
        start_time = (
            float(data["init_time"]) * 1000
        )  # Convert seconds to milliseconds for pydub
        end_time = (
            float(data["final_time"]) * 1000 if "final_time" in data else len(sound)
        )  # Handle missing final time

        # Extract the audio segment
        sliced_audio = sound[int(start_time) : int(end_time)]

        # Create the output file name
        output_file = os.path.join(output_dir, f"file_name_part{i+1}.mp3")

        # Export the sliced audio segment as a new MP3 file
        sliced_audio.export(output_file, format="mp3")
