---
title: Graphics Demo Programming
url: http://diaryofagraphicsprogrammer.blogspot.com/2011/09/graphics-demo-programming.html
author: Wolfgang Engel
published: '2011-09-18'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

About 8 or ten years ago I started thinking about doing a graphics demo for the demo scene. I started to prepare a minimum skeleton that should compile to the smallest possible exe. Over the years I kept this Skeleton alive going from Windows XP to Windows 7 and from DirectX 8 to DirectX 10.

More than three years ago I put the source code up on Google Code here and kept updating it:


http://code.google.com/p/graphicsdemoskeleton/


Although the source code is rather short, I played around with many ideas over the years. I read articles by the demo scene about getting smaller exe's just by using Visual Studio. After realizing that my exe got bigger with every new Visual Studio version, I switched to Pelles C; a free development environment with a compiler that follows the C99 standard:


http://www.smorgasbordet.com/pellesc/


My exe is now 838 bytes in size without violating Windows rules about releasing occupied resources. I tried to replace some of the code with assembly code, especially the entry points of the D3D functions and saved a few bytes at some point in time but removed it again because it was too inconvenient.

At some point (probably while it was running on DirectX 9) I implemented a small GPU particle system that didn't add much to the size, which was pretty cool.

One of the interesting things I found out was that HLSL code was packing in some cases smaller than C code for the CPU. I found this remarkable and I thought it would be a cool idea to write a small CPU stub and then go from there in HLSL.

I know there will be times when I go back to this piece of code and wonder what else I can do with it and spend half an hour looking through it. It was certainly the project with some of the lowest priorities in the last ten years ... maybe you can take the source and do something cool with it :-)


There is also a whole demo framework released by Inigo Quelez here


http://www.iquilezles.org/www/material/isystem1k4k/isystem1k4k.htm


Other useful links are:


http://yupferris.blogspot.com/

http://4klang.untergrund.net/

## No comments:

Post a Comment