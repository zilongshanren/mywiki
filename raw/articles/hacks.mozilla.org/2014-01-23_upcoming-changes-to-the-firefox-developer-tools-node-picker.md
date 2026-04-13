---
title: Upcoming changes to the Firefox Developer tools node picker – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2014/01/upcoming-changes-to-the-firefox-developer-tools-node-picker/
author: Chris Heilmann
published: '2014-01-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

If you are a user of the [Firefox Developer tools](https://developer.mozilla.org/en-US/docs/Tools/) you’ll soon see a change of the node picker of the [Page Inspector](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector) component.

As [documented on Bugzilla](https://bugzilla.mozilla.org/show_bug.cgi?id=916443) and reported by [Patrick Brosset](http://twitter.com/patrickbrosset) these changes mean:

- The node inspect button in the devtools has moved from the inspector-panel toolbar, on the left, to the toolbox toolbar, on the right:


- The highlighter is shown as you hover over nodes in the markup-panel (instead of having to click on them)
- What was called the “lock” state isn’t there anymore. This means, once a node is selected in the markup-panel or by using the inspect button and clicking on the page, the highlighter isn’t going to stay visible for as long as you don’t select another node. This was sometimes frustrating as it may be hiding things you wanted to see.

You can see the [new functionality in action](http://www.youtube.com/watch?v=zBYEg40ByCM) on YouTube.

This improves the compatibility in user interaction with other developer tools and makes it easier to move in between nodes should you have picked the wrong one.

Are there any other things you like to see in the Firefox Developer tools? Tell us, and [don’t be shy to get involved and file bugs](https://wiki.mozilla.org/DevTools/GetInvolved).

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 14 comments

BobJanuary 23rd, 2014 at 01:49Hervé RenaultJanuary 23rd, 2014 at 02:09Robert Nyman [Editor]January 23rd, 2014 at 07:00DelapouiteJanuary 23rd, 2014 at 02:34Mike RatcliffeJanuary 23rd, 2014 at 06:20LukeJanuary 23rd, 2014 at 08:15Victor PorofJanuary 23rd, 2014 at 09:23elavJanuary 23rd, 2014 at 06:36Dane MacMillanJanuary 23rd, 2014 at 08:16MaxJanuary 23rd, 2014 at 08:55Mike RatcliffeJanuary 28th, 2014 at 06:50thinsoldierJanuary 30th, 2014 at 14:07IgnatiusFebruary 8th, 2014 at 10:37Mike RatcliffeFebruary 10th, 2014 at 03:42