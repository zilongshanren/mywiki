---
title: 'Tilt: Visualize your Web page in 3D – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2011/07/tilt-visualize-your-web-page-in-3d/
author: Paul Rouget
published: '2011-07-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Tilt** is a Firefox extension that lets you visualize any web page DOM tree in 3D. It is being developed by [Victor Porof](http://twitter.com/victorporof) (3D developer responsible with the Firefox extension itself), along with [Cedric Vivier](http://twitter.com/#%21/neonux) (creating a WebGL optimized equivalent to the privileged canvas.drawWindow, see [#653656](https://bugzilla.mozilla.org/show_bug.cgi?id=653656)) and [Rob Campbell](http://twitter.com/robcee) (who first thought about creating a 3D visualization of a webpage). Everything started initially as a Google Summer of Code project, but now, with an enthusiastic team behind it and so many new features and ideas, it has become an active Developer Tools project.

Tilt is a fun new Firefox extension focused on creating a 3D visualization of a webpage.

Since the DOM is essentially a tree-like representation of a document, this tool layers each node based on the nesting in the tree, creating stacks of elements, each having a corresponding depth and being textured according to the webpage rendering itself.

Unlike other developer tools or inspectors, Tilt allows for instant analysis of the relationship between various parts of a webpage in a graphical way, but also making it easy for someone to see obscured or out-of-page elements. Moreover, besides the 3D stacks, various information is available on request, regarding each node’s type, id, class, or other attributes if available, providing a way to inspect (and edit) the inner HTML and other properties.

## Based on WebGL

The visualization is drawn using WebGL, for dynamic, fast, in-browser rendering. At initialization, Tilt creates individual 3D objects (structures describing how the webpage geometry looks like) using the DOM, with the BODY as the lowest layer and the base of the document upon which descendant nodes are layered. For each successive level, another platform is built, adding depth to the 3D webpage mesh. For example, stacks are built from DIVs, ULs, or any containing node with children.

## Controls

Controlling the visualization is achieved using a virtual trackball (arcball), which rotates around the X and Y axes. Other mouse events exist to control yaw, pitch, roll, pan, zoom, as well as various additional keyboard shortcuts. The controller is not tied to these peripherals only however, making it accessible and easily scalable for other input methods or devices. Double clicking a node brings up the Ace Cloud9 IDE editor, showing more useful information about the node and the inner HTML.

## Try it

