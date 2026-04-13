---
title: Drag Elements, Console History, and more – Firefox Developer Edition 39 – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/04/drag-elements-console-history-and-more-firefox-developer-edition-39/
author: J Ryan Stinnett
published: '2015-04-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Quite a few big new features, improvements, and bug fixes made their way into Firefox Developer Edition 39. Update your Firefox [Developer Edition](https://www.mozilla.org/en-US/firefox/channel/#developer), or [Nightly](https://nightly.mozilla.org/) builds to try them out!

The [Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector) now allows you to move elements around via [drag and drop](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_HTML#Drag_and_drop). Click and hold on an element and then drag it to where you want it to go. This feature was added by contributor Mahdi Dibaiee.

Back in [Firefox 33](https://hacks.mozilla.org/2014/07/event-listeners-popup-media-sidebar-cubic-bezier-editor-more-firefox-developer-tools-episode-33/), a tooltip was added to the rule view to allow editing curves for cubic bezier CSS animations. In Developer Edition 39, we’ve greatly enhanced the tooltip’s UX by adding various standard curves you can try right away, as well as cleaning up the overall appearance. This enhancement was added by new contributor John Giannakos.

![cubic](../../assets/f196b0ab0775cb9a.gif)


The CSS animations panel we debuted in [Developer Edition 37](https://hacks.mozilla.org/2015/01/web-animation-tools-network-security-insights-font-inspector-improvements-and-more-firefox-developer-tools-episode-37/) now includes a time machine. You can rewind, fast forward, and set the current time of your animations.

Previously, when the DevTools console closed, your past [Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) history was lost. Now, [Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) history is persisted across sessions. The recent commands you’ve entered will remain accessible in the next toolbox you open, whether it’s in another tab or after restarting Firefox. Additionally, we’ve added a `clearHistory`

console command to reset the stored list of commands.

The shorthand `$_`

has been added as an alias for the last result evaluated in the [Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console). If you evaluated an expression without storing the result to a variable (for example), you can use this as a quick way to grab the last result.

We now format pseudo-array-like objects as if they were arrays in the [Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) output. This makes a pseudo-array-like object easier to reason about and inspect, just like a real array. This feature was added by contributor Johan K. Jensen.

![pseudo-array](../../assets/3c59268ae211c646.png)


WiFi debugging for Firefox OS has landed. WiFi debugging allows [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) to connect to your Firefox OS device via your local WiFi network instead of a USB cable. We’ll discuss this feature in more detail in a future post.

[WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) gained support for Cordova-based projects. If you’re working on a mobile app project using Cordova, [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) now knows how to build the project for devices it supports without any extra configuration.

- Attribute changes only flash the changed attribute in the
[Markup View](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_HTML), instead of the whole element. [Canvas Debugger](https://hacks.mozilla.org/2014/03/introducing-the-canvas-debugger-in-firefox-developer-tools/)now supports setTimeout for animations.[Inline box model highlighting.](https://hacks.mozilla.org/2015/03/understanding-inline-box-model/)[Browser Toolbox](https://developer.mozilla.org/en-US/docs/Tools/Browser_Toolbox)can now be opened from a shortcut: Cmd-Opt-Shift-I / Ctrl-Alt-Shift-I.[Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor)now shows the remote server’s IP address and port.- When an element’s highlighted in the
[Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector), you can now use the arrow keys to highlight the current element’s parent (left key), or its first child, or its next sibling if it has no children, or the next node in the tree if it has no siblings (right key). This is especially useful when an element and its parent occupy the same space on the screen, making it difficult to select one of them using only the mouse.

For an even more complete list, check out [all 200 bugs resolved](http://mzl.la/1GiJGQm) during the Firefox 39 development cycle.

Thanks to all the new developers who made their first DevTools contribution this release:

- Anush
- Brandon Max
- Geoffroy Planquart
- Johan K. Jensen
- John Giannakos
- Mahdi Dibaiee
- Nounours Heureux
- Wickie Lee
- Willian Gustavo Veiga

Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here, [add/vote for ideas on UserVoice](http://mzl.la/devtools), or get in touch with the team at [@FirefoxDevTools on Twitter](https://twitter.com/FirefoxDevTools).

## About
[
J. Ryan Stinnett ](https://convolv.es/)

Staff Engineer working on Firefox DevTools at Mozilla.

## 5 comments

Alex@ndreApril 15th, 2015 at 01:46IvanApril 16th, 2015 at 05:21AndrisApril 28th, 2015 at 05:23J. Ryan StinnettApril 29th, 2015 at 09:04Mervas DayiMay 9th, 2015 at 08:13