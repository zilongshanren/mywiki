---
title: timelapse.js - Video retiming for the web.
url: https://enkimute.github.io/timelapse.js/
author: Enki's blog
published: '2017-04-04'
source_blog: Enki's blog – Math, Graphics, Programming.
source_site: https://enkimute.github.io/
category: graphics
fetched: '2026-04-19'
---

GIT

![view on github](../../assets/cb9f317b98c6b74a.png)

# timelapse.js - Video retiming for the web.

Create timelapse videos from webcam or canvas in your browser.

## Get timelapse !

![](../../assets/a2c3af97434f2f79.jpg)


881 bytes - [https://enkimute.github.io/res/timelapse.min.js](https://enkimute.github.io/res/timelapse.min.js)

## What is timelapse ?

The new MediaRecorder API allows you to capture video’s from webcam or canvas. Its great to record webM or mp4 videos of your webGL/canvas games, and super easy to use. There are however a number of use cases that are not covered by the MediaRecorder API. You can setup the recording rate, but playback and recording are by definition the same rate.

This means you can’t use MediaRecorder to save webM’s from say your javascript raytracer (they’ll playback at rendering speed .. might be a tad to slow) - you can’t speed up webcam capture to create cool timelapse video’s either ..

## Enter timelapse.js

Timelapse.js is a tiny utility that can take the MediaRecorder output and retime it to a different framerate. You could capture a webcam at 5 fps and play it at 30 for a beautifull timelapse, or render at minutes per frame and still play at 30 fps. Check out the samples below to see how easy it is ..

## Example : Canvas timelapse.

Click the record button, draw on the canvas then hit the play button to see the timelapse.

| Canvas | Video |
|---|---|

Here’s the call to timelapse :

```
var chunks=[];
mediaRecorder.ondataavailable=function(e){ chunks.push(e.data) }
mediaRecorder.onstop = function(){
timelapse(chunks,30,function(blob){
demoVideo.src = URL.createObjectURL(blob);
demoVideo.play();
});
};
```