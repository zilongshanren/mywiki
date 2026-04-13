---
title: Direct2D Azure hits Firefox 7 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/09/direct2d-azure-hits-firefox-7/
author: Mozilla Hacks
published: '2011-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Based on a blog post originally posted here by Bas Schouten, Firefox Developer. *

Hrm, Azure, what’s that again?

You can find out all about Azure other blog posts, there’s an [introduction](http://blog.mozilla.com/joe/2011/04/26/introducing-the-azure-project/) from Joe Drew and there’s several more in detailed posts discussing the Direct2D Azure backend and the performance implications to be found on my blog. The bottom line is that we’re working on a new graphics API that will be used for rendering in Gecko.

What does that mean for Firefox 7?

Well, we’re currently only using it with Direct2D and when using canvas. This allows us to stress test it, although a wide array of tests has been run, and it has been in use by our Aurora and Beta testers for a while now, there might still be issues we might have missed. If these issues show in the final release we’ll only have caused a regression in Canvas and for a limited subset of our users, rather than in all browser rendering. The bottom line is you should generally see a speed improvement using 2D Canvas in Firefox 7 when using Windows 7 or Vista with a sufficiently powerful graphics card.

So what’s next, what’s the status?

We’re currently working hard on both a Cairo and a [Skia](https://bugzilla.mozilla.org/show_bug.cgi?id=687187) backend for the Azure API, this means we’ll be able to use the Azure API on all platforms. Possibly getting some quick performance benefits on platforms where Skia outperforms the cairo backends we’re currently using. At the same time we’re working on creating a layer that will allow controlled migration of all our content drawing code from the current ‘Thebes’ API’s to the new Azure API. Once that is done webpage rendering in general can start taking advantage of all the latest work!

That’s about all I have for you right now, enjoy!