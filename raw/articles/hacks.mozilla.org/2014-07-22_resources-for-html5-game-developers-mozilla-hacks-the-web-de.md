---
title: Resources for HTML5 game developers – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/07/resources-for-html5-game-developers/
author: Chris Heilmann; Victor Porof Posted; Featured Article; HTML
published: '2014-07-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today we released Firefox 31 and it offers a couple of new features that help HTML5 game developers to code and debug sophisticated games. In addition Mozilla [blogged about the first commercial games](https://blog.mozilla.org/blog/2014/07/22/first-commercial-web-games-launch-leveraging-mozilla-pioneered-technology/) leveraging asm.js, Dungeon Defenders Eternity and Cloud Raiders both of which were cross-compiled in to JavaScript using the Emscripten compiler. Games like these show that HTML5 is ready as a game platform.

If you are interested in working with Emscripten you can get more information at the main [Emscripten wiki](https://github.com/kripken/emscripten/wiki) or grab the code on the [github page](https://github.com/kripken/emscripten). Another good resource is the getting started with [Emscripten tutorial](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Emscripten/Introducing#Getting_started_tutorials) on MDN. If you are wondering about the performance of asm.js, read [asm.js performance improvements in the latest version of Firefox make games fly!](https://hacks.mozilla.org/2014/05/asm-js-performance-improvements-in-the-latest-version-of-firefox-make-games-fly/) for details.

In this post we’ll introduce you to some of the resources built by Mozillians that allow you to code and debug HTML5 based games. This list is not exhaustive and we appreciate feedback on any valuable resources that would help in this arena. Don’t be shy and tell us about them in the comments.

## Where To Start

When developing an HTML5 based game, you have a lot of choices to make. These range from what editor to use, if the game will use Canvas 2d, WebGL, SVG, or CSS up to which specific rendering frameworks and game engines to use. Most of these decisions will be based on the developer experience and the platforms the game will be published on. No article will answer all these questions but we wanted to put together a post that would help get you started down the path.

One of the key resources available for game developers on MDN is the [Games Zone](https://developer.mozilla.org/en-US/docs/Games). This section of MDN contains general game development articles, demos, external resources and examples. It also includes detailed descriptions of some of the APIs that a developer will need to be aware of when implementing an HMTL5 game, including sound management, networking, storage and graphics rendering. We are currently in the process of adding content and upgrading the zone. In the future we hope to have content and examples for most common scenarios, frameworks and tool chains.

In the meantime here are a few posts and MDN articles that help game developers getting started.

## Tools

As an HTML5 developer you will have no shortage of tools at your disposal. In the Mozilla community we have been hard at work expanding the features that Firefox Developer Tools provide. These include a full-featured [JavaScript Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger), [Style Editor](https://developer.mozilla.org/en-US/docs/Tools/Style_Editor), [Page Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector), [Scratchpad](https://developer.mozilla.org/en-US/docs/Tools/Scratchpad), [Profiler](https://developer.mozilla.org/en-US/docs/Tools/Profiler), [Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) and [Web Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console).

In addition to these, some notable tools have been updated or introduced recently and offer some great functionality for the game developer.

## Canvas Debugger

With the current release of Firefox, we added a Canvas Debugger to the browser.

![s_canvasdebugger](../../assets/5c37373178a1f355.png)


The Canvas Debugger allows you to trace through all canvas context calls that are used to generate a frame. Calls are color coded for specific calls for things like drawing elements or using a specific shader program. The Canvas Debugger is not only useful when developing a WebGL based game but can also be used when debugging a Canvas 2D based game. In the game below you can see in the animation strip as each image is drawn to the canvas. You can click any of these lines to get directly to the part of your JavaScript responsible for this action.

![s_captainrogers](../../assets/291aa67fdbf25757.png)


Two very common issues that have been reported when using the Canvas Debugger are with animations generated using [setInterval instead of requestAnimationFrame](https://bugzilla.mozilla.org/show_bug.cgi?id=978948) and [inspecting canvas elements in an iFrame](https://bugzilla.mozilla.org/show_bug.cgi?id=981748).

To get more information about the Canvas Debugger be sure to read over [Introducing the Canvas Debugger in Firefox Developer Tools](https://hacks.mozilla.org/2014/03/introducing-the-canvas-debugger-in-firefox-developer-tools/).

## Shader Editor

When developing WebGL based games it is very useful to be able to test and alter shader programs while the application is running. Using the Shader Editor within the developer tools makes this possible. Vertex and Fragment Shader programs can be modified without the need to reload the page, or black boxed to see what effect this has on the resulting output.

![s_ShaderEditor](../../assets/dec8570e10ab997d.png)


For more information on the Shader Editor, be sure to see [Live editing WebGL shaders with Firefox Developer Tools](https://hacks.mozilla.org/2013/11/live-editing-webgl-shaders-with-firefox-developer-tools/) post and take a look at this [MDN article](https://developer.mozilla.org/en-US/docs/Tools/Shader_Editor) which contains a couple of videos showing live editing.

## Web Audio Editor

The current version of Firefox Aurora (32) – has a Web Audio Editor. The Editor displays a graphical representation of all the Audio Nodes and their connections in the current AudioContext. You can drill down to specific attributes of each node to inspect them.

![s_webaudioeditor](../../assets/70730776f493e2f9.png)


The [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) provides more robust and complex sound creation, manipulation and processing than what is available in the HTML5 [Audio tag](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Using_HTML5_audio_and_video). When using the Web Audio API make sure to read over [Writing Web Audio API code that works in every browser](https://developer.mozilla.org/en-US/Apps/Build/Manipulating_media/Web_Audio_API_cross_browser) as it contains pertinent information about support for the various audio nodes.

For more information on the Web Audio Editor be sure to read this [Hacks article](https://hacks.mozilla.org/2014/06/introducing-the-web-audio-editor-in-firefox-developer-tools/) introducing the Web Editor and this [MDN article](https://developer.mozilla.org/en-US/docs/Tools/Web_Audio_Editor).

## Network Monitor

When developing an HTML5 based game network impact can be not only cumbersome but also costly if the user is on mobile device. Using the Network Monitor you can visually inspect all network request for location, time spent on the operation, and the type and size of the artifact.

![s_networkmon](../../assets/2a314c62c0a46ff8.png)


In addition you can use the Network Monitor to get a visual performance analysis of your app when cached versus non-cached.

![s_networkcache](../../assets/13cdc4936071d5b0.png)


To get more information on the Network Monitor see the [MDN page](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor).

## Web IDE

When starting your game one of your first choices will be which editor to use. And there are a lot of them (Sublime, Eclipse, Dreamweaver, vi, etc). In most cases a you already have a favorite. If you are interested in doing your development within the Browser you may want to have a look at the Web IDE that was recently released in Firefox Nightly.

![s_webide](../../assets/ad7b0ad5feb51254.png)


The Web IDE project provides not only a fully functional editor but also acts as a publishing agent to various local and remote platforms, debugger, template framework and application manager. In addition the framework supporting this project provides APIs that will allow other editors to use functionality provided in the tool. To get more details on the work that is being done in this area have a look at [this post](https://hacks.mozilla.org/2014/06/webide-lands-in-nightly/).

In order to keep up-to-date with news on the Firefox Developer Tools, follow their [article series](https://hacks.mozilla.org/2014/06/toolbox-inspector-scratchpad-improvements-firefox-developer-tools-episode-32/) on the Hacks blog. For more detailed information on new, stable developer tools features, check out their documentation on [MDN](https://developer.mozilla.org/en-US/docs/Tools).

## APIs

The MDN Games Zone lists various APIs and [articles](https://developer.mozilla.org/en-US/docs/Games/Introduction) that are useful for beginning game development.

![s_apis](../../assets/2ddf6b678fc3f0d0.png)


In addition to these resources you may be interested in looking over some additional posts that can be valuable for development.

If your game is going to support multiplayer interaction using either WebRTC or WebSockets you may also be interested in looking at Together.js which provides collaborative features for web apps. To get an idea what is possible take a look at [Introducing TogetherJS](https://hacks.mozilla.org/2013/10/introducing-togetherjs/).

Many games will require storage and [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) can be used to handle these needs. For information on extending the capabilities of IndexedDB read over [Breaking the Borders of IndexedDB](https://hacks.mozilla.org/2014/06/breaking-the-borders-of-indexeddb/). You may also be interested in [localForage](https://github.com/mozilla/localForage) which provides browser agnostic support for simple storage. To get more details about this library read over this [Hacks post](https://hacks.mozilla.org/2014/02/localforage-offline-storage-improved/).

## Game Optimization

HTML5 games today offer a great deal of power to the game developer. That said many of these games are going to be played on a mobile device, which in comparison to your desktop will pale in performance. So if you plan on your game being a success across platforms it is important that you optimize your code. The [Optimizing your JavaScript Game for Firefox OS](https://hacks.mozilla.org/2013/05/optimizing-your-javascript-game-for-firefox-os/) post has a lot of great techniques to help you build a game that performs well on low-end mobile devices.

## Localization

In order to reach the most users of your game you may want to consider offering it in different languages. As part of this developers should start with localization built into the game. We are doing a great deal of work around recruiting translators to help you translate your game. To get more information about this initiative see [this post](https://hacks.mozilla.org/2014/05/introducing-translationtester-and-localization-support-for-open-web-apps/).

## Your Voice

As Mozilla is about the community of developers and users, we want your help and your feedback. If you have recommendations for specific features that you would like to see in the products make sure to either get involved in discussion on [irc.mozilla.org](https://wiki.mozilla.org/IRC) or through our [mailing lists](https://lists.mozilla.org/listinfo/). You can also log bugs at [bugzilla.mozilla.org](https://bugzilla.mozilla.org/). In addition we are also provide additional feedback channels for our [DevTools](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas) and [Open Web Apps](https://openwebapps.uservoice.com/forums/258478-open-web-apps).

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## About Victor Porof

Mozillian, hacker, working on Firefox DevTools.

## 9 comments

vladimir batista tamayoJuly 22nd, 2014 at 08:47Robert Nyman [Editor]July 22nd, 2014 at 09:45Dhondi SrikantJuly 22nd, 2014 at 21:45Robert Nyman [Editor]July 23rd, 2014 at 02:09NoitidartAugust 5th, 2014 at 00:01Robert Nyman [Editor]August 5th, 2014 at 01:11dhidyAugust 5th, 2014 at 21:47GergőAugust 6th, 2014 at 13:44AkhtarAugust 11th, 2014 at 01:10