from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import random
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

videos = []

skipCurrentSong = False


def convertPlaylistToCSV(url):
    r = requests.get(url)
    page = r.text
    soup = bs(page, 'html.parser')
    res = soup.find_all('a', {'class': 'pl-video-title-link'})
    for l in res:
        videos.append('https://www.youtube.com' + l.get("href"))


@app.route('/', methods=['GET'])
def getRoot():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def postRoot():
    url = request.form['url']
    url = url.split(',')
    for x in url:
        if "playlist" in url:
            convertPlaylistToCSV(request.form['url'])
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
    return redirect('/')


@app.route('/api/checkSkipCurrentSong', methods=['GET'])
def checkSkipCurrentSong():
    global skipCurrentSong
    print skipCurrentSong
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
