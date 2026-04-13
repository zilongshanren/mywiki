---
title: Developing cross-browser extensions with web-ext 3.2.0 – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/10/developing-cross-browser-extensions-with-web-ext-3-2-0/
author: Luca Greco
published: '2019-10-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [ web-ext](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Getting_started_with_web-ext) tool was created at Mozilla to help you build browser extensions faster and more easily. Although our first launch focused on support for desktop Firefox, followed by Firefox for Android, our vision was always to support cross-browser development once we shipped Firefox support.

With the 3.2.0 release, you can use `web-ext`

to truly build cross-browser extensions! Here is an example of developing an extension in [Google Chrome](https://www.google.com/chrome/) using the [run](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/web-ext_command_reference#web-ext_run) command:

`$ web-ext run -t chromium`


What’s even better is you can run your extension in both Firefox and Chrome at the same time:

`$ web-ext run -t firefox-desktop -t chromium`


As you’d expect, you can develop in any other [Chromium](https://www.chromium.org/)-based browser such as [Brave](https://brave.com/), [Microsoft Edge](https://www.microsoft.com/en-us/windows/microsoft-edge), [Opera](https://www.opera.com/) or [Vivaldi](https://vivaldi.com/). Here’s an example of developing in Opera:

`$ web-ext run -t chromium --chromium-binary /usr/bin/opera`


Firefox’s [WebExtensions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions) API has always strived for [Chrome API](https://developer.chrome.com/extensions/api_index) compatibility but several improvements have resulted in subtle differences, like how WebExtensions APIs always return promises. Mozilla already offers the [webextensions-polyfill](https://github.com/mozilla/webextension-polyfill) library to normalize promises and other things across both browser platforms.

And now, we are excited to offer a robust development solution for cross-browser extensions! Once you give it a try, let us know if you run into [issues](https://github.com/mozilla/web-ext/issues/new) or have ideas for improvement.

Here is an example of launching an extension in Firefox and Chrome then editing a CSS file in the extension source to show off the [automatic reloading](https://extensionworkshop.com/documentation/develop/getting-started-with-web-ext/#Automatic_extension_reloading) feature.


## Other new features in `web-ext`

3.2.0

Chromium browser support isn’t the only nice new feature. Thanks to [parse-json 5.0.0](https://github.com/sindresorhus/parse-json), the parsing errors on the extension manifest and locale files will now include a code frame. This will make it a lot easier to track down and fix mistakes.

## About Luca Greco

## About
[
kumar303 ](http://farmdev.com/)

Kumar hacks on Mozilla web services and tools for various projects, such as those supporting [Firefox Add-ons](https://github.com/mozilla/addons/). He hacks on lots of [random open source projects](https://github.com/kumar303/) too.

## 3 comments

Scott Fortmann-RoeOctober 16th, 2019 at 10:05kumar303October 16th, 2019 at 10:23anonymousOctober 28th, 2019 at 09:04