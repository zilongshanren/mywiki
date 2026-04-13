---
title: Aurora 12 is out – improvements and updated Developer Tools – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/02/aurora-12-is-out-improvements-and-updated-developer-tools/
author: Robert Nyman
published: '2012-02-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Aurora 12](http://www.mozilla.org/firefox/channel/) is out, together with updated Developer Tools, and these are the improvements/changes.


## Highlights

A few of the improvements that stand out a little more:

### ECMAScript Harmony’s Simple Map and Set builtins

For testing purposes, we have implemented [ECMAScript Harmony’s Simple Map and Set builtins](http://wiki.ecmascript.org/doku.php?id=harmony:simple_maps_and_sets). This is only in Aurora and will be disabled when it goes to beta, so please test it out now and give feedback! There is also [MDN documentation on Set](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Set) and [MDN documentation on Map](https://developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Map) if you want to learn more.

If you are more interested in Harmony progress, [read up on our implementation work for ECMAScript 6](https://wiki.mozilla.org/ES6_plans)

### Support multitouch on Android

We’re happy to now have implemented [multitouch](https://developer.mozilla.org/en/DOM/Touch_events) for Firefox on Android!

### Let authors put line breaks (newlines) in tooltips (title attribute)

It might seem like a small thing, but has been discussed quite some time. You can now [use newlines for tooltips](https://bugzilla.mozilla.org/show_bug.cgi?id=358452)!

### XMLHttpRequest should allow you to specify a network timeout in ms (for async requests)

Instead of timeouts and similar, this offers a way to [specify a network timeout for XMLHttpRequests](https://bugzilla.mozilla.org/show_bug.cgi?id=525816) using [the timeout attribute](http://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#the-timeout-attribute).

## List of improvements

Here are all the improvements we’ve made complete with links to each bug listing for those who want to read up more on respective implementation.

### DOM

[When JavaScript is disabled, alternate content provided within the canvas element is not rendered and the canvas element still is rendered](https://bugzilla.mozilla.org/show_bug.cgi?id=302566)[Support multitouch on Android](https://bugzilla.mozilla.org/show_bug.cgi?id=603008)[Implement text/html for @mozilla.org/xmlextras/domparser](https://bugzilla.mozilla.org/show_bug.cgi?id=102699)[Implement DOMError as defined in DOM 4](https://bugzilla.mozilla.org/show_bug.cgi?id=705640)[Let authors put line breaks (newlines) in tooltips (title attribute)](https://bugzilla.mozilla.org/show_bug.cgi?id=358452)

### JavaScript

[Implement Harmony simple Map and Set builtins](https://bugzilla.mozilla.org/show_bug.cgi?id=697479)[Implement ArrayBuffer.slice](https://bugzilla.mozilla.org/show_bug.cgi?id=718128)[Removed support for sharp variables](https://developer.mozilla.org/en/JavaScript/Sharp_variables_in_JavaScript)

### Layout

[There is no Bidi/Joining algorithm on Arabic/Persian texts in MathML](https://bugzilla.mozilla.org/show_bug.cgi?id=208309)[Implement border-image revisions in latest css3-background](https://bugzilla.mozilla.org/show_bug.cgi?id=497995)[Implement column-fill property of CSS3 spec](https://bugzilla.mozilla.org/show_bug.cgi?id=695222)[remove handling of percentages as intrinsic widths/heights (SVG height=”100%” width=”100%” defaults)](https://bugzilla.mozilla.org/show_bug.cgi?id=611099)[getBoundingClientRect needs to take transforms into account](https://bugzilla.mozilla.org/show_bug.cgi?id=591718)[Adjust MathML text integration point treatment to comply with spec changes](https://bugzilla.mozilla.org/show_bug.cgi?id=711049)[Remove a pop loop from <rp> and <rt> handling, because the loop has been removed from the spec long ago](https://bugzilla.mozilla.org/show_bug.cgi?id=711052)[(munderover-align) [MathML3] munder, mover, munderover: add support for the align attribute](https://bugzilla.mozilla.org/show_bug.cgi?id=557476)[Implement CSS3 text-align-last](https://bugzilla.mozilla.org/show_bug.cgi?id=536557)[Add a ‘length’ property to DOMSVGStringList](https://bugzilla.mozilla.org/show_bug.cgi?id=711958)[SVGTests interface is not implemented](https://bugzilla.mozilla.org/show_bug.cgi?id=607854)

### Media

### Network

[Return correct websocket close code when browser navigates away from page](https://bugzilla.mozilla.org/show_bug.cgi?id=712188)[Allow XHR to data URL](https://bugzilla.mozilla.org/show_bug.cgi?id=702820)[XMLHttpRequest should allow to specify a network timeout in ms (for async requests)](https://bugzilla.mozilla.org/show_bug.cgi?id=525816)

### Tools

## Developer Tools

There has been a total of 89 improvements to Web Console, Scratchpad, Style Editor, Page Inspector, Style Inspector, HTML view and Page Inspector 3D view (Tilt). Here are the highlights:

[Errors and messages that were logged before the Web Console was opened are displayed when the console is opened up to a queue size limit](https://bugzilla.mozilla.org/show_bug.cgi?id=611032)[Scratchpad now includes Find and uses the standard platform key binding (ctrl-F/cmd-F)](https://bugzilla.mozilla.org/show_bug.cgi?id=650345)[Scratchpad now includes Jump to Line and uses the standard platform key binding ctrl/cmd-J](https://bugzilla.mozilla.org/show_bug.cgi?id=714942)[Style Editor now includes transitions](https://bugzilla.mozilla.org/show_bug.cgi?id=687698)[Style Editor adds in a closing brace for new rules to avoid disrupting the rest of the CSS](https://bugzilla.mozilla.org/show_bug.cgi?id=713612)[You can now remove nodes from the Page Inspector 3D view by pressing ‘x’. This makes it easier to visually select the node you want.](https://bugzilla.mozilla.org/show_bug.cgi?id=715647)[Normal close window keybinding works for Style Editor](https://bugzilla.mozilla.org/show_bug.cgi?id=720431)[Page Inspector highlighter now updates its position as the page changes](https://bugzilla.mozilla.org/show_bug.cgi?id=566092)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

dr.pradhanApril 25th, 2012 at 02:51Janet SwisherApril 25th, 2012 at 11:36GrampaJerryApril 25th, 2012 at 07:43Robert NymanApril 25th, 2012 at 15:28GrampaJerryApril 25th, 2012 at 07:46JanApril 26th, 2012 at 14:49Jean-Yves PerrierApril 26th, 2012 at 15:52JanApril 27th, 2012 at 03:27Will PeavyMay 11th, 2012 at 13:39AlexMay 2nd, 2012 at 11:43JanMay 3rd, 2012 at 07:26Michael HallMay 3rd, 2012 at 05:23JanMay 3rd, 2012 at 07:31JamesJuly 12th, 2012 at 03:52