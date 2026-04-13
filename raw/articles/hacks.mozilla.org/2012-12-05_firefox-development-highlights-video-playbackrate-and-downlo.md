---
title: 'Firefox Development Highlights: video.playbackRate and download attribute
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/12/firefox-development-highlights-video-playbackrate-download-attribute/
author: Paul Rouget
published: '2012-12-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Here are the latest features in Firefox for developers, as part of our [Bleeding Edge series](https://hacks.mozilla.org/category/bleeding-edge/), and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## <video>: support for custom playbackRate

Setting `video.playbackRate`

changes the “video speed”. 1.0 is regular speed, 2.0 is 2 times faster. From the [MDN documentation on HTMLMediaElement](https://developer.mozilla.org/docs/DOM/HTMLMediaElement):

The default playback rate for the media. 1.0 is “normal speed,” values lower than 1.0 make the media play slower than normal, higher values make it play faster.


Example:

```
```

Interactive demo:

## <a> “download” attribute

In some cases, resources are intended for later use rather than immediate viewing. To indicate that a resource is intended to be downloaded for use later, rather than immediately used, the download attribute can be specified on the a or area element that creates the hyperlink to that resource.


This attribute is particularly useful with [blobs](https://developer.mozilla.org/docs/DOM/Blob). With Blobs, You can create files in JavaScript. A binary blob can be an image built in a canvas element for example. Linking binary blobs to a `<a>`

element (with a [URL constructor](https://developer.mozilla.org/docs/DOM/window.URL.createObjectURL)) and marking this `<a>`

element as downloadable with this new attribute, the user will be able to save the blob as a file on his hard-drive.

Example from [Tom Schuster’s blog post about his work on the HTML5 download attribute](http://javascript-reverse.tumblr.com/post/37056936789/html5-download-attribute): ]

```
var blob = new Blob(["Hello World"]);
var a = document.createElement("a");
a.href = window.URL.createObjectURL(blob);
a.download = "hello-world.txt";
a.textContent = "Download Hello World!";
```

It has also been covered on HTML5Rocks in [Downloading resources in HTML5](http://updates.html5rocks.com/2011/08/Downloading-resources-in-HTML5-a-download).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

WebDevPLDecember 6th, 2012 at 08:37Robert NymanDecember 6th, 2012 at 08:42Mindaugas JakutisDecember 19th, 2012 at 00:50Florina LöfflerApril 1st, 2013 at 08:07