---
title: 'Firefox OS Development: Web Components and Mozilla Brick – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2013/09/firefox-os-development-web-components-and-mozilla-brick/
author: Chris Heilmann
published: '2013-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In this edition of “Firefox OS: The platform HTML5 deserves” ([the previous six videos are published here](https://hacks.mozilla.org/category/videoseries/)), Mozilla’s Principal Evangelist Chris Heilmann ([@codepo8](http://twitter.com/codepo8)) grilled Mozilla’s “Senior HTML5 Engineer Angle Bracket Coordinator” Matthew Claypotch ([@potch](http://twitter.com/potch)) about the exciting new possibilities of Web Components for Web App developers and how Mozilla’s Brick library, a collection of custom elements to build applications with, can help with the transition. You can [watch the interview on YouTube](https://www.youtube.com/watch?v=eS1O46O5saA).

## The Why of Web components

There is a problem with the Web as a platform for applications: HTML, the language that makes it easy to mark up documents and give them meaning doesn’t have enough elements to build applications. There are quite a few new elements in the HTML5 spec, but their support is sketchy across browsers and there are still a lot of widgets missing that other platforms like Flex or iOS give developers out-of-the-box. As a result, developers build their own “widgets” like menu bars, slider controls and calendars using non-semantic HTML (mostly DIV elements) and make them interactive using JavaScript and theme-able using CSS.

This is a great workaround but the issue is that we add on top of the functionality of browsers instead of extending the way they already function. In other words, a browser needs to display HTML and does a great job doing that at least 60 frames per second. We then add our own widget functionality on top of that and animate and change the display without notifying the browser. We constantly juggle the performance of the browser and our own code on top of it. This leads to laggy interfaces, battery drain and flickering.

To work around that problem a few companies and standards body members are working on the [Web Components](http://www.w3.org/TR/2013/WD-components-intro-20130606/) specification which allows developers to extend the browser’s understanding of markup with own elements. Instead of writing a slider control and make it work after the browser already displayed the document, you define a slider element and become part of the normal display flow. This means our widgets get more responsive, don’t work against the browser’s rendering flow and all in all perform better. Especially on low spec mobile devices this is a massive win. The whole thing already happens: if you for example add a video element to the document you see a video controller with a timed slider bar, a play button and volume controls. All of these are HTML, CSS and JavaScript and you can even see them in the debugging tools:

![Anatomy of a video element](../../assets/b916b91fee6d5d08.png)


Firefox OS, being targeted at low end devices can benefit a lot from widgets that are part of the rendering flow, which is why Mozilla created [Mozilla Brick](http://mozilla.github.io/brick/), a collection of custom elements to build applications with. Earlier we introduced the concept using a library called [XTags](http://www.x-tags.org/), which powers Brick. Using Brick, it is very simple to create for example a [deck based application layout](http://mozilla.github.io/brick/demos/deck/index.html) using the following markup:

```
```
0I'm the first card!
1
These cards can contain any markup!




2


The resulting app consists of three decks that can be animated into another without having to do anything but call a `deck.shuffleNext();`

function.

Web Components are a huge topic right now and many libraries and frameworks appear each week. We hope that by using Brick we can enable developers to build very responsive apps for Firefox OS quickly and cleanly and leave the pain of making your app perform really well up to the OS.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 10 comments

Ivan DejanovicSeptember 27th, 2013 at 01:59Chris HeilmannSeptember 27th, 2013 at 02:25Doug ReederSeptember 27th, 2013 at 13:52pdSeptember 27th, 2013 at 07:13pdSeptember 27th, 2013 at 07:15nadrimajstorSeptember 28th, 2013 at 14:13ArasSeptember 28th, 2013 at 16:01FredOctober 1st, 2013 at 13:43niutechSeptember 29th, 2013 at 11:37DLOctober 2nd, 2013 at 04:41