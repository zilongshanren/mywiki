---
title: Firefox Development Highlights – Viewport percentage, canvas.toBlob() and WebRTC
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/10/firefox-development-highlights-viewport-percentage-canvas-toblob-and-webrtc/
author: Paul Rouget
published: '2012-10-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

To keep you updated on the latest features in Firefox, here is again a blog post highlighting the most recent changes. This is part of our [Bleeding Edge series](https://hacks.mozilla.org/category/bleeding-edge/), and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## Viewport-percentage lengths

Gecko now supports new lenght units: vh, vw, vmin and vmax. 1vh is 1% of the viewport height, and the length doesn’t depend on its container size. We can build designs that are directly proportional to the page size (think about HTML slides for example, which are supposed to keep the same appearance regardless the size of the page).

- vh
- 1/100th of the height of the viewport.
- vw
- 1/100th of the width of the viewport.
- vmin
- 1/100th of the minimum value between the height and the width of the viewport.
- vmax
- 1/100th of the maximum value between the height and the width of the viewport.

Read more about [CSS Viewport-percentage lengths on MDN](https://developer.mozilla.org/en-US/docs/CSS/length#Viewport-percentage_lengths).

## <canvas>.toBlob()

A Blob object represents a file-like object of immutable, raw data. Blobs can be used by different APIs, like the File API or IndexedDB. We can create an alias URL the refers to the blob with [window.URL.createObjectURL](https://developer.mozilla.org/en-US/docs/DOM/window.URL.createObjectURL), which can be used in place of data URLs in some cases (which is better memory wise).

Now, a canvas element can export its content as an image blob with the `toBlob()`

method (this replaces the non standard mozGetAsFile function). `toBlob`

is asynchronous:

`toBlob(callback, type) // type is "image/png" by default`

For more information, see [Example: Getting a file representing the canvas on MDN](https://developer.mozilla.org/en-US/docs/DOM/HTMLCanvasElement#Example.3A_Getting_a_file_representing_the_canvas).

## WebRTC in Firefox Nightly and Firefox Aurora (Firefox 18)

To enable our WebRTC code in Firefox’s Nightly desktop build, browse to [about:config](about:config) and change the `media.peerconnection.enabled`

preference to `true`

. More [WebRTC documentation on MDN](https://developer.mozilla.org/en-US/docs/WebRTC), and we plan to have future blog posts about WebRTC here on Mozilla Hacks.

Additionally, if you are interested in a steady flow of the latest Firefox highlights, you can also follow @FirefoxNightly on Twitter.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 2 comments

Robin AmphlettFebruary 20th, 2013 at 03:01Robert Nyman [Editor]February 20th, 2013 at 07:12