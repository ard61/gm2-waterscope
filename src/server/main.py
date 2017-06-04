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
        self.params = {}

    def start(self, **params):
        """
        Start mjpg-streamer, wait until it has warmed up, and return success/failure
        """
        if self.proc:
            self.stop()
        self.proc = subprocess.Popen(self.create_args(**params),
                                     stderr=subprocess.PIPE, universal_newlines=True)

        # Block until we have read the line "Encoder Buffer Size" from stderr.
        while self.proc.poll() is None:
            time.sleep(0.01)
            line = self.proc.stderr.readline()
            if line != "":
                sys.stdout.write(line)
                sys.stdout.flush()
                if "Encoder Buffer Size" in line:
                    print("mjpg-streamer successfully started!")
                    # Save our parameters if the stream starts ok
                    self.params = params
                    return True

        # If mjpg-streamer stopped, it means there was an error.
        sys.stdout.write(self.proc.stderr.read())
        sys.stderr.write("Error starting mjpg-streamer!\n")
        self.proc = None
        return False

    def stop(self):
        """
        Kill mjpg-streamer, wait until it has stopped, then return.
        """
        if self.proc:
            self.proc.terminate()
            self.proc.wait()
        self.proc = None

    def create_args(self, **params):
        return ['mjpg_streamer', '-o', 'output_http.so -w ./www', '-i', 
                'input_raspicam.so -x {0} -y {1} -fps {2} -sh {3} -co {4} -br {5} -sa {6}'
                    .format(params['width'],
                            params['height'], 
                            params['fps'], 
                            params['sharpness'], 
                            params['contrast'], 
                            params['brightness'], 
                            params['saturation'])]

    def safe_args(self, **params):
        width = params.get('width')
        height = params.get('height')
        fps = params.get('fps')
        sharpness = params.get('sharpness')
        contrast = params.get('contrast')
        brightness = params.get('brightness')
        saturation = params.get('saturation')

        # Do some error checking for security, as we pass those values on to mjpg_streamer.
        supported_resolutions = [(1280, 720),
                                  (1920, 1080),
                                  (640, 480),
                                  (320, 240)]
        if (width, height) not in supported_resolutions:
            width, height = (self.params.get('width', default=1280),
                             self.params.get('height', 720))
        supported_fps = range(1, 31)
        if fps not in supported_fps:
            fps = self.params.get('fps', default=10)
        if sharpness not in range(-100,101):
            sharpness = self.params.get('fps', default=0)
        if contrast not in range(-100,101):
            contrast = self.params.get('contrast', default=0)
        if brightness not in range(0,101):
            brightness = self.params.get('brightness', default=50)
        if saturation not in range(-100,101):
            saturation = self.params.get('saturation', default=0)

        return {
            "width": width
            "height": height
            "fps": fps
            "sharpness": sharpness
            "contrast": contrast
            "brightness": brightness
            "saturation": saturation
        }

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
    get_args = stream.safe_args(flask.request.args)
    if stream.start(get_args):
        return flask.Response(status="200 OK")
    else:
        return flask.Response(status="500 INTERNAL SERVER ERROR")

@app.route('/capture', methods=['GET'])
def capture():
    """
    Capture a still photo at max resolution and send it to the user
    """

    # Need to stop the stream first
    stream.stop()

    get_args = stream.safe_args(flask.request.args)

    raspistill_args = ['raspistill', '--width', '2592', '--height', '1944',
                       '--nopreview', '--output', 'capture.jpg', '--timeout', '1500',
                       '--quality', '100', '--thumb', 'none',
                       '-sh', get_args['sharpness'], '-co', get_args['contrast'],
                       '-br', get_args['brightness'], '-sa', get_args['saturation']]
    subprocess.run(raspistill_args)

    # Start the stream again, with the previous parameters implied
    stream.start()
    flask.send_file("capture.jpg", mimetype="image/jpeg")


@app.route('/move', methods=['GET'])
def move():
    get_args = flask.request.args
    x = get_args.get('X', default=0)
    y = get_args.get('Y', default=0)
    z = get_args.get('Z', default=0)

    motors.move(x, y, z)
    return flask.Response(status="200 OK")
