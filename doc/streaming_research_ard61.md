## Streaming - Antoine's research


### A few streaming technologies I found

#### 'Hacky' solutions
*	Motion JPEG: encode the video as a stream of images, sent individually.  
	*	Can be done using Flask - cf [Miguel Grinberg blog](https://blog.miguelgrinberg.com/post/video-streaming-with-flask)
	*	Or mjpeg-streamer - cf [Miguel Grinberg blog](https://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android)
	*	Or RPi-Cam-Web-Interface (choice of apache/nginx/lighttpd) - cf [elinux website](http://elinux.org/RPi-Cam-Web-Interface)
		*	Is said to work beautifully, with good resolution and low latency. However there seems to be latency before capturing photo or video. 
		*	We could reuse many parts of their project!

*	Netcat a raw H.264 stream and read it from a compatible media player e.g. MPlayer- see [the RPi blog](https://www.raspberrypi.org/blog/camera-board-available-for-sale/)  
	*	Any browser support? Is it possible to embed an open source media player plugin in a browser? -> here it's a raw TCP stream, can we make it HTTP so a browser can receive it?
	* 	Might need some complicated setup
	*	Not sure it'll recover from errors well either.

#### State-of-the art streaming standards
It seems there are 3 commonly-used standards for adaptive streaming i.e. changing the bitrate to adapt to fluctuating network conditions: HLS (HTTP Live Streaming), MPEG-Dash and RTMP - see [this report](https://developer.jwplayer.com/articles/html5-report/#adaptive-streaming). HLS and MPEG-Dash are natively supported by HTML5 whereas RTMP requires a Flash plugin which is becoming deprecated (and isn't open source). 

*	HTTP Live Streaming - made by Apple  
	*	This [gist](https://gist.github.com/chrislavender/cad26500c9655627544f) explains
	*	Browser support table [from JWPlayer website](https://developer.jwplayer.com/articles/html5-report/adaptive-streaming/hls.html)

*	MPEG-Dash
	*	[Wikipedia article](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)

#### Ready-made solutions that implement these technologies

*	HTML5 video streaming  
	*	[StackOverflow](http://stackoverflow.com/questions/40045857/live-video-streaming-with-html-5) it mentions that two ways to stream the video are MPEG-Dash and HLS (HTTP Live Streaming). Also provides some useful links. 
	*	W3CSchools documentation for [HTML](https://www.w3schools.com/html/html5_video.asp) and [JavaScript](https://www.w3schools.com/tags/ref_av_dom.asp)

*	WebRTC - Open Source APIs for streaming media from server to browser  
	*	This was the library we were recommended to use at the company hackathon during my internship last summer.
	*	cf [official website](https://webrtc.org/)
	*	and [tutorial](https://codelabs.developers.google.com/codelabs/webrtc-web)


### How should we compare the technologies?
*	Latency (average and maximum)
*	Resolution
*	Can it stream well for a long time (i.e. not error-prone)?
	*	What would be an acceptable frequency of error?
*	Robustness - can it recover gracefully from errors?
	*	Ideally just reloading the webpage would solve the problem, or not even having to. 