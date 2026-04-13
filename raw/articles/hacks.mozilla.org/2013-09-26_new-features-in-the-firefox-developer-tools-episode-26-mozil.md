---
title: 'New Features in the Firefox Developer Tools: Episode 26 – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2013/09/new-features-in-the-firefox-developer-tools-episode-26/
author: Paul Rouget
published: '2013-09-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 26 was just uplifted to the Aurora release channel which means we are back to report on new features in Firefox Developer Tools. Here’s a summary of some of the most exciting new features.

## Inspector: pseudo element support

To get more flexibility in the design of an element without using additional nodes, it’s very common to use [CSS pseudo elements](https://developer.mozilla.org/en-US/docs/Web/CSS/Pseudo-elements), eg (`:before/:after{content:””}`). In the Inspector it’s now possible to see the rules applied to pseudo elements.

![](../../assets/b003eb7eddce734e.png)


## Debugger: break on uncaught exceptions

It’s now possible to pause the debugger on uncaught exceptions. It makes debugging unexpected errors easier and prevents the developer from having to step over a barrage of exceptions which were handled by Try/Catch blocks.

## Web Console: Better text selection

It used to be hard to select text from the web console. Fixing this bug needed a whole rewrite of the console output area. This will make copying/pasting logs much simpler and provides the ground-work for improved console output features landing soon.

## Global UI improvements

It is now possible to zoom in and zoom out for the UI of all the developer tools. Do you prefer bigger fonts? Hit `Ctrl +`

. Smaller? `Ctrl -`

. (`Cmd`

in Mac OS X).

The DOM view in the Inspector has also been improved. The selection is more obvious and it’s easier to expand nodes and very long attributes are now cropped.

Keyboard shortcuts improvements: It’s now easier to control the tools from the keyboard. We’ve created many new keyboard shortcuts and tried to be compatible with other browsers. All the [available keyboard shortcuts for the Developer Tools](https://developer.mozilla.org/en-US/docs/Tools/Keyboard_shortcuts) are listed on MDN.

As an added bonus, we also moved the URL preview (the bar that pops out when hovering a link with the mouse) above the toolbox. It doesn’t cover the Web Console input or any other tool anymore.

## Responsive Design View

The Responsive Design View comes with 3 new improvements:

- Touch Event simulation (mouse events are translated to touch events)
- Quick screenshot
- Precise resize. Press Ctrl while moving the mouse for a more accurate resize

## When can I use these features?

All of these features and more are available in the [Firefox Aurora](http://www.mozilla.org/firefox/aurora/) release channel. In another 12 weeks, these features will roll over into Firefox stable.

Have some feedback about devtools? Ping [@FirefoxDevTools](https://twitter.com/FirefoxDevTools) on Twitter, or swing by #devtools on [irc.mozilla.org](https://wiki.mozilla.org/IRC).

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 17 comments

Patrick H LaukeSeptember 26th, 2013 at 01:53AntwanSeptember 26th, 2013 at 02:22Paul RougetSeptember 26th, 2013 at 02:41LukeOctober 2nd, 2013 at 19:48Patrick H LaukeSeptember 26th, 2013 at 02:50Robert Nyman [Editor]September 26th, 2013 at 04:16Nicolas ToniazziSeptember 26th, 2013 at 06:04Ken SaundersSeptember 27th, 2013 at 04:50Robert Nyman [Editor]September 27th, 2013 at 04:56pdSeptember 27th, 2013 at 07:14KWiersoSeptember 27th, 2013 at 14:50AlbertSeptember 27th, 2013 at 08:17Robert Nyman [Editor]September 27th, 2013 at 13:02James MOctober 1st, 2013 at 06:26Mike RatcliffeOctober 6th, 2013 at 13:51zalexOctober 10th, 2013 at 13:34Mike RatcliffeOctober 10th, 2013 at 16:35