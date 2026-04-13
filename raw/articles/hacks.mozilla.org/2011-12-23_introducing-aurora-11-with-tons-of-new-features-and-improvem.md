---
title: Introducing Aurora 11 with tons of new features and improvements – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/12/introducing-aurora-11-with-tons-of-new-features-and-improvements/
author: Robert Nyman
published: '2011-12-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We have now released [Aurora 11](http://www.mozilla.org/en-US/firefox/channel/), soon to become Firefox 11, and wanted to cover all the the things we have improved in this version!


## Highlights

- To quickly edit the outerHTML of an element, we have now added support for element.outerHTML.
- The Battery API
- Storing files in IndexedDB
- Support for loop attributes for media elements
- SPDY (off by preferences)
- WebSockets no longer needs a prefix when you call them

## All new features

Below is a list of all the new improvements in Aurora 11, grouped by category together with a link to each bug in bugzilla if you are interested in reading up more about it and its process.

### DOM

[Support element.outerHTML property](https://bugzilla.mozilla.org/show_bug.cgi?id=92264)[SVGSVGElement.getElementById not implemented](https://bugzilla.mozilla.org/show_bug.cgi?id=280391)[IndexedDB: support indexedDB.cmp](https://bugzilla.mozilla.org/show_bug.cgi?id=692642)[IndexedDB: multientry indexes](https://bugzilla.mozilla.org/show_bug.cgi?id=692630)[IndexedDB now support all key types, including floating point numbers, dates and arrays!](https://bugzilla.mozilla.org/show_bug.cgi?id=692614)[Battery API](https://bugzilla.mozilla.org/show_bug.cgi?id=678694)[Support HTML parsing in XMLHttpRequest per XMLHttpRequest Level 2](https://bugzilla.mozilla.org/show_bug.cgi?id=651072)[Remove the no-argument form of requestAnimationFrame](https://bugzilla.mozilla.org/show_bug.cgi?id=704171)[requestAnimationFrame callback function name should be “sample”, not “onBeforePaint”](https://bugzilla.mozilla.org/show_bug.cgi?id=704175)[Allow mozRequestAnimationFrame requests to be cancelable](https://bugzilla.mozilla.org/show_bug.cgi?id=647518)[Use cancelRequestAnimationFrame where appropriate instead of boolean flags](https://bugzilla.mozilla.org/show_bug.cgi?id=708173)[Add mozCancelAnimationFrame](https://bugzilla.mozilla.org/show_bug.cgi?id=710981)[Implement Event constructors](https://bugzilla.mozilla.org/show_bug.cgi?id=675884)[Implement HTML event ctors](https://bugzilla.mozilla.org/show_bug.cgi?id=708701)[Implement MouseEvent and UIEvent ctors](https://bugzilla.mozilla.org/show_bug.cgi?id=709127)[Enable storing files in IndexedDB](https://bugzilla.mozilla.org/show_bug.cgi?id=661877)[IndexedDB: Allow passing an array as keypath](https://bugzilla.mozilla.org/show_bug.cgi?id=694138)

### GFX

### Layout

[-moz-text-size-adjust CSS property](https://bugzilla.mozilla.org/show_bug.cgi?id=627842)[[css3-conditional] allow @-rules inside of @media and @-moz-document](https://bugzilla.mozilla.org/show_bug.cgi?id=511909)

### Media

### Network

[SPDY (Preffed off)](https://wiki.mozilla.org/Platform/Features/SPDY)[Enable Extended Protection (channel and service binding) for NTLM authentication](https://bugzilla.mozilla.org/show_bug.cgi?id=573043)[add workaround for broken Outlook Web App (OWA) attachment handling](https://bugzilla.mozilla.org/show_bug.cgi?id=704989)[HTTP content type charset parameter accepts single quotes](https://bugzilla.mozilla.org/show_bug.cgi?id=700589)[XMLHttpRequest can fire an abort event after a load event, but should not](https://bugzilla.mozilla.org/show_bug.cgi?id=703380)[Disallow responseType and withCredentials for sync XHR](https://bugzilla.mozilla.org/show_bug.cgi?id=701787)[Allow Cross-Origin URLs in EventSource (Server-Sent Events)](https://bugzilla.mozilla.org/show_bug.cgi?id=664179)[Support unprefixed responseType == “json” in XMLHttpRequest](https://bugzilla.mozilla.org/show_bug.cgi?id=707142)[Implement Binary Messages for Websockets](https://bugzilla.mozilla.org/show_bug.cgi?id=676439)[Add HSTS support for websockets](https://bugzilla.mozilla.org/show_bug.cgi?id=664284)[No longer dispatch incoming WebSocket messages in CLOSING state](https://bugzilla.mozilla.org/show_bug.cgi?id=710964)[Set WebSocket message size limit to 2 GB](https://bugzilla.mozilla.org/show_bug.cgi?id=711205)[Tracking bug: unprefix WebSockets](https://bugzilla.mozilla.org/show_bug.cgi?id=695635)

### Performance

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 47 comments

Robson SobralDecember 23rd, 2011 at 12:55Robert NymanDecember 23rd, 2011 at 13:21nyanDecember 25th, 2011 at 07:49Robson SobralDecember 27th, 2011 at 08:53Robert NymanDecember 30th, 2011 at 17:21Robson SobralDecember 23rd, 2011 at 13:41Robert NymanDecember 30th, 2011 at 17:21Jonas SickingDecember 23rd, 2011 at 17:16Robert NymanDecember 30th, 2011 at 17:22John A. Bilicki IIIDecember 23rd, 2011 at 23:08thinsoldierDecember 27th, 2011 at 10:59Robert NymanDecember 30th, 2011 at 17:41tommy kayFebruary 11th, 2012 at 10:41pdDecember 24th, 2011 at 09:11Robert NymanDecember 30th, 2011 at 17:24abralJanuary 30th, 2012 at 06:48GioDecember 25th, 2011 at 04:00Robert NymanDecember 30th, 2011 at 17:25pdDecember 31st, 2011 at 07:14pdDecember 31st, 2011 at 07:16Robert NymanJanuary 2nd, 2012 at 04:47pdJanuary 2nd, 2012 at 06:13Robert NymanJanuary 3rd, 2012 at 06:30David WalshDecember 25th, 2011 at 05:45thinsoldierDecember 27th, 2011 at 10:39DannyDecember 28th, 2011 at 06:14Robert NymanDecember 30th, 2011 at 17:27Robert NymanDecember 30th, 2011 at 17:27JoeDecember 28th, 2011 at 10:00Robert NymanJanuary 2nd, 2012 at 04:57GioDecember 31st, 2011 at 02:54Robert NymanJanuary 2nd, 2012 at 04:58SriniJanuary 1st, 2012 at 02:48Robert NymanJanuary 2nd, 2012 at 05:00OrNotJanuary 10th, 2012 at 23:19Robert NymanJanuary 12th, 2012 at 11:53tokaiJanuary 12th, 2012 at 06:12Robert NymanJanuary 12th, 2012 at 11:54Robson SobralJanuary 12th, 2012 at 12:08pdJanuary 13th, 2012 at 03:21Robson SobralJanuary 13th, 2012 at 10:14SunilJanuary 16th, 2012 at 01:51Robert NymanJanuary 17th, 2012 at 03:19janssen kurtFebruary 10th, 2012 at 13:15Jean-Yves PerrierFebruary 10th, 2012 at 22:56JordanMarch 23rd, 2012 at 11:09Robert NymanMarch 23rd, 2012 at 12:02