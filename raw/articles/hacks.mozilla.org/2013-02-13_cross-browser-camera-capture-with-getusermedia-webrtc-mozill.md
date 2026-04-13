---
title: Cross-browser camera capture with getUserMedia/WebRTC – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2013/02/cross-browser-camera-capture-with-getusermediawebrtc/
author: Daniel Davis
published: '2013-02-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Overview

With Firefox adding [support for getUserMedia](http://caniuse.com/stream), three of the major desktop browsers now have the ability to get data from cameras without the use of plugins. As it’s still early days, however, the implementations differ slightly between browsers. Below is an example of how to work around these differences and a script to do the heavy lifting for you, but first, an overview of how the three browsers stack up.

| Firefox 18 | Opera 12 | Chrome 24 | |
|---|---|---|---|
| Requires vendor prefix | Yes (moz) | No | Yes (webkit) |
Triggered with `autoplay` attribute |
No | Yes | Yes |
| Requires enabling by user | Yes
|
No | No |
Firing of `playing` event |
Repeatedly | Once | Once |
Supports `file://` protocol |
Yes | Yes | No |
| Tab playing notification | None | Icon | Animated icon |
| Permission request | Each page load | First page load only | Each page load |

*getUserMedia has to be enabled in Firefox by setting the media.peerconnection.enabled option to true in about:config.*


There are a few more differences once we start coding so let’s walk through it. Our recipe for getUserMedia success will be broken down into the following easy steps:

[A helping of HTML5](https://hacks.mozilla.org#html5)[A dollop of feature detection](https://hacks.mozilla.org#detection)[A spoonful of streaming](https://hacks.mozilla.org#streaming)[Ready for serving](https://hacks.mozilla.org#serving)[A final tip](https://hacks.mozilla.org#events)

Deep breath – here we go…

## A helping of HTML5

Our main task in this short tutorial is just to get a moving image displaying in a page. In that respect, it’s no different to regular video so the first step is a simple `<video>`

element in our HTML:

That’s it. No `controls`

, no `src`

, no nothing.

Over to the JavaScript, and obviously we need to get a reference to the `<video>`

element, which we can do like so (or alternatively with an `id`

):

`var video = document.querySelector('video');`

## A dollop of feature detection

Now it gets interesting as we check for getUserMedia support. We’re definitely not going to use unreliable user agent sniffing for this — no, we’ll do it the easy way by checking for the `navigator.getUserMedia`

object. This is prefixed in Firefox and Chrome so first it’s handy to assign it to a common object for all browsers. While we’re at it, let’s do it for the `window.URL`

object as well which we’ll use later on.

```
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
```

And next, the actual existence checking:

```
if (navigator.getUserMedia) {
// Call the getUserMedia method here
} else {
console.log('Native device media streaming (getUserMedia) not supported in this browser.');
// Display a friendly "sorry" message to the user.
}
```

If getUserMedia is supported, we need to pass it three arguments — an options object, a success callback function and an error callback function. Note that the error callback is required in Firefox but optional in Opera and Chrome. The options argument is a JSON-style object that specifies whether audio, video or both are to be used. The following example code is for video only:

`navigator.getUserMedia({video: true}, successCallback, errorCallback);`

### Dialogs requesting camera access

![](../../assets/1408c5acb3468aee.png)

![](../../assets/1f08b530b11a819a.png)

![](../../assets/379a7ba95846108f.png)

## A spoonful of streaming

So far so good, so let’s define what happens next. The success callback function receives an argument containing the video stream from the camera and we want to send that stream to our `<video>`

element. We do this by setting its `src`

attribute but there are a couple of things to bear in mind:

- Firefox uses the
`mozSrcObject`

attribute whereas Opera and Chrome use`src`

. - Chrome uses the
`createObjectURL`

method whereas Firefox and Opera send the stream directly.

With Firefox, `video.mozSrcObject`

is initially null rather than undefined so we can rely on this to detect for Firefox’s support ([hat tip to Florent](https://hacks.mozilla.org/2013/02/cross-browser-camera-capture-with-getusermediawebrtc/comment-page-1/#comment-1995239)). Once the stream knows where to go we can tell the video stream to play.

```
function successCallback(stream) {
if (video.mozSrcObject !== undefined) {
video.mozSrcObject = stream;
} else {
video.src = (window.URL && window.URL.createObjectURL(stream)) || stream;
};
video.play();
}
```

## Ready for serving

And there you have it. Add a simple error callback function and we have a working cross-browser script which looks something like this:

```
window.addEventListener('DOMContentLoaded', function() {
'use strict';
var video = document.querySelector('video');
function successCallback(stream) {
// Set the source of the video element with the stream from the camera
if (video.mozSrcObject !== undefined) {
video.mozSrcObject = stream;
} else {
video.src = (window.URL && window.URL.createObjectURL(stream)) || stream;
}
video.play();
}
function errorCallback(error) {
console.error('An error occurred: [CODE ' + error.code + ']');
// Display a friendly "sorry" message to the user
}
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
window.URL = window.URL || window.webkitURL || window.mozURL || window.msURL;
// Call the getUserMedia method with our callback functions
if (navigator.getUserMedia) {
navigator.getUserMedia({video: true}, successCallback, errorCallback);
} else {
console.log('Native web camera streaming (getUserMedia) not supported in this browser.');
// Display a friendly "sorry" message to the user
}
}, false);
```

## Available on GitHub

To get started with accessing getUserMedia in a cross web browser fashion, we have also put [a working example on GitHub: GumWrapper](https://github.com/tagawa/GumWrapper).

## A final tip

If you want to do anything fancy with the camera’s stream like capture a still image or add fancy effects, you’ll probably want to send its data to a canvas context. You can use [ drawImage()](https://developer.mozilla.org/en-US/docs/HTML/Canvas/Tutorial/Using_images#drawImage) for this, in which case you’ll need the dimensions of the video. These are available through the

`video.videoWidth`

and `video.videoHeight`

properties but beware — they’re only set when the browser has information about the stream. This means you have to listen for certain events before you can get these properties. There are a few relevant events, always fired in the following order:`play`

`loadedmetadata`

`loadeddata`

`playing`


The `play`

event is fired after the `video.play()`

method is called but there may be a slight delay before the video actually starts playing. That’s where the `playing`

event comes in but note that it’s fired repeatedly in Firefox while the stream or video is playing. Before that are a couple of data events, the first of which is just for metadata, however in Firefox this doesn’t include video dimensions. Consequently, the most reliable event to listen for is the `loadeddata`

event — you can then be sure of knowing the width and height of the video stream. You could code it up like this:

```
video.addEventListener('loadeddata', function() {
console.log('Video dimensions: ' + video.videoWidth + ' x ' + video.videoHeight);
}, false);
```

Incidentally, you could also use the stream’s dimensions as a further error check, for example checking whether the width and height are above 0. This would avoid problems such as the user’s webcam being broken or simply not plugged in.

And there you have it. I’m sure the differences between browsers will disappear as the technology matures but for the time being, the above code should help you on your way.

## About
[
Daniel Davis ](http://about.me/danieldavis)

[@ourmaninjapan](http://twitter.com/ourmaninjapan) Daniel's work experience includes developer evangelism at Opera Software and web development, IT training and project management in both the UK and Japan. Currently a staff member of the Japanese "html5j" developer community with a soft spot for ukuleles.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 25 comments

Arindam ChakrabortyFebruary 13th, 2013 at 08:12Robert Nyman [Editor]February 13th, 2013 at 09:05Brett ZamirFebruary 13th, 2013 at 19:49VNFebruary 14th, 2013 at 11:56Robert Nyman [Editor]February 15th, 2013 at 05:11Daniel DavisFebruary 15th, 2013 at 07:01Florent F.February 14th, 2013 at 13:16Daniel DavisFebruary 15th, 2013 at 07:43udevFebruary 17th, 2013 at 00:57Robert Nyman [Editor]February 18th, 2013 at 03:00CraigFebruary 18th, 2013 at 16:58Robert Nyman [Editor]February 19th, 2013 at 01:44jamie McDonnellFebruary 21st, 2013 at 03:43Robert Nyman [Editor]February 21st, 2013 at 04:11jamie McDonnellFebruary 21st, 2013 at 07:25jamie McDonnellFebruary 21st, 2013 at 07:28Robert Nyman [Editor]February 21st, 2013 at 13:28Merih AkarFebruary 26th, 2013 at 08:57Robert Nyman [Editor]February 26th, 2013 at 16:47Merih AkarFebruary 26th, 2013 at 18:04Robert Nyman [Editor]February 26th, 2013 at 18:09Hasit MistryApril 4th, 2013 at 11:58Robert Nyman [Editor]April 5th, 2013 at 01:28guska076April 10th, 2013 at 06:14Robert Nyman [Editor]April 10th, 2013 at 07:49