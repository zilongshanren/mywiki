---
title: Developer Edition 45 – Animations, Memory Tools and More – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2015/12/developer-edition-45-animations-memory-tools-and-more/
author: Lin Clark
published: '2015-12-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox Developer Edition 45 has improvements to DevTools that will help you track down memory usage, dig into CSS animations, and more. In this post we’ll cover some of these changes – be sure to [download the latest Developer Edition](https://www.mozilla.org/en-US/firefox/developer/all/) to try them yourself.

## CSS animation tool++

The animation tool has many additions:

- When you click on an animation in the timeline, you’ll now see a list of the animated properties plus keyframes which show you the change in values over time.
- If an animation is moving too fast for you to see what’s going on, you can now slow it down by changing the playback rate.
- Animations running on the compositor thread have a lightning bolt icon next to them. This means that they will
[remain smooth even if the rest of the page is slow](https://developer.mozilla.org/en-US/docs/Tools/Performance/Scenarios/Animating_CSS_properties#CSS_property_cost).

Learn more about [using the animation tool](https://www.youtube.com/watch?v=Un3u4wuGT8Q) in the latest episode of Patrick Brosset’s screencast series: “Using the Dev Tools to understand CSS”.

Beyond the animation improvements, the inspector’s search tool was also improved. It now matches results from all markup in the page and subframes.

## What’s eating your memory?

We’ve improved the way you can inspect memory usage and find what is consuming memory. With snapshot diffing, you can inspect changes in the heap contents since a previous snapshot. And with snapshot filtering, you can show only memory allocated in a certain file or function, or show only the objects of a specific [[class]] type.

Read more about the [Memory Tool](https://hacks.mozilla.org/2015/11/firefoxs-new-memory-tool/) and [documentation about how to get started with it](https://developer.mozilla.org/en-US/docs/Tools/Memory). We’ve also put together a quick [gif that walks through the diffing process](https://hacks.mozilla.org/wp-content/uploads/2015/12/memory-diffing.gif).

## A bit of polish

We’ve also been working on polish and bug fixes across the toolbox – here are some of the highlights.

### Console

If you’re working with WeakMap and WeakSet objects, you can now see their entries in the web console.

Also, logs coming from service workers show up by default in controlled tabs. There is still a lot of work coming to improve the service worker debugging experience, follow [this tracking bug](https://bugzil.la/943220) for more.

### Network monitor

- You’ll see markers showing when DOMContentLoaded and load events fire in
[the network timeline](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor#Timeline). - You can now filter out filenames based on a string match. Just use “-” in front of the string, which is a handy way to narrow down a big list of requests.

And a big thanks to contributors Albert Juhé and Tim Nguyen for their help in making the [netmonitor table UI match](https://bugzilla.mozilla.org/show_bug.cgi?id=951714) the rest of the toolbox.

There are a lot of improvements in this version so [download it now](https://www.mozilla.org/en-US/firefox/developer/all/) — it’s free!

## About
[
Lin Clark ](https://twitter.com/linclark)

Lin works in Advanced Development at Mozilla, with a focus on Rust and WebAssembly.

## 2 comments

JensDecember 23rd, 2015 at 01:33jamesJanuary 18th, 2016 at 10:55