---
title: 'Firefox 54: E10S-Multi, WebExtension APIs, CSS clip-path – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2017/06/firefox-54-e10s-webextension-apis-css-clip-path/
author: Dan Callahan
published: '2017-06-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## “E10S-Multi:” A new multi-process model for Firefox

Today’s release completes Firefox’s transformation into a fully multi-process browser, running many simultaneous content processes in addition to a UI process and, on Windows, a special [GPU process](https://ashughes.com/?p=426). This design makes it easier to utilize all of the cores available on modern processors and, in the future, to securely sandbox web content. It also improves stability, ensuring that a single content process crashing won’t take out all of your other tabs, nor the rest of the browser.

An initial version of multi-process Firefox (codenamed “Electrolysis”, or “e10s” for short) [debuted with Firefox 48 last August](https://blog.mozilla.org/futurereleases/2016/08/02/whats-next-for-multi-process-firefox/). This first version moved Firefox’s UI into its own process so that the browser interface remains snappy even under load. Firefox 54 takes this further by running many content processes in parallel: each one with its own RAM and CPU resources managed by the host operating system.

Additional processes *do* come with a small degree of memory overhead, no matter how well optimized, but we’ve worked wonders to reduce this to the bare minimum. Even with those optimizations, we wanted to do more to ensure that Firefox is respectful of your RAM. That’s why, instead of spawning a new process with every tab, Firefox sets an upper limit: four by default, but [configurable by users](https://support.mozilla.org/en-US/kb/performance-settings) (`dom.ipc.processCount`

in `about:config`

). This keeps you in control, while still letting Firefox take full advantage of multi-core CPUs.

To learn more about Firefox’s multi-process architecture, check out this [Medium post about the search for the “Goldilocks” browser](https://medium.com/mozilla-tech/the-search-for-the-goldilocks-browser-and-why-firefox-may-be-just-right-for-you-1f520506aa35).

## New WebExtension APIs

Firefox continues its rapid implementation of new WebExtension APIs. These APIs are [designed to work cross-browser](https://hacks.mozilla.org/2017/06/cross-browser-extensions-available-now-in-firefox/), and will be the only APIs available to add-ons when Firefox 57 launches this November.

Most notably, it’s now possible to create [custom DevTools panels](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/API/devtools.panels) using WebExtensions. For example, the screenshot below shows the Chrome version of the [Vue.js DevTools](https://github.com/vuejs/vue-devtools) running in Firefox without any modifications. This dramatically reduces the maintenance burden for authors of devtools add-ons, ensuring that no matter which framework you prefer, its tools will work in Firefox.

Additionally:

[Sidebars can be created](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/sidebar_action)via a`sidebar_action`

manifest property. Together with other APIs, sidebars can be used to implement[vertical](https://addons.mozilla.org/en-US/firefox/addon/sidebar-tabs-webextension/)or[tree-style](https://addons.mozilla.org/firefox/addon/tree-tabs/)tabs, among other things.- WebExtensions can now
[replace or customize the New Tab page](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/chrome_url_overrides). ([Example](https://github.com/mdn/webextensions-examples/tree/master/top-sites)). - WebExtensions can also register support for
[custom protocols](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/manifest.json/protocol_handlers). For example, an add-on could redirect`irc://`

links to IRCCloud.

Read about the full set of new and changed APIs on the [Add-ons Blog](https://blog.mozilla.org/addons/2017/03/13/webextensions-firefox-54/), or check out the complete [WebExtensions documentation](https://developer.mozilla.org/en-US/Add-ons/WebExtensions) on MDN.

## CSS shapes in clip-path

The CSS clip-path property allows authors to define which parts of an element are visible. Previously, Firefox only supported clipping paths defined as SVG files. With Firefox 54, authors can also use [CSS shape functions](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape) for circles, ellipses, rectangles or arbitrary polygons ([Demo](https://codepen.io/ladybenko/pen/oWJBwW)).

Like many CSS values, clipping shapes can be animated. There are some [rules that control how the interpolation](https://developer.mozilla.org/en-US/docs/Web/CSS/basic-shape#Interpolation_of_basic_shapes) between values is performed, but long story short: as long as you are interpolating between the same shapes, or polygons with the same number of vertices, you should be fine. Here’s how to animate a circular clipping:

You can also dynamically change clipping according user input, like in this example that features a “periscope” effect controlled by the mouse:

To learn more, check [our article on clip-path](https://hacks.mozilla.org/2017/06/css-shapes-clipping-and-masking/) from last week.

## Project Dawn

Lastly, the release of Firefox 54 marks the completion of the[ Project Dawn](http://release.mozilla.org/firefox/release/2017/05/30/Dawn-update.html) transition, eliminating Firefox’s pre-beta release channel, codenamed “Aurora.” Firefox releases now move directly from Nightly into Beta every six weeks. Firefox Developer Edition, which was based on Aurora, is now based on Beta.

For early adopters, we’ve also made Firefox Nightly for Android [available on Google Play](https://play.google.com/store/apps/details?id=org.mozilla.fennec_aurora).

## About
[
Dan Callahan ](http://dancallahan.info)

Engineer with Mozilla Developer Relations, former Mozilla Persona developer.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 22 comments

edJune 13th, 2017 at 12:50Israel MJune 13th, 2017 at 16:49Dan CallahanJune 13th, 2017 at 18:48EganJune 14th, 2017 at 01:57Juraj M.June 13th, 2017 at 14:07oJune 13th, 2017 at 18:34Dan CallahanJune 13th, 2017 at 18:38SapaJune 14th, 2017 at 02:30Dan CallahanJune 14th, 2017 at 12:26SuryaJune 15th, 2017 at 11:39Dan CallahanJune 15th, 2017 at 20:25jonJune 15th, 2017 at 11:50Dan CallahanJune 15th, 2017 at 20:22RobertLuJune 16th, 2017 at 03:38Dan CallahanJune 16th, 2017 at 06:28gabeJune 16th, 2017 at 10:13Dan CallahanJune 16th, 2017 at 10:21BaraaJune 27th, 2017 at 03:36Dan CallahanJune 27th, 2017 at 10:31BaraaJune 27th, 2017 at 12:24Dan CallahanJune 27th, 2017 at 16:12BaraaJune 28th, 2017 at 00:08