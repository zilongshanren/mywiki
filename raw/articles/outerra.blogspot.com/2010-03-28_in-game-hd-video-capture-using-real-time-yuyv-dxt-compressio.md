---
title: In-Game HD Video Capture using Real-Time YUYV-DXT Compression
url: https://outerra.blogspot.com/2010/03/in-game-hd-video-capture-using-real.html
author: Outerra
published: '2010-03-28'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The method used in this approach was inspired by an article about

[Real-Time YCoCg-DXT Compression](http://developer.nvidia.com/object/real-time-ycocg-dxt-compression.html)which presented a real-time GPU compression algorithm to DXT formats.

Standard DXT texture formats aren't very suitable for compression of general images like the game frames, the higher contrast results in artifacts like color bleeding and color blocking. The article introduced YCoCg-DXT format that encodes colors to

[YCoCg](http://wiki.multimedia.cx/index.php?title=YCoCg)color space (intensity and orange and green chrominance). It also contains the source code for real-time GPU compression and comparison of achieved results.

The YCoCg format is suitable for decompression on GPU, because decoding YCoCg values back to RGB only takes a few shader instructions. However, for the purpose of decoding the frame data in a video codec, a better format is a YUV-based one that allows to decode the data directly to the video surface without additional conversions. The best format for this seemed to be YUYV with 16 bits per sample, which means there's one U and V value per 2 horizontal samples.

The compression algorithm differs from the YCoCg-DXT one in the initial color space conversion to YUYV and in that it encodes 4x4 YY, U and V blocks in the way alpha component is encoded in DXT5 format.

The algorithm is as follows:

- Video frames are compressed with fragment shader to YUYV-DXT format by render to texture technique, reducing the data to 1/3 of its original size
- The compressed textures are
__asynchronously__read back to CPU - The data are continuously written to disk

The compression on GPU reduces the bandwidth needed between CPU and GPU, but more importantly also the bandwidth needed for disk writes. Sustainable write speed of a SATA drives is somewhere around 55MB/s, transferring a raw 1280x720/30fps video takes 79.1MB/s, while the DXT compressed video only takes 26.4MB/s. A Full-HD video stream is 59.3MB/s.

To capture the frame buffer data the application first renders to an intermediate target. The compression shader uses this as the input texture, rendering to a uint4 target with one quarter width and height of the original resolution, that is then read back to CPU memory.

The next step is decoding the captured video. To make this easy I've written a custom video codec and video format plugin for

[ffmpeg](http://ffmpeg.org/)library. The format was named Yog (from

**Y**C

**o**C

**g**) as the encoding was originally in YCoCg format, changed only later to YUYV.

The game produces *.yog video files that can be directly replayed by ffplay or converted to another video format with the ffmpeg utility. They are also recognized by any video processing software that uses ffmpeg or ffplay executables or uses the avcodec and avformat dlls from the suite, such as

[WinFF](http://winff.org/)or

[FFe](http://corz.org/windows/software/ffe/)or many others.

### Results

After starting the video recording in our game the frame rate drops only by a few fps, and it's still playable normally, unlike when recording for example with Fraps. Disadvantage is that this has to be integrated into the renderer path.

Quality wise the results are quite good, as it can be seen on the following screen shots:

Original

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_uFtUBEoo2b8sxW983xe0txKTE0dCcz5q8wfDMaJ2PJxPPKCT8cdGNF5kSVGiI4Ach8jSVovhWlupO0RncSX-hFWxfAtdPsoRWgKs81=s0-d)


YUYV compressed, note this is slightly lighter because of an issue in ffmpeg that has to be solved yet.

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_uZJ1TJ0Y0Arj_JZGpI2TzONlFchm0nvxB8RLc6S3VedtzLzwi6_rw1GjvnMlGm9r6df5QKHpgNFWeAeasVOQmZMtJe8iye98BOf0Y=s0-d)


The difference, 4X amplified

![](https://lh3.googleusercontent.com/blogger_img_proxy/AEn0k_vSVrX5JQugAXwlKJZjtcVZa88SfFi1vQZvVii113JhOJJzyGwjuCMM-GTZJxu1wxBsSLnyoqQx33pYxBWfxPPduUzLOl-p8A720T43Rw=s0-d)


The source code and further implementation details can be found at

[outerra.com/video/index.html](http://www.outerra.com/video/index.html)

## 5 comments:

Very interesting! Thanks! ^__^

PS: Since your work is based on Ignacio's work I have to ask... whats the license of your code? MIT as well? :o)

Yes MIT for the shader; I'm not sure what will be the desired license for the ffmpeg code, it can be MIT too or dual LGPL/MIT.

amazing! great work! can't wait to try this in Ogre

Could the lighter colors be a YUV vs YUVJ issue?

Might be, but there's also an issue with sRGB space - gamma value should be carried over in the file too and specified for ffmpeg. But it seemed to ignore that, I should consult it with ffmpeg guys.

Post a Comment