---
title: Firebug 1.8 New Features – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/07/firebug-1-8-new-features/
author: Jan Honza Odvarko
published: '2011-07-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Firebug 1.8](http://getfirebug.com/releases/firebug/1.8/firebug-1.8.0.xpi) compatible with **Firefox 5.0** [has been released](http://blog.getfirebug.com/2011/07/29/firebug-1-8-0/) and I would like to get this opportunity and introduce some new features in this version.

Firebug 1.8 has been also uploaded to [AMO](https://addons.mozilla.org/en-US/firefox/addon/firebug/), but it can take some time to appear.

![Firebug Firebug](../../assets/0ce0d0753630c881.png)


First of all, check out the following compatibility table:

**Firefox 3.6**with[Firebug 1.7.3](https://addons.mozilla.org/en-US/firefox/addon/firebug/versions/?page=1#version-1.7.3)**Firefox 4.0**with[Firebug 1.7.3](https://addons.mozilla.org/en-US/firefox/addon/firebug/versions/?page=1#version-1.7.3)**Firefox 5.0**with[Firebug 1.8](https://addons.mozilla.org/en-US/firefox/addon/firebug/)(and also[Firebug 1.7.3](https://addons.mozilla.org/en-US/firefox/addon/firebug/versions/?page=1#version-1.7.3))**Firefox 6.0**with[Firebug 1.9a0](http://getfirebug.com/releases/firebug/1.9/firebug-1.9.0a0.xpi)(and Firebug 1.8 as soon as 6.0 is out)**Firefox 7.0**with[Firebug 1.9a0](http://getfirebug.com/releases/firebug/1.9/firebug-1.9.0a0.xpi)**Firefox 8.0**with[Firebug 1.9a0](http://getfirebug.com/releases/firebug/1.9/firebug-1.9.0a0.xpi)

### console.timeStamp()

There is a new API that can be used to create time-stamps during Javascript execution and compare them together with HTTP traffic timing on the timeline in the Net panel: `console.timeStamp();`


![console.timeStamp()](../../assets/f53842c9bc144b9a.png)


See [detailed description](http://www.softwareishard.com/blog/firebug/firebug-1-8-console-timestamp/) of this feature with examples how to use it.

### IP Address displayed in the Net Panel

The Net panel displays remote & local IP address + port number for each request. There are two additional columns, see the screen-shot:

![Net Panel IP Address & Port](../../assets/bbdf9f5a8fc70a46.png)


### HTML Preview Reloaded

This feature is back and better than before. Now you can adjust height of the preview by drag-and-drop to see more or less content as necessary.

![Resizeable HTML Preview](../../assets/d54239404a58b4a0.png)


### Improved Script Location List

Script location list available in the Script panel adjusts its size automatically according to the screen size and uses scroll-bar as needed. This makes easier for the user to pick up the right script.

![Script Location List](../../assets/f6a844462d25de96.png)


### Command Line Content Persistence

Command line content is now persistent across reloads. This feature allows to quickly execute the same expression on different pages. This is one of many little details that make Firebug the indispensable tool.

### New DOM Panel Options

The DOM panel has two new options:

![New options in the DOM panel](../../assets/0bb8329a850c38cb.png)


**Show Own Properties Only**check if you don’t want see the prototype chain for objects**Show Enumerable Properties Only**check if you want to see only enumerable properties

### CSS Panel Color Tooltips

A tooltip with color preview is displayed for colors specified in various formats. Supported formats are: hex, rgb, rgba, hsl and hsla.

![Color Tips](https://hacks.mozilla.org/wp-content/uploads/2011/07/csspanel-colortips.png)


### Shortcuts for Changing CSS values

Firebug is great when tweaking CSS of the current page to perfection. Now, there are also new keyboard shortcuts for changing CSS values (numbers).

*Ctrl+Up/Down*increases/decreases by**0.1***Shift+Up/Down*increases/decreases by**10**

### Better Support for External Editors

As you might know Firebug allows to configure and open an external editor (or IDE). There has been two arguments you could pass to such editor:

![External editors](../../assets/cc7cd4656a9901a7.png)


*%url*URL of the file (if %url is not present, %file will be added by default)*%file*Path to the local file (or to the temporary copy)

Firebug 1.8 introduces a new **%line** argument that allows to open the external editor scrolled at the right position (according to the current scroll position in the the Script panel).

*%line*Line number

### Box Sizing Exposed

CSS3 introduced a new property called **box-sizing**, which allows the user changing the box model for an element and thereby influence element layout. Value of this property is now exposed in the **Layout side panel**.

![Box-sizing property](../../assets/b1bc29d19d017bc8.png)


Honza

## 14 comments

Style ThingJuly 29th, 2011 at 19:06AutoJuly 30th, 2011 at 17:56GaryJuly 31st, 2011 at 14:54Gaurav MishraJuly 31st, 2011 at 23:26Harry WilesAugust 1st, 2011 at 01:25Chris JordanAugust 1st, 2011 at 09:47HonzaAugust 1st, 2011 at 09:56SIFENovember 13th, 2012 at 03:32Chris JordanAugust 1st, 2011 at 10:38Louis R. StephensAugust 2nd, 2011 at 10:35SamukaAugust 1st, 2011 at 19:36SebastienAugust 2nd, 2011 at 03:28HonzaAugust 2nd, 2011 at 03:54DanielSeptember 12th, 2011 at 16:59