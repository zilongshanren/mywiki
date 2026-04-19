---
title: 'Godot Space Mouse Official Release : 6DOF Viewport Camera Control in Godot
  Engine'
url: https://cybereality.com/godot-space-mouse-official-release-6dof-viewport-camera-control-in-godot-engine/
author: Cybereality
published: '2022-06-21'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

I’ve just released my latest Godot Engine project, a plug-in which allows you to use a Space Mouse or Space Navigator from 3Dconnexion to control the viewport camera in the Godot editor. The 3Dconnexion devices are like an analog stick on steroids, and allow you to move position in the full x, y, z axes as well as rotate along yaw, pitch, and roll, all at the same time.

This 3D mouse is usually positioned on the left of the keyboard, so you can use your right hand and the traditional mouse for other functions (setting parameters, moving objects, selection, etc.) without constantly context switching.

![](../../assets/71c926187db1996e.jpg)

The plug-in works via a library called HIDAPI, so it does not require any drivers, it is self-contained. Support on Windows and Linux is very good. For macOS, there are some incompatibilities with the official driver that I was not able to fix. So if you are using macOS, you will need to uninstall the drivers before using this plug-in. Otherwise, it works as you would expect on all platforms.

I’ve been using the Space Mouse for a while, and it is very handy. It works with most 3D DCC applications, like Maya, 3DS Max, Blender, and so on. Definitely a time saver, and also allows you to view your work at angles that are not possible with a mouse, so it can be extremely useful. The hardware starts at $150, but it’s a worthwhile investment if you do any sort of 3D art on the computer.

The plug-in is available for Windows, Linux, and macOS as a free download.