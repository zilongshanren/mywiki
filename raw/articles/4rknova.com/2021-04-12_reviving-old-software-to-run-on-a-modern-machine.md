---
title: Reviving old software to run on a modern machine
url: https://www.4rknova.com/blog/2021/04/12/reviving-old-software
author: Nikolaos Papadopoulos
published: '2021-04-12'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

My partner recently came across an old educational software title from 1997 that brought back happy memories from her childhood. The software was developed by “The Learning Company” and was part of a series called “Reader Rabbit’s Reading Development Library”. The company released 4 installments in total.

![01](../../assets/edb25e362f793c0b.jpg)


I thought it would be a nice surprise to help recreate some of those cherished memories and took on the challenge of making this outdated software run on a modern machine and OS.

I was able to track down a copy of the CD for the 3rd installment in ebay and soon afterwards I found myself playing around with Windows 3.11 in Virtualbox to make it work.

As expected, a basic installation of the OS was not sufficiently equipped to run the CD and some additional programs and drivers were required. To install all the additional components, I needed to create some floppy disk images which were then mounted within Virtualbox to simulate a physical floppy drive. I’ve written about how to do this in [a previous blog post](https://www.4rknova.com/blog/2021/03/24/creating-floppy-disk-images). The whole process involved a lot of trial and error, installing programs and drivers to solve issues one by one.

The first step was to install the MS-DOS E-IDE / ATAPI CD-ROM device driver so that the OS can read the CD.

![01](../../assets/4d27e144d14d7e8c.png)


Next I installed better display drivers so that I can set the display to a higher resolution of 1024x768 with 256 colors.

![01](../../assets/8d06e0ee433c7fc8.png)


With video sorted, I moved on to audio, installing sound blaster 16 drivers and utilities.

Another dependency to resolve was WinG [2], a graphics and animation framework that was introduced in 1994 and was later on superseded by DirectX.

![04](../../assets/4965999f9f9886f0.png)


Finally I mounted the CD in Virtualbox and installed the software.

![05](../../assets/05a98b66cb1cf1a4.png)


With all the dependencies resolved I could finally run the software.

![06](../../assets/b4016acca01733a7.png)