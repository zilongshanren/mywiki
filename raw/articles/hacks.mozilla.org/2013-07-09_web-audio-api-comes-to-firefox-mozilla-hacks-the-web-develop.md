---
title: Web Audio API comes to Firefox – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/07/web-audio-api-comes-to-firefox/
author: Ehsan Akhgari
published: '2013-07-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We have been working on implementing the [Web Audio API](https://developer.mozilla.org/en-US/docs/Web_Audio_API) in Firefox for a while now, and we currently have basic support for the API implemented on [Firefox Nightly](http://nightly.mozilla.org/) and [Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/). Web Audio provides a number of cool features that can be used in order to create music applications, games, and basically any application which requires advanced audio processing.

## Features

Here are some examples of the features:

- Scheduling events to happen at exact times during audio playbacks
- Various types of audio filters to create effects such as echo, noise cancellation, etc.
- Sound synthesis to create electronic music
- 3D positional audio to simulate effects such as a sound source moving around the scene in a game
- Integration for WebRTC to apply effects to sound coming in from external input (a WebRTC call, a guitar plugged in to your device, etc.) or to sound which is transmitted to the other party in a WebRTC call
- Analysing the audio data in order to create sound visualizers, etc.

## Code sample

Here is a simple example of what you can build with Web Audio. Let’s imagine that you’re working on a game, and you want to play a gunshot sound as soon as the player clicks on your game canvas. In order to make sure that you’re not affected by things like network delay, the audio decoder delay, etc., you can use Web Audio to preload the audio into a buffer as part of the loading process of your game, and schedule it precisely when you receive a click event.

In order to create a neater sound effect, we can additionally loop the sound while the mouse is pressed, and create a fade-out effect when you release the mouse. The following code sample shows how to do that:

```
// Load the sound file from the network
var decodedBuffer;
var ctx = new AudioContext();
var xhr = new XMLHttpRequest();
xhr.open("GET", "gunshot.ogg", true);
xhr.responseType = "arraybuffer";
xhr.send();
xhr.onload = function() {
// At this point, xhr.response contains the encoded data for gunshot.ogg,
// so let's decode it into an AudioBuffer first.
ctx.decodeAudioData(xhr.response, function onDecodeSuccess(buffer) {
decodedBuffer = buffer;
}, function onDecodeFailure() { alert('decode error!'); });
};
// Set up a mousedown/mouseup handler on your game canvas
canvas.addEventListener("mousedown", function onMouseDown() {
var src = ctx.createBufferSource();
src.buffer = decodedBuffer; // play back the decoded buffer
src.loop = true; // set the sound to loop while the mouse is down
var gain = ctx.createGain(); // create a gain node in order to create the fade-out effect when the mouse is released
src.connect(gain);
gain.connect(ctx.destination);
canvas.src = src; // save a reference to our nodes to use it later
canvas.gain = gain;
src.start(0); // start playback immediately
}, false);
canvas.addEventListener("mouseup", function onMouseUp() {
var src = canvas.src, gain = canvas.gain;
src.stop(ctx.currentTime + 0.2); // set up playback to stop in 200ms
gain.gain.setValueAtTime(1.0, ctx.currentTime);
gain.gain.linearRampToValueAtTime(0.001, ctx.currentTime + 0.2); // set up the sound to fade out within 200ms
}, false);
```

## The first WebAudio implementations and WebKit

The Web Audio API was first implemented in Google Chrome using the `webkitAudioContext`

prefix. We have been discussing the API on the W3C Audio Working Group and have been trying to fix some of the problems in the earlier versions of the API. In some places, doing that means that we needed to break backwards compatibility of code which targets `webkitAudioContext`

.

There is a [guide on how to port those applications to the standard API](https://developer.mozilla.org/en-US/docs/Web_Audio_API/Porting_webkitAudioContext_code_to_standards_based_AudioContext). There is also the [ webkitAudioContext monkeypatch](https://github.com/cwilso/webkitAudioContext-MonkeyPatch) available which handles some of these changes automatically, which can help to make some of the code targeting `webkitAudioContext`

to work in the standard API.

## The implementation in Firefox

In Firefox, we have implemented the standard API. If you’re a web developer interested in creating advanced audio applications on the web, it would be really helpful for you to review [Porting webkitAudioContext code to standards based AudioContext](https://developer.mozilla.org/en-US/docs/Web_Audio_API/Porting_webkitAudioContext_code_to_standards_based_AudioContext) to get a sense of all of the non-backwards-compatible changes made to the API through the standardization process.

We are currently hoping to release Web Audio support in Firefox 24 for desktop and Android, unless something unexpected happens that would cause us to delay the release, but you can use most parts of the API on [Nightly](http://nightly.mozilla.org/) and Aurora right now.

There are still some missing bits and pieces, including `MediaStreamAudioSourceNode`

, `MediaElementAudioSourceNode`

, `OscillatorNode`

and HRTF panning for `PannerNode`

. We’ll add support for the remaining parts of the API in the coming weeks on Nightly and [Firefox Aurora](http://www.mozilla.org/en-US/firefox/aurora/).

## About Ehsan Akhgari

Ehsan works on various bits and pieces in Gecko.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

Jan KrutischJuly 9th, 2013 at 14:42Robert Nyman [Editor]July 9th, 2013 at 16:41Carl DavidáJuly 9th, 2013 at 17:52Ehsan AkhgariJuly 9th, 2013 at 18:01Robert Nyman [Editor]July 10th, 2013 at 01:48phi2xJuly 9th, 2013 at 23:05Clayton GulickJuly 10th, 2013 at 09:27Robert Nyman [Editor]July 10th, 2013 at 11:06NixonJuly 10th, 2013 at 10:10BingoJuly 10th, 2013 at 22:55BozhoJuly 12th, 2013 at 00:11Jan KrutischJuly 12th, 2013 at 01:01Kong Ying JennyJuly 12th, 2013 at 07:03AmpJuly 12th, 2013 at 07:30pablocubicoJuly 25th, 2013 at 07:34Ehsan AkhgariJuly 25th, 2013 at 14:48