---
title: Cross-domain WebGL textures disabled in Firefox 5 – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2011/06/cross-domain-webgl-textures-disabled-in-firefox-5/
author: Benoit Jacob
published: '2011-06-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In Firefox 5, it is no longer possible to use cross-domain elements as the source for WebGL textures. We made this change in response to security concerns around the possibility of cross domain information leakage. Unfortunately, that means that some WebGL-using pages are no longer working. We are working with the WebGL WG on a solution to allow such pages to resume working as soon as possible — read on for details.

### The security rules about cross-domain images

A cross-domain image is an image coming from a different domain than the canvas. A basic rule of Web security is that scripts must not be able to read pixel data from cross-domain images — they can only “blindly” display them. In more concrete terms, imagine that you currently have a session open on your bank’s website, allowing you to download scanned copies of cheques you’ve written. You don’t want scripts loaded in other tabs, from other websites, to be able to read your scanned cheques! Similarly, when you draw a cross-domain image onto a 2D canvas, using drawImage(), the canvas becomes “tainted” so that it’s no longer possible for scripts to read its pixels. This prevents a loophole whereby a canvas would be used as a proxy to read cross-domain images.

### The problem with cross-domain images as WebGL textures

When a cross-domain image was used as a WebGL texture, the WebGL canvas was “tainted” so that reading from it was no longer possible. Theoretically, that eliminated the concern. But a while ago, a researcher wrote to the public WebGL list with a [possible attack](http://www.khronos.org/webgl/public-mailing-list/archives/1010/msg00034.html) that could still allow reading pixels from WebGL textures. The idea was to paint the texture one pixel at a time with a WebGL fragment shader crafted to take an amount of time proportional to its brightness, and then time how long it takes: that would conceivably allow to get an approximation of the original image. Initially this attack seemed difficult to execute practically, but since then further research, including a [proof-of-concept](http://www.contextis.co.uk/resources/blog/webgl/poc/index.html) has been published which shows the attack to be more realistic than initially expected.

### The response

The WebGL spec has been [updated](http://www.khronos.org/registry/webgl/specs/latest/#4.2) to disallow using cross-domain images as WebGL textures, and Mozilla’s implementation in Firefox 5 has been [updated](https://bugzilla.mozilla.org/show_bug.cgi?id=656277) accordingly. A non-normative section has also been added allowing cross-domain images that have [CORS](http://en.wikipedia.org/wiki/Cross-Origin_Resource_Sharing) approval. Using CORS in this case is a way for servers to explicitly say when an image is OK to be read by cross-domain scripts. CORS support for WebGL is a high priority for us and will be [implemented](https://bugzilla.mozilla.org/show_bug.cgi?id=662599) very soon.

A [wiki page](https://developer.mozilla.org/en/WebGL/Cross-Domain_Textures) explains some more details. Affected scripts will generate a DOM_SECURITY_ERR exception and, just before that, a JS warning explaining what happened and linking to that wiki page.

[some existing Web content](https://bugzilla.mozilla.org/show_bug.cgi?id=662570). We initially wanted to wait for the CORS approach to be implemented before we blocked cross-domain textures. Our primary priority has always been the safety of our users, though, and so we decided to fix the security issue immediately in Firefox 5. This timing also accounts for the fact that CORS handling will become increasingly useful only as online content providers roll out support.

## 9 comments

phillihpJune 10th, 2011 at 12:19Gary CodingJune 21st, 2011 at 23:21Benoit JacobJune 22nd, 2011 at 04:34Julian AdamsJune 22nd, 2011 at 05:39Benoit JacobJune 22nd, 2011 at 05:55Gry CodingJune 22nd, 2011 at 09:27skierpageJuly 19th, 2011 at 14:55louisremiJuly 20th, 2011 at 07:37Henri AstreOctober 4th, 2011 at 09:34