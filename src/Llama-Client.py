import os
import time
import pafy
import subprocess
from subprocess import call
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
        if checkSkip():
            call(['killall','-9','vlc'])
            break
    os.remove(filepath)


def play(filepath):
    os.system("vlc " + filepath)


def playVideo(url):
    video = pafy.new(url)
    length = convertTime(video.duration)
    bestAudio = video.getbestaudio()
    filepath = "temp." + bestAudio.extension
    bestAudio.download(filepath=filepath)
    print length
    subprocess.Popen(["vlc", filepath, "vlc://quit"])
    musicTimer(length, filepath)


def checkSkip():
    rx = requests.get('http://127.0.0.1:80/api/checkSkipCurrentSong')
    print(rx.text)
    if rx.text == "True":
        return True
    else:
        return False


while(True):
    try:
        r = requests.get('http://127.0.0.1:80/api/getNextVideo')
        if r.text != "None":
            playVideo(r.text)
        else:
            pass
    except:
        pass
