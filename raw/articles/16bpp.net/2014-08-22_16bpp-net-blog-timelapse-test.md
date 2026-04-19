---
title: '16BPP.net: Blog / timelapse_test'
url: https://16bpp.net/blog/post/timelapse_test
published: '2014-08-22'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

I've been a little bit busy lately for the past week. I've had to move down to Cincinnati for my current Co-Op and it took much longer to prepare, move, and get settled in than I though it would. I've been a little bit delayed on making this post, but better late than never.

Early in my summer vacation I went down to D.C. on a small trip. While visiting the Smithsonian Institute and picked up one of those crystal growing kits. I remember playing with one when I was much younger (around ten or so) and thought it would be fun to grow another one. They didn't have the blue color anymore, so I opted to get a pack labeled “Emerald.” I thought it would be extra fun to do a timelapse of the crystal growing.

It took a few days to write a decent application to do this. My tools were C++, OpenCV, ffmpeg, and a very low resolution webcam. The app comes in two parts:

- Capture softare
- A script to compile images

Once everything was setup, I set the software to run for just five days, taking one picture per minute. The package said that it would only take that long for the crystal to grow, but that was a lie. I had to run the setup for two weeks and half a day. This resulted in 21,000+ images (totaling 1.5 GB of disk space).

I wanted to run the film at 30 fps, but 21,000+ images would result in something around fifteen minutes long, so I only used every fifth image for the final movie. You can it below:

I'm sorry that I don't have any other photographs of the crystal, or the “Magical Crystal Fun-Box,” that I grew it in. You'll just have to use your imagination for that last one. Source code for the application can be found [here](https://github.com/define-private-public/timelapse_test) on my github.