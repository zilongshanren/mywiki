---
title: Progress on OMTC, unprefixed Visibility API and CSS improvements – Firefox
  Development Highlights – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/11/progress-on-omtc-unprefixed-visibility-api-and-css-improvements-firefox-development-highlights/
author: Paul Rouget
published: '2012-11-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

To keep all you web developers in the loop about new features and improvements in Firefox, and to be able to test and experiment in an early stage, here’s the latest [Firefox Development Highlights](https://hacks.mozilla.org/category/firefox/firefox-development-highlights/). This is part of our [Bleeding Edge series](https://hacks.mozilla.org/category/bleeding-edge/), and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## Good progress on OMTC (“Off Main Thread Compositing”)

A direct advantage of OMTC is a more responsive user interface. Rendering a web page is a complex process that involves different operations, like computing the layout of the page, downloading the different resources, decoding images, or executing JavaScript code.

Some of these operations are executed in a same thread. Some of them are executed in the main thread, where most of the User Interface interactions are handled. If an operation takes times in this main thread, it would then block the UI and makes the UI feel sluggish.

So, we want to move as many operations as possible into another thread. One of these operations we want to move is called “Compositing”. It’s responsible for “flattening” the page. A page is made of layers. For example, a layer for the fixed-background, a layer for a piece of test, and a layer for a video element. Flattening the page, compositing it, will merge these layers into one texture.

In [Firefox OS](http://www.mozilla.org/firefoxos/) and [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en), the Compositing operations are made in a different thread. And we are making some good progress to get OMTC working for Firefox Desktop.

To delve more into this, we recommend reading [Off Main Thread Compositing (OMTC) and why it matters](https://benoitgirard.wordpress.com/2012/05/15/off-main-thread-compositing-omtc-and-why-it-matters/).

## The visibility API has been unprefixed

The [Page Visibility API](https://developer.mozilla.org/docs/DOM/Using_the_Page_Visibility_API) lets you know when a webpage is visible or in focus. With tabbed browsing, there is a reasonable chance that any given webpage is in the background and thus not visible to the user.

When the user minimizes the webpage or moves to another tab, the API sends a `visibilitychange`

event regarding the visibility of the page. You can detect the event and perform some actions or behave differently. For example, if your web app is playing a video, it would pause the moment the user looks at another browser, and plays again when the user returns to the tab. The user does not lose her place in the video and can continue watching.

To that end, for `mozHidden`

and `mozvisibilitychange`

, the `moz`

prefix is not required anymore.

## CSS improvements

We always need more CSS support, right? Here are the latest changes:

### @page CSS at-rule

The [@page CSS at-rule](https://developer.mozilla.org/docs/CSS/@page) is used to modify some CSS properties when printing a document. You can’t change all CSS properties with @page. You can only change the margins, orphans, widows, and page breaks of the document. Attempts to change any other CSS properties will be ignored.

For example, you can write a specific style for left pages, and one for right pages (think “book”) with the `:left`

and `:right`

pseudo classes, or for the very first page with `:first`

.

### page-break-inside CSS property

The [page-break-inside CSS property](https://developer.mozilla.org/docs/CSS/page-break-inside) adjusts page breaks *inside* the current element:

```
page-break-inside:auto;
```


Automatic page breaks (default behavior):

```
page-break-inside:avoid;
```


Avid page breaks before the element:

```
/* avoid page break inside the paragraph */
p { page-break-inside: avoid; }
```


### text-transform:full-width

For [CSS text-transform](https://developer.mozilla.org/docs/CSS/text-transform), `full-width`

forces the writing of a character, mainly ideograms and latin scripts inside a square, allowing them to be aligned in the usual East Asian scripts (like Chinese or Japanese).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Paul MorrisNovember 22nd, 2012 at 06:50Paul MorrisNovember 22nd, 2012 at 06:57Robert NymanNovember 22nd, 2012 at 07:15Martin MelcherDecember 5th, 2012 at 09:32