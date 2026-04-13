---
title: Firefox Development Highlights – Per Window Private Browsing & Canvas' globalCompositeOperation
  new values – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/12/firefox-development-highlights-per-window-private-browsing-canvas-globalcompositeoperation-new-values/
author: Paul Rouget
published: '2012-12-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

On a regular basis, we like to highlight the latest features in Firefox for developers, as part of our [Bleeding Edge series](https://hacks.mozilla.org/category/bleeding-edge/), and most examples only work in [Firefox Nightly](http://nightly.mozilla.org/) (and could be subject to change).

## Per Window Private Browsing

Private browsing is very useful for web developers. A new private session doesn’t include existing persistent data (cookies and HTML5 storage). It’s convenient if we want to test a website that stores data (login and persistent informations) without cleaning every time these cached data, or if we want to login to a service with 2 different users.

Until now, when entering Private Browsing in Firefox, it was closing the existing session to start a new one. Now, Firefox will keep the current session and open a new private window. You can test it in Firefox Nightly (to be Firefox 20). There’s still some frontend work to do, but the feature works.

## Canvas’ globalCompositeOperation new values

The ‘globalCompositeOperation’ canvas property lets you define how you want canvas to draw images over an existing image. By default, when canvas draws an image over existing pixels, the new image is just replacing the pixels. But there are other ways to mix pixels. For example, if you set `ctx.globalCompositeOperation = "lighter"`

, pixel color values are added, and it creates a different visual effect.

There are several effects available, and more on them can be found in [globalCompositeOperation on MDN](https://developer.mozilla.org/docs/HTML/Canvas/Tutorial/Compositing).

Rik Cabanier from Adobe has extended the [Canvas specification](https://dvcs.w3.org/hg/FXTF/rawfile/tip/compositing/index.html#canvascompositingandblending) to include more effects. He has also [implemented these new effects in Firefox Nightly](https://bugzilla.mozilla.org/show_bug.cgi?id=748433). These new effects are called “blend modes”. These are more advanced ways of mixing colors.

Please take a look at the [list of these new blending modes](https://dvcs.w3.org/hg/FXTF/rawfile/tip/compositing/index.html#blending).

And here’s an example of how to use them:

If you don’t use Firefox Nightly, here is a (long) screenshot:

![image](../../assets/14f41fc1a5d7939c.png)


## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 9 comments

Caspy7December 24th, 2012 at 02:29kApril 3rd, 2013 at 05:45Robert Nyman [Editor]April 3rd, 2013 at 08:11scootergrisenApril 6th, 2013 at 14:58Slipp D.April 8th, 2013 at 00:48Robert Nyman [Editor]April 8th, 2013 at 10:08Slipp D.April 8th, 2013 at 10:19Michael MullanyApril 8th, 2013 at 11:07Robert Nyman [Editor]April 8th, 2013 at 23:55