import subprocess

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return """<!DOCTYPE html>
<html>

<head>
  <title>Flask + MJPEG streaming test</title>
</head>

<body>
  <img width="640" height="480" src="http://172.24.1.1:8080/?action=stream" />
</body>

</html>
"""

class MJpegStream():
    def __init__(self):
        self.mjpg_streamer_args = ['cd ~/mjpg-streamer-master/mjpg-streamer-experimental && ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -fps 10 -x 1280 -y 720"']
        self.proc = None

    def start(self):
        #self.proc = subprocess.Popen(self.vlc_args, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.proc = subprocess.Popen(self.mjpg_streamer_args, shell=True)

    def stop(self):
        self.proc.terminate()

stream = MJpegStream()
stream.start()