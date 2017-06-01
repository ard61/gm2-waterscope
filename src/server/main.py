import subprocess
import flask

app = flask.Flask(__name__)

class MJpegStream():
    def __init__(self):
        self.proc = None

    def start(self, *args, **kwargs):
        if self.proc:
            self.stop()
        self.proc = subprocess.Popen(self.create_args(*args, **kwargs), cwd='~/mjpg-streamer-master/mjpg-streamer-experimental')

    def stop(self):
        self.proc.terminate()

    def create_args(self, width=1280, height=720, fps=10, sharpness=0, contrast=0, brightness=50, saturation=0):
        return ['mjpg_streamer', '-o', 'output_http.so -w ./www', '-i', 
                'input_raspicam.so -x {0} -y {1} -fps {2} -sh {3} -co {4} -br {5} -sa {6}'.format(width, height, fps, sharpness, contrast, brightness, saturation)]

stream = MJpegStream()

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/start_stream', methods=['GET'])
def start_stream():
    get_args = flask.request.args
    width = get_args.get('width')
    height = get_args.get('height')
    fps = get_args.get('fps')

    # Do some error checking
    supported_resolutions = [(1280, 720),
                              (1920, 1080),
                              (640, 480),
                              (320, 240)]
    if (width, height) not in supported_resolutions:
        width, height = 1280, 720

    supported_fps = range(1, 30)
    if fps not in supported_fps:
        fps = 10

    stream.start(width=width, height=height, fps=fps)