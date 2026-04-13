---
title: 'Firefox 55: first desktop browser to support WebVR – Mozilla Hacks - the Web
  developer blog'
url: https://hacks.mozilla.org/2017/08/firefox-55-supports-webvr/
author: Dan Callahan
published: '2017-08-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**WebVR Support on Desktop**

Firefox on Windows is the [first desktop browser](https://hacks.mozilla.org/2017/08/webvr-for-all-windows-users/) to support the new [WebVR](https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API) standard (and macOS support is in [Nightly](https://nightly.mozilla.org/)!). As the originators of WebVR, Mozilla wanted it to embody the same principles of standardization, openness, and interoperability that are hallmarks of the Web, which is why WebVR works on any device: Vive, Rift, and beyond.

To learn more, check out [vr.mozilla.org](https://vr.mozilla.org/), or dive into [A-Frame](https://aframe.io/), an open source framework for building immersive VR experiences on the Web.

**New Features for Developers**

Firefox 55 supports several new ES2017/2018 features, including [async generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Method_definitions#Async_generator_methods) and the rest/spread (“`...`

“) operator for objects:

```
let a = { foo: 1, bar: 2 };
let b = { bar: 'two' };
let c = { ...a, ...b }; // { foo: 1, bar: 'two' };
```


MDN has great documentation on using `...`

with [object literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_operator#Spread_in_object_literals) or for [destructuring assignment](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment), and the [TC39 proposal](https://github.com/tc39/proposal-object-rest-spread) also provides a concise overview of this feature.

Over in DevTools, the Network panel now supports filtering results with queries like “`status-code:200`

“.

There are also new, optional columns for cookies, protocol, scheme, and more that can be hidden or shown inside the Network panel, as seen in the screenshot above.

**Making Firefox Faster**

We’ve implemented several new features to keep Firefox itself running quickly:

- New installations of Firefox on Windows will now default to the more stable and secure 64-bit version. Existing installations will upgrade to 64-bit with our next release, Firefox 56.
- Restoring a session or restarting Firefox with many tabs open is now an order of magnitude faster. For reasons unknown,
[Dietrich Ayala](https://twitter.com/dietrich)has a Firefox profile with**1,691 open tabs**. With Firefox 54, starting up his instance of Firefox took 300 seconds and 2 GB of memory. Today, with Firefox 55, it takes just[15 seconds and 0.5 GB](https://metafluff.com/2017/07/21/i-am-a-tab-hoarder/)of memory. This improvement is primarily thanks to the tireless work of an external contributor, Kevin Jones, who virtually eliminated the fixed costs associated with restoring tabs. - Users can now
[adjust Firefox’s number of content processes](https://support.mozilla.org/kb/performance-settings)from within Preferences. Multiple content processes[debuted in Firefox 54](https://hacks.mozilla.org/2017/06/firefox-54-e10s-webextension-apis-css-clip-path/), and allow Firefox to take better advantage of modern, multi-core CPUs, while still being respectful of RAM utilization. - Firefox now uses its built-in
[Tracking Protection](https://developer.mozilla.org/en-US/Firefox/Privacy/Tracking_Protection)lists to identify and[throttle tracking scripts](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/setTimeout#Throttling_of_tracking_timeout_scripts)running in background pages. After a short grace period, Firefox will increase the minimum`setInterval`

or`setTimeout`

for callbacks scheduled by tracking scripts to**10 seconds**while the tab is in the background. This is in addition to our usual 1 second throttling for background tabs, and helps ensure that unused tabs can’t invisibly ruin performance or battery life. Of course, tabs that are playing audio or video are not throttled, so music in a background tab won’t stutter. - With the announcement of
[Flash’s end of life](https://blogs.adobe.com/conversations/2017/07/adobe-flash-update.html), and in coordination with[Microsoft](https://blogs.windows.com/msedgedev/2017/07/25/flash-on-windows-timeline/)and[Google](https://www.blog.google/products/chrome/saying-goodbye-flash-chrome/), Firefox 55 now requires users to explicitly[click to activate Flash](https://blog.mozilla.org/futurereleases/2017/07/25/firefox-roadmap-flash-end-life/)on web pages as we work together toward completely removing Flash from the Web platform in 2020.

**Making the Web Faster**

Firefox 55 introduces several new low-level capabilities that help improve the performance of demanding web applications:

- The
[IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)API allows the browser to respond to the visibility of elements on a page far more efficiently and reliably than existing hacks with polling or invisible Flash movies. You can read more in[my article on IntersectionObserver](https://hacks.mozilla.org/2017/08/intersection-observer-comes-to-firefox/)from last week.

[SharedArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SharedArrayBuffer)and[Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics)objects are new JavaScript primitives that allow workers to share and simultaneously access the same memory. This finally makes efficient multi-threading a reality on the Web. The only downside? Developers have to care about thread safety, mutexes, etc. when sharing memory, just like in any other multi-threaded language. You can learn more about`SharedArrayBuffer`

in[this code cartoon introduction](https://hacks.mozilla.org/2017/06/a-cartoon-intro-to-arraybuffers-and-sharedarraybuffers/)and[this explainer article](https://hacks.mozilla.org/2016/05/a-taste-of-javascripts-new-parallel-primitives/)from last year.- The
[requestIdleCallback()](https://developer.mozilla.org/en-US/docs/Web/API/Background_Tasks_API)API offers a new way to schedule callbacks whenever the browser has a few extra, unused milliseconds between frames, or whenever a maximum timeout has elapsed. This makes it possible to squeeze work into the margins where the browser would otherwise be idle, and to defer lower priority work while the browser is busy. Using this API requires a bit of finesse, but[MDN has great documentation](https://developer.mozilla.org/en-US/docs/Web/API/Background_Tasks_API)on how to use`requestIdleCallback()`

effectively.

**Making the Web More Secure**

[Geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation) and [Storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API) join the ranks of powerful APIs like [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API) that are only allowed on secure, `https://`

origins. If your site needs a TLS certificate, consider [Let’s Encrypt](https://letsencrypt.org/): a completely free, automated, and non-profit Certificate Authority.

Additionally, Firefox 55 will [not allow plug-ins to load from or on non-HTTP/S schemes](https://bugzilla.mozilla.org/show_bug.cgi?id=1335475), such as `file:`

.

**New WebExtension APIs**

WebExtensions can now:

[Replace the new tab page](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/chrome_settings_overrides)and modify the browser’s search engine.[Change proxy settings](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/proxy)dynamically.[Request and inspect permissions](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/permissions)that they have been granted.- Opt-in to the browser’s native styling via the
`browser_styles`

manifest property on sidebars, action menus, and more.

**And more…**

There are many more changes in the works as we get ready for the [next era of Firefox](https://www.cnet.com/special-reports/mozilla-firefox-fights-back-against-google-chrome/) in November. Some users of Firefox 55 will begin seeing our new [Firefox Screenshots](https://screenshots.firefox.com/) feature, the Bookmarks / History sidebar can now be docked on either side of the browser, and we just announced three new [Test Pilot experiments](https://testpilot.firefox.com).

For a complete overview of what’s new, refer to the official [Release Notes](https://www.mozilla.org/en-US/firefox/55.0/releasenotes/), MDN’s [Firefox 55 for Developers](https://developer.mozilla.org/en-US/Firefox/Releases/55), and the [Mozilla Blog announcement](https://blog.mozilla.org/blog/2017/08/08/webvr-new-speedy-features/) .

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## 16 comments

J. Pablo FernándezAugust 8th, 2017 at 11:52Frank L. Laifer, Major, USAF(retired)August 10th, 2017 at 11:47Dan CallahanAugust 10th, 2017 at 12:03Andrea NieldAugust 10th, 2017 at 17:43Dan CallahanAugust 11th, 2017 at 11:36jonAugust 8th, 2017 at 23:53Dan CallahanAugust 9th, 2017 at 02:00Lawrence SanAugust 9th, 2017 at 12:38Dan CallahanAugust 9th, 2017 at 12:56Daniel LevyAugust 18th, 2017 at 20:33Christian AarfingAugust 28th, 2017 at 07:28danAugust 15th, 2017 at 17:23bjmAugust 16th, 2017 at 08:09Rob PolAugust 17th, 2017 at 01:20PeggyAugust 22nd, 2017 at 00:46Dan CallahanAugust 31st, 2017 at 09:28