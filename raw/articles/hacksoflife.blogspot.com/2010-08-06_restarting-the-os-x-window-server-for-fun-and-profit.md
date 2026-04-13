---
title: Restarting the OS X Window Server for Fun and Profit
url: http://hacksoflife.blogspot.com/2010/08/restarting-os-x-window-server-for-fun.html
author: Benjamin Supnik
published: '2010-08-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

(If you are having trouble imagining this, close your eyes and visualize a desktop where nothing but the mouse moves, but as you drag what were your windows, small pieces of your scene graph flicker in and out of what used to be your open windows, as if you were just showing random parts of video memory. Okay, maybe it is a little bit fun.)

Here's what you need to get your life back:

- Have remote ssh enabled in the sharing control panel. ssh into your machine. Odds are, the remote shell is perfectly happy, even if the desktop looks like you hired Picasso as your art lead and he was extra high that day.
- Kill -9 pid will bring back the desktop some of the time. That is, sometimes just killing off your app is enough to get your desktop back. Typically this is a win in the case where the driver is constantly resetting and you just can't use the UI because the reset cycle is slow.
- If that doesn't work, this will kill off the entire window manager (including, um, everything...the Finder, your app, X-Code, icanhazcheesburger):
`sudo killall -HUP WindowServer`


## No comments:

## Post a Comment