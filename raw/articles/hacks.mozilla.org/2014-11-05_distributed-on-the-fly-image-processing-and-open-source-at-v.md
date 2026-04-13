---
title: Distributed On-the-Fly Image Processing and Open Source at Vimeo – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/11/distributed-on-the-fly-image-processing-and-open-source-at-vimeo/
author: Derek Buitenhuis
published: '2014-11-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When you think of Vimeo, you probably think of video — after all, it’s what we do. However, we also have to handle creation and distribution a lot of images: thumbnails, user portraits, channel headers, and all the various awesome graphics around Vimeo, to name a few.

For a very long time, all of this content was static and served from the CDN as-is. If we wanted to introduce a new video resolution, we would have to run batch jobs to get new, higher resolution thumbnails from all of the videos on the site, where possible. This also means that if we ever wanted to tweak the quality of said images, we would be out of luck. It also meant on mobile, or on a high DPI screen, we had to serve the same size images as on our main site, unless we wanted to store higher and/or lower resolution versions of the same images.

Enter ViewMaster.

About two years ago, during one of our code jams, one of our mobile site developers brought the issue to us, the transcode team, in search of a backend solution. ViewMaster was born that night, but sat idle for a long time after, due to heavy workloads, before being picked up again a few months ago.

We’ll go into more detail below, but a quick summary of what ViewMaster is and does is:

