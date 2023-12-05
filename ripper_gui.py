import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from io import BytesIO
import tempfile
import os
import tkinter as tk
from tkinter import filedialog

def download_and_combine(video_url, audio_url, output_path):
    # Download video and audio files
    video_content = requests.get(video_url).content
    audio_content = requests.get(audio_url).content

    # Create temporary files for video and audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_file:
        video_file.write(video_content)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
        audio_file.write(audio_content)

    try:
        # Create VideoFileClip and AudioFileClip objects
        video_clip = VideoFileClip(video_file.name)
        audio_clip = AudioFileClip(audio_file.name)

        # Combine video and audio
        video_clip = video_clip.set_audio(audio_clip)

        # Write the combined video to the output file
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Combined video saved to {output_path}")

    finally:
        # Clean up temporary files
        os.remove(video_file.name)
        os.remove(audio_file.name)

def download_and_combine_bulk(series_title, video_urls, audio_urls, output_folder):
    for i, (video_url, audio_url) in enumerate(zip(video_urls, audio_urls), start=1):
        episode_title = f"S01E{i:02d} - {series_title}.mp4"
        output_path = os.path.join(output_folder, episode_title)
        download_and_combine(video_url, audio_url, output_path)

def get_bulk_input():
    series_title = input("Enter the title of the series: ")
    video_urls = input("Enter video URLs separated by commas: ").split(",")
    audio_urls = input("Enter audio URLs separated by commas: ").split(",")
    output_folder = filedialog.askdirectory(title="Select output folder")
    return series_title.strip(), video_urls, audio_urls, output_folder

def main():
    root = tk.Tk()
    root.withdraw()

    mode = input("Choose mode (single/bulk): ").lower()

    if mode == "single":
        input_format = input("Enter the video and audio URLs in the format VIDEO_URL|AUDIO_URL: ")
        video_url, audio_url = input_format.split("|")
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="Save As")
        download_and_combine(video_url.strip(), audio_url.strip(), output_path)
    elif mode == "bulk":
        series_title, video_urls, audio_urls, output_folder = get_bulk_input()
        download_and_combine_bulk(series_title, video_urls, audio_urls, output_folder)
    else:
        print("Invalid mode. Please choose 'single' or 'bulk'.")

if __name__ == "__main__":
    main()
