---
title: Record almost everything in the browser with MediaRecorder – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2016/04/record-almost-everything-in-the-browser-with-mediarecorder/
author: Soledad Penadés
published: '2016-04-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) lets you record media streams, i.e. moving images and audio. The result of these recordings can be, for example, an OGG file, like the ones you use to listen to music.

Browser-wise, we can obtain streams in many ways. Let’s start with something you might be familiar with: we’ll get a stream off a webcam, using the [MediaDevices](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) interface:

```
navigator.mediaDevices.getUserMedia({
audio: true
}).then(function (stream) {
// do something with the stream
}
```


Once we have the stream, we can create the `MediaRecorder` instance:

```
var recorder = new MediaRecorder(stream);
```


This instance is just like other JavaScript objects: it **has methods** we can call, and it **emits events** we can listen to. The most important methods are `start` and `stop`. The most important event is `dataavailable`, which signals that the encoding has finished and the recording is ready for us to consume.

With this knowledge, we can record audio like this:

```
recorder.addEventListener('dataavailable', function(e) {
// e.data contains the audio data! let's associate it to an <audio> element
var el = document.querySelector('audio');
el.src = URL.createObjectURL(e.data);
});
// start recording here...
recorder.start();
// and eventually call this to stop the recording, perhaps on the press of a button
recorder.stop();
```


