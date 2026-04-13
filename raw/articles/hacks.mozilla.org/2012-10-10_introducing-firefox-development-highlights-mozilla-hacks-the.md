---
title: Introducing Firefox Development Highlights – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/10/introducing-firefox-development-highlights/
author: Paul Rouget
published: '2012-10-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We know he have a lot of readers out there interested in the Open Web and its capabilities, and part of that is to see the latest additions and implemented features in Firefox. Therefore, we’re introducing [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/) here at Mozilla Hacks.

## Introduction

The purpose of this post is to highlight some of the latest (couple of weeks) developments in Firefox and Gecko. Bear in mind that these changes might be backed out at any time and they are part of our [Bleeding Edge posts](https://hacks.mozilla.org/category/bleeding-edge/).

You can test them out in [Firefox Nightly](http://nightly.mozilla.org/).

If you are interested in a steady flow of the latest highlights, you can also follow [@FirefoxNightly](https://twitter.com/FirefoxNightly) on Twitter.

## Graphic

Firefox’ graphic stack received some great improvements lately: better scaling algorithm for images and support for retina display. Gecko now downscales images using a high-quality scaling algorithm. You can see the improvements in this screenshot (click on it for a larger version):

This is disabled on mobile, where we worry about speed/multicore abilities. It’s also disabled on OS X, which has high-quality downscaling built in.

Gecko now supports HiDPI displays, for web pages, plugins and for Firefox’ UI.

## Standards

CSS3 flexbox model is now available in Gecko, behind a preference: `layout.css.flexbox.enable`

. Go to [about:config](about:config) in Firefox and add that as a preference, set to `true`

.

Quote from [W3C](http://dev.w3.org/csswg/css3-flexbox/):

In the flex layout model, the children of a flex container can be laid out in any direction, and can “flex” their sizes, either growing to fill unused space or shrinking to avoid overflowing the parent. Both horizontal and vertical alignment of the children can be easily manipulated. Nesting of these boxes (horizontal inside vertical, or vertical inside horizontal) can be used to build layouts in two dimensions.


## Web Workers

Support for transferable objects from HTML5 spec.

If you want to send data to/from a Web Worker, you have to use postMessage() method. Internally what happens is that the data is duplicated using the structured cloned algorithm and then the copy is sent. To make this sharing faster, HTML5 specs add a new concept: transferable objects, data is transferred from one context to another without copy. Note: data is no longer available once transferred to the new context. Right now we can transfer just ArrayBuffers, but maybe in the future we will support other data types.


## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

krisOctober 10th, 2012 at 10:44Robert NymanOctober 10th, 2012 at 12:46krisOctober 10th, 2012 at 20:59Robert NymanOctober 11th, 2012 at 03:26Ken SaundersOctober 11th, 2012 at 18:29Robert NymanOctober 11th, 2012 at 23:41JayJanuary 24th, 2013 at 16:21