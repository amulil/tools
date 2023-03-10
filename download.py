# Importing modules
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from tqdm import tqdm

# Getting video id from url
url = input("Enter the url of the youtube video: ")
video_id = url.split("v=")[-1]

# Create a YouTube object
yt = YouTube(url)

# Get the highest resolution stream
yt.streams.filter(progressive=True).get_highest_resolution().download(filename="{}.mp4".format(video_id))

# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
# iterate over all available transcripts
for transcript in transcript_list:
    subs_zh = transcript.translate('zh-Hans').fetch()
subs_en = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

formatter = SRTFormatter()
# .format_transcript(transcript) turns the transcript into a SRT string.
srt_formatted_zh = formatter.format_transcript(subs_zh)
srt_formatted_en = formatter.format_transcript(subs_en)

# Now we can write it out to a file.
with open('{}_zh.srt'.format(video_id), 'w', encoding='utf-8') as json_file:
    json_file.write(srt_formatted_zh)
with open('{}_en.srt'.format(video_id), 'w', encoding='utf-8') as json_file:
    json_file.write(srt_formatted_en)