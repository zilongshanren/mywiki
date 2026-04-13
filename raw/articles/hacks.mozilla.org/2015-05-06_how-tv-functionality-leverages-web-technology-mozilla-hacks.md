---
title: How TV Functionality Leverages Web Technology – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/05/how-tv-functionality-leverages-web-technology/
author: Mozilla
published: '2015-05-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The convergence of Internet-based IPTV, Video-on-Demand (VoD) and traditional broadcasting is happening now. As more and more web technology comes to television, the gap between web apps and native apps is rapidly narrowing.

Firefox OS now supports the [TV Manager API](http://seanyhlin.github.io/TV-Manager-API/), a baseline of the [W3C TV Control API](http://w3c.github.io/tvapi/spec/) (the editor’s draft driven by the TV Control API Community Group), which allows web-based applications to acquire information such as the Electronic Program Guide (or EPG) from service providers, and also to manage native TV hardware such as tuners and remotes. Firefox OS also relies on multiple API specifications to fully support TV functionality on a web platform. Some APIs are still on the road to becoming standards. Here is an overview of some common TV functions which can be implemented today via these Web APIs.

## Tuner, channel, and EPG management

One of the primary goals of the [TV Control API](http://w3c.github.io/tvapi/spec/) is to enable standard use cases, such as channel switching and other activities generally available and expected in conventional remote controls. The API exposes specific tuner, channel, and EPG information to the web app and also allows indirect interactions with the tuner modules. Some applications, like virtual remote control, are easy to enable with this API. And the web content has the flexibility to manipulate multiple tuners if resource-permitted. In addition, event-driven notifications about channel scanning status and EPG updates provide a dynamic way to access broadcasting information.

The following example shows how to get the available tuners and set the current playing source via the API.

```
// Retrieve all the available tuners.
navigator.tv.getTuners().then(function(tuners) {
// Just use the first tuner.
var tuner = tuners[0];
// Set the 'oncurrentsourcechanged' event handler.
tuner.oncurrentsourcechanged = function(event) {
// The current source has changed.
};
// Get the supported source types for the tuner.
var sourceTypes = tuner.getSupportedSourceTypes();
// Just use the first source.
tuner.setCurrentSource(sourceTypes[0]).then(function() {
// Succeeded to set the source.
}, function(error) {
// Failed to set the source.
});
}, function(error) {
// Failed to get tuners.
});
```


## Streaming

When it comes to TV streaming, multiple web specifications work together. The [Media Capture and Streams API](http://www.w3.org/TR/mediacapture-streams/) enables access to multimedia streams from local devices, and it defines a `MediaStream`

interface to carry video/audio tracks and other stream-relevant attributes. The current streaming data for each tuner can be wrapped in a `MediaStream`

instance and retrieved via the [TV Control API](http://w3c.github.io/tvapi/spec/). Then the web content can start playing the stream by assigning it to HTML5 `<a href="http://www.w3.org/TR/html5/embedded-content-0.html#the-video-element" target="_blank"><video></a>`

elements. Here’s an example:

```
// Retrieve all the available TV tuners and then play
// the stream for the first tuner.
navigator.tv.getTuners().then(function(tuners) {
// Assuming a video element is already accessible to
// variable |video|, just assign the stream to it.
video.srcObject = tuners[0].stream;
});
```


The [Media Capture and Streams API](http://www.w3.org/TR/mediacapture-streams/) and the HTML5 `<a href="http://www.w3.org/TR/html5/embedded-content-0.html#the-video-element" target="_blank"><video></a>`

element provide attributes and methods to help manage streaming contents. Combining the APIs and HTML5 elements makes the development of some advanced TV streaming scenarios, such as concurrent display for multiple streams (i.e., Picture-in-Picture), easier to accomplish and more flexible.

## Track management

While playing video streams, sometimes the media content provides multiple audio channels and even includes subtitles. For instance, a film or a sports show may be broadcast with multiple supported languages available for the viewer to select. Thus, there are two lists of `VideoTrack`

and `AudioTrack`

objects in the HTML5 `<a href="http://www.w3.org/TR/html5/embedded-content-0.html#the-video-element" target="_blank"><video></a>`

element to help the web content utilize available video and audio tracks respectively. Meanwhile, the [Media Capture and Streams API](http://www.w3.org/TR/mediacapture-streams/) also provides certain methods to dynamically manage associated media tracks. With this flexibility, web content is able to play a video stream that’s originated from another connected device, such as a camera.

The HTML5 `<a href="http://www.w3.org/TR/html5/embedded-content-0.html#the-video-element" target="_blank"><video></a>`

element has a list of `TextTrack`

instances. These tracks can be associated with a specific video tag to represent different instances, such as subtitles, captions, and metadata. In addition, multiple `TextTrackCue`

objects containing time-sensitive data can be affiliated with them, and used to control timing of the display for subtitles and captions.

## Recording

The [MediaStream Recording API](http://www.w3.org/TR/mediastream-recording/) provides a `MediaRecorder`

interface to fulfill recording requirements over the `MediaStream`

. It lets the web content select the appropriate supported encoding format for the stream, and also enables the recorded media to be accessed either as a whole blob or in smaller buffers.

In cooperation with the [Task Scheduler API](http://www.w3.org/TR/task-scheduler/) and [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker_API), you can even add DVR-style scheduling functionality to your web app or web-driven device. On the other hand, the EPG data retrieved via [TV Control API](http://w3c.github.io/tvapi/spec/) may also help the application record specific TV programs.

## Emergency alert

Sometimes a public alert may be sent out via TV broadcasting or other communication systems when an emergency or natural disaster occurs such an earthquake, tsunami, or hurricane. A corresponding event-triggering mechanism included with the [TV Control API](http://w3c.github.io/tvapi/spec/) can be used to help a web application manage an alert.

```
// Assuming variable |currentSource| is associated with
// the playing TV signal.
currentSource.onemergencyalerted = function (event) {
var type = event.type; // i.e. “Earthquake”.
var severityLevel = event.severityLevel;
var description = event.description;
// Display the emergency information.
// (More attributes could be available.)
};
```


## Final thoughts

TV broadcast mechanisms and applications are on a fast track to evolve rapidly, as is the web technology. Since many of the web specifications and APIs mentioned are still in the standardization progress, more functionality or further improvements might be added to make television experience more *webby*. As always, you can contribute to the evolution of these Web APIs by following along on relevant standards mailing lists and filing bugs when you find them.

## 10 comments

Pete CoxMay 6th, 2015 at 08:04Marco ChenMay 10th, 2015 at 20:46IvanMay 6th, 2015 at 10:32AndréMay 7th, 2015 at 01:41Clinton Gallagher @virtualCableTVMay 6th, 2015 at 16:19Brett ZamirMay 8th, 2015 at 03:06Brett ZamirMay 8th, 2015 at 03:22Marco ChenMay 10th, 2015 at 20:59Brett ZamirMay 11th, 2015 at 02:28SimonMay 12th, 2015 at 01:34