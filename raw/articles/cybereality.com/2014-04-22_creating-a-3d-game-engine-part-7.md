---
title: Creating a 3D Game Engine (Part 7)
url: https://cybereality.com/creating-a-3d-game-engine-part-7/
author: Cybereality
published: '2014-04-22'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

I know it has been quite some time since the last update, and I thought I would be much further by now. Truth be told, I have been a little distracted the last few months with things totally tangential to graphics programming. In any case, I’ve had some motivation recently to continue on the 3D game engine and began doing further research and reading. However, research doesn’t get results on it’s own. 90% of the time, you just have to start doing whatever it is you want to do whether you think you’re ready or not. So that brings us here, to this totally underwhelming screen shot.

![Engine Zero Blank](../../assets/281a17c44744b9a9.jpg)


Yes, it is a blank pink screen. You can calm down. What you are not seeing is some basic boiler-plate code to initialize DirectX 11, clear the back-buffer to a plain color, and the basic Win32 message pump. I have also started to give some structure to the application, with a namespace and class that encapsulates the Direct3D related code. Right now it is a bit hard-coded for a lot of stuff, but I wanted to get it working first and then I can refine and refactor as needed. I’m actually feeling really excited about the prospects of having my own 3D engine, and hope to power through a lot of this foundation stuff so I can get some interactive demos up and running. If everything goes well, I plan to publish updates in this series more frequently as I progress. Thanks for watching.