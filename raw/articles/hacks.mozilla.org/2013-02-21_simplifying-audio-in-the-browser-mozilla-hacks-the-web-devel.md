---
title: Simplifying audio in the browser – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/simplifying-audio-in-the-browser/
author: James Simpson
published: '2013-02-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The last few years have seen tremendous gains in the capabilities of browsers, as the latest HTML5 standards continue to get implemented. We can now render advanced graphics on the canvas, communicate in real-time with WebSockets, access the local filesystem, create offline apps and more. However, the one area that has lagged behind is audio.

The [HTML5 Audio](https://developer.mozilla.org/en-US/docs/HTML/Element/audio) element is great for a small set of uses (such as playing music), but doesn’t work so well when you need low-latency, precision playback.

Over the last year, a new audio standard has been developed for the browser, which gives developers direct access to the audio data. [Web Audio API](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html) allows for high precision and high performing audio playback, as well as many advanced features that just aren’t possible with the HTML5 Audio element. However, support is still limited, and the API is considerably more complex than HTML5 Audio.

## Introducing howler.js

The most obvious use-case for high-performance audio is games, but most developers have had to settle for HTML5 Audio with a Flash fallback to get browser compatibility. My company, [GoldFire Studios](http://goldfirestudios.com), exclusively develops games for the open web, and we set out to find an audio library that offered the kind of audio support a game needs, without relying on antiquated technologies. Unfortunately, there were none to be found, so we wrote our own and open-sourced it: [howler.js](http://howlerjs.com).

Howler.js defaults to Web Audio API and uses HTML5 Audio as the fallback. The library greatly simplifies the API and handles all of the tricky bits automatically. This is a simple example to create an audio sprite (like a CSS sprite, but with an audio file) and play one of the sounds:

```
var sound = new Howl({
urls: ['sounds.mp3', 'sounds.ogg'],
sprite: {
blast: [0, 2000],
laser: [3000, 700],
winner: [5000, 9000]
}
});
// shoot the laser!
sound.play('laser');
```

## Using feature detection

At the most basic level, this works through feature detection. The following snippet detects whether or not Web Audio API is available and creates the audio context if it is. Current support for Web Audio API includes Chrome 10+, Safari 6+, and iOS 6+. It is also in the pipeline for Firefox, Opera and most other mobile browsers.

```
var ctx = null,
usingWebAudio = true;
if (typeof AudioContext !== 'undefined') {
ctx = new AudioContext();
} else if (typeof webkitAudioContext !== 'undefined') {
ctx = new webkitAudioContext();
} else {
usingWebAudio = false;
}
```

Audio support for different codecs varies across browsers as well, so we detect which format is best to use from your provided array of sources with the `canPlayType`

method:

```
var audioTest = new Audio();
var codecs = {
mp3: !!audioTest.canPlayType('audio/mpeg;').replace(/^no$/,''),
ogg: !!audioTest.canPlayType('audio/ogg; codecs="vorbis"').replace(/^no$/,''),
wav: !!audioTest.canPlayType('audio/wav; codecs="1"').replace(/^no$/,''),
m4a: !!(audioTest.canPlayType('audio/x-m4a;') || audioTest.canPlayType('audio/aac;')).replace(/^no$/,''),
webm: !!audioTest.canPlayType('audio/webm; codecs="vorbis"').replace(/^no$/,'')
};
```

## Making it easy

These two key components of howler.js allows the library to automatically select the best method of playback and source file to load and play. From there, the library abstracts away the two different APIs and turns this (a simplified Web Audio API example without all of the extra fallback support and extra features):

```
// create gain node
var gainNode, bufferSource;
gainNode = ctx.createGain();
gainNode.gain.value = volume;
loadBuffer('sound.wav');
var loadBuffer = function(url) {
// load the buffer from the URL
var xhr = new XMLHttpRequest();
xhr.open('GET', url, true);
xhr.responseType = 'arraybuffer';
xhr.onload = function() {
// decode the buffer into an audio source
ctx.decodeAudioData(xhr.response, function(buffer) {
if (buffer) {
bufferSource = ctx.createBufferSource();
bufferSource.buffer = buffer;
bufferSource.connect(gainNode);
bufferSource.start(0);
}
});
};
xhr.send();
};
```

(Note: some old [deprecated names](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#DeprecationNotes) were `createGainNode`

and `noteOn`

, if you see them in other examples on the web)

Into this:

```
var sound = new Howl({
urls: ['sound.wav'],
autoplay: true
});
```

It is important to note that neither Web Audio API nor HTML5 Audio are the perfect solution for everything. As with anything, it is important to select the right tool for the right job. For example, you wouldn’t want to load a large background music file using Web Audio API, as you would have to wait for the entire data source to load before playing. HTML5 Audio is able to play very quickly after the download begins, which is why howler.js also implements an override feature that allows you to mix-and-match the two APIs within your app.

## Audio in the browser is ready

I often hear that audio in the browser is broken and won’t be useable for anything more than basic audio streaming for quite some time. This couldn’t be further from the truth. The tools are already in today’s modern browsers. High quality audio support is here today, and Web Audio API and HTML5 combine to offer truly plugin-free, cross-browser audio support. Browser audio is no longer a second-class citizen, so let’s all stop treating it like one and keep making apps for the open web.

## About
[
James Simpson ](http://goldfirestudios.com)

James is the CEO and founder of [GoldFire Studios](http://goldfirestudios.com), who use HTML5 to develop real-time, multiplayer games for the web. Over the last decade-plus, his games and game-related products have reached millions around the world since starting to develop at age 13. He frequently tweets about Javascript, HTML5, game development and startups [on Twitter](http://twitter.com/GoldFireStudios).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 10 comments

AlexFebruary 21st, 2013 at 06:44Paul MorrisFebruary 21st, 2013 at 09:17James SimpsonFebruary 21st, 2013 at 09:25Paul MorrisFebruary 21st, 2013 at 13:49James SimpsonFebruary 21st, 2013 at 13:50Tom PouceFebruary 21st, 2013 at 10:23Robert Nyman [Editor]February 21st, 2013 at 13:20James CreadyFebruary 21st, 2013 at 14:37Robert Nyman [Editor]February 21st, 2013 at 14:45bekamFebruary 21st, 2013 at 14:32