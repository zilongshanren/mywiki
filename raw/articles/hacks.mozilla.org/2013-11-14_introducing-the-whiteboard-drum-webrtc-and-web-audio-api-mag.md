---
title: Introducing the Whiteboard Drum – WebRTC and Web Audio API magic – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/11/introducing-the-whiteboard-drum-webrtc-and-web-audio-api-magic/
author: Tatsuya Shinyagaito
published: '2013-11-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Browser functionality has expanded rapidly, way beyond merely “browsing” a document. Recently, Web browsers finally gained audio processing abilities with the [Web Audio API](https://developer.mozilla.org/en-US/docs/Web_Audio_API). It is powerful to the point of building serious music applications.

Not only that, but it is also very interesting when combined with other APIs. One of these APIs is `getUserMedia()`

, which allows us to capture audio and/or video from the local PC’s microphone / camera devices. [Whiteboard Drum](http://www.g200kg.com/whiteboarddrum/) ([code on GitHub](https://github.com/g200kg/WhiteboardDrum)) is a music application, and a great example of what can be achieved using Web Audio API and `getUserMedia()`

.

I demonstrated Whiteboard Drum at the Web Music Hackathon Tokyo in October. It was a very exciting event on the subject of Web Audio API and Web MIDI API. Many instruments can collaborate with the browser, and it can also create new interfaces to the real world.

![](../../assets/ab5cdbb6b3c078b5.jpeg)


I believe this suggests further possibilities of Web-based music applications, especially using Web Audio API in conjunction with other APIs. Let’s explain how the key features of Whiteboard Drum work, showing relevant code fragments as we go.

## Overview

First of all, let me show you a picture from the Hackathon:

![](../../assets/03cb63ce29431b43.jpg)


And a easy movie demo:

As you can see, Whiteboard Drum plays a rhythm according to the matrix pattern on the whiteboard. The whiteboard has no magic; it just needs to be pointed at by a WebCam. Though I used magnets in the demo, you can draw the markers using pen if you wish. Each row represents the corresponding instruments of Cymbal, Hi-Hat, Snare-Drum and Bass-Drum, and each column represents timing steps. In this implementation, the sequence has 8 steps. The color blue will activate the grid normally, and the red will activate with accent.

The processing flow is:

- The whiteboard image is captured by the WebCam
- The matrix pattern is analysed
- This pattern is fed to the drum sound generators to create the corresponding sound patterns

![](../../assets/ebeb77ad1421ae6f.png)


Although it uses nascent browser technologies, each process itself is not so complicated. Some key points are described below.

## Image capture by getUserMedia()

`getUserMedia()`

is a function for capturing video/audio from webcam/microphone devices. It is a part of [WebRTC](http://www.webrtc.org/) and a fairly new feature in web browsers. Note that the user’s permission is required to get the image from the WebCam. If we were just displaying the WebCam image on the screen, it would be trivially easy. However, we want to access the image’s raw pixel data in JavaScript for more processing, so we need to use `canvas`

and the `createImageData()`

function.

Because pixel-by-pixel processing is needed later in this application, the captured image’s resolution is reduced to 400 x 200px; that means one rhythm grid is 50 x 50 px in the rhythm pattern matrix.

Note: Though most recent laptops/notebooks have embedded WebCams, you will get the best results on Whiteboard Drum from an external camera, because the camera needs to be precisely aimed at the picture on the whiteboard. Also, the selection of input from multiple available devices/cameras is not standardized currently, and cannot be controlled in JavaScript. In Firefox, it is selectable in the permission dialog when connecting, and it can be set up from “contents setup” option of the setup screen in Google Chrome.

### Get the WebCam video

We don’t want to show these parts of the processing on the screen, so first we hide the `video`

:

Now to grab the video:

```
video = document.getElementById("video");
navigator.getUserMedia=navigator.getUserMedia||navigator.webkitGetUserMedia||navigator.mozGetUserMedia;
navigator.getUserMedia({"video":true},
function(stream) {
video.src= window.URL.createObjectURL(stream);
video.play();
},
function(err) {
alert("Camera Error");
});
```

### Capture it and get pixel values

We also hide the `canvas`

:

Then capture our video data on the `canvas`

:

```
function Capture() {
ctxcapture.drawImage(video,0,0,400,200);
imgdatcapture=ctxcapture.getImageData(0,0,400,200);
}
```

The video from the WebCam will be drawn onto the `canvas`

at periodic intervals.

## Image analyzing

Next, we need to get the 400 x 200 pixel values with `getImageData()`

. The analyzing phase analyses the 400 x 200 image data in an 8 x 4 matrix rhythm pattern, where a single matrix grid is 50 x 50 px. All necessary input data is stored in the `imgdatcapture.data`

array in RGBA format, 4 elements per pixel.

```
var pixarray = imgdatcapture.data;
var step;
for(var x = 0; x < 8; ++x) {
var px = x * 50;
if(invert)
step=7-x;
else
step=x;
for(var y = 0; y < 4; ++y) {
var py = y * 50;
var lum = 0;
var red = 0;
for(var dx = 0; dx < 50; ++dx) {
for(var dy = 0; dy < 50; ++dy) {
var offset = ((py + dy) * 400 + px + dx)*4;
lum += pixarray[offset] * 3 + pixarray[offset+1] * 6 + pixarray[offset+2];
red += (pixarray[offset]-pixarray[offset+2]);
}
}
if(lum < lumthresh) {
if(red > redthresh)
rhythmpat[step][y]=2;
else
rhythmpat[step][y]=1;
}
else
rhythmpat[step][y]=0;
}
}
```

This is honest pixel-by-pixel analysis of grid-by-grid loops. In this implementation, the analysis is done for the luminance and redness. If the grid is “dark”, the grid is activated; if it is red, it should be accented.

The luminance calculation uses a simplified matrix — R * 3 + G * 6 + B — that will get ten times the value – meaning – which means getting the value of range 0 to 2550 for each pixel. And the redness R – B is a experimental value because all that is required is a decision of Red or Blue. The result is stored in the `rhythmpat`

array, with a value of 0 for nothing, 1 for blue or 2 for red.

## Sound generation through the Web Audio API

Because the [Web Audio API](https://developer.mozilla.org/en-US/docs/Web_Audio_API) is a very cutting edge technology, it is not yet supported by every web browser. Currently, Google Chrome/Safari/Webkit-based Opera and Firefox (25 or later) support this API. **Note:** Firefox 25 is the latest version released at the end of October.

For other web browsers, I have developed a polyfill that falls back to Flash: [WAAPISim, available on GitHub](https://github.com/g200kg/WAAPISim). It provides almost all functions of the Web Audio API to unsupported browsers, for example Internet Explorer.

Web Audio API is a large scale specification, but in our case, the sound generation part requires just a very simple use of the Web Audio API: load one sound for each instrument and trigger them at the right times. First we create an audio context, taking care of vendor prefixes in the process. Prefixes currently used are webkit or no prefix.

```
audioctx = new (window.AudioContext||window.webkitAudioContext)();
```

Next we load sounds to buffers via XMLHttpRequest. In this case, different sounds for each instrument (bd.wav / sd.wav / hh.wav / cy.wav) are loaded into the `buffers`

array:

```
var buffers = [];
var req = new XMLHttpRequest();
var loadidx = 0;
var files = [
"samples/bd.wav",
"samples/sd.wav",
"samples/hh.wav",
"samples/cy.wav"
];
function LoadBuffers() {
req.open("GET", files[loadidx], true);
req.responseType = "arraybuffer";
req.onload = function() {
if(req.response) {
audioctx.decodeAudioData(req.response,function(b){
buffers[loadidx]=b;
if(++loadidx < files.length)
LoadBuffers();
},function(){});
}
};
req.send();
}
```

The Web Audio API generates sounds by routing graphs of nodes. Whiteboard Drum uses a simple graph that is accessed via `AudioBufferSourceNode`

and `GainNode`

. `AudioBufferSourceNode`

play back the AudioBuffer and route to destination(output) directly (for normal *blue* sound), or route to destination via the `GainNode`

(for accented *red* sound). Because the `AudioBufferSourceNode`

can be used just once, it will be newly created for each trigger.

![](../../assets/c8b64e0716ab3fc1.png)


Preparing the `GainNode`

as the output point for accented sounds is done like this.

```
gain=audioctx.createGain();
gain.gain.value=2;
gain.connect(audioctx.destination);
```

And the trigger function looks like so:

```
function Trigger(instrument,accent,when) {
var src=audioctx.createBufferSource();
src.buffer=buffers[instrument];
if(accent)
src.connect(gain);
else
src.connect(audioctx.destination);
src.start(when);
}
```

All that is left to discuss is the accuracy of the playback timing, according to the rhythm pattern. Though it would be simple to keep creating the triggers with a `setInterval()`

timer, it is not recommended. The timing can be easily messed up by any CPU load.

To get accurate timing, using the time management system embedded in the Web Audio API is recommended. It calculates the `when`

argument of the `Trigger()`

function above.

```
// console.log(nexttick-audioctx.currentTime);
while(nexttick - audioctx.currentTime < 0.3) {
var p = rhythmpat[step];
for(var i = 0; i < 4; ++i)
Trigger(i, p[i], nexttick);
if(++step >= 8)
step = 0;
nexttick += deltatick;
}
```

In Whiteboard Drum, this code controls the core of the functionality. `nexttick`

contains the accurate time (in seconds) of the next step, while `audioctx.currentTime`

is the accurate current time (again, in seconds). Thus, this routine is getting triggered every 300ms - meaning look ahead to 300ms in the future (triggered in advance while nextticktime - currenttime < 0.3). The commented `console.log`

will print the timing margin. While this routine is called periodically, the timing is collapsed if this value is negative.

For more detail, here is a helpful document: [A Tale of Two Clocks - Scheduling Web Audio with Precision](http://www.html5rocks.com/en/tutorials/audio/scheduling/)

## About the UI

Especially in music production software like DAW or VST plugins, the UI is important. Web applications do not have to emulate this exactly, but something similar would be a good idea. Fortunately, the very handy [WebComponent library webaudio-controls](https://github.com/g200kg/webaudio-controls) is available, allowing us to define knobs or sliders with just a single HTML tag.

![](../../assets/78e80abd1414f115.png)


**NOTE**: webaudio-controls uses Polymer.js, which sometimes has stability issues, causing unexpected behavior once in a while, especially when combining it with complex APIs.

## Future work

This is already an interesting application, but it can be improved further. Obviously the camera position adjustment is an issue. Analysis can be more smarter if it has an auto adjustment of the position (using some kind of marker?), and adaptive color detection. Sound generation could also be improved, with more instruments, more steps and more sound effects.

How about a challenge?

Whiteboard Drum is available at [http://www.g200kg.com/whiteboarddrum/](http://www.g200kg.com/whiteboarddrum/), and the [code is on GitHub](https://github.com/g200kg/WhiteboardDrum).

Have a play with it and see what rhythms you can create!

## About
[
Tatsuya Shinyagaito ](http://www.g200kg.com/)

Software Developer, especially related to audio. Developing many VST plugins , Web-based Audio/Music applications. Tatsuya Shinyagaito A.K.A. g200kg

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Sten HougaardNovember 14th, 2013 at 00:45Arin SimeNovember 15th, 2013 at 09:09Pavel DemyanenkoNovember 28th, 2013 at 01:51Abdul QabizDecember 7th, 2013 at 06:23