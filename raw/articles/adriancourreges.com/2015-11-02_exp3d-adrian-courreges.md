---
title: Exp3D - Adrian Courrèges
url: http://www.adriancourreges.com/projects/exp3d/
author: Adrian Courrèges
published: '2015-11-02'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/2221c5de5a6efc08.png)

[Exp3D](http://www.breakingbyte.com/exp3d/) is a space shooter I released on Android in 2013.

I began writing it from scratch during my free time, back in 2011 when Android was exploding.
During the development, desktop support (*Windows/Linux/Mac*) was added, followed by a *WebGL* port by transcompiling to pure *Javascript*.

The source code is [freely available on GitHub](https://github.com/acourreges/exp3d).

## Architecture

The game runs on top of a minimalistic multiplatform framework I wrote from scratch. The source is entirely in Java, there is no “native” code included. The main loop doesn’t perform any dynamic allocation to maintain a constant 60FPS with 0 GC pauses, this was achieved by relying heavily on object pooling. 95% of the code (25k lines) is written on top of this framework and thus is shared between the different platforms.

The rendering engine can run on either a fixed-pipeline (*OpenGL ES 1.1*) or a programmable-pipeline (*OpenGL ES 2.0*, *WebGL*).

The *WebGL* version was quite straight-forward to create: I got it working over a week-end using [GWT](http://www.gwtproject.org/) to transcompile the *Java* codebase into *Javascript*.

If you want to know more details about the architecture of Exp3D you can read a [post about it on the Breaking Byte blog](http://www.breakingbyte.com/blog/2013/10/19/making-of-exp3d-architecture/).