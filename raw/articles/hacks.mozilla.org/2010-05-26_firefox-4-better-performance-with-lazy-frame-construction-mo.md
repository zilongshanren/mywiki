---
title: 'Firefox 4: Better performance with Lazy Frame Construction – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2010/05/better-performance-with-lazy-frame-construction/
author: Paul Rouget
published: '2010-05-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post from Timothy Nikkel’s blog.*

*Lazy Frame Construction is new to Gecko and allows many DOM operations (appendChild, insertBefore, etc) to not trigger immediate reflows. This can vastly improve the interactive performance of very complex web pages. If you want to test this out, you should get a Firefox Nightly.*

Lazy frame construction recently landed on mozilla-central. To explain what this means and how this improves things we need some background. Each node in the DOM tree of a webpage has a frame created for it that is used to determine where on the page the node is drawn and its size. A frame corresponds closely to the concept of a [box from the CSS spec](http://www.w3.org/TR/CSS2/box.html). We used to create frames for DOM nodes eagerly; that is as soon as a node was inserted into the document we would create a frame for it. But this can create wasted effort in many situations. For example if a script inserts a large number of nodes into the DOM we would create a frame for each node when it is inserted. But with lazy frame construction we can process all those nodes at once in a big batch, saving overhead. Furthermore the time it takes to create those frames no longer blocks that script, so the script can go and do what it needs to and the frames will get created when they are needed. There are other situations where a script would insert nodes into the document and remove them immediately, so there is no need to ever create a frame for these as they would never be painted on screen.

So now when a node is inserted into a document the node is flagged for needing a frame created for it, and then the next time the refresh driver notifies (currently at 20 ms intervals) the frame is created. The refresh driver is also what drives reflow of webpages and CSS & SVG animations.

Let’s look at two examples where lazy frame construction helps.

In this example we insert 80000 div elements and then we flush all pending layout to time how long it takes before the changes made by the script are done and visible to the user. The script can continue executing without flushing layout, but we do it here to measure how long the actual work takes.

```
var stime = new Date();
var container = document.getElementById("container");
var lastchild = document.getElementById("lastchild");
for (var i = 0; i < 80000; i++) {
var div = document.createElement("div");
container.insertBefore(div, lastchild);
}
document.documentElement.offsetLeft; // flush layout
var now = new Date();
var millisecondselapsed = (now.getTime() - stime.getTime());
```

With lazy frame construction we are able to process the insertion of all 80000 div elements in one operation, saving the overhead of 80000 different inserts. In a build without lazy frame construction I get an average time of 1358 ms, with lazy frame construction I get 777 ms.

This example comes from a real webpage. We append a div and then set “div.style.position = ‘absolute’;”, and repeat that 2000 times, and then we flush all pending layout to time how long it takes before the changes made by the script are done and visible to the user.

```
var stime = new Date();
var container = document.getElementById("container2");
for (var i = 0; i < 2000; i++) {
var div = document.createElement("div");
container.appendChild(div);
div.style.position = "absolute";
}
document.documentElement.offsetLeft; // flush layout
var now = new Date();
var millisecondselapsed = (now.getTime() - stime.getTime());
```

With lazy frame construction we don't even bother creating the frame for the div until after the position has been set to absolute, so we don't waste any effort. In a build without lazy frame construction I get an average time of 4730 ms, with lazy frame construction I get 130 ms.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 40 comments

mynameMay 26th, 2010 at 06:24PinoMay 26th, 2010 at 06:32Pavel DudrenovMay 26th, 2010 at 07:42BorisMay 26th, 2010 at 09:07PavelMay 26th, 2010 at 10:55BorisMay 26th, 2010 at 12:36pavelMay 26th, 2010 at 15:31BorisMay 26th, 2010 at 19:03Richard Le PoidevinMay 26th, 2010 at 09:04LonerGothMay 26th, 2010 at 09:48LonerGothMay 26th, 2010 at 09:55LonerGothMay 26th, 2010 at 09:56CaChiMay 26th, 2010 at 10:32hommMay 26th, 2010 at 11:29sawrubMay 26th, 2010 at 19:59LumiMay 27th, 2010 at 00:35carolMay 27th, 2010 at 08:26Wurdebalg HurrstMay 27th, 2010 at 12:00BenbenMay 28th, 2010 at 13:35Tyler DurdenMay 29th, 2010 at 14:54OpperhertJune 7th, 2010 at 05:43carolJune 11th, 2010 at 08:46AliJuly 6th, 2010 at 14:49GilfuinJuly 7th, 2010 at 06:15BorisJuly 7th, 2010 at 17:36AliJuly 7th, 2010 at 23:09AnonymousAugust 25th, 2010 at 17:33Marc DixAugust 29th, 2010 at 23:19Luis AlvaradoSeptember 20th, 2010 at 00:53edorivaiSeptember 23rd, 2010 at 14:54MichelNovember 14th, 2010 at 07:36Shane BundyMarch 13th, 2011 at 09:51Shane BundyMarch 14th, 2011 at 16:48Shane BundyMarch 14th, 2011 at 16:50psxloverMarch 22nd, 2011 at 14:05dang ky ten mienJanuary 15th, 2012 at 10:48