import sys
import time
import subprocess
import flask

# TODO: FIX FileNotFoundError when trying to connect to motor board
#import fergboard_motors  # fergboard_motors.py
#motors = fergboard_motors.Motors()

app = flask.Flask(__name__)

class MJpegStream():
    def __init__(self):
        self.proc = None

    def start(self, *args, **kwargs):
        if self.proc:
            self.stop()
        self.proc = subprocess.Popen(self.create_args(*args, **kwargs), stderr=subprocess.PIPE, universal_newlines=True)

        # Block until we have read the line "Encoder Buffer Size" from stderr.
        while self.proc.poll() is None:
            time.sleep(0.01)
            line = self.proc.stderr.readline()
            if line != "":
                sys.stdout.write(line)
                sys.stdout.flush()
                if "Encoder Buffer Size" in line:
                    print("mjpg-streamer successfully started!")
                    return True

        # If mjpg-streamer stopped, it means there was an error.
        sys.stdout.write(self.proc.stderr.read())
        sys.stderr.write("Error starting mjpg-streamer!\n")
        return False

    def stop(self):
        self.proc.terminate()

    def create_args(self, width=1280, height=720, fps=10, sharpness=0, contrast=0, brightness=50, saturation=0):
        return ['mjpg_streamer', '-o', 'output_http.so -w ./www', '-i', 
                'input_raspicam.so -x {0} -y {1} -fps {2} -sh {3} -co {4} -br {5} -sa {6}'.format(width, height, fps, sharpness, contrast, brightness, saturation)]

stream = MJpegStream()
stream.start()

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/start_stream', methods=['GET'])
def start_stream():
    """
    Restarts the mjpg-streamer stream, waits to see if it has completed
    properly, and returns success/error.
    """
    get_args = flask.request.args
    width = get_args.get('width')
    height = get_args.get('height')
    fps = get_args.get('fps')
    sharpness = get_args.get('sharpness')
    contrast = get_args.get('contrast')
    brightness = get_args.get('brightness')
    saturation = get_args.get('saturation')

    # Do some error checking for security, as we pass those values on to mjpg_streamer.
    supported_resolutions = [(1280, 720),
                              (1920, 1080),
                              (640, 480),
                              (320, 240)]
    if (width, height) not in supported_resolutions:
        width, height = 1280, 720
    supported_fps = range(1, 31)
    if fps not in supported_fps:
        fps = 10
    if sharpness not in range(-100,101):
        sharpness = 0
    if contrast not in range(-100,101):
        contrast = 0
    if brightness not in range(0,101):
        brightness = 50
    if saturation not in range(-100,101):
        saturation = 0

    if stream.start(width=width, height=height, fps=fps):
        return flask.Response(status="200 OK")
    else:
        return flask.Response(status="500 INTERNAL SERVER ERROR")

@app.route('/capture', methods=['GET'])
def capture():
    """
    Capture a still photo at max resolution and send it to the user
    """
    flask.send_file("capture.jpg", mimetype="image/jpeg")


@app.route('/move', methods=['GET'])
def move():
    get_args = flask.request.args
    x = get_args.get('X', default=0)
    y = get_args.get('Y', default=0)
    z = get_args.get('Z', default=0)

    motors.move(x, y, z)
    return flask.Response(status="200 OK")
