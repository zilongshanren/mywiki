---
title: Using the Firefox DevTools to Debug fetch() on GitHub – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2015/03/using-the-firefox-devtools-to-debug-fetch-on-github/
author: Dan Callahan
published: '2015-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox Nightly recently added preliminary support for [Fetch](https://hacks.mozilla.org/2015/03/this-api-is-so-fetching/), a modern, [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)-based replacement for XMLHttpRequest (XHR). Our initial work supported most of the [Fetch Specification](https://fetch.spec.whatwg.org/), but not quite all of it. Specifically, when Fetch first appeared in Nightly, we hadn’t yet implemented serializing and de-serializing of [FormData objects](https://developer.mozilla.org/docs/Web/API/FormData).

GitHub was already using Fetch in production with a [home-grown polyfill](https://github.com/github/fetch), and required support for serializing FormData in order to upload images to GitHub Issues. Thus, when our early, incomplete implementation of Fetch landed in Nightly, the GitHub polyfill stepped out of the way, and image uploads from Firefox broke.

In the 15-minute video below, Dan Callahan shows a real-world instance of using the [Firefox Developer Tools](https://developer.mozilla.org/docs/Tools) to help find, file, and fix [Bug 1143857](https://bugzilla.mozilla.org/show_bug.cgi?id=1143857): “Fetch does not serialize FormData body; breaks GitHub.” This isn’t a canned presentation, but rather a comprehensive, practical demonstration of actually debugging minified JavaScript and broken event handlers using the Firefox DevTools, reporting a Gecko bug in Bugzilla, and ultimately testing a patched build of Firefox.

Use the following links to jump to a specific section of [the video on YouTube](https://www.youtube.com/watch?v=PUgRMRQoTq4):

[0:13](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=0m13s)– The error[0:50](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=0m50s)– Using the Network Panel[1:30](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=1m30s)– Editing and Resending HTTP Requests[2:02](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=2m2s)– Hypothesis: FormData was coerced to a String, not serialized[2:40](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=2m40s)– Prettifying minified JavaScript[3:10](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=3m10s)– Setting breakpoints on event handlers[4:57](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=4m57s)– Navigating the call stack[7:54](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=7m54s)– Setting breakpoints on lines[8:56](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=8m56s)– GitHub’s FormData constructor[10:48](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=10m48s)– Invoking fetch()[11:53](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=11m53s)– Verifying the bug by testing fetch() on another domain[12:52](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=12m52s)– Checking the docs for fetch()[13:42](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=13m42s)– Filing a Gecko bug in Bugzilla[14:42](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=14m42s)– The lifecycle of Bug 1143857: New, Duplicate, Reopened, Resolved[15:41](http://www.youtube.com/watch?v=PUgRMRQoTq4&t=15m41s)– Verifying a fixed build of Firefox

We expect [Firefox Developer Edition](https://www.mozilla.org/firefox/developer/) version 39 to ship later this month with full support for the Fetch API.

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 3 comments

Šime VidasMarch 19th, 2015 at 20:39Dan CallahanMarch 20th, 2015 at 05:17fvschMarch 22nd, 2015 at 07:02