---
title: Developer Edition 47 – User agent emulation, popup debugging and more – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/03/developer-edition-47-user-agent-emulation-popup-debugging-and-more/
author: Tim Nguyen
published: '2016-03-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

This week marks the release of [Firefox Developer Edition 47](https://www.mozilla.org/en-US/firefox/developer/)! In recent weeks, we’ve covered the [DevTools reload add-on](https://hacks.mozilla.org/2016/02/introducing-devtools-reload/) and [service worker tooling](https://hacks.mozilla.org/2016/03/debugging-service-workers-and-push-with-firefox-devtools/), so be sure to check out those posts. In this post, we’ll cover the rest of the updates and changes in this Developer Edition release.

## User Agent emulation

We have added the ability to emulate a custom user agent on any webpage from responsive mode. You can now simply type your new user agent string inside the “Custom User Agent” field. You can use this to check whether a site uses user agent sniffing. For example, you can type in a mobile browser user agent to see how a website would look on your phone.

Here is a screencast of the feature:

![User Agent Emulation](../../assets/86baabb0356f8f0c.gif)


## Retaining paths as graph

In the previous release, we added a *dominator view* to help you debug memory-intensive applications. In this version, we’ve improved it by adding a retaining paths panel, which gives you a graph displaying all the nodes that are preventing a selected node from being *garbage collected*. This is particularly useful when you are debugging a possible memory leak. You can read more about this feature in the MDN documentation [here](https://developer.mozilla.org/en-US/docs/Tools/Memory/Dominators_view#Retaining_Paths_panel).

Here is a screenshot of the graph:

![](https://mdn.mozillademos.org/files/12770/dominators-retaining-paths-1.png)


## Console multi-line input

The way multi-line input in the console is handled has been improved. When pressing the “Enter” key, the console will now detect whether your input is complete or not. If it is, pressing “Enter” will simply execute your command. If not, pressing “Enter” will add a new line to your input, so you can seamlessly continue writing your command.

## Storage Inspector

The storage inspector now has support for [cache storage](https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage), which is very useful if you’re debugging a service worker. Be sure to check [Sole Penadés’ blog post](https://hacks.mozilla.org/2016/03/debugging-service-workers-and-push-with-firefox-devtools/) that dives into the details of service worker debugging.

In addition to cache storage support, you can now filter the contents of the table using the search box located on the top toolbar. Here’s a screenshot of the feature:

![](../../assets/fb6426e9c9baae90.png)


## Theme changes

In this release, we gave a visual tune-up to the toolbox. We have made small tweaks such as reducing the default tab width and adding new icons inside the memory tool, but we have also made some major changes. For example, we gave the light theme a complete makeover, to give it a lighter and more polished look and feel.

Here is a screenshot of the new light theme:

![Refreshed light theme](../../assets/33beb57f1054ec57.png)


We have also updated the debugger gutter style—conditional breakpoints are now highlighted in the gutter in orange. Here’s a screenshot:

![New debugger gutter](../../assets/d4f0665a2de3b9ed.png)


Finally, we have moved the network monitor toolbar to the top to be more accessible and more consistent with the other tools.

![Network monitor toolbar](../../assets/54648bfee93553df.png)


## Debugging popups for addons

In preparation for the release of [WebExtensions](https://wiki.mozilla.org/WebExtensions), we are adding new features that will make add-on debugging easier. In this release, we’ve made inspecting popups much easier. You can now lock popups so they don’t disappear once you click away. To use this feature, you need to launch the [Browser Toolbox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Toolbox) and click the icon with the four squares located in the top-right corner of the toolbox. You can read more about how to debug your extensions [here](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Debugging#Debugging_popups).

Here is a screencast showing this feature in action:

## Other notable changes

In addition to the improvements above, we have polished various areas throughout the toolbox, in particular:

We have also removed the 3D view, since this feature conflicts with the multi-process version of Firefox. If you’d like to use the feature, you can install [this add-on](https://addons.mozilla.org/en-US/firefox/addon/tilt/) instead.

Finally, the font inspector has been disabled by default, since it will be reworked for future releases. You can re-enable the tool by toggling the `devtools.fontinspector.enabled` preference in `about:config`.

Thanks to everyone that has contributed to this Developer Edition release! Grab a copy of [the latest Developer Edition](https://www.mozilla.org/en-US/firefox/developer/all/) now and let us know what you think.

## About Tim Nguyen

I work on web browsers.

## 16 comments

Nazar MokrynskyiMarch 17th, 2016 at 10:08Brian GrinsteadMarch 17th, 2016 at 11:00Nazar MokrynskyiMarch 17th, 2016 at 11:21EvertMarch 17th, 2016 at 13:31Tim NguyenMarch 18th, 2016 at 12:07LukeMarch 18th, 2016 at 22:31Šime VidasMarch 17th, 2016 at 21:36MichaëlMarch 18th, 2016 at 02:52Maël LavaultMarch 18th, 2016 at 03:12Tim NguyenMarch 18th, 2016 at 12:11Mike RatcliffeMarch 24th, 2016 at 09:15Tom LivingstonMarch 23rd, 2016 at 13:53Mike RatcliffeMarch 24th, 2016 at 09:18Tom LivingstonMarch 24th, 2016 at 09:58Bill WhiteMarch 28th, 2016 at 06:39Brian GrinsteadMarch 28th, 2016 at 10:32