---
title: Better Asset Management | PlayCanvas Blog
url: https://blog.playcanvas.com/better-asset-management
author: Dave Evans
published: '2015-11-03'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

![PlayCanvas Editor](../../assets/780c8056360455e3.png)


Forget about Twitter changing stars to hearts. PlayCanvas introduces **Asset Folders**!

It's been a long time coming, but today we've revolutionized the way you organize your PlayCanvas assets. Folders, sub-folders, and folders within other folders are all supported right now in the PlayCanvas Editor. We've also updated all the icons to make everything clear crisp and beautiful.

*Some special notes because nothing is quite that simple:*

**Source assets** are now always visible in your asset panel. This means you might see some extra files that you didn't realize you had. Source assets are files that are in a format that you can't use at runtime in your game. You'll see these for some textures and for 3D model and animation formats, they look like asset icons with a dashed border around them.

![source-assets](../../assets/47bf96fa488d4e04.jpg)

*Source asset visible in the editor*

**Scripts** are still a little bit special and we've put them in their own Scripts folder which you can't put other assets in or modify at the moment. We're working on some exciting changes to the way scripting is handled.

**Folders** are just a organization tool in the Editor, so don't try and use them in your game scripts. Stick to script attributes and asset tags for finding your assets in scripts.