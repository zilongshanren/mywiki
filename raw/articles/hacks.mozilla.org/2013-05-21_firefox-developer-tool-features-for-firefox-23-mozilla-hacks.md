---
title: Firefox Developer Tool Features for Firefox 23 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/05/firefox-developer-tool-features-for-firefox-23/
author: Rob Campbell
published: '2013-05-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Another uplift has left the building and it’s time to take a look at what’s in Firefox Developer Tools in Firefox 23 currently Aurora, our pre-beta channel. You can download it from [the Aurora Download page](http://www.mozilla.org/en-US/firefox/aurora/) today. Firefox 23 is currently scheduled to hit the release channel on Tuesday August 6th, 2013.

Episode XXIII is a barn-storming, hair-raising spectacle of incredible epicness that is sure to delight and amuse. If you want a sneak peak at features under active development, give [Nightly](http://nightly.mozilla.org/) a try.

## Network Monitor

There’s a new tool in the toolbox: The Network Monitor. It’s a classic waterfall timeline view of network activity on a site. This data’s been available since Firefox 4 via the Web Console, albeit in a less visually pleasing way.

Please file bugs under the [Developer Tools: Netmonitor](https://bugzilla.mozilla.org/enter_bug.cgi?product=Firefox) component in Bugzilla.

## Remote Style Editor

In Firefox 23, you can now edit styles via a Remote Connection on a suitably-enabled device. This should be great help for App Developers interested in testing and debugging styles on a mobile device over the remote protocol in real time.

As of the time of this writing, the Remote Style Editor should be compatible with Firefox for Android version 23, also scheduled for uplift to Aurora. We are working on [incorporating the Style Editor Actors for the remote protocol into the Firefox OS Simulator](https://github.com/mozilla/r2d2b2g/issues/499) and investigating what it will take to backport them to Firefox OS release.

## Options Panel

We’ve added a Gear menu to the Toolbar containing an Options panel for turning tools on or off. As we add more stuff, this is going to be a popular place to manage preferences related to the Developer Tools.

Currently, there are options to turn on the Light or Dark theme for the tools and enable Chrome Debugging.

## Initial SourceMap Support for Debugger Protocol

The first pieces of SourceMap support for the Debugger have landed and we are now able to serve up SourceMapped JS files for your debugging pleasure. Soon to follow will be column support for breakpoints allowing you to debug minified JS with a SourceMap.

Watch for the upcoming blog post by Nick Fitzgerald on Hacks explaining the magic.

## Variables View Everywhere

Our Variables View is an improved Object Inspector and an integral part of our Debugger. Naturally, we wanted to put it in Everything. So now the Web Console and Scratchpad have a Variables View. Use the ESC key to close it.

## Browser Console

If you have Chrome Debugging turned on, check out the Browser Console. It’s a replacement for the ancient Error Console and gives you a Chrome-context command line for executing JavaScript against the browser. It’s nice and should be enabled by default in Firefox 24.

## GCLI Appcache Command

We finally have a little something for developers trying to use App Cache to store offline data. A new `appcache`

command for the Graphical Command Line. You can read about it in Mike Ratcliffe’s [The Application Cache is no longer a Douchebag](http://flailingmonkey.com/application-cache-not-a-douchebag).

## Web Console in Debugger Frame

The Web Console is now fully-remoted (and has been since version 18). It now makes use of the Debugger’s current Frame if paused on a breakpoint.

## Multiple Paused Debuggers

You can now debug multiple tabs at the same time using the Script Debugger. Previously, when attempting to use the debugger on two separate tabs, you’d be given a notification to resume the debugger in the other tab. Now you can debug as many tabs as you like.

There is one caveat to this awesome power, however. Due to the nested event loops each Debugger creates, you have to resume each tab in the order in which they were paused. Debug carefully and always carry a big stack.

You can see a comprehensive list of [bugfixes](https://bugzilla.mozilla.org/buglist.cgi?list_id=6499762&resolution=FIXED&classification=Client%20Software&chfieldto=2013-05-13&chfield=target_milestone&query_format=advanced&chfieldfrom=2013-03-20&chfieldvalue=Firefox%2023&bug_status=RESOLVED&bug_status=VERIFIED&component=Developer%20Tools&component=Developer%20Tools%3A%203D%20View&component=Developer%20Tools%3A%20Console&component=Developer%20Tools%3A%20Debugger&component=Developer%20Tools%3A%20Framework&component=Developer%20Tools%3A%20Graphic%20Commandline%20and%20Toolbar&component=Developer%20Tools%3A%20Inspector&component=Developer%20Tools%3A%20Netmonitor&component=Developer%20Tools%3A%20Profiler&component=Developer%20Tools%3A%20Responsive%20Mode&component=Developer%20Tools%3A%20Scratchpad&component=Developer%20Tools%3A%20Source%20Editor&component=Developer%20Tools%3A%20Style%20Editor&product=Firefox) in table form in [Firefox 23 Developer Tools Fixes](http://robcee.net/2013/new-features-in-firefox-developer-tools-episode-23/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 24 comments

RonMay 21st, 2013 at 02:54Rob CampbellMay 21st, 2013 at 04:41AndréMay 21st, 2013 at 03:08SkatoxMay 21st, 2013 at 06:29DanielMay 21st, 2013 at 06:51ericMay 21st, 2013 at 05:56LukeJune 10th, 2013 at 23:37SkatoxMay 21st, 2013 at 06:29leeoniyaMay 21st, 2013 at 08:22DougMay 21st, 2013 at 10:52RahlyJune 19th, 2013 at 15:49Thomas AndersenMay 21st, 2013 at 11:55Rob CampbellMay 21st, 2013 at 17:42LukeJune 19th, 2013 at 19:52ArasMay 21st, 2013 at 20:24Christopher ShanklandMay 22nd, 2013 at 05:52Rob CampbellMay 22nd, 2013 at 06:34GauravMay 22nd, 2013 at 05:59Oğuz ÇelikdemirMay 22nd, 2013 at 11:21piotr_czMay 24th, 2013 at 00:46Rob CampbellMay 24th, 2013 at 03:42Mathew PorterMay 24th, 2013 at 15:28UsefJune 6th, 2013 at 23:35UsefJune 6th, 2013 at 23:40