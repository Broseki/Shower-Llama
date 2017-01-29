import os
import time
import pafy
import subprocess
from flask import Flask
from flask import render_template
from flask import request


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

'''
def fetchSongUrl():
    r = requests.get('http://127.0.0.1:5000/api/' + API_KEY + '/getNextSong')
    return r.text


def checkStop():
    r = requests.get('http://127.0.0.1:5000/api/' + API_KEY + '/getPlayStatus')
    if r.text == "next":
        pass
    elif r.text == "stop":
        pass


def checkEAS():
    global lastEAS
    r = requests.get('http://127.0.0.1:5000/api/' + API_KEY + '/getEASStatus')
    if r.text != "clear" and r.text != lastEAS:
        lastEAS = r.text
        playVideo('https://www.youtube.com/watch?v=zXhb596PlgI')
        os.system('say ' + r.text)
'''


@app.route('/', methods=['GET'])
def getRoot():
    return render_template("index.html")


@app.route('/api/play', methods=['POST'])
def postRoot():
    url = request.form['url']
    # time.sleep(30)
    url = url.split(',')
    for x in url:
        playVideo(x)
    return "OK!"


while(True):
    try:
        app.run()
    except:
        pass