You can find the Tilt source code and the latest extension builds [on Github](https://github.com/victorporof/Tilt), and a development blog with milestone updates on [blog.mozilla.com/tilt](http://blog.mozilla.com/tilt).

For now, to test the extension, just download the latest stable build ([tilt.xpi](https://github.com/victorporof/Tilt/raw/master/bin/Tilt.xpi): *download the file, then open it with Firefox or drag’n drop it on Firefox*), install it and search for Tilt inside the Tools menu. Or, you can use Ctrl+Shift+L (or Cmd+Shift+L if you’re on a Mac) to start the visualization. Close it at any time with the Esc key. Tilt works with any webpage, so you can even inspect this blog to see how it looks in 3D.

## Future

More features are soon to be added, some of which include: modifying and updating the 3D webpage mesh on the fly (as the webpage changes, exposing CSS transforms for each node, plus customizing stack spacing, thickness, transparency etc.), rendering elements with absolute position or floats differently (e.g., hovering above the webpage based on their z-index), creating a more developer-friendly environment and better integration with the Ace editor and the Firefox Developer Tools. (highlighting the currently selected node, instant 3D preview), exporting the visualization to other browsers or applications (as a 3D object file, probably .obj and/or COLLADA).

The greatest milestone will be achieving seamless 3D navigation between webpages, as in a normal 2D environment.

For more information about upcoming tasks visit the [TODO.md](https://github.com/victorporof/Tilt/blob/master/TODO.md) list.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 108 comments

BuzuJuly 20th, 2011 at 08:28Jeff HammelJuly 20th, 2011 at 09:51Joss CrowcroftJuly 20th, 2011 at 10:12Paul RougetJuly 20th, 2011 at 10:15Vitor De MarioJuly 20th, 2011 at 10:23AjayJuly 20th, 2011 at 10:39Rian ArionaJuly 20th, 2011 at 10:59mattew fedakJuly 20th, 2011 at 11:00francoisJuly 20th, 2011 at 12:22Keith BarrowsJuly 20th, 2011 at 11:07JerrieJuly 21st, 2011 at 04:25GalaxyJuly 20th, 2011 at 11:13skylamerJuly 20th, 2011 at 11:21AliJuly 20th, 2011 at 11:39Michael BehanJuly 20th, 2011 at 11:41skilamerJuly 20th, 2011 at 11:48Riley StrongJuly 20th, 2011 at 12:02vicapowJuly 20th, 2011 at 12:19ZukWooJuly 20th, 2011 at 12:20Michael ScovettaJuly 20th, 2011 at 12:40MedJuly 20th, 2011 at 12:45Saurabh MukhekarJuly 20th, 2011 at 13:08AndrewJuly 20th, 2011 at 13:33MaxJuly 20th, 2011 at 14:32Paul RougetJuly 20th, 2011 at 21:43Yuriy RomadinJuly 20th, 2011 at 14:43Ken SaundersJuly 20th, 2011 at 15:37Ken SaundersJuly 20th, 2011 at 15:39Eric BiellerJuly 20th, 2011 at 15:52andreiJuly 20th, 2011 at 16:08db48xJuly 20th, 2011 at 18:44JeffJuly 20th, 2011 at 21:14Paul RougetJuly 20th, 2011 at 21:38Wren RJuly 20th, 2011 at 22:49Gaurav MishraJuly 20th, 2011 at 23:16AdamTJuly 21st, 2011 at 01:13Paul LiddingtonJuly 21st, 2011 at 04:12morganJuly 21st, 2011 at 01:42Alex HallJuly 21st, 2011 at 03:42ClaudiuJuly 21st, 2011 at 03:49Uwe chardonJuly 21st, 2011 at 03:51KoldkaffeJuly 21st, 2011 at 03:58Murali KumarJuly 21st, 2011 at 04:01UnusJuly 21st, 2011 at 04:15ChichiJuly 21st, 2011 at 04:19RobIIIJuly 21st, 2011 at 04:31Martin DubéJuly 21st, 2011 at 04:52Vanessa TibikaJuly 21st, 2011 at 05:16CharbelJuly 21st, 2011 at 05:20Daniel SJuly 21st, 2011 at 05:26mooJuly 21st, 2011 at 06:19EelkeJuly 21st, 2011 at 06:25JackJuly 21st, 2011 at 07:08CharbelJuly 21st, 2011 at 07:47darwinJuly 21st, 2011 at 08:42KimJuly 21st, 2011 at 11:01ernestJuly 21st, 2011 at 11:12DarrynJuly 21st, 2011 at 13:56Stephanie DaughertyJuly 21st, 2011 at 21:29Vasileios TopouzJuly 22nd, 2011 at 02:59Norbert VietenJuly 22nd, 2011 at 06:18BlakeygJuly 22nd, 2011 at 08:28RicardoAugust 2nd, 2011 at 08:50MZAugust 9th, 2011 at 19:12ApoleonJuly 24th, 2011 at 06:59MichaelJuly 24th, 2011 at 19:06SJJuly 26th, 2011 at 04:07louisremiJuly 26th, 2011 at 09:46AjayJuly 26th, 2011 at 04:46NiklasJuly 26th, 2011 at 15:26ChakJuly 27th, 2011 at 02:24ClaudiuJuly 27th, 2011 at 03:43Mudit JainJuly 27th, 2011 at 18:56witekJuly 30th, 2011 at 07:16Ayush GuptaJuly 31st, 2011 at 04:06J.S.WebschmiedeJuly 31st, 2011 at 10:24SteveMJuly 31st, 2011 at 19:04Jubayer ArefinJuly 31st, 2011 at 23:42pwAugust 1st, 2011 at 06:50ThugOctober 21st, 2011 at 03:26EnricoAugust 2nd, 2011 at 05:46neilAugust 2nd, 2011 at 06:11SteFAugust 2nd, 2011 at 07:11Kevin HarterAugust 3rd, 2011 at 08:22EricFebruary 5th, 2012 at 16:05Alexey ZinovievAugust 10th, 2011 at 23:44Chico Web DesignAugust 31st, 2011 at 16:57paris triathlonSeptember 29th, 2011 at 09:23paris triathlonOctober 3rd, 2011 at 01:54evanOctober 2nd, 2011 at 04:36Niall FlynnOctober 21st, 2011 at 08:18AlbertOctober 28th, 2011 at 22:33WojtekNovember 2nd, 2011 at 12:19ProvaNovember 4th, 2011 at 08:16BosiNovember 10th, 2011 at 12:05Siddharth SaxenaNovember 14th, 2011 at 10:21techglimpseNovember 29th, 2011 at 03:12DanDecember 6th, 2011 at 10:21kathrinJanuary 8th, 2012 at 13:39Lee JordanJanuary 14th, 2012 at 10:56Guilherme MonteiroJanuary 27th, 2012 at 22:01simone medriMarch 14th, 2012 at 08:02TodorMarch 16th, 2012 at 07:34FranciscoMarch 30th, 2012 at 23:05JamieApril 29th, 2012 at 19:24SEO BiellaNovember 29th, 2012 at 18:22Agung WisesoFebruary 8th, 2013 at 01:33chrisApril 8th, 2013 at 19:04