- Written in Go and C.
- Resizes, filters, crops, and encodes (with optimizations such as
[pngout](http://www.jonof.id.au/kenutils)to different formats on-the-fly, and entirely in memory. - Can be scaled out; each server is ‘dumb’.
- Reworked thumbnailing that picks one ‘good’ thumbnail per video, during upload, and stores a master for use with the on-the-fly processing later on.
- Migrates our existing
*N*versions of each image to one master, high quality image to be stored.

This allows us to:

- Serve smaller or larger images to different screen types, depending on DPI, and OS.
- Serve optimized images for each browser; e.g. WebP for Chrome, and JPEG-XR for IE11+.
- Easily introduce new video resolutions and player sizes.
- Scale thumbnail images to the size of an embed, for display.
- Introduce new optimizations such as
[mozjpeg](https://github.com/mozilla/mozjpeg)instantly, and without any significant migration problems.

Now for the slightly more technical bits.

## General Architectural Overview and Migration

![ViewMaster Flow](../../assets/0e17970d4b846905.png)


A general look at the process is given in the diagram above. If you’d like a more detailed look at the infrastructure and migration strategy (and a higher res diagram), including what some of those funny names mean, head over to the [Making Vimeo Blog](http://making.vimeo.com/post/101852060824/on-the-fly-image-generation-architecture-and-migration) to check it out!

## Open Source

The actual image processing happens entirely in memory â€” the disk is never hit. The main image processing service is written in Go, and making somewhat liberal use of its C FFI to call several libraries and a few tiny C routines, open source or otherwise. It is known that calling C functions from Go has an overhead, but in practice, this has been negligible compared to the time taken by much more intensive operations inside the libraries, such as decoding, encoding, resizing, etc.

The process is rather straight forward: The video frame is seeked to and decoded and converted to RGB (yes, JPEG is [YCbCr](http://en.wikipedia.org/wiki/YCbCr), but it made more sense for the master to be stored as RGB to us) and/or the image is decoded, and various calculations are done to account for things like non-square pixels, cropping, resizing, aspect ratios, etc. The image is then resized, encoded, and optimized. All of this is done in-memory using buffered IO in Go (via `bufio`

), and if need be piped to an external process and back to the service where libraries are not available, such as the case is with [Gifsicle](http://www.lcdf.org/gifsicle/) and [pngout](http://www.jonof.id.au/kenutils).

Plenty of tricks are used to speed things up, such as detecting the image type and resolution based on mime-type, libmagic, and the libraries listed below, so we don’t need to call `avformat_find_stream_info`

, which does a full decode of the image to get this information.

A few of the notable open source libraries we leverage (and contribute to!), include:

[FFmpeg](https://ffmpeg.org)&[Libav](https://libav.org)– Base image decoding libraries (libavcodec), resizing (swscale), remote image access. Now supports CMYK JPEGs too![FFMS2](../../assets/7025bc80db041851.img)– Frame accurate seeking using the above libraries.[libwebp](https://code.google.com/p/webp/)– WebP encoding.[LCMS2](http://www.littlecms.com/)– ICC profile handling.

On top of those, we’ve written several Go packages to aid in this as well, some of which we have just open sourced:

[go-util](https://github.com/vimeo/go-util/)– General utility functions for Go.[go-iccjpeg](https://github.com/vimeo/go-iccjpeg/)– ICC profile extraction from a generic`io.Reader`

.[go-magic](https://github.com/vimeo/go-magic/)– Idiomatic Go bindings for the libmagic C API using`io.Reader`

.[go-imgparse](https://github.com/vimeo/go-imgparse/)– Resolution extraction from JPEG, PNG, and WebP images optimized for I/O and convenience, again using a standard`io.Reader`

.[go-taglog](https://github.com/vimeo/go-taglog/)– Extended logging package compatible with the standard Go logging package.[go-mediainfo](https://github.com/dwbuiten/go-mediainfo/)– Very basic binding for MediaInfo.

## Future

Although we are currently optimizing quite well for PNG, and WebP, there is still lots to be done. To that end, we have been involved with an contributing to a number open source projects to create a better and faster web experience. A few are discussed below. It may not have been obvious though, since we tend to use our standard email accounts to contribute, rather than our corporate ones… Sneaky!

** mozjpeg** – Very promising already, having added features such as scan optimization, trellis quantization, DHT/DQT table merging, and deringing via overshoot clipping, with future features such as

[optimized quantization tables for high DPI displays](https://github.com/mozilla/mozjpeg/issues/76)and

[globally optimal edge extension](https://github.com/mozilla/mozjpeg/issues/82#issuecomment-51732574). We plan to roll this out after the plan for

[ABI compatibility](https://github.com/mozilla/mozjpeg/issues/85)is implemented in 3.0, and also we plan to then add support to

[ImageMagick](http://imagemagick.org)to benefit the greater community, if someone else has not already.

** jxrlib** – Awesome of Microsoft to open source this, but it needs a bit of work API-wise (that is, an actual API). Until fairly recently, it could not even be built as a library.

** jpeg-recompress** – Alongside mozjpeg, something akin to this is very desirable for JPEG generation. Uses the excellent

[IQA](http://tdistler.com/iqa/build.html)with mozjpeg and some other metrics (one implemented poorly) by me!).

**Open Source PNG optimization library** – This was a bit of a sticking point with us. The current open source PNG optimization utils do not support any in-memory API at all, or in fact, even piping via stdin/stdout. [pngout](http://www.jonof.id.au/kenutils) is the only tool which even supports piping. Long term, we’d like to be able to ditch the closed source tool and contribute an API to one of these projects.

**Photoshop, GIMP, etc. plugins** – I plan to implement these using the above-mentioned libraries, so designers can more easily reap the benefits of better image compression.

## About
[
Derek Buitenhuis ](https://github.com/dwbuiten)

Transcoder dude at Vimeo, and DSP hacker. Really into coffee. Reallllllllllllllllly.

## 7 comments

Valérie MartinNovember 5th, 2014 at 11:31Derek BuitenhuisNovember 5th, 2014 at 13:12Fabricio ZuardiNovember 5th, 2014 at 14:50Michael DoeNovember 6th, 2014 at 05:51IvanNovember 7th, 2014 at 04:58Fabricio C ZuardiNovember 10th, 2014 at 07:29SimonNovember 12th, 2014 at 15:08