---
title: Poor man's animation framework
url: https://anteru.net/blog/2010/poor-man-s-animation-framework
published: '2010-11-08'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

I had to produce an animation towards the end of the research project, and as usual, there was not enough time left for heavy-duty video editing work. Everything for the animation had to be done really fast and still produce the correct result. As the video should compare our algorithm

- Labelling: I needed to put labels on the animation, so it would be clear which part shows which algorithm.
- Four-up comparison: I.e. splitting the screen into four quadrants, and playing back four different streams in sync.
- High compression quality: Of course, the compression should not introduce new artefacts or hide those from the algorithm.

## Duct tape, glue, and a hammer

I decided pretty early on to reuse the [animation framework I had for regression testing](https://anteru.net/blog/2010/11/01/938/). That is, I could produce fixed-frame-rate rendering of the animation path and write out every single frame to disk. So the first step was to do exactly this, some [Python](http://python.org) glue and then just dumping out the whole animation.

For processing the images, I decided to use [ImageMagick](http://www.imagemagick.org/) as the all-around tool. In particular, ImageMagick has [great functionality to label images](http://www.imagemagick.org/Usage/annotating/#anno_on), so I slapped a Python wrapper around the ImageMagick executable and went through all images to label them.

[Stiching](http://www.imagemagick.org/Usage/montage/#geometry_size) & [cropping](http://www.imagemagick.org/Usage/crop/#crop_percent) can be also done with ImageMagick. While it requires a lot of disk I/O to do so, it’s still pretty fast and there is no quality loss in the pipeline (all my images where PNG throughout all the processing.) I did everything step-by-step with intermediate outputs for easy debugging. That is, I cropped the image firsts, generated four outputs, stitched them together and added the labels on top. That’s easier than adding the labels first, especially if you need to resize the images. For resizing, ImageMagick provides [point-filtering](http://www.imagemagick.org/Usage/resize/#point) which is very useful as there is no blurring from the resizing, which was crucial for my stuff.

Finally, I would number the images and run them through [VirtualDub](http://virtualdub.org) to create a single AVI file with no compression – basically appending each image after the other. There was only one step left, compressing the AVI, and it turns out that [FFMPEG](http://www.ffmpeg.org/)’s h264 implementation is pretty good, especially with the [two-pass compression with variable bit rate](http://rob.opendot.cl/index.php/useful-stuff/ffmpeg-x264-encoding-guide/). I used something around 2.5 MBit for 720p, which resulted in a 10 MiB file for 30 seconds.

## Caveats

There are some caveats here which took me a while to figure out:

- After labelling a 24-bit PNG with a transparent label, ImageMagick changed the depth to 32-bit. Unfortunately, VirtualDub cannot load 32-bit PNGs, and all the guides I found which explained how to get rid of the alpha channel somehow didn’t help. What helped was to write the final image as TGA.
- FFMPEG two-phase encoding: With one-phase encoding, the quality seems equivalent but the compression is worse, so I opted to use the two-pass encoding. My main problem was that the input AVI was larger than my main memory, so reading through the file was pretty slow … still, the two-pass results were worth the additional compression time. For the record, I used the
`very_slow`

presets :) - Virtual Dub’s default framerate is 10 frames per second. You have to change it before writing the AVI, for some reason or another, setting the fps in FFMPEG didn’t help.