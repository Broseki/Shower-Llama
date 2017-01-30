from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import random


lastEAS = ''

app = Flask(__name__)


videos = []

skipCurrentSong = False


@app.route('/', methods=['GET'])
def getRoot():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def postRoot():
    url = request.form['url']
    url = url.split(',')
    for x in url:
        videos.append(x)
    return redirect('/')


@app.route('/api/getNextVideo', methods=['GET'])
def getNextVideo():
    if len(videos) > 0:
        link = random.choice(videos)
        videos.remove(link)
        return link
    else:
        return "None"


@app.route('/api/clearList', methods=['GET'])
def clearList():
    global videos
    videos = []
    return redirect("/")


@app.route('/api/skipCurrentSong', methods=['GET'])
def setSkipCurrentSong():
    global skipCurrentSong
    skipCurrentSong = True
    return redirect("/")


@app.route('/api/checkSkipCurrentSong', methods=['GET'])
def checkSkipCurrentSong():
    global skipCurrentSong
    if skipCurrentSong:
        skipCurrentSong = False
        return "True"
    else:
        return "False"


while(True):
    try:
        app.run(host='0.0.0.0', port=80)
    except:
        pass
