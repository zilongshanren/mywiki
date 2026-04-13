---
title: Firefox 83 is upon us – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/11/firefox-83-is-upon-us/
author: Chris Mills
published: '2020-11-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Did November spawn a monster this year? In truth, November has given us a few snippets of good news, far from the least of which is the launch of Firefox 83! In this release we’ve got a few nice additions, including Conical CSS gradients, overflow debugging in the Developer Tools, enabling of WebRender across more platforms, and more besides.

This blog post provides merely a set of highlights; for all the details, check out the following:

## DevTools

In the [HTML Pane](https://wiki.developer.mozilla.org/en-US/docs/Tools/Page_Inspector/UI_Tour#HTML_pane), scrollable elements have a “scroll” badge next to them, which you can now toggle to highlight elements causing an overflow (expanding nodes as needed to make them visible):

![devtools page inspector showing a scroll badge next to an element that is scrolling](../../assets/a6dde458a9a5e9f7.png)


You will also see an “overflow” badge next to the node causing the overflow.

![Firefox devtools screenshot showing an overflow badge next to a child element that is causing its parent to overflow](../../assets/fdfc5fb489bcbf01.png)


And in addition to that, if you hover over the node(s) causing the overflow, the UI will show a “ghost” of the content so you can see how far it overflows.

![Firefox UI showing a highlighted paragraph and a ghost of the hidden overflow content](../../assets/e420ea5658c3ef3b.png)


These new features are very useful for helping to debug problems related to overflow.

## Web platform additions

Now let’s see what’s been added to Gecko in Firefox 83.

### Conic gradients

We’ve had support for [linear gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/linear-gradient) and [radial gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/radial-gradient) in CSS images (e.g. in [ background-image](https://developer.mozilla.org/en-US/docs/Web/CSS/background-image)) for a long time. Now in Firefox 83 we can finally add support for

[conic gradients](https://developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient())to that list!

You can create a really simple conic gradient using two colors:

```
conic-gradient(red, orange);
```


![simple conic gradient that goes from red to orange](../../assets/c190fcb2fb760bd8.png)


But there are many options available. A more complex syntax example could look like so:

```
conic-gradient(
from 45deg /* vary starting angle */
at 30% 40%, /* vary position of gradient center */
red, /* include multiple color stops */
orange,
yellow,
green,
blue,
indigo 80%, /* vary angle of individual color stops */
violet 90%
)
```


![complex conic gradient showing all the colors of the rainbow, positioned off center](../../assets/983d695dc33119f9.png)


And in the same manner as the other gradient types, you can create repeating conic gradients:

```
repeating-conic-gradient(#ccc 20deg, #666 40deg)
```


![repeating conic gradient that continually goes from dark gray to light gray](../../assets/a4962cf877e8180c.png)


For more information and examples, check out our [conic-gradient()](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/conic-gradient()#Examples) reference page, and the [Using CSS gradients](https://wiki.developer.mozilla.org/en-US/docs/Web/CSS/CSS_Images/Using_CSS_gradients#Using_conic_gradients) guide.

## WebRender comes to more platforms

We started work on our [WebRender](https://hacks.mozilla.org/2017/10/the-whole-web-at-maximum-fps-how-webrender-gets-rid-of-jank/) rendering architecture a number of years ago, with the aim of delivering the whole web at 60fps. This has already been enabled for Windows 10 users with suitable hardware, but today we bring the WebRender experience to Win7, Win8 and macOS 10.12 to 10.15 (not 10.16 beta as yet).

It’s an exciting time for Firefox performance — try it now, and let us know what you think!

## Pinch to zoom on desktop

Last but not least, we’d like to draw your attention to pinch to zoom on desktop — this has long been requested, and finally we are in a position to enable pinch to zoom support for:

- Windows laptop touchscreens
- Windows laptop touchpads
- macOS laptop touchpads

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## One comment

Zac SvobodaNovember 18th, 2020 at 10:01