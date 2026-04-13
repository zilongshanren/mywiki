---
title: Easy audio capture with the MediaRecorder API – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2014/06/easy-audio-capture-with-the-mediarecorder-api/
author: Chris Mills
published: '2014-06-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder_API) is a simple construct, used inside `Navigator.getUserMedia()`

, which provides an easy way of recording media streams from the user’s input devices and instantly using them in web apps. This article provides a basic guide on how to use MediaRecorder, which is supported in Firefox Desktop/Mobile 25, and Firefox OS 2.0.

## What other options are available?

Capturing media isn’t quite as simple as you’d think on Firefox OS. Using [getUserMedia()](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.getUserMedia) alone yields raw PCM data, which is fine for a stream, but then if you want to capture some of the audio or video you start having to perform manual encoding operations on the PCM data, which can get complex very quickly.

Then you’ve got the [Camera API on Firefox OS](https://developer.mozilla.org/en-US/docs/Web/API/Navigator.mozCameras), which until recently was a certified API, but has been downgraded to privileged recently.

[Web activities](https://developer.mozilla.org/en/docs/WebAPI/Web_Activities) are also available to allow you to grab media via other applications (such as Camera).

the only trouble with these last two options is that they would capture only video with an audio track, and you would still have separate the audio if you just wanted an audio track. MediaRecorder provides an easy way to capture just audio (with video coming later — it is _just_ audio for now.)

## A sample application: Web Dictaphone

![An image of the Web dictaphone sample app - a sine wave sound visualization, then record and stop buttons, then an audio jukebox of recorded tracks that can be played back.](https://mdn.mozillademos.org/files/7885/web-dictaphone.png)


To demonstrate basic usage of the MediaRecorder API, we have built a web-based dictaphone. It allows you to record snippets of audio and then play them back. It even gives you a visualization of your device’s sound input, using the Web Audio API. We’ll concentrate on the recording and playback functionality for this article.

You can see this [demo running live](http://mdn.github.io/web-dictaphone/), or [grab the source code](https://github.com/mdn/web-dictaphone) on Github ([direct zip file download](https://github.com/mdn/web-dictaphone/archive/master.zip).)

## CSS goodies

The HTML is pretty simple in this app, so we won’t go through it here; there are a couple of slightly more interesting bits of CSS worth mentioning, however, so we’ll discuss them below. If you are not interested in CSS and want to get straight to the JavaScript, skip to the “Basic app setup” section.

### Keeping the interface constrained to the viewport, regardless of device height, with calc()

The [calc function](https://developer.mozilla.org/en-US/docs/Web/CSS/calc) is one of those useful little utility features that’s cropped up in CSS that doesn’t look like much initially, but soon starts to make you think “Wow, why didn’t we have this before? Why was CSS2 layout so awkward?” It allows you do a calculation to determine the computed value of a CSS unit, mixing different units in the process.

For example, in Web Dictaphone we have theee main UI areas, stacked vertically. We wanted to give the first two (the header and the controls) fixed heights:

```
header {
height: 70px;
}
.main-controls {
padding-bottom: 0.7rem;
height: 170px;
}
```

However, we wanted to make the third area (which contains the recorded samples you can play back) take up whatever space is left, regardless of the device height. Flexbox could be the answer here, but it’s a bit overkill for such a simple layout. Instead, the problem was solved by making the third container’s height equal to 100% of the parent height, minus the heights and padding of the other two:

```
.sound-clips {
box-shadow: inset 0 3px 4px rgba(0,0,0,0.7);
background-color: rgba(0,0,0,0.1);
height: calc(100% - 240px - 0.7rem);
overflow: scroll;
}
```

**Note**: `calc()`

has good support across modern browsers too, even going back to Internet Explorer 9.

### Checkbox hack for showing/hiding

This is fairly well documented already, but we thought we’d give a mention to the checkbox hack, which abuses the fact that you can click on the `<label>`

of a checkbox to toggle it checked/unchecked. In Web Dictaphone this powers the Information screen, which is shown/hidden by clicking the question mark icon in the top right hand corner. First of all, we style the `<label>`

how we want it, making sure that it has enough z-index to always sit above the other elements and therefore be focusable/clickable:

```
label {
font-family: 'NotoColorEmoji';
font-size: 3rem;
position: absolute;
top: 2px;
right: 3px;
z-index: 5;
cursor: pointer;
}
```

Then we hide the actual checkbox, because we don’t want it cluttering up our UI:

```
input[type=checkbox] {
position: absolute;
top: -100px;
}
```

Next, we style the Information screen (wrapped in an `<aside>`

element) how we want it, give it fixed position so that it doesn’t appear in the layout flow and affect the main UI, transform it to the position we want it to sit in by default, and give it a transition for smooth showing/hiding:

```
aside {
position: fixed;
top: 0;
left: 0;
text-shadow: 1px 1px 1px black;
width: 100%;
height: 100%;
transform: translateX(100%);
transition: 0.6s all;
background-color: #999;
background-image: linear-gradient(to top right, rgba(0,0,0,0), rgba(0,0,0,0.5));
}
```

Last, we write a rule to say that when the checkbox is checked (when we click/focus the label), the adjacent `<aside>`

element will have it’s horizontal translation value changed and transition smoothly into view:

```
input[type=checkbox]:checked ~ aside {
transform: translateX(0);
}
```

## Basic app setup

To grab the media stream we want to capture, we use `getUserMedia()`

(`gUM`

for short). We then use the MediaRecorder API to record the stream, and output each recorded snippet into the source of a generated `<audio>`

element so it can be played back.

First, we’ll add in a forking mechanism to make `gUM`

work, regardless of browser prefixes, and so that getting the app working on other browsers once they start supporting `MediaRecorder`

will be easier in the future.

```
navigator.getUserMedia = ( navigator.getUserMedia ||
navigator.webkitGetUserMedia ||
navigator.mozGetUserMedia ||
navigator.msGetUserMedia);
```

Then we’ll declare some variables for the record and stop buttons, and the `<article>`

that will contain the generated audio players:

```
var record = document.querySelector('.record');
var stop = document.querySelector('.stop');
var soundClips = document.querySelector('.sound-clips');
```

Finally for this section, we set up the basic `gUM`

structure:

```
if (navigator.getUserMedia) {
console.log('getUserMedia supported.');
navigator.getUserMedia (
// constraints - only audio needed for this app
{
audio: true
},
// Success callback
function(stream) {
},
// Error callback
function(err) {
console.log('The following gUM error occured: ' + err);
}
);
} else {
console.log('getUserMedia not supported on your browser!');
}
```

The whole thing is wrapped in a test that checks whether `gUM`

is supported before running anything else. Next, we call `getUserMedia()`

and inside it define:

**The constraints**: Only audio is to be captured; MediaRecorder only supports audio currently anyway.**The success callback**: This code is run once the`gUM`

call has been completed successfully.**The error/failure callback**: The code is run if the`gUM`

call fails for whatever reason.

**Note**: All of the code below is placed inside the gUM success callback.

## Capturing the media stream

Once `gUM`

has grabbed a media stream successfully, you create a new Media Recorder instance with the `MediaRecorder()`

constructor and pass it the stream directly. This is your entry point into using the MediaRecorder API — the stream is now ready to be captured straight into a Blob, in the default encoding format of your browser.

```
var mediaRecorder = new MediaRecorder(stream);
```

There are a series of methods available in the [MediaRecorder interface](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) that allow you to control recording of the media stream; in Web Dictaphone we just make use of two. First of all, `MediaRecorder.start()`

is used to start recording the stream into a Blob once the record button is pressed:

```
record.onclick = function() {
mediaRecorder.start();
console.log(mediaRecorder.state);
console.log("recorder started");
record.style.background = "red";
record.style.color = "black";
}
```

When the MediaRecorder is recording, the `MediaRecorder.state`

property will return a value of “recording”.

Second, we use the `MediaRecorder.stop()`

method to stop the recording when the stop button is pressed, and finalize the Blob ready for use somewhere else in our application.

```
stop.onclick = function() {
mediaRecorder.stop();
console.log(mediaRecorder.state);
console.log("recorder stopped");
record.style.background = "";
record.style.color = "";
}
```

When recording has been stopped, the `state`

property returns a value of “inactive”.

Note that there are other ways that a Blob can be finalized and ready for use:

- If the media stream runs out (e.g. if you were grabbing a song track and the track ended), the
`Blob`

is finalized. - If the
`MediaRecorder.requestData()`

method is invoked, the`Blob`

is finalized, but recording then continues in a new`Blob`

. - If you include a timeslice property when invoking the
`start()`

method — for example`start(10000)`

— then a new`Blob`

will be finalized (and a new recording started) each time that number of milliseconds has passed.

## Grabbing and using the blob

When the blob is finalized and ready for use as described above, a `dataavailable`

event is fired, which can be handled using a `mediaRecorder.ondataavailable`

handler:

```
mediaRecorder.ondataavailable = function(e) {
console.log("data available");
var clipName = prompt('Enter a name for your sound clip');
var clipContainer = document.createElement('article');
var clipLabel = document.createElement('p');
var audio = document.createElement('audio');
var deleteButton = document.createElement('button');
clipContainer.classList.add('clip');
audio.setAttribute('controls', '');
deleteButton.innerHTML = "Delete";
clipLabel.innerHTML = clipName;
clipContainer.appendChild(audio);
clipContainer.appendChild(clipLabel);
clipContainer.appendChild(deleteButton);
soundClips.appendChild(clipContainer);
var audioURL = window.URL.createObjectURL(e.data);
audio.src = audioURL;
deleteButton.onclick = function(e) {
evtTgt = e.target;
evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
}
}
```

Let’s go through the above code and look at what’s happening.

First, we display a prompt asking the user to name their clip.

Next, we create an HTML structure like the following, inserting it into our clip container, which is a `<section>`

element.

```
```
*your clip name*


After that, we create an object URL pointing to the event’s `data`

attribute, using `window.URL.createObjectURL(e.data)`

: this attribute contains the Blob of the recorded audio. We then set the value of the `<audio>`

element’s `src`

attribute to the object URL, so that when the play button is pressed on the audio player, it will play the Blob.

Finally, we set an `onclick`

handler on the delete button to be a function that deletes the whole clip HTML structure.

## Conclusion

And there you have it; MediaRecorder should serve to make your app media recording needs easier. Have a play around with it and let us know what you think: we are looking forward to seeing what you’ll build!

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

Brett ZamirJune 11th, 2014 at 02:35Chris MillsJune 11th, 2014 at 02:44AlejandroJune 11th, 2014 at 05:30Chris MillsJune 11th, 2014 at 07:31Sam DuttonJune 11th, 2014 at 06:33lcamachoJune 11th, 2014 at 07:17Chris MillsJune 11th, 2014 at 07:31Mindaugas J.June 11th, 2014 at 11:39omitsolutionsJune 24th, 2014 at 01:54