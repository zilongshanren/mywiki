---
title: How to Reset Steam VR When It Can't Talk to the Rift
url: http://hacksoflife.blogspot.com/2017/06/how-to-reset-steam-vr-when-it-cant-talk.html
author: Benjamin Supnik
published: '2017-06-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Periodically in the coarse of writing an OpenVR app, I find that SteamVR can't talk to my HMD. One of the 500 processes that collaborate to make VR work has kicked the bucket. Here's the formula to fix it.


First, kill the process tree based on OVRServer_x64. All the Oculus stuff should die and then immediately respawn. Minimize their portal thingie.


Kill every vrXXX process (vrserver, vrmonitor,vrcompositor, vrdashboard). SteamVR should not look like it's running and will not auto-relaunch.


Now you're good - relaunch your game and SteamVR should restart and be able to communicate with the headset.

First, kill the process tree based on OVRServer_x64. All the Oculus stuff should die and then immediately respawn. Minimize their portal thingie.

Kill every vrXXX process (vrserver, vrmonitor,vrcompositor, vrdashboard). SteamVR should not look like it's running and will not auto-relaunch.

Now you're good - relaunch your game and SteamVR should restart and be able to communicate with the headset.

## No comments:

## Post a Comment