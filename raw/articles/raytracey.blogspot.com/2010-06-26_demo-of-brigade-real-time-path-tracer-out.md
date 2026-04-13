---
title: Demo of Brigade real-time path tracer out!
url: http://raytracey.blogspot.com/2010/06/demo-of-brigade-real-time-path-tracer.html
author: Sam Lapere
published: '2010-06-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://igad.nhtv.nl/~bikker/](http://igad.nhtv.nl/%7Ebikker/)

Anyone (remotely) interested in real-time raytracing, owning a CUDA enabled GPU or a powerful CPU, must definitely try this excellent demo! It works with Geforce 8000 cards and upwards, but can also use the CPU only if you don't have a CUDA card. (UPDATE: some people on XP machines cannot run the program because of a msvcrt.dll error. Removing opengl32.dll from the Brigade folder seems to solve the problem). There are 4 different scenes to choose from, some are animated with "planes" flying around. You can simply edit "scene.txt" to change scene, resolution, samples per pixel and so on. This is a video of one of the scenes:


It's an amazing piece of software with huge potential. Afaik, the CPU uses bidirectional path tracing while divergent rays are path traced on the GPU. Scenes and materials are very simple, but nevertheless I am still stunned that real-time path tracing with animated objects is possible today. (Bidirectional) path tracing solves most limitations encountered by other real-time GI methods which rely on image space techniques or can only be used in diffuse and semi-glossy scenes. Speed is the only limit. I can't wait to see Brigade run on a cluster of PC's each containing multiple Fermi's (as is suggested in the readme file). Looking very forward to the games that the Dutchies will produce with this technology ;-)

[http://www.youtube.com/watch?v=qC2zKIqttzk](http://www.youtube.com/watch?v=qC2zKIqttzk)It's an amazing piece of software with huge potential. Afaik, the CPU uses bidirectional path tracing while divergent rays are path traced on the GPU. Scenes and materials are very simple, but nevertheless I am still stunned that real-time path tracing with animated objects is possible today. (Bidirectional) path tracing solves most limitations encountered by other real-time GI methods which rely on image space techniques or can only be used in diffuse and semi-glossy scenes. Speed is the only limit. I can't wait to see Brigade run on a cluster of PC's each containing multiple Fermi's (as is suggested in the readme file). Looking very forward to the games that the Dutchies will produce with this technology ;-)

## 1 comment:

Real-time GI? Lighting looks baked, probably something like precomputed radiance transfer by Sloan.

Post a Comment