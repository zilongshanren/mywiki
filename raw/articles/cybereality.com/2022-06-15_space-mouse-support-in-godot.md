---
title: Space Mouse Support in Godot
url: https://cybereality.com/space-mouse-support-in-godot/
author: Cybereality
published: '2022-06-15'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

I’m currently working on a plug-in for the Godot Engine that enables support for 3Dconnexion 6DOF controllers like the Space Navigator. If you are not aware, this is a little puck, sort of like a huge analog stick, except that it works on 6 degrees of freedom. Meaning you get full x/y/z position and rotation, allowing you to orient 3D objects on a computer naturally (rather than using odd combinations of the mouse and keyboard to emulate multiple axes). These space mouse devices have been available for quite some time and are most popular with professionals (such as CAD modelers) rather than game developers, but they are quite useful for any sort of modeling. Support is great for the main 3D DCC apps such as Maya and Blender, though less common for game engines.

![](../../assets/4701a7d4c1005e5d.jpg)

My plug-in Godot Space Mouse will allow Space Navigator support for orienting the viewport camera in the Godot Engine editor. As a plug-in, there is limited access to what it can do, so there are still some conflicts when switching between the traditional mouse and the space mouse, but I think it works well enough to be useful. The video above displays an early development version of the plug-in, which is working on Ubuntu Linux 22.04 and Godot Engine 3.4.4. I made some additional progress today on the smoothness of the movement (there are a few choppy areas in the video, somewhat due to screen recording). I will need to get cross-platform support working before release, as I plan to launch for Windows and macOS, in addition to Linux. This may take around 1 or 2 weeks, but I already found some libraries that look promising and it should not be too hard. Please hang tight.