---
title: Box model highlighter, Web Console improvements, Firefox OS HUD + more – Firefox
  Developer Tools Episode 30 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/03/box-model-highlighter-web-console-improvements-firefox-os-hud-more-firefox-developer-tools-episode-30/
author: Brian Grinstead
published: '2014-03-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 30 was just uplifted to the [Aurora release channel](https://www.mozilla.org/en-US/firefox/aurora/), so let’s take a look at the most important DevTools changes in this release.

# Inspector

One of our most requested features has been to highlight box model regions of elements on the page. We are happy to report that this feature has landed in Firefox 30. One of the great things is that the colors of the box model highlighter match the box model diagram found in the right pane of the inspector more clearly than before.

Check out the [inspector documentation](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector#Box_model_view) to read more about the new functionality, or just see the screenshot and short video below:

There is a new font family tooltip to the CSS rule view. Hover over a font-family value to see an inline preview of the font. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=702577))

![Inspector font family preview](../../assets/680c224a1d6fb7db.png)


# Web Console

There are some big improvements in the web console to help view and navigate output.

- Better highlighting for all JS objects and functions in console output (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=584733)) - Highlight and jump to nodes from the Console (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=757866)) - We have added support for console.count() (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=922208)).

![Highlight and jump to nodes from console](../../assets/1e9b4f59d42fdc5e.png)


Running the `cd()`

command in the console switches the scope between iframes. Read more in the [cd command documentation](https://developer.mozilla.org/en-US/docs/Tools/Web_Console#Working_with_iframes). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=609872))

![Console cd() command](../../assets/f8f114a82aea9357.png)


You can read more from Mihai [about the ongoing changes to the web console](http://www.robodesign.ro/mihai/blog/web-console-improvements-episode-30#firefox30). He has also been [documenting the web console API for extension authors](https://developer.mozilla.org/en-US/docs/Tools/Web_Console/Custom_output).

# Firefox OS

The network monitor is now working with Firefox OS. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=917227))

There is now memory tracking ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=963498)) and jank tracking ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=963499)) in the Firefox OS Developer HUD. You can read much more about jank (aka “event loop lag”) in Paul’s [ Firefox OS: tracking reflows and event loop lags](http://paulrouget.com/e/fxoshud/).

# Network Monitor

The Network Monitor has a new look to go along with some new features:

- The design of the network timeline has been updated, which has actually improved scroll performance on the panel. (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=909251)) - Hovering over a request with an image response now shows a popup with the image. (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=859135)) - Network requests with an image response now display a thumbnail near the file name. (
[development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=859136))

![Network Monitor Timeline UI](../../assets/374d7c4a10764497.png)


Network requests with a JSON-like response will show an object preview, even if the response type is plain text. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=964977))

# Toolbox

There is new behavior for console shortcut key (`cmd+alt+k`

or `ctrl+shift+k`

). It now focuses the input line in web console at all times, opening the toolbox if necessary but never closing it. There are [more details about this change on robcee’s blog](http://robcee.net/2014/updated-console-keyboard-shortcuts-in-firefox/). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=612253))

To save some space on the top toolbar, there are now options to hide command buttons, like Scratchpad. The only buttons enabled by default now are Inspect Element, Split Console, and Responsive Mode. [More information about this change on the devtools mailing list](https://groups.google.com/d/msg/mozilla.dev.developer-tools/zhFZRLnlmVw/qFalqQTUUOMJ). ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=974947)). To enable Scratchpad, Paint Flashing, or Tilt, just click on the checkbox in the options panel.

We would like to give a special thanks to all 46 people who contributed patches to DevTools this release! Here is a [list of all DevTools bugs resolved for Firefox 30](http://mzl.la/1p7uKJ2).

Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here or get in touch with the team at [@FirefoxDevTools](https://twitter.com/firefoxdevtools).

## About Brian Grinstead

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 50 comments

EthanMarch 25th, 2014 at 09:44PatrickMarch 25th, 2014 at 09:48Brian GrinsteadMarch 25th, 2014 at 10:33LukeMarch 26th, 2014 at 17:45Robert Nyman [Editor]March 25th, 2014 at 10:27Hervé Renault (@HerveRenault)March 25th, 2014 at 10:00Robert Nyman [Editor]March 25th, 2014 at 10:27JeffMarch 25th, 2014 at 10:08Brian GrinsteadMarch 25th, 2014 at 10:11starwedMarch 25th, 2014 at 10:23Brian GrinsteadMarch 25th, 2014 at 11:31somedudeMarch 25th, 2014 at 12:27Robert Nyman [Editor]March 25th, 2014 at 12:40NateMarch 25th, 2014 at 12:46Brian GrinsteadMarch 25th, 2014 at 12:54SrapMarch 26th, 2014 at 02:29Brian GrinsteadApril 2nd, 2014 at 09:22Jaroslav MaturaMarch 25th, 2014 at 16:15Brian GrinsteadMarch 25th, 2014 at 18:25EricMarch 25th, 2014 at 17:10Jeff GriffithsMarch 26th, 2014 at 10:45AlexMarch 25th, 2014 at 17:17Brian GrinsteadMarch 25th, 2014 at 18:16MikeMarch 25th, 2014 at 20:05Luke MichaelsMarch 25th, 2014 at 22:46morkMarch 26th, 2014 at 04:12NiclasMarch 26th, 2014 at 07:57Brian GrinsteadMarch 26th, 2014 at 08:10MickMarch 28th, 2014 at 09:56Jeff GriffithsMarch 28th, 2014 at 10:22MickMarch 29th, 2014 at 13:45Robert Nyman [Editor]March 31st, 2014 at 02:35Jeff GriffithsMarch 31st, 2014 at 09:25Hervé RenaultMarch 28th, 2014 at 10:19Jeff GriffithsMarch 28th, 2014 at 10:24Hervé RenaultMarch 28th, 2014 at 10:27goliatoneMarch 30th, 2014 at 20:18Robert Nyman [Editor]March 31st, 2014 at 02:37JeffMarch 31st, 2014 at 08:19JeffMarch 31st, 2014 at 09:04Jeff GriffithsMarch 31st, 2014 at 09:26Dane MacMillanApril 1st, 2014 at 07:57Jeff GriffithsApril 1st, 2014 at 13:25CarolinaApril 1st, 2014 at 17:15TimApril 2nd, 2014 at 11:47aheuApril 2nd, 2014 at 17:54Mihai SucanApril 3rd, 2014 at 04:39opoApril 6th, 2014 at 07:44Mihai SucanApril 7th, 2014 at 08:57HubertApril 22nd, 2014 at 03:06