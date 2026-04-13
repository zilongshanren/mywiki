---
title: WebIDE, Storage inspector, jQuery events, iframe switcher + more – Firefox
  Developer Tools Episode 34 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/09/webide-storage-inspector-jquery-events-iframe-switcher-more-firefox-developer-tools-episode-34/
author: Heather Arthur
published: '2014-09-16'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A new set of Firefox Developer Tools features has just been uplifted to the [Aurora channel](http://www.mozilla.org/firefox/aurora/). These features are available right now in Aurora, and will be in the Firefox 34 release in November. This release brings new tools (storage inspector, WebIDE), an updated profiler, and handy enhancements to the existing tools:

## WebIDE

WebIDE, a new tool for in-browser app development, has been enabled by default in this release. [WebIDE](https://developer.mozilla.org/docs/Tools/WebIDE) lets you create a new [Firefox OS](https://developer.mozilla.org/Firefox_OS) app (which is just a web app) from a template, or open up the code for an already created app. From there you can edit the app’s files. It’s one click to run the app in a simulator and one more to debug it with the developer tools. Open WebIDE from Firefox’s “Web Developer” menu. ([docs](https://developer.mozilla.org/docs/Tools/WebIDE))

## Storage inspector

There’s a new panel that shows the data your page has stored in cookies, localStorage, sessionStorage, and IndexedDB, which was created mostly by [Girish Shama](https://mozillians.org/en-US/u/grssam/). Enable the [Storage](https://developer.mozilla.org/docs/Tools/Storage_Inspector) panel by checking off [Settings](https://developer.mozilla.org/docs/Tools/Tools_Toolbox#Settings) > “Default Developer Tools” > “Storage”. The panel is read-only right now, with editing ability planned for a future release. ([docs](https://developer.mozilla.org/docs/Tools/Storage_Inspector)) ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=970517)) ([UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5707193-i-need-a-better-insight-into-appcache-and-offline))

## jQuery events

The event listener popup in the [Inspector](https://developer.mozilla.org/docs/Tools/Page_Inspector) now supports jQuery. This means the popup will display the function you attached with e.g. `jQuery.on()`

, and not the jQuery wrapper function itself. See [this post](http://flailingmonkey.com/view-jquery-and-jquery-live-events-in-firefox-devtools/) for more info and how to add support for your preferred framework. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1044932))

## Iframe switcher

Change the frame you’re debugging using the new frame selection menu. Selecting a frame will switch *all* of the tools to debug that iframe, including the Inspector, Console, and Debugger. Add the frame selection button by checking off [Settings](https://developer.mozilla.org/docs/Tools/Tools_Toolbox#Settings) > “Available Toolbox Buttons” > “Select an iframe”. ([docs](https://developer.mozilla.org/docs/tools/Working_with_iframes)) ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=977043))([UserVoice request](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5893367-allow-switching-between-active-frames-in-the-conso))

## Updated profiler

An updated JavaScript profiler appears in the new “Performance” tab (formerly the “Profiler” tab). New to the profiler are a frame rate timeline and categories for frames like “network” and “graphics”. ([docs](https://developer.mozilla.org/docs/Tools/Performance)) ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=879008))

## console.table()

Add a call to `console.table()`

anywhere in your JavaScript to log data to the console using a table-like display. Log any object, array, [Map](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Map), or [Set](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Set). Sort a column in the table by clicking on its header. ([docs](https://developer.mozilla.org/docs/Web/API/Console.table)) ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=899753))

## Selector preview

Hover over a CSS selector in the Inspector or Style Editor to highlight all the nodes that match that selector on the page. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=971662))

## Other mentions

**Persistent split console**– The split console (opened by pressing ESC) will now open with the tools if you had it open the last time the tools were closed. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=974550))**Web audio – AudioParam connections**– the[Web Audio Editor](https://developer.mozilla.org/docs/Tools/Web_Audio_Editor)now displays connections from AudioNodes to AudioParams. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1032129))

Special thanks to the 41 contributors that added [all the features and fixes](http://mzl.la/Zfc5VY) in this release.

Comment here, shoot feedback to [@FirefoxDevTools](http://twitter.com/firefoxdevtools) on Twitter, or propose changes on the [Developer Tools feedback channel](http://mzl.la/devtools). If you’d like to help out, check out the [guide to getting involved](https://wiki.mozilla.org/DevTools/GetInvolved).

## About Heather Arthur

Firefox developer tools developer at Mozilla, working mainly on the style tools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 35 comments

derpSeptember 16th, 2014 at 12:22tmntSeptember 16th, 2014 at 13:48ChristophSeptember 16th, 2014 at 14:53Robert Nyman [Editor]September 17th, 2014 at 00:02aeischeidSeptember 16th, 2014 at 15:15Robert Nyman [Editor]September 17th, 2014 at 00:03thevasyaSeptember 16th, 2014 at 21:40Robert Nyman [Editor]September 17th, 2014 at 00:03NoitidartSeptember 17th, 2014 at 08:22Robert Nyman [Editor]September 25th, 2014 at 12:49Jerry VoelkerSeptember 17th, 2014 at 11:20Robert Nyman [Editor]September 25th, 2014 at 12:49David FrankSeptember 19th, 2014 at 02:01Mark FinkleSeptember 22nd, 2014 at 20:53SunngSeptember 21st, 2014 at 23:21Joe WalkerSeptember 23rd, 2014 at 11:58Robert Nyman [Editor]September 25th, 2014 at 12:54ff userSeptember 22nd, 2014 at 01:18Robert Nyman [Editor]September 25th, 2014 at 12:52EricSeptember 22nd, 2014 at 02:07Robert Nyman [Editor]September 25th, 2014 at 12:55mieSeptember 22nd, 2014 at 04:41Robert Nyman [Editor]September 25th, 2014 at 12:55wazooSeptember 22nd, 2014 at 08:36Robert Nyman [Editor]September 25th, 2014 at 12:56Davos Seaworth LordOfTheRainwoodSeptember 22nd, 2014 at 12:46mehmet yilmazSeptember 23rd, 2014 at 01:42Robert Nyman [Editor]September 25th, 2014 at 12:57RobSeptember 23rd, 2014 at 05:13Joe WalkerSeptember 23rd, 2014 at 12:03Michael NiemannSeptember 23rd, 2014 at 08:31J. Ryan StinnettSeptember 23rd, 2014 at 13:36thinsoldierSeptember 24th, 2014 at 07:43thinsoldierSeptember 24th, 2014 at 07:44marioOctober 14th, 2014 at 15:53