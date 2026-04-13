---
title: WebRTC enabled, H.264/MP3 support in Win 7 on by default, Metro UI for Windows
  8 + more – Firefox Development Highlights – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/webrtc-enabled-h-264mp3-support-in-win-7-on-by-default-metro-ui-for-windows-8-more-firefox-development-highlights/
author: Paul Rouget
published: '2013-02-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Time again for looking at the latest progress with Firefox. These posts are part of our [Bleeding Edge](https://hacks.mozilla.org/category/bleeding-edge/) and [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/) series – take note that most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## WebRTC enabled by default

Previously, you needed to go to about:config in Firefox and set the `media.peerconnection.enabled`

option to `true`

, but now it’s enabled by default. This is a huge step forward, to be able to run WebRTC directly in a web browser without it needing any special settings or configuration.

For more details behind this decision, please read [Pref on WebRTC by default](https://bugzilla.mozilla.org/show_bug.cgi?id=796463).

Want to get started with WebRTC? Then we recommend our article [Cross-browser camera capture with getUserMedia/WebRTC](https://hacks.mozilla.org/2013/02/cross-browser-camera-capture-with-getusermediawebrtc/).

## Metro UI

The new Firefox User Interface for Windows 8 has landed (if you had Firefox Nightly as your default browser, reset that permission to see the new UI).

There are [more screenshots available](http://imgur.com/a/d5feb#0) too.

## H.264 & MP3 support enabled by default in Windows 7

We [talked about H.264 & MP3 support before](https://hacks.mozilla.org/2013/01/firefox-development-highlights-h-264-mp3-support-on-windows-scoped-stylesheets-more/), and now that support is activated by default.

We are still working on supporting Mac OS X and Linux.

## WebAudio API progress

We are working on implementing the [WebAudio API](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#methodsandparams-AudioContext), and the first parts of support has just started appearing.

It’s available in about:config in the `media.webaudio.enabled`

preference – set it to `true`

to enable it and be able to access things such as `AudioContext.decodeAudioData`

.

## Crypto API: window.crypto.getRandomValues

If you provide an integer-based TypedArray (i.e. Int8Array, Uint8Array, Int16Array, Uint16Array, Int32Array, or Uint32Array), [window.crypto.getRandomValues](https://developer.mozilla.org/en-US/docs/DOM/window.crypto.getRandomValues) is going fill the array with cryptographically random numbers:

```
/* assuming that window.crypto.getRandomValues is available */
var array = new Uint32Array(10);
window.crypto.getRandomValues(array);
console.log("Your lucky numbers:");
for (var i = 0; i < array.length; i++) {
console.log(array[i]);
}
```

## canvas: ctx.isPointInStroke

This has been uplifted to Firefox 19 Beta.

From the [WHATWG mailing list](http://lists.w3.org/Archives/Public/public-whatwg-archive/2012Nov/0148.html):

"We have recently implemented isPointInStroke(x,y) in Firefox (https://bugzilla.mozilla.org/show_bug.cgi?id=803124). This is a parallel to isPointInPath(x,y) and returns true if the point is inside the area contained by the stroking of a path."


## JavaScript: Math.imul

[Math.imul](https://developer.mozilla.org/en-US/docs/JavaScript/Reference/Global_Objects/Math/imul) allows for fast 32-bit integer multiplication with C-like semantics. This feature is useful for projects like Emscripten.

Polyfill:

```
function imul(a, b) {
var ah = (a >>> 16) & 0xffff;
var al = a & 0xffff;
var bh = (b >>> 16) & 0xffff;
var bl = b & 0xffff;
// the shift by 0 fixes the sign on the high part
return (al * bl) + (((ah * bl + al * bh) << 16) >>> 0);
}
```

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 21 comments

Sam Tobin-HochstadtFebruary 20th, 2013 at 06:01Robert Nyman [Editor]February 20th, 2013 at 07:09NateFebruary 27th, 2013 at 02:29Robert Nyman [Editor]February 27th, 2013 at 07:37GreatFebruary 20th, 2013 at 18:12Robert Nyman [Editor]February 21st, 2013 at 01:28Adam UllmanFebruary 20th, 2013 at 18:25Robert Nyman [Editor]February 21st, 2013 at 01:30BenzFebruary 21st, 2013 at 08:51Robert Nyman [Editor]February 21st, 2013 at 13:25bitinnApril 9th, 2013 at 21:40Robert Nyman [Editor]April 10th, 2013 at 04:06T-BoneFebruary 24th, 2013 at 13:12Robert Nyman [Editor]February 26th, 2013 at 16:32Dark ShikariFebruary 26th, 2013 at 14:33Robert Nyman [Editor]February 26th, 2013 at 16:49mikecaoMarch 10th, 2013 at 22:24Robert Nyman [Editor]March 11th, 2013 at 07:35mikecaoMarch 13th, 2013 at 02:01Robert Nyman [Editor]March 13th, 2013 at 02:48mikecaoMarch 13th, 2013 at 18:56