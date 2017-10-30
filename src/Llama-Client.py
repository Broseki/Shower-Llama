import os
import time
import subprocess
from subprocess import call
import requests
import wget
from mutagen.mp3 import MP3


# Returns an int length of the audio file
def getAudioFileDuration(filename):
    audio = MP3(filename)
    return int(audio.info.length)


# Runs a timer that detects when a song should
# be skipped
def musicTimer(timer, filename):
    for x in range(0, timer):
        time.sleep(1)
        if checkSkip():
            call(['killall','-9','vlc'])
            os.remove(filename)
            break
    os.remove(filename)


# Gets and returns the Youtube URL of the song
def getAudioUrl(url):
    output = subprocess.Popen(["/usr/bin/node", "/usr/lib/node_modules/offliberty/bin/off", url], stdout=subprocess.PIPE).communicate()[0]
    return output[14:]


# Starts playing the song from Youtube
def playVideo(url):
    mp3url = getAudioUrl(url)
    print mp3url
    filename = wget.download(mp3url)
    length = getAudioFileDuration(filename)
    subprocess.Popen(["vlc", filename, "vlc://quit"])
    musicTimer(length, filename)


# Checks the server to see if the current song should be skipped
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
