---
title: 'Developer Edition 40: Always active network monitoring, CSS rules filtering,
  and much more – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2015/05/developer-edition-40-always-active-network-monitoring-css-rules-filtering-and-more/
author: Brian Grinstead
published: '2015-05-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 40 was just uplifted, and we have a lot of updates to share. This release took a major effort by Developer Tools contributors to address feedback we’ve heard directly from people using our tools. Grab a copy of the [ Developer Edition browser](https://www.mozilla.org/en-US/firefox/developer/) and check it out.

## Experimental Multi-process Support: A Request

When you update to Developer Edition 40, you’ll be prompted to opt in to test [multi-process Firefox](https://developer.mozilla.org/en-US/Firefox/Multiprocess_Firefox). Please consider helping us test this new feature and providing feedback around any issues you see.

## New in the Inspector

- There is now a filter box in the CSS Rules view that lets you find rules that match a string. See the
[Filter Styles screencast](https://www.youtube.com/watch?v=9w8vDIWqnAE)or the screenshot below. (Development notes:[1120616](https://bugzilla.mozilla.org/show_bug.cgi?id=1120616)and[1157293](https://bugzilla.mozilla.org/show_bug.cgi?id=1157293).)

- There is a new CSS documentation tooltip for CSS properties. Right click on any property in the CSS Rules view and select “Show MDN Docs” to see more information about that property. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=980006).)

- Inspector search now includes results from iframes and also includes class / id results without the CSS prefix. (Development notes:
[873443](https://bugzilla.mozilla.org/show_bug.cgi?id=873443)and[1149346](https://bugzilla.mozilla.org/show_bug.cgi?id=1149346).) - There is a new CSS Filter Editor Tooltip added by Mahdi Dibaiee. Check out the
[CSS Filter Editor Tooltip screencast](https://www.youtube.com/watch?v=t3NKmmWfklU)for a demo, or try it on the[filter demos page](https://developer.mozilla.org/en-US/docs/Web/CSS/filter#Functions)in Developer Edition. ([development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1055181)) - The Animation Inspector has had some major updates. It now shows subtree animations, playback rate can be controlled, and it previews and highlights animated DOM nodes. (Development notes:
[1155651](https://bugzilla.mozilla.org/show_bug.cgi?id=1155651),[1155653](https://bugzilla.mozilla.org/show_bug.cgi?id=1155653), and[1144615](https://bugzilla.mozilla.org/show_bug.cgi?id=1144615).)

There are too many changes to list in this post, but here are a few more interesting updates you may come across in the Inspector:

- The Box Model view has legends for the regions and tooltips to show which CSS rule invoked the computed value. (Development notes:
[1141571](https://bugzilla.mozilla.org/show_bug.cgi?id=1141571)and[1151956](https://bugzilla.mozilla.org/show_bug.cgi?id=1151956).) - shift+clicking a color swatch switches between color unit formats in place. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1136257).) - New
*Scroll Into View*,*Open Link in New Tab*,*Copy Link*,*Open In Style Editor*, and*Open in Debugger*context menu items in the Markup View. (Development notes:[901250](https://bugzilla.mozilla.org/show_bug.cgi?id=901250),[921102](https://bugzilla.mozilla.org/show_bug.cgi?id=921102), and[1158822](https://bugzilla.mozilla.org/show_bug.cgi?id=1158822).)

## Network Monitor News

- One of the top requests in our UserVoice feedback channel has been to
[make the network panel always active](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/suggestions/5893748-make-the-network-panel-always-active)once the toolbox is opened. We are happy to say you no longer need to switch to this panel to begin recording network traffic. ([Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=862341).) - Cached network requests now show up in the Network Monitor. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=764958).)

Here’s a selection of other changes and improvements in this release:

- New
*Copy Response*,*Copy URL parameters*, and*Copy Request/Response Headers*context menu items on each request. (Development notes:[955933](https://bugzilla.mozilla.org/show_bug.cgi?id=955933),[1150717](https://bugzilla.mozilla.org/show_bug.cgi?id=1150717), and[1150715](https://bugzilla.mozilla.org/show_bug.cgi?id=1150715).) - Search box to filter requests. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=892229).) - IP address included in
*Domain*tooltip for network monitor. ([Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1150697).) - Added access keys to the request context menu. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1158046).)

## Web Console

- New console method:
`console.dirxml()`

. ([Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=922212).) - New filter options in the web console to show console messages from workers. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1125205).) - Quotes in strings are no longer added if logged via console.log. Thanks to new contributor Dmitry Sagalovskiy for adding this feature! (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=977586).)

## Debugger

- New
*Copy URL*and*Open in New Tab*context menu items for debugger sources. ([Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=848502).) - Breaking in unnamed eval scripts now works. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=1131756).)

## General

*Open Link In New Tab*item is now added to sheets in the Style Editor. ([Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=992947).)- There is a button to collapse the Inspector sidebar completely. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=994055).) - The Developer toolbar matches the light devtools theme when applied. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=969914)). - Refreshed theme colors for better contrast. (
[Development notes](https://bugzilla.mozilla.org/show_bug.cgi?id=947242).) - Better HiDPI support for Windows. (Development notes:
[1147702](https://bugzilla.mozilla.org/show_bug.cgi?id=1147702)and[1023546](https://bugzilla.mozilla.org/show_bug.cgi?id=1023546).)

Special thanks to all the people who contributed patches to Firefox Developer Tools this release! Here is a [list of all the DevTools bugs resolved for Firefox 40](http://mzl.la/1DNDHyV). Kudos to the many contributors.

Do you have feedback, bug reports, feature requests, or questions? As always, you can comment here, get in touch with the team at [@FirefoxDevTools](https://twitter.com/firefoxdevtools), or share your constructive feedback and feature requests on our [Firefox Dev Tools feedback channel](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas/).

## 7 comments

JerryMay 20th, 2015 at 10:28Brian GrinsteadMay 20th, 2015 at 11:07Kamal BhattMay 22nd, 2015 at 16:34jsantellMay 24th, 2015 at 13:08Brian GrinsteadMay 20th, 2015 at 10:43Nate WiebeMay 26th, 2015 at 05:16Jeff GriffithsMay 27th, 2015 at 19:50