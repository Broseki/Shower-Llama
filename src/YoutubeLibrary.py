from pytube import YouTube
import os


def playVideo(url):
    yt = YouTube(url)
    yt.set_filename('video')
    video = yt.get('mp4', '360p')
    video = yt.get('mp4')
    video.download('')
    os.system("open video.mp4")
