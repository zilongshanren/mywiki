---
title: installer
url: http://hacksoflife.blogspot.com/2011/08/installer.html
author: Benjamin Supnik
published: '2011-08-19'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A few tricks to get out of jail with OS X installs and updates...


If you have a package that just won't install due to bad voodoo (this can happen if you install a lot of seeds and the stars misalign) you can use this to force the install with this:


If you need to install from an OS CD you can find the package to use for this trick in


One use for this is to force an install onto a partition that the OS doesn't understand. I had my main drive triple-booted to OS X 10.5.8, Windows Vista (don't get me started) and Ubuntu 8.whatever. Remaking this delicate balance without three OS reinstalls is virtually impossible, but the OS X Snow Leopard installer didn't want to install because it didn't understand the partition map.


The fix on the net is to resize the OS X partition, which causes Disk Utility to fondle the partition map in some useful way, but there's no way I want to risk my other OS installs. Installing the OS from the command line with a forced install lets me simply dump the OS onto the drive, and then rEFIt just works because, well, it's rEFIt.

If you have a package that just won't install due to bad voodoo (this can happen if you install a lot of seeds and the stars misalign) you can use this to force the install with this:

`sudo CM_BUILD=CM_BUILD COMMAND_LINE_INSTALL=1 installer -verbose -pkg MacOSXUpd10.6.5.pkg -target /`

If you need to install from an OS CD you can find the package to use for this trick in

`/Volumes/volname/System/Installatoin/Packages/OSInstall.mpkg`

One use for this is to force an install onto a partition that the OS doesn't understand. I had my main drive triple-booted to OS X 10.5.8, Windows Vista (don't get me started) and Ubuntu 8.whatever. Remaking this delicate balance without three OS reinstalls is virtually impossible, but the OS X Snow Leopard installer didn't want to install because it didn't understand the partition map.

The fix on the net is to resize the OS X partition, which causes Disk Utility to fondle the partition map in some useful way, but there's no way I want to risk my other OS installs. Installing the OS from the command line with a forced install lets me simply dump the OS onto the drive, and then rEFIt just works because, well, it's rEFIt.

## No comments:

## Post a Comment