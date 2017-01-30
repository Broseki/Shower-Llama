import os
import time
import pafy
import subprocess
from flask import Flask
import requests


lastEAS = ''

app = Flask(__name__)

def convertTime(timex):
    timeArray = str(timex).split(":")
    seconds = 0
    seconds += int(timeArray[0]) * 60 * 60
    seconds += int(timeArray[1]) * 60
    seconds += int(timeArray[2])
    return seconds


def musicTimer(timer, filepath):
    for x in range(0, timer):
        time.sleep(1)
        print x
    os.remove(filepath)


def play(filepath):
    os.system("/Applications/VLC.app/Contents/MacOS/VLC " + filepath)


def playVideo(url):
    video = pafy.new(url)
    length = convertTime(video.duration)
    bestAudio = video.getbestaudio()
    filepath = "temp." + bestAudio.extension
    bestAudio.download(filepath=filepath)
    print length
    subprocess.Popen(["/Applications/VLC.app/Contents/MacOS/VLC", filepath, "vlc://quit"])
    musicTimer(length, filepath)


while(True):
    try:
        r = requests.get('http://127.0.0.1:5000/api/getNextVideo')
        if r.text != "None":
            print r.text
        else:
            pass
    except:
        pass
