---
title: STB style MPEG video writer
url: https://www.jonolick.com/home/mpeg-video-writer
author: Szwagier
published: '2016-09-25'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
Announcing my STB style 256 lines of code MPEG1/2 writer!
In this initial release the features are: 1) 256 lines of C code (single file) 2) no memory allocations 3) public domain 4) patent free (as far as I know) There is a lot left to be done, notably the encoding of P frames and audio. However, this is very useful as is for a drop-in MPEG writer in any project. Basic Usage: FILE *fp = fopen("foo.mpg", "wb"); jo_write_mpeg(fp, frame0_rgbx, width, height, 60); jo_write_mpeg(fp, frame1_rgbx, width, height, 60); jo_write_mpeg(fp, frame2_rgbx, width, height, 60); // ... fclose(fp); Some notes that this writer takes advantage of the fact that MPEG1/2 is designed so that you can literally concatenate files together to combine movies. Technically each frame is its own movie (until p-frames are implemented, then a set of frames would be its own movie). Some video players mess up here and don't decode correctly, but MPlayer, SMPlayer, FFMpeg and others work correctly. So this is great as a quick intermediate format! Have fun and code responsibly! (j/k)
|
## Archives
## Categories |