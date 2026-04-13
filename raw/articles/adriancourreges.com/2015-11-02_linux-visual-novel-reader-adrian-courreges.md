---
title: Linux Visual Novel Reader - Adrian Courrèges
url: http://www.adriancourreges.com/projects/livino-reader/
author: Adrian Courrèges
published: '2015-11-02'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/8c15d0bd34d48097.gif)


Linux Visual Novel Reader *(LiViNo Reader)* provides a live translation of Japanese words rendered within a game, simply
by mouse-hovering them.

It works by combining:

![](../../assets/e28f189b05ff719d.png)


## Download

The source code of the modified version of Wine as well as the Firefox extension are both [available on GitHub](https://github.com/acourreges/livino-reader).

For detailed instructions about installation see below.

## Screenshots

![](../../assets/114440ee98c82d48.jpg)


## Installation

It mainly boils down to recompiling Wine with a [custom patch](https://github.com/acourreges/livino-reader/raw/master/dist/livino-wine-1.6.2.patch), it should work with any Linux distribution Wine can run on.

Here is a step-by-step tutorial, I use a 32-bit Ubuntu 15.04 as an example, which ships with Wine 1.6.2. You might have to adapt a bit if you’re using a different distribution or Wine version.

We will download the sources of Wine 1.6.2, patch them, compile and install our new custom version of Wine.

First let’s install some software needed to compile and package applications, as well as all the development libraries Wine depends on:

```
sudo apt-get update
sudo apt-get install build-essential fakeroot dpkg-dev devscripts
sudo apt-get build-dep wine
```


We have everything we need to compile the sources, let’s create some folder and put the Wine sources inside:

```
mkdir ~/wineCustom && cd ~/wineCustom
apt-get source wine
```


Now let’s grab the patch from GitHub and apply it:

```
wget https://github.com/acourreges/livino-reader/raw/master/dist/livino-wine-1.6.2.patch
cd wine1.6-1.6.2
patch -p1 < ../livino-wine-1.6.2.patch
```


We then compile and create a new custom package of Wine:

```
dpkg-buildpackage -rfakeroot -uc -b
```


And we wait… and wait… until the compiler is done making the CPU burn and the fan spin. This step can take several hours on an old machine.

After the new package is generated we can install it.
We first install all the runtime dependencies for Wine (quick and dirty version: install the Wine from the official repositories and remove it).
We then replace only the Wine package with our custom version.

```
sudo apt-get install wine1.6
sudo apt-get remove wine1.6
sudo dpkg -i ../*.deb
```


Great! Our custom version of Wine is installed. We don’t need the `~/wineCustom`

folder anymore, you can delete it.

#### Firefox extension

This step is much simpler: just add [this add-on](https://addons.mozilla.org/en-us/firefox/addon/livino-reader/) to your Firefox.

Alternatively you can also manually download the add-on [XPI file](https://github.com/acourreges/livino-reader/raw/master/dist/livino%40adriancourreges.com.xpi)
and install it from the Add-ons menu of Firefox. (Firefox Developer Edition can accept unsigned extensions.)

![](../../assets/a88e33c008d9136e.png)


## Use

Launch your game with Wine and play until some text is displayed on the screen.

Launch Firefox and click on “Tools”, “LiViNo Reader” and turn on Rikaichan.

![](../../assets/dbbbd8f0d5308586.png)


Enjoy the live-translation!

## How does it work?

Most of the visual novels rely on Windows’ [GDI library](https://en.wikipedia.org/wiki/Graphics_Device_Interface) to draw glyphs on the screen,
more specifically for each character a call to `GetGlyphOutlineW()`

is made.

There are some tools on Windows to hook such calls to the DLL like [AGTH](https://sites.google.com/site/agthook/) or
[Oh! Text Hooker](http://ohhara.sarang.net/ohthk/)
but with Wine it’s even easier: we can directly play with the source code.

The characters are dumped into a temporary HTML file. The custom Firefox extension then simply monitors changes made to this file and refreshes the page when necessary.

## Known issues

Some visual novels are built upon the RealLive engine, you can check by looking for a `RealLive.exe`

file in the game folder.

This engine uses a cache and does not necessarily call the glyph function every time it draws a character.

Fortunately there’s a patch for the RealLive engine to disable its cache mechanism, making it compatible with LiViNo, look for “rlivepch.exe” on Google.

Some games make double-calls to `GetGlyphOutlineW()`

when drawing a single glyph. You might experience some double-printing, but LiViNo Reader tries
its best to heuristically determine if a game has such behavior and automatically adjust to stream only one out of two characters.