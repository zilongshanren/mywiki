---
title: Mozilla developer preview (Gecko 1.9.3a2) now available – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2010/03/mozilla-developer-preview-gecko-1-9-3a2-now-available/
author: Christopher Blizzard
published: '2010-03-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

We’ve posted a new release of our Mozilla developer preview series as a way to test new features that we’re putting into the Mozilla platform. These features may or may not make it into a future Firefox release, either for desktops or for mobile phones. But that’s why we do these releases – to get testing and feedback early so we know how to treat them.

Note that this release does not contain two things that have gotten press recently: [D2D](http://www.basschouten.com/blog1.php/2009/11/22/direct2d-hardware-rendering-a-browser) or the new [JavaScript VM](http://hacks.mozilla.org/2010/03/improving-javascript-performance-with-jagermonkey/) work we’ve been doing.

Since this is a weblog focused on web developers, I think that it’s important to talk about what’s new for all of you. So we’ll jump right into that:

### Out of Process Plugins

We did an [a1 release](http://hacks.mozilla.org/2010/02/mozilla-developer-preview-gecko-1-9-3a1-available-for-download/) about three weeks ago in order to get testing on some of the new web developer features (which we’ll list here again.) The biggest change between that release and this one is the inclusion of out of process plugins for Windows and Linux. (Mac is a little bit more work and we’re working on it as fast as our little fingers will type.)

There are a lot of plugins out there on the web, and they exist to varying degrees of quality. So we’re pushing plugins out of process so that when [one of them crashes](http://www.flickr.com/photos/christopherblizzard/4397728218/) it doesn’t take the entire browser with it. (It also has lots of other nice side effects – we can better control memory usage, CPU usage and it also helps with general UI lag.)

If you want to know more about it, have a look at [this post by Ben Smedberg](http://benjamin.smedbergs.us/blog/2010-03-03/firefox-safe-from-plugin-crashes/) who goes over how it works, what prefs you can set and how you can help test it. It would help us a lot of you did.

(If you really want to get on the testing train we strongly suggest you start running our [nightly builds](http://nightly.mozilla.org) which are the ultimate in bleeding edge but are generally stable enough for daily use.)

Anyway, on to the feature list and performance improvements taken from the [release announcement](https://developer.mozilla.org/devnews/index.php/2010/03/03/mozilla-developer-preview-now-available-with-out-of-process-plugins/):

### Web Developer Features

- Support for
[Content Security Policy](https://developer.mozilla.org/en/Introducing_Content_Security_Policy). This is largely complete, minus the ability to disable`eval()`

. - The placeholder attribute for <input/> and <textarea> is now supported.
- Support for SMIL Animation in SVG. Support for animating some SVG attributes is still under development and the
`animateMotion`

element isn’t supported yet. - Support for CSS Transitions. This support is not quite complete: support for animation of transforms and gradients has not yet been implemented.
- Support for WebGL, which is disabled by default but can be enabled by changing a preference. See
[this blog post](http://hacks.mozilla.org/2009/09/webgl-for-firefox/)and[this blog post](http://hacks.mozilla.org/2009/12/webgl-draft-released-today/)for more details. - Support for the
`getClientRects`

and`getBoundingClientRect`

methods on Range objects. See[bug 396392](https://bugzilla.mozilla.org/show_bug.cgi?id=396392)for details. - Support for the
`setCapture`

and`releaseCapture`

methods on DOM elements. See[bug 503943](https://bugzilla.mozilla.org/show_bug.cgi?id=503943)for details. - Support for the HTML5
. See`History.pushState()`

and`History.replaceState()`

methods and the`popstate`

event[bug 500328](https://bugzilla.mozilla.org/show_bug.cgi?id=500328)for details. - Support for the
`<a href="https://developer.mozilla.org/en/CSS/background-image">-moz-image-rect()</a>`

value for background-image. See[bug 113577](https://bugzilla.mozilla.org/show_bug.cgi?id=113577)for more details.

For the full list of new web developer features please visit our page on [Upcoming Features for Web Developers](https://developer.mozilla.org/en/Upcoming_Firefox_features_for_developers).

### Performance Improvements

- We’ve removed link history lookup from the main thread and made it asynchronous. This results in
[less I/O during page loads](https://wiki.mozilla.org/Firefox/Goals/2010Q1/IO_Reduction)and improves overall browser responsiveness. - Loading the
[HTML5 spec](http://www.whatwg.org/specs/web-apps/current-work/)no longer causes very long browser pauses. - A large number of layout performance improvements have been made, including work around DOM access times, color management performance, text area improvements and many other hot spots in the layout engine.
- The JavaScript engine has many improvements: String handling is improved, faster closures, some support for recursion in TraceMonkey to name a few.
- Improvements to the performance of repainting HTML in
`<foreignObject>`

. - Strings are not copied between the main DOM code and
[web workers](https://developer.mozilla.org/En/Using_web_workers), improving performance for threaded JavaScript which moves large pieces of data between threads.

## 14 comments

Robert EisenbraunMarch 5th, 2010 at 14:02RyanMarch 5th, 2010 at 20:48BorisMarch 5th, 2010 at 20:59Magne AnderssonMarch 7th, 2010 at 03:37zwuMarch 6th, 2010 at 01:49zwuMarch 6th, 2010 at 04:42Robert O’CallahanMarch 6th, 2010 at 14:12Christopher BlizzardMarch 7th, 2010 at 15:23Erik HarrisonMarch 7th, 2010 at 19:44BorisMarch 9th, 2010 at 15:05patrickMarch 10th, 2010 at 23:49knmaoskdMarch 17th, 2010 at 07:00billy bobMarch 17th, 2010 at 09:28