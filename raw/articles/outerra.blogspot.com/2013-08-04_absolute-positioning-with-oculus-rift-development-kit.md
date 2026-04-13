---
title: Absolute positioning with Oculus Rift development kit
url: https://outerra.blogspot.com/2013/08/absolute-positioning-with-oculus-rift.html
author: Outerra
published: '2013-08-04'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After incorporating support for Oculus Rift into our Outerra tech demo (see the




For my tests I picked the marker code




Using a recent build of opentrack (


Here's a short video showing the augmented Rift tracking in action:





A couple of notes:



With ArUco marker the usage is very simple, but it has to be made more robust. Some ideas for enhancement:


Since only the positional information is needed from the tracker, the simplest and probably the most robust implementation of a positional tracker would be adding just 2 wide-angle LEDs on the Rift, and using the point tracker plugin with it. Point light from the LEDs will be strong enough to overcome the problems of detection in various lighting conditions. However, it would require a small modification of the Rift.


Steps to set it up with Outerra:



[Outerra + Oculus Rift Test 2 - MiG 29 flight](http://www.youtube.com/watch?v=2LPPdV2Md1c)video), I've been pondering about a possibility to add absolute positional tracking to the Oculus Rift devkit. During the forum discussions about the support for FreeTrack/FaceTrackNoIR/opentrack in Outerra, Stanisław Halik, one of the[opentrack](https://github.com/opentrack/opentrack)developers, pointed me to[ArUco](http://www.uco.es/investiga/grupos/ava/node/26).[ArUco](http://www.uco.es/investiga/grupos/ava/node/26)is a library built on top of[OpenCV](http://opencv.org/), providing the ability to analyze video image and detect coded markers an their positional information. ArUco supports up to 1024 different markers, that are encoded in a 5x5 grid. ArUco tracker is supported in recent builds of[opentrack](http://ts3.cosaofficial.pl/opentrack/), so I could use it with our recently added support for FreeTrack protocol.For my tests I picked the marker code

[787](http://www.outerra.com/images/787.svg), printed it and stuck it on the Rift.Using a recent build of opentrack (

[≥ opentrack-20130803](http://ts3.cosaofficial.pl/opentrack/)), and a video camera (tested with Logitech C270 and an older Sonix SN9C201 camera) with FreeTrack protocol output I managed to get the positional tracking working in addition to the Rift tracker, with only a few minor changes required to our FT client implementation.Here's a short video showing the augmented Rift tracking in action:

A couple of notes:

- the added positional tracking definitely helps with the dizziness, the brain doesn't get confused by the missing degree of motion
- currently the positional tracking does not use any filtering, resulting in occasional oscillation
- ArUco in opentrack is currently quite sensitive to lighting conditions, bright parts of captured image outside of the marker can break the detection
- when opentrack loses the track of the marker, camera stays on the last position, and after the position info is regained, the camera may suddenly jump into a new position

With ArUco marker the usage is very simple, but it has to be made more robust. Some ideas for enhancement:

- using multiple markers - ArUco can detect an array of markers, so there can be multiple ones covering also the sides, that would not lose track when you turn your head to the sides
- direct integration of ArUco - simplifying the setup even more
- ultimately it would be best to use the info from Rift's accelerometer to capture the positional movement dynamics, and use the absolute positional info from the auxiliary tracker just to correct the drift

Since only the positional information is needed from the tracker, the simplest and probably the most robust implementation of a positional tracker would be adding just 2 wide-angle LEDs on the Rift, and using the point tracker plugin with it. Point light from the LEDs will be strong enough to overcome the problems of detection in various lighting conditions. However, it would require a small modification of the Rift.

Steps to set it up with Outerra:

- print one of the ArUco markers (or print the
[787](http://www.outerra.com/images/787.svg)marker used here) - download a recent
[opentrack](http://ts3.cosaofficial.pl/opentrack/)build - in opentrack, select the aruco tracker and configure your camera in the settings
- select FreeTrack 2.0 for the game protocol, and optionally one of the filters
- start opentrack, verify that it can see and interpret marker position and orientation correctly
- once this works, leave opentrack running and launch outerra.exe
- Outerra will automatically use Rift tracker together with any FreeTrack tracker it finds running

## No comments:

Post a Comment