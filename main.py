import sys
import argparse
import youtuber_fetcher as  yt



def main():
    parser = argparse.ArgumentParser(description="Collect a YouTube URL.")
    parser.add_argument('url', type=str, help='The YouTube URL to process')
    args = parser.parse_args()
    
    youtube_id = yt.get_id(args.url)
    mp3_file_nm = yt.save_audio(args.url)
    transcription_file_nm = yt.get_transcript(youtube_id, "japanse_title", "ja")

    yt.slice_mp3_from_json(mp3_file_nm, transcription_file_nm)


if __name__ == '__main__':
    main()