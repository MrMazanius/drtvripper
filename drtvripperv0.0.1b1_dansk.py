import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from io import BytesIO
import tempfile
import os
import tkinter as tk
from tkinter import filedialog

def download_and_combine(video_url, audio_url, output_path):
    video_content = requests.get(video_url).content
    audio_content = requests.get(audio_url).content

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_file:
        video_file.write(video_content)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:
        audio_file.write(audio_content)

    try:
        video_clip = VideoFileClip(video_file.name)
        audio_clip = AudioFileClip(audio_file.name)

        video_clip = video_clip.set_audio(audio_clip)

        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print(f"Kombineret video gemt til {output_path}")

    finally:
        os.remove(video_file.name)
        os.remove(audio_file.name)

def download_and_combine_bulk(series_title, video_urls, audio_urls, output_folder):
    for i, (video_url, audio_url) in enumerate(zip(video_urls, audio_urls), start=1):
        episode_title = f"S01E{i:02d} - {series_title}.mp4"
        output_path = os.path.join(output_folder, episode_title)
        download_and_combine(video_url, audio_url, output_path)

def get_bulk_input():
    series_title = input("Indtast seriens titel: ")
    video_urls = input("Indtast video-URL'er adskilt af komma: ").split(",")
    audio_urls = input("Indtast lyd-URL'er adskilt af komma: ").split(",")
    output_folder = filedialog.askdirectory(title="Vælg output-mappe")
    return series_title.strip(), video_urls, audio_urls, output_folder

def main():
    root = tk.Tk()
    root.withdraw()

    mode = input("Vælg tilstand (enkelt/masse): ").lower()

    if mode == "enkelt":
        input_format = input("Indtast video- og lyd-URL'er i formatet VIDEO_URL|AUDIO_URL: ")
        video_url, audio_url = input_format.split("|")
        output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4-filer", "*.mp4")], title="Gem som")
        download_and_combine(video_url.strip(), audio_url.strip(), output_path)
    elif mode == "masse":
        series_title, video_urls, audio_urls, output_folder = get_bulk_input()
        download_and_combine_bulk(series_title, video_urls, audio_urls, output_folder)
    else:
        print("Ugyldig tilstand. Vælg venligst 'enkelt' eller 'masse'.")

if __name__ == "__main__":
    main()