This was [fairly](https://mozdevs.github.io/MediaRecorder-examples/record-live-audio.html) [short](https://mozdevs.github.io/MediaRecorder-examples/record-live-audio.js), and we were able to encode audio in the browser, natively, without using plugins or loading external libraries.

## What’s new

Now that we know the basics, we’re ready for the new and shiny: **we can finally record video in the browser!**

Video is a complex subject, but `MediaRecorder` makes it easy enough. To demonstrate, we can build on the previous example and record videos instead.

The first thing we’ll do is change the way we initialise the stream. We’ll ask for audio *and* video:

```
navigator.mediaDevices.getUserMedia({
audio: true,
video: true // <-- new!
})
```


The [rest of the code](https://mozdevs.github.io/MediaRecorder-examples/record-video-and-audio.js) is essentially the same, except we set the `src` of a `<video>` element instead of an `<audio>` element. [Try it out.](https://mozdevs.github.io/MediaRecorder-examples/record-video-and-audio.html)

Isn’t that beautiful? Allow me to insist that we didn’t load any external library or transpile existing C or C++ encoders into highly optimised JavaScript with something like Emscripten, asm.js or the way less portable PNaCl. The **code is just 62 lines without any external dependency**, as it makes use of built-in browser features. SIXTY TWO! Including comments!

We’re saving both on bandwidth and processor power consumption, because native code is more efficient for video encoding. We are also reusing code that is used for other platform features anyway. **We all win**.

## Ramping up

`MediaRecorder` doesn’t care what’s in the stream or where the stream came from. This is a very powerful feature: we can modify the streams in various ways using other Web APIs, before we hand them over to a `MediaRecorder` instance. [Web Audio](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) and [WebGL](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Getting_started_with_WebGL) are particularly well suited for manipulating data in an efficient, performant way, so you will see them often used together with `MediaRecorder`.

The [Media Capture collection of new APIs](https://github.com/w3c?utf8=%E2%9C%93&query=mediacapture) (which also includes the Media Recorder API) describes an extension to `<canvas>`, `<audio>`, and `<video>` elements that enables capture of the output of the element as a stream. We can also do stream manipulation, such as creating new streams and adding tracks to them, or decomposing streams into tracks and taking them in and out of other streams as we please, with or without further processing.

But let’s look at all these techniques step-by-step…

### From DOM element to stream

For example, let’s start with recording a video of an animation rendered in a `<canvas>` element. All we do is call the `captureStream()` method on the canvas:

```
var canvasStream = canvas.captureStream();
```


Then we proceed as before, creating an instance of `MediaRecorder` with the stream we just obtained:

```
var recorder = new MediaRecorder(canvasStream);
```


You can see [an example](https://mozdevs.github.io/MediaRecorder-examples/record-canvas-to-video.html) that generates a clip with white noise, which is periodically rendered in a canvas using `requestAnimationFrame`.

*“But this only shows how to record a canvas without external input”*, I hear you saying. And you are correct! To manipulate the incoming images and then record the stream:

```
// set the stream as src for a video element
video.src = URL.createObjectURL(stream)
// periodically draw the video into a canvas
ctx.drawImage(video, 0, 0, width, height);
// get the canvas content as image data
var imageData = ctx.getImageData(0, 0, width, height);
// apply your pixel magic to this bitmap
var data = imageData.data; // data is an array of pixels in RGBA
for (var i = 0; i < data.length; i+=4) {
var average = (data[i] + data[i + 1] + data[i + 2]) / 3;
data[i] = average >= 128 ? 255 : 0; // red
data[i + 1] = average >= 128 ? 255 : 0; // green
data[i + 2] = average >= 128 ? 255 : 0; // blue
// note: i+3 is the alpha channel, we are skipping that one
}
```


In this example, [we apply a simple filter to the input video](https://mozdevs.github.io/MediaRecorder-examples/render-and-filter-video-into-canvas.html) using a canvas. Recording it is a matter of using `captureStream()` on the canvas as well, as you can see in [this other example](https://mozdevs.github.io/MediaRecorder-examples/filter-and-record-live-video.html).

That said, canvas pixel manipulation is not the most efficient solution. WebGL is better for these applications, but it’s also harder to set up and a bit of overkill for this example.

*Note: the spec also describes using the captureStream method on <audio> and <video> elements, but this is not implemented in browsers yet.*

### From `AudioContext` to `stream` to `AudioContext`

Streams can be used both as input and output nodes in Web Audio, by using the right type of audio nodes. This allows us to take an audio stream into the `AudioContext` and manipulate it using the audio graph. We then send the output to another stream, out of the `AudioContext`, for further consuming or processing.

Supposing we have a `stream` and an `audioContext`, we would need to create an instance of [MediaStreamAudioSourceNode](https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamAudioSourceNode) to use the audio of the stream in the audio context:

```
var sourceNode = audioContext.createMediaStreamSource(stream);
```


We could connect this node directly to `audioContext.destination` if we wanted to hear the input:

```
sourceNode.connect(audioContext.destination);
```


Or we could connect it to a filter to modify the sound, and connect the filter to the `audioContext.destination` instead. In this way, we only hear the filtered version and not the original:

```
var filter = audioContext.createBiquadFilter();
filter.connect(audioContext.destination);
sourceNode.connect(filter);
```


If we want to capture this filtered version, we need to create a [MediaStreamAudioDestination](https://developer.mozilla.org/en-US/docs/Web/API/MediaStreamAudioDestinationNode) node, and connect the filter to it, instead of to `audioContext.destination` only:

```
var streamDestination = audioContext.createMediaStreamDestination();
filter.connect(streamDestination);
```


Everything that is connected to `streamDestination` will be streamed out of the audio graph via the `stream` attribute on the node, which we can then use to create an instance of `MediaRecorder` and record filtered sounds:

```
var filteredRecorder = new MediaRecorder(streamDestination.stream);
```


Here’s an example that [applies a filter to the input audio](https://mozdevs.github.io/MediaRecorder-examples/filter-and-record-live-audio.html) before recording.

### All together now

In the above sections we looked at how to process video and audio separately. Complex applications will require us to do both at the same time.

You could use the input stream ‘as is’ to process both in parallel, but there is a catch: since we need to render the stream in a video that has to be playing, you will hear the unprocessed audio. The previous example didn’t have that issue because we requested a stream *without* an audio track. You could think: *“Ah, I can mute the video element!”*, but that also mutes the stream, leaving you with no audio to process.

The solution is to create two new streams, one for video and another for audio, add to them the respective video and audio tracks only, and use them as inputs to process them in parallel. When we’re done, we’ll join the outputs together in a single stream.

Let’s start by creating a new stream, with the `MediaStream` constructor:

```
var videoStream = new MediaStream();
```


We’ll use the `getVideoTracks()` method to list the *video* tracks, and add them to the `videoStream`:

```
var videoTracks = inputStream.getVideoTracks();
videoTracks.forEach(function(track) {
videoStream.addTrack(track);
});
```


Of course there’s also a method to list the audio tracks only. We’ll use it for the `audioStream`:

```
var audioStream = new MediaStream();
var audioTracks = inputStream.getAudioTracks();
audioTracks.forEach(function(track) {
audioStream.addTrack(track);
});
```


We can now use these new streams as inputs for the video and audio processing in parallel.

```
// Manipulate videoStream into a canvas, as shown above
// [...]
// Then get result from canvas stream into videoOutputStream
var videoOutputStream = videoCanvas.captureStream();
// Manipulate audio with an audio context, as shown above
// [...]
// Then get result from audio destination node into audioOutputStream
var audioOutputStream = streamDestination.stream;
```


At the end, we’ll have two output streams: `videoOutputStream` and `audioOutputStream`, which we need to combine together into the final stream. This time, we can use the `getTracks()` method, which will help us make the code a bit more generic:

```
var outputStream = new MediaStream();
[audioOutputStream, videoOutputStream].forEach(function(s) {
s.getTracks().forEach(function(t) {
outputStream.addTrack(t);
});
});
```


And then we can use the `outputStream` as usual as argument for the `MediaRecorder` constructor!

```
var finalRecorder = new MediaRecorder(outputStream);
```


You can have a look at [Boo!](https://mozdevs.github.io/boo/) for a complete demonstration of all these techniques working together. It is a video booth which runs entirely client side, including audio and video processing and encoding.

## Browser support

Right now, browser support isn’t what we would describe as *stellar*, but it’s getting great really quickly.

Desktop Firefox supports video and audio recording and all the other techniques we’ve described above, right *out of the box*, starting with [Firefox Developer Edition 47](https://www.mozilla.org/en-US/firefox/developer/).

`MediaRecorder` doesn’t currently work on Firefox for Android, but we’re looking to enable it quickly, in the Firefox 48 release cycle. The performance on mobile may not be awesome to start with, but we’ll work to get hardware encoding working as soon as we can this year.

There’s partial support in Chrome 47+ and Opera 36+: they only support video recording from WebRTC streams. (Streams coming from canvas with `captureStream()` and streams coming from Web Audio are not currently supported.) You also need to enable the *support for experimental web platform features* flag in `chrome://flags` and `opera://flags` respectively, and restart the browser. The feature (and audio recording) is enabled [by default in Chrome 49](https://developers.google.com/web/updates/2016/01/mediarecorder). Microsoft Edge seems to be open to implement this too at some point— in fact, one of the spec editors works at Microsoft.

This shouldn’t stop you from using the feature as an additional layer of enhancement in your website.

To avoid breaking your code in a silly way or displaying non-functional recording UI buttons or similar when users access the website in a browser where `MediaRecorder` is unavailable, make sure to detect support for it first. Show extra features only if they are supported, to prevent things appearing and disappearing from the screen.

For example, you could check if the `window` object contains a `MediaRecorder` property:

```
if(window.MediaRecorder !== undefined) {
// great! show recording UI
}
```


## Further information and resources

Hopefully this has piqued your interest and you want to learn more about the [ MediaRecorder API](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) and friends!

We have prepared [an online collection of simple examples](https://mozdevs.github.io/MediaRecorder-examples) that demonstrate individual techniques, instead of a single big ‘code monolith’ that tries to demo everything at the same time. You can also clone [the entire repository](https://github.com/mozdevs/MediaRecorder-examples). It’s advisable to use the modern [mediaDevices.getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) syntax, so we have provided a [polyfill](https://github.com/mozdevs/mediaDevices-getUserMedia-polyfill) for compatibility with platforms that haven’t implemented it yet. Please note that the examples *do not* include the polyfill, for simplicity.

As mentioned above, [Boo!](https://mozdevs.github.io/boo/) is a video booth capable of applying video and audio effects in real time and also capturing the output in short clips, all running on the browser. [Source code](https://github.com/mozdevs/boo) is available as well.

And if you want to compare how far we’ve gone since the last time we spoke about `MediaRecorder` in the blog, read [Chris Mills’ take](https://hacks.mozilla.org/2014/06/easy-audio-capture-with-the-mediarecorder-api/), published in June 2014. Hint: we’ve come a very long way.

Let us know about the cool stuff you build!

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## 10 comments

Valentin C.April 7th, 2016 at 10:45Maire ReavyApril 7th, 2016 at 12:06darktrojanApril 8th, 2016 at 02:13Soledad PenadésApril 14th, 2016 at 05:22Szymon NowakApril 13th, 2016 at 07:41Maire ReavyApril 13th, 2016 at 08:32Fuad anuarApril 18th, 2016 at 22:01NatalieApril 22nd, 2016 at 04:52NoitidartMay 1st, 2016 at 04:40Maire ReavyMay 2nd, 2016 at 11:33