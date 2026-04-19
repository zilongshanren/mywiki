---
title: Creating floppy disk images in Linux
url: https://www.4rknova.com/blog/2021/03/24/creating-floppy-disk-images
author: Nikolaos Papadopoulos
published: '2021-03-24'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The code snippet below shows how to create, format and mount a 1.44MB floppy disk image file, and then write files into it.

$ dd bs=512 count=2880 if=/dev/zero of=floppy.img $ sudo mkfs.msdos floppy.img $ sudo mount -o loop image.img /media/floppy/ $ cp ./files/* /media/floppy $ sudo umount /media/floppy/