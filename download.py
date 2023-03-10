# Importing modules
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

# Getting video id from url
url = input("Enter the url of the youtube video: ")
video_id = url.split("v=")[-1]

# Create a YouTube object
yt = YouTube(url)

# Get the highest resolution stream
stream = yt.streams.get_highest_resolution()

# Download the video and rename it
stream.download(filename="{}.mp4".format(video_id))

# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
# iterate over all available transcripts
for transcript in transcript_list:
    subs_zh = transcript.translate('zh-Hans').fetch()

subs_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

# Writing subtitles to srt files
with open(f'{video_id}_zh.srt', 'w') as f_zh:
    for i, sub in enumerate(subs_zh):
        f_zh.write(f"{i+1}\n")
        f_zh.write(f"{sub['start']} --> {sub['start'] + sub['duration']}\n")
        f_zh.write(f"{sub['text']}\n\n")

with open(f'{video_id}_en.srt', 'w') as f_en:
    for i, sub in enumerate(subs_en):
        f_en.write(f"{i+1}\n")
        f_en.write(f"{sub['start']} --> {sub['start'] + sub['duration']}\n")
        f_en.write(f"{sub['text']}\n\n")

# Combining subtitles into video with ffmpeg
import subprocess

command = [
    "ffmpeg",
    "-i", f"{video_id}.mp4",
    "-vf", f"subtitles={video_id}_zh.srt:force_style='Alignment=2', subtitles={video_id}_en.srt:force_style='Alignment=10'",
    "-c:v", "libx264",
    "-c:a", "copy",
    "-crf", "23",
    "-preset", "medium",
    "-movflags", "+faststart",
    f"{video_id}_dual.mp4"
]

subprocess.run(command)