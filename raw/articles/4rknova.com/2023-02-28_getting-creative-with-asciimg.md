---
title: Getting creative with asciimg
url: https://www.4rknova.com/blog/2023/02/28/asciimg-slideshows
author: Nikolaos Papadopoulos
published: '2023-02-28'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

A while back I wrote Asciimg, a minimalistic tool that can display images within a terminal. The tool implements a rudimentary dithering algorithm to translate colour intensities to ascii characters. I was recently playing around with it and thought of a few creative ways to put it to use.

If you wish to try the examples below yourself, the source code for Asciimg is available at [github](https://github.com/4rknova/asciimg).

# Image slideshows

In this example I wanted to create a simple slideshow of a set of images. Asciimg’s threshold switch is used to create a fade-in effect while transitioning to each new image. To facilitate faster image loading and avoid putting unnecessary strain on my SSD, I create a ramdisk, and copy the images into the respective mapped directory.

$ sudo mkdir /tmp/ramdisk $ sudo chmod 777 /tmp/ramdisk $ sudo mount -t tmpfs -o size=1024m myramdisk /tmp/ramdisk $ cd /tmp/ramdisk

The slideshow logic is straight forward and can be trivially implemented in any language. Here’s how to do it in a simple bash shell script one-liner:

$ for i in *.jpg; do for j in {25..1}; do sleep 0.02 && asciimg "$i" -threshold `echo "scale=3;$j/25" | bc` -res ${COLUMNS}x${LINES}; done; sleep 1; done

This is what it looks like:

![An animated slideshow of famous scientists portraits](../../assets/09574b7724155f37.gif)


# Videos

The next logical step is of course to try and play videos within the terminal. This example is slightly more elaborate. I use ffmpeg to read a video file and dump the frames read to an image file in the ramdisk I created above.

$ ffmpeg -re -i video.mp4 -y -update 1 -s 200x200 /tmp/ramdisk/frame.jpg

In another terminal I then use the watch tool to run Asciimg and display that image in the terminal every 0.1 seconds.

$ watch -n0.1 asciimg frame.jpg -res ${COLUMNS}x${LINES}

To demonstrate this, I recorded a clip from Carl Sagan’s 1980 Cosmos series, episode 1: The shores of the cosmic ocean. This is what it looks like:

![Excerpt from Carl Sagan's Cosmos rendered with Asciimg](../../assets/89161ee09be4e991.gif)