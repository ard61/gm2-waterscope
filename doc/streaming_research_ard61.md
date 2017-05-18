Streaming - Antoine's research


Here are a few streaming technologies I found:
*	Motion JPEG: encode the video as a stream of images, sent individually.
	*	Can be done using Flask - cf [Miguel Grinberg blog](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
	*	Or mjpeg-streamer - cf [Miguel Grinberg blog](https://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android)
	*	Or cf RPi-Cam-Web-Interface (choice of apache/nginx/lighttpd) - cf [elinux website](http://elinux.org/RPi-Cam-Web-Interface)
		*	Is said to work beautifully, with good resolution and good latency. However there seems to be latency before capturing photo or video. 
		*	We could reuse many parts of their project!

*	Netcat a raw H.264 stream and read it from a compatible media player e.g. MPlayer- see [the RPi blog](https://www.raspberrypi.org/blog/camera-board-available-for-sale/)
	*	Any browser support? Is it possible to embed an open source media player plugin in a browser? -> here it's a raw TCP stream, can we make it HTTP so a browser can receive it?
	* 	Might need some complicated setup
	*	Not sure it'll recover from errors well either.

*	HTML5 video streaming, like what JWPlayer does. 


How should we compare the technologies?
*	Latency (average and maximum)
*	Resolution
*	Can it stream well for a long time (i.e. not error-prone)?
	*	What would be an acceptable frequency of error?
*	Robustness - can it recover gracefully from errors?
	*	Ideally just reloading the webpage would solve the problem, or not even having to. 