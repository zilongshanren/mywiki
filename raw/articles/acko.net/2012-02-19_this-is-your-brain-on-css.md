---
title: This is Your Brain on CSS
url: https://acko.net/blog/this-is-your-brain-on-css/
author: Steven Wittens
published: '2012-02-19'
source_blog: Hackery, Math & Design — Acko.net
source_site: https://acko.net/
category: graphics
fetched: '2026-04-19'
---

![This is Your Brain on CSS](../../assets/fed233ccbbf588cb.jpg)

# This is Your Brain on CSS

First things first: the CSS 3D renderer used to power ~~this~~ *the previous* site is now [available on GitHub.com](https://github.com/unconed/CSS3D.js). However, it's still limited to only solid lines and planes. It's also limited to WebKit browsers, as Firefox's CSS 3D support just isn't quite there yet.

But CSS 3D is not a one trick pony, and as with many things, what you get out of it depends entirely on what you put in. So here's a disembodied head made out of CSS 3D. It consists of nothing more than a bunch of images stacked up against each other, and integrates perfectly with the existing 3D parallax on this site. Click and drag to rotate, or use the slider to look inside.

Making the basic effect was actually quite easy. I took an MRI from the [Stanford Volume Data Archive](http://graphics.stanford.edu/data/voldata/) and wrote a small script to turn it into a sheet of CSS sprites. There's [one file for color](http://acko.net/files/mri/MRbrain-color.jpg), [one for opacity](http://acko.net/files/mri/MRbrain-alpha8.png), totalling about 2.1 MB. Both files are composited into Canvases and placed in slices into the DOM, offset forward or backwards in 3D. Then there's just some minor logic to rotate the slices in 90 degree increments to follow the camera.

But the slices are rendered as is, and the MRI consists of [boring grayscale data](http://acko.net/files/mri/MRbrain-alpha8.png). Luckily, I can precompute any amount of shaders and effects I want and just bake them into the slices. I geeked out by applying fake specular lighting, for that 'fresh meat' look, and volumetric obscurance to enhance the sense of depth on the inside. I changed the palette to gory colors based on local density, giving the impression of flesh and bone knitting itself together. Creepy, but cool.

I wrapped it in a custom widget, using straight up CSS rather than Three.js this time. I've wanted to play with [Tangle.js](http://worrydream.com/Tangle/), so I used that to hook up the camera controls and slider. That's pretty much it. In an ideal world, the jarring transition when rotating would be covered up by a nice transition, but the browsers don't like it.