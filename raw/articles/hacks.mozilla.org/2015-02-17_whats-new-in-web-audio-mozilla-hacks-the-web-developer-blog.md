---
title: What’s new in Web Audio – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/02/whats-new-in-web-audio/
author: Soledad Penadés
published: '2015-02-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Introduction

It’s been a while since we said anything on Hacks about the [Web Audio API](http://webaudio.github.io/web-audio-api/). However, with Firefox 37/38 hitting our Developer Edition/Nightly browser channels, there are some interesting new features to talk about!

This article presents you with some new Web Audio tricks to watch out for, such as the new `StereoPannerNode`, promise-based methods, and more.

## Simple stereo panning

Firefox 37 introduces the [StereoPannerNode](https://developer.mozilla.org/docs/Web/API/StereoPannerNode) interface, which allows you to add a stereo panning effect to an audio source simply and easily. It takes a single property: `pan`—an [a-rate](http://webaudio.github.io/web-audio-api/#a-rate) AudioParam that can accept numeric values between -1.0 (full left channel pan) and 1.0 (full right channel pan).

### But don’t we already have a PannerNode?

You may have already used the older [PannerNode](https://developer.mozilla.org/docs/Web/API/PannerNode) interface, which allows you to position sounds in 3D. Connecting a sound source to a `PannerNode`

causes it to be “spatialised”, meaning that it is placed into a 3D space and you can then specify the position of the listener inside. The browser then figures out how to make the sources sound, applying panning and doppler shift effects, and other nice 3D “artifacts” if the sounds are moving over time, etc:

```
var audioContext = new AudioContext();
var pannerNode = audioContext.createPanner();
// The listener is 100 units to the right of the 3D origin
audioContext.listener.setPosition(100, 0, 0);
// The panner is in the 3D origin
pannerNode.setPosition(0, 0, 0);
```

This works well with WebGL-based games as both environments use similar units for positioning—an array of x, y, z values. So you could easily update the position, orientation, and velocity of the `PannerNode`s as you update the position of the entities in your 3D scene.

But what if you are just building a conventional music player where the songs are already stereo tracks, and you actually don’t care at all about 3D? You have to go through a more complicated setup process than should be necessary, and it can also be computationally more expensive. With the increased usage of mobile devices, every operation you don’t perform is a bit more battery life you save, and users of your website will love you for it.

### Enter StereoPannerNode

`StereoPannerNode` is a much better solution for simple stereo use cases, as described above. You don’t need to care about the listener’s position; you just need to connect source nodes that you want to spatialise to a `StereoPannerNode` instance, then use the `pan` parameter.

To use a stereo panner, first create a `StereoPannerNode` using [createStereoPanner()](https://developer.mozilla.org/docs/Web/API/AudioContext.createStereoPanner), and then connect it to your audio source. For example:

```
var audioCtx = window.AudioContext();
// You can use any type of source
var source = audioCtx.createMediaElementSource(myAudio);
var panNode = audioCtx.createStereoPanner();
source.connect(panNode);
panNode.connect(audioCtx.destination);
```

To change the amount of panning applied, you just update the `pan` property value:

```
panNode.pan.value = 0.5; // places the sound halfway to the right
panNode.pan.value = 0.0; // centers it
panNode.pan.value = -0.5; // places the sound halfway to the left
```

You can see [http://mdn.github.io/stereo-panner-node/](http://mdn.github.io/stereo-panner-node/) for a complete example.

Also, since `pan` is an [a-rate AudioParam](http://webaudio.github.io/web-audio-api/#a-rate) you can design nice smooth curves using parameter automation, and the values will be updated per sample. Trying to do this kind of change over time would sound weird and unnatural if you updated the value over multiple [requestAnimationFrame](https://developer.mozilla.org/docs/Web/API/window.requestAnimationFrame) calls. And you can’t automate `PannerNode` positions either.

For example, this is how you could set up a panning transition from left to right that lasts two seconds:

```
panNode.pan.setValueAtTime(-1, audioContext.currentTime);
panNode.pan.linearRampToValueAtTime(1, audioContext.currentTime + 2);
```

The browser will take care of updating the `pan` value for you. And now, as of recently, you can also visualise these curves using the Firefox Devtools [Web Audio Editor](http://hacks.mozilla.org/2014/06/introducing-the-web-audio-editor-in-firefox-developer-tools/).

### Detecting when StereoPannerNode is available

It might be the case that the Web Audio implementation you’re using has not implemented this type of node yet. (At the time of this writing, it is supported in Firefox 37 and Chrome 42 only.) If you try to use `StereoPannerNode` in these cases, you’re going to generate a beautiful `undefined is not a function` error instead.

To make sure `StereoPannerNode`s are available, just check whether the `createStereoPanner()` method exists in your `AudioContext`:

```
if (audioContext.createStereoPanner) {
// StereoPannerNode is supported!
}
```

If it doesn’t, you will need to revert back to the older `PannerNode`.

## Changes to the default `PannerNode` panning algorithm

The default panning algorithm type used in `PannerNode`s used to be `HRTF`, which is a high quality algorithm that rendered its output using a convolution with human-based data (thus it’s very realistic). However it is also *very* computationally expensive, requiring the processing to be run in additional threads to ensure smooth playback.

Authors often don’t require such a high level of quality and just need something that is *good enough*, so the default `PannerNode.type` is now `equalpower`, which is much cheaper to compute. If you want to go back to using the high quality panning algorithm instead, you just need to change the type:

```
pannerNodeInstance.type = 'HRTF';
```

Incidentally, a `PannerNode` using `type = 'equalpower'` results in the same algorithm that `StereoPannerNode` uses.

## Promise-based methods

Another interesting feature that has been recently added to the Web Audio spec is [Promise](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise)-based versions of certain methods. These are [OfflineAudioContext.startRendering()](https://developer.mozilla.org/docs/Web/API/OfflineAudioContext.startRendering_%28promise%29) and [AudioContext.decodeAudioData](https://developer.mozilla.org/docs/Web/API/AudioContext.decodeAudioData).

The below sections show how the method calls look with and without Promises.

### OfflineAudioContext.startRendering()

Let’s suppose we want to generate a minute of audio at 44100 Hz. We’d first create the context:

```
var offlineAudioContext = new OfflineAudioContext(2, 44100 * 60, 44100);
```

#### Classic code

```
offlineAudioContext.addEventListener('oncomplete', function(e) {
// rendering complete, results are at `e.renderedBuffer`
});
offlineAudioContext.startRendering();
```

#### Promise-based code

```
offlineAudioContext.startRendering().then(function(renderedBuffer) {
// rendered results in `renderedBuffer`
});
```

### AudioContext.decodeAudioData

Likewise, when decoding an audio track we would create the context first:

```
var audioContext = new AudioContext();
```

#### Classic code

```
audioContext.decodeAudioData(data, function onSuccess(decodedBuffer) {
// decoded data is decodedBuffer
}, function onError(e) {
// guess what... something didn't work out well!
});
```

#### Promise-based code

```
audioContext.decodeAudioData(data).then(function(decodedBuffer) {
// decoded data is decodedBuffer
}, function onError(e) {
// guess what... something didn't work out well!
});
```

In both cases the differences don’t seem major, but if you’re composing the results of promises sequentially or if you’re waiting on an event to complete before calling several other methods, promises are really helpful to avoid *callback hell*.

### Detecting support for Promise-based methods

Again, you don’t want to get the dreaded `undefined is not a function` error message if the browser you’re running your code on doesn’t support these new versions of the methods.

A quick way to check for support: look at the returned type of these calls. If they return a Promise, we’re in luck. If they don’t, we have to keep using the old methods:

```
if((new OfflineAudioContext(1, 1, 44100)).startRendering() != undefined) {
// Promise with startRendering is supported
}
if((new AudioContext()).decodeAudioData(new Uint8Array(1)) != undefined) {
// Promise with decodeAudioData is supported
}
```

## Audio workers

Although the spec has not been finalised and they are not implemented in any browser yet, it is also worth giving a mention to Audio Workers, which —you’ve guessed it— are a specialised type of web worker for use by Web Audio code.

Audio Workers will replace the almost-obsolete [ScriptProcessorNode](https://developer.mozilla.org/en-US/docs/Web/API/ScriptProcessorNode). Originally, this was the way to run your own custom nodes inside the audio graph, but they actually run on the main thread causing all sorts of problems, from audio glitches (if the main thread becomes stalled) to unresponsive UI code (if the `ScriptProcessorNode`

s aren’t fast enough to process their data).

The biggest feature of audio workers is that they run in their own separate thread, just like any other [Worker](https://developer.mozilla.org/docs/Web/API/Worker). This ensures that audio processing is prioritised and we avoid sound glitches, which human ears are very sensitive to.

There is an ongoing discussion on the w3c [web audio list](https://lists.w3.org/Archives/Public/public-audio/); if you are interested in this and other Web Audio developments, you should go check it out.

Exciting times for audio on the Web!

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 3 comments

FelipeFebruary 17th, 2015 at 18:49soleFebruary 19th, 2015 at 09:41Lara HMarch 6th, 2015 at 03:51