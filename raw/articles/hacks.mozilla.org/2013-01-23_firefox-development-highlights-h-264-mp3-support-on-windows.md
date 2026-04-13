---
title: Firefox Development Highlights – H.264 & MP3 support on Windows, scoped stylesheets
  + more – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/01/firefox-development-highlights-h-264-mp3-support-on-windows-scoped-stylesheets-more/
author: Paul Rouget
published: '2013-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Time for the first look this year into the latest developments with Firefox. This is part of our [Bleeding Edge](https://hacks.mozilla.org/category/bleeding-edge/) and [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/) series, and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## H.264 & MP3 support on Windows

[Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox) and [Firefox OS](http://www.mozilla.org/firefoxos/) already support H.264 and MP3. We are also working on bringing these formats to Firefox Desktop. On Windows 7 and above, you can already test it by turning on the preference `media.windows-media-foundation.enabled`

in [about:config](about:config). Decoding is done on the OS side (no decoder included in Firefox source code, not like WebM or Ogg Theora). For Linux and Mac, work is in progress.

## The new Downloads panel has been enabled

We have now enabled the new Downloads panel:

## Scoped style attribute

It’s now possible to define scoped style elements. Usually, when we write a stylesheet, we use `<style>...</style>`

, and CSS code is applied to the whole document. If the `<style>`

tag is nested inside a node (let’s say a `<div>`

), and the `<style>`

tag includes the `scoped`

attribute (`<style scoped>`

), then the CSS code will apply only to a subtree of the document, starting with the parent node of the `<style>`

element. The root of the subtree can also be referred via the `:scope`

pseudo-class.

![](../../assets/6f15a1902fa96598.png)


### Demo

Our friends over at HTML5Rocks have also written about it in [A New Experimental Feature: scoped stylesheets](http://updates.html5rocks.com/2012/03/A-New-Experimental-Feature-style-scoped).

## @supports and CSS.supports

In Firefox 17, we shipped the `@supports`

CSS at-rule. This lets you define specific CSS code only if some features are supported. For example:

```
@supports not (display: flex) {
/* If flex box model is not supported, we use a different layout */
#main {
width: 90%;
}
}
```

In Firefox 20, it’s now possible to do the same thing, but within JavaScript:

```
if (CSS.supports("display", "flex")) {
// do something relying on flexbox
}
```

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 34 comments

SkouaJanuary 23rd, 2013 at 09:06Robert NymanJanuary 23rd, 2013 at 13:23pdFebruary 13th, 2013 at 09:50Robert Nyman [Editor]February 14th, 2013 at 05:39pdFebruary 20th, 2013 at 04:30AKApril 8th, 2013 at 19:47Fawad HassanJanuary 23rd, 2013 at 10:48Robert NymanJanuary 23rd, 2013 at 13:38Dan FormanJanuary 23rd, 2013 at 14:16Robert NymanJanuary 23rd, 2013 at 14:51Dan FormanJanuary 23rd, 2013 at 15:26Robert NymanJanuary 23rd, 2013 at 15:49ArnoJanuary 25th, 2013 at 08:54Robert Nyman [Editor]January 25th, 2013 at 14:26ArnoFebruary 1st, 2013 at 05:50Robert Nyman [Editor]February 1st, 2013 at 06:40John A. Bilicki IIIFebruary 1st, 2013 at 05:29Robert Nyman [Editor]February 1st, 2013 at 06:43John A. Bilicki IIIFebruary 1st, 2013 at 06:53Robert Nyman [Editor]February 1st, 2013 at 07:03AKFebruary 10th, 2013 at 00:01Robert Nyman [Editor]February 12th, 2013 at 03:27MattFebruary 20th, 2013 at 14:20Robert Nyman [Editor]February 21st, 2013 at 01:26MGMarch 9th, 2013 at 23:30Robert Nyman [Editor]March 11th, 2013 at 07:37MGMarch 11th, 2013 at 11:30Bhaavan MerchantMarch 21st, 2013 at 00:56Robert Nyman [Editor]March 21st, 2013 at 01:18kringelMarch 23rd, 2013 at 22:37kringelMarch 23rd, 2013 at 22:45nullabilityApril 3rd, 2013 at 12:12Robert Nyman [Editor]April 4th, 2013 at 03:34AKApril 8th, 2013 at 19:47