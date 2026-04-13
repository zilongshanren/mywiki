---
title: Debugging and editing webpages in 3D – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/10/debugging-and-editing-webpages-in-3d/
author: Victor Porof
published: '2011-10-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Tilt** is a Firefox addon that lets you visualize any web page in 3D. A new update is available, coming with more developer-oriented features. Try the [addon](https://hacks.mozilla.org#availableasanaddon).

http://www.youtube.com/watch?v=_7eG_PONHRw

Since the [first alpha version of Tilt was announced](http://hacks.mozilla.org/2011/07/tilt-visualize-your-web-page-in-3d/) (a Firefox extension focused on creating a 3D visualization of a webpage), a lot of work has been done to add a great number of developer-oriented features. These focus on debugging the structure of a webpage, inspecting styling and attributes for each node and seamlessly refreshing the visualization when the DOM structure changes or after contents of document are repainted.

## Solve nesting problems

Tilt is useful when searching problems in the HTML structure (like finding unclosed DIV elements for example) by providing the extra third dimension, layering each node based on nesting in the DOM tree. Stacks of elements visually represent branches in the DOM, and each node can be inspected for the inner HTML contents, its computed CSS style and the attributes.

Clicking anywhere on the visualization highlights a color-coded rectangle surrounding the corresponding node. Double click shows up the source preview for that node. Tilt also tries to show the most relevant information when needed (one is most likely to inspect the attributes of an input, button or image element, for example, but can easily switch between HTML, CSS and attributes view at any time).

## Minidom map

The “minidom” is a tree view representation showing a minimalistic snapshot of the document object model. Each node is assigned a color associated by tag name (blue for div, green for span etc.) and represented as a strip, along with visual markers for the id and/or class if available. Each one of these strips also has a width relative to the type, id and class name length for the respective element, and the corresponding 3D stack in the visualization has color-coded margins. The coloring for individual elements is easily changeable using the color picker near to the minidom legend.

Clicking a strip in the tree view (or directly a stack on the 3D document visualization mesh) also highlights the node with a colored quad. This behavior is a good way to relate with the Style Inspector, and a more unified interaction between Tilt and other Developer Tools is planned in the future. All of these additions make it easier to analyze the bounds of each node, along with the HTML, computed CSS and attributes.

## Realtime editing

Because Tilt is able to detect when a webpage’s DOM structure changes or when a repaint is necessary, integration is seamless with existing Developer Tools. Using Tilt and Firebug or Style Editor at the same time is easy. One can enable or disable CSS properties, changing the style of a node, and the visualization changes accordingly.

http://www.youtube.com/watch?v=ae1p5W20Ug8

*To enable realtime updates for the 3D webpage, go to the Options menu and check “Refresh visualization”.*

## Useful for learning

Developer tools such as “view source” have always been used to help people learn about web development. The 3D view highlights the structure of a page better than a flat view, thus anyone can immediately understand the parent-child relationship between nodes in a webpage, their positioning and how the layout is influenced.

One use case for this is the Hackasaurus mashup. The [X-Ray Goggles](http://hackasaurus.org/goggles/) is a nice and fun tool designed to make it easier to learn about the different document node types, the “building blocks” which create a webpage.

## Export

A requested feature was the ability to export the visualization as a 3D mesh, to be used in games or other 3D editors. Tilt adds the ability to export to *.obj*, along with a material *.mtl* file and a *.png* texture (a screenshot of the entire webpage). The open *.obj* format ensures the fact that the mesh can be opened with almost any editor. Here’s a ray-traced rendering of [hacks.mozilla.org](http://hacks.mozilla.org/2011/07/tilt-visualize-your-web-page-in-3d/) in [Blender](http://www.blender.org/):

## Fun with experiments

As soon as it was released, many people found clever and interesting alternative ways to interact with Tilt. One experiment was creating a 3D visualization of an image, by exporting chunks of pixels to a HTML representation. The result was a voxel-like representation, with node blocks and stacks instead of pixels. A simple [Image2Tilt converter](http://tinyurl.com/Img2Tilt) was written in JavaScript, and you can try it directly in the browser.

http://www.youtube.com/watch?v=7YXq4gylERE

Accelerometer support was another addition based on community request. This shows how easy it is to add functionality that wasn’t originally planned.

http://www.youtube.com/watch?v=rbTLwVEfPn0

You can view the source code, fork it and also contribute to the addon with ideas or feature requests on Github, at [github.com/victorporof/Tilt](https://github.com/victorporof/Tilt).

The latest version of [Tilt](https://github.com/victorporof/Tilt/raw/master/bin/Tilt.xpi) can be found on [Github](https://github.com/victorporof/Tilt/raw/master/bin/Tilt.xpi), but you can also download Tilt as an [addon from addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/addon/tilt/).

For compatibility, Tilt requires WebGL capabilities. Go to [get.webgl.org](http://get.webgl.org/) to check availability and troubleshoot any issues. The current version works with Firefox 6.0 to latest [10.0 Nightly releases](http://ftp.mozilla.org/pub/mozilla.org/firefox/nightly/latest-trunk/) (latest Nightly builds now also support WebGL anti-aliasing, working great with Tilt).

To start Tilt, hit *Control+Shift+M* (or *Command+Shift+M* if you’re on Mac OS), or go to **Web Developer -> Tilt**, available in the Firefox application menu (or the Tools menu on Mac OS). You can modify this hotkey (and other properties) from the Options menu after starting Tilt.

More information about Tilt, the development process and milestone updates can be found on [blog.mozilla.com/tilt](http://blog.mozilla.com/tilt).

## Future

Tilt has become an active Developer Tools project, and an ongoing effort is made to integrate it with other existing tools like Style Inspector and Style Editor ([source code](https://github.com/neonux/StyleEditor) and [latest builds](http://neonux.com/StyleEditor/builds/)). As the 3D view of a webpage has proven to be useful for debugging, this main functionality will gradually become part of Firefox in future releases.

## About Victor Porof

Mozillian, hacker, working on Firefox DevTools.

## 14 comments

DannyOctober 26th, 2011 at 10:16seriouslyOctober 28th, 2011 at 14:35CSSmetalOctober 26th, 2011 at 12:24DanielOctober 26th, 2011 at 14:28ThomasOctober 28th, 2011 at 13:29victorOctober 31st, 2011 at 08:01adiblolOctober 28th, 2011 at 13:52victorOctober 31st, 2011 at 08:02OllieDecember 2nd, 2011 at 17:42justin stormsDecember 16th, 2011 at 16:08YESJanuary 27th, 2012 at 02:12gyurciFebruary 15th, 2012 at 07:25MikeApril 17th, 2012 at 04:59ashishAugust 14th, 2012 at 23:13