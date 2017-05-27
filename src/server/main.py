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
  <img width="640" height="480" src="http://127.0.0.1:8554/" />
</body>

</html>
"""

class MJpegStream():
    def __init__(self):
        self.vlc_args = ['cvlc', '--no-audio', 'v4l2:///dev/video0', '--v4l2-width', '640',
                         '--v4l2-height', '480', '--v4l2-chroma', 'MJPG', '--v4l2-hflip', '1',
                         '--v4l2-vflip', '1', '--v4l2-fps', '20', '--sout',
                         '#transcode{vcodec=MJPG,fps=20}:standard{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=:8554/}'
                         , '-I dummy']
        self.proc = None

    def start(self):
        #self.proc = subprocess.Popen(self.vlc_args, stdin=None, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.proc = subprocess.Popen(self.vlc_args)
        #self.proc = subprocess.Popen("cvlc --no-audio v4l2:///dev/video0 --v4l2-width 640 --v4l2-height 480 --v4l2-chroma MJPG --v4l2-hflip 1 --v4l2-vflip 1 --v4l2-fps 20 --sout '#transcode{vcodec=MJPG,fps=20}:standard{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=:8554/}' -I dummy", shell=True)

    def stop(self):
        self.proc.terminate()

stream = MJpegStream()
stream.start()