---
title: Generating Stereo Anaglyphs with ImageMagick
url: https://www.4rknova.com/blog/2018/07/08/stereo-anaglyphs
author: Nikolaos Papadopoulos
published: '2018-07-08'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

When generating a pair of stereoscopic images, it’s useful to have a way of testing the disparity and overall quality without having to put on an HMD device. ImageMagick provides a set of tools that allow performing a wide range of image processing. Amongst other things it allows creating Red-Cyan anaglyphs of stereo image pairs.

The tool is very intuitive to use:

$ composite -stereo 0:0 0.png 1.png anaglyph.png

Below, you can see a stereo anaglyph of left and right eye images I generated using my own renderer [XTracer](https://github.com/4rknova/xtracer), and fused together using ImageMagick.

Red-Cyan stereo glasses are required to properly view the stereo image.

![Stereo anaglyph of a reflective sphere suspended above a field](../../assets/cfdacb5bcde29a34.png)