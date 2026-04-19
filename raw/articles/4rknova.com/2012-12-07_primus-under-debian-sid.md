---
title: Primus Under Debian/Sid
url: https://www.4rknova.com/blog/2012/12/07/primus
author: Nikolaos Papadopoulos
published: '2012-12-07'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

Primus is a VirtualGL alternative for bumblebee that promises a significant performance boost. While a few distributions have already included primus in their repositories, this is not the case for debian. Furthermore, I could not find any information online on how to use primus under debian, or any explicit reference by any user that has been successful with it.

Below you will find instructions on how I managed to get it working. I do not claim that my method is correct and it is possible that there is a better way to do this. If you have any suggestions, feel free to contact me. In this guide I will assume that you already have a working installation of bumblebee. If that is not the case then the instructions below are of no use to you.

# Compilation

First off, you will need to have multiarch enabled and the following packages installed: *gcc-multilib*, *g++-multilib*. Once this is done, fetch the original code from github.

git clone git://github.com/amonakov/primus.git

At this point if you try to compile the library with the stock makefile and use the provided script to run your applications, you will end up with the following error message:

primus: fatal: failed to load any of the libraries: /usr/$LIB/nvidia-bumblebee/libGL.so.1; /usr/$LIB/nvidia-bumblebee/libGL.so.1: cannot open shared object file: No such file or directory.

This is due to the fact that the path for *libGL.so.1* might differ from one distribution to another. I am not sure why the developer chose to hard-code it instead of including a configuration script, therefore I will assume there is a good reason for it. In any case, the correct path must be provided at compile time, so what we need to do is tweak the Makefile.

cd primus sed -i "s%nvidia-bumblebee%nvidia/current%g" Makefile

Note that your system's configuration might be different. In that case you will have to find the correct path on your own. The following might help:

sudo find /usr/ -name "libGL.so.1"

The final step is to compile the library. Issue the following commands:

LIBDIR=lib/x86_64-linux-gnu make CXX=g++\ -m32 LIBDIR=lib/i386-linux-gnu make

This will result to a built of both the 32 and 64-bit version of the library. Again, the lib/x86_64-linux-gnu and lib/i386-linux-gnu parametres are debian specific and you might have to change them to match your system's configuration. To use primus issue the following:

./primusrun env vblank_mode=0 myprogram

and replace myprogram with whatever you want to execute. The env parameter disables vsync so that you can actually see the difference in performance.

# Benchmarking

Bumblebee / VirtualGL:

![Screenshot of glxspheres before the fix](../../assets/d76aff60a134efd8.png)


Bumblebee / Primus:

![Screenshot of glxspheres after the fix](../../assets/1d586b92e038f5b1.png)