---
title: 'Developer Edition 42: Wifi Debugging, Win10, Multiprocess Firefox, ReactJS
  tools, and more – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/08/developer-edition-42-wifi-debugging-win10-multiprocess-firefox-reactjs-tools-and-more/
author: Brian Grinstead
published: '2015-08-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 42 has arrived! In this release, we put a lot of effort into the quality and polish of the Developer Edition browser. Although many of the [bugs resolved this release](http://mzl.la/1DQeEkp) don’t feature in the [Release Notes](https://www.mozilla.org/en-US/firefox/42.0a2/auroranotes/), these small fixes make the tools faster and more stable. But there’s still a lot to report, including a major change to how Firefox works.

### Debugging over wifi

Now, with [remote website debugging](https://developer.mozilla.org/docs/Tools/Remote_Debugging/Debugging_Firefox_for_Android_over_Wifi), you can debug Firefox for Android devices over wifi – no USB cable or ADB needed.

### Multiprocess is enabled by default

[Multiprocess Firefox](https://wiki.mozilla.org/Electrolysis) (aka E10s) has been enabled by default in Developer Edition. When it’s enabled, Firefox renders and executes web-related content in a single background *content* process. If you experience any issues with addons after updating to Developer Edition 42, try [disabling incompatible addons](http://arewee10syet.com/) or [reverting to a single process mode](https://wiki.mozilla.org/File:E10s-toggle-in-preferences.png) using *about:preferences*.

### Windows 10 theme support

The Developer Edition theme has a new look in Windows 10 to match the OS styling. Take a look:

### React Developer Tools support for Firefox

If you’re developing with ReactJS, you may have noticed that the React project recently released a beta for their developer tools extension, [including initial support for Firefox](http://www.infoq.com/news/2015/08/React-Devtools-beta). While there are no official builds yet of the Firefox version, the source is available on [github](https://github.com/facebook/react-devtools/tree/master).

### Other notable changes

- Asynchronous call stacks now allow you to follow the code flow through setTimeout, DOM event handlers, and Promise handlers. (
[Bug 981514](https://bugzil.la/981514)) - There is a new
[configurable Firefox OS simulator](https://developer.mozilla.org/en-US/docs/Tools/WebIDE/Setting_up_runtimes#Configuring_Simulators)page in WebIDE. From here, you can change a simulator to run with a custom profile and screen size, using a list of presets from reference devices. ([Bug 1156834](https://bugzil.la/1156834)) [CSS filter presets](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_CSS_filters#Saving_filter_presets)are now available in the inspector. ([Bug 1153184](https://bugzil.la/1153184))- The MDN tooltip now uses syntax highlighting for code samples. (
[Bug 1154469](https://bugzil.la/1154469)) - When using the “copy” keyboard shortcut in the inspector, the outerHTML of the selected node is now copied onto the clipboard. (
[Bug 968241](https://bugzil.la/968241)) - New UX improvements have landed in the style editor’s search feature. (
[Bug 1159001](https://bugzil.la/1159001),[Bug 1153474](https://bugzil.la/1153474)) - CSS variables are now treated as normal declarations in the inspector. (
[Bug 1142206](https://bugzil.la/1142206)) - CSS autocomplete popup now supports pressing ‘down’ to list all results in an empty value field (
[Bug 1142206](https://bugzil.la/1142206))

Thanks to everyone who contributed time and energy to help the DevTools team in this release of Firefox Developer Edition 42! Each release takes a lot of effort from people writing patches, testing, documenting, reporting bugs, sending feedback, discussing features, etc. You can help set our priorities by sharing constructive feedback and letting us know [what you’d like from Firefox Developer Tools](http://mzl.la/devtools).

You can [download Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) now, for free.

## 11 comments

Ult ComboAugust 24th, 2015 at 12:38Dan CallahanAugust 24th, 2015 at 13:00Ult ComboAugust 24th, 2015 at 15:41Tim NguyenAugust 24th, 2015 at 16:20Ult ComboAugust 24th, 2015 at 16:24LucasAugust 27th, 2015 at 12:21AlexandreAugust 28th, 2015 at 00:24Brian GrinsteadAugust 28th, 2015 at 08:30NickolayAugust 29th, 2015 at 14:45Brian GrinsteadAugust 31st, 2015 at 09:16Brian GrinsteadSeptember 1st, 2015 at 14:20