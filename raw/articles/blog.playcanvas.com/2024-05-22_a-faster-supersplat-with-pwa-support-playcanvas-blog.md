---
title: A Faster SuperSplat with PWA Support | PlayCanvas Blog
url: https://blog.playcanvas.com/a-faster-supersplat-with-pwa-support
author: Will Eastcott
published: '2024-05-22'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Today, we are announcing the latest release of [SuperSplat](https://playcanvas.com/supersplat/editor), the open source tool for editing and optimizing 3D Gaussian Splats. If you don't have a PLY file to hand, [here's an example](https://playcanvas.com/supersplat/editor?load=https://raw.githubusercontent.com/playcanvas/engine/main/examples/assets/splats/biker.ply)!

![SuperSplat PWA](../../assets/889f2080dd791efd.png)


[Version 0.17.1](https://github.com/playcanvas/supersplat/releases/tag/v1.17.1) focuses on two key areas: performance and PWA support.

## Performance Improvements[](https://blog.playcanvas.com#performance-improvements)

SuperSplat is now *over 2x faster on the GPU*! 🏃

Compare before and after (notice GPU time dropping from 32ms to 13.5ms for the bike scene):

![SuperSplat PWA](../../assets/f2de78f460248a43.webp)


This is thanks to the [v1.71.0 release](https://github.com/playcanvas/engine/releases/tag/v1.71.0) of the PlayCanvas Engine, which includes a dramatic overhaul of how splats are processed by the GPU. For the technical details, take a look at [this pull request](https://github.com/playcanvas/engine/pull/6357).

The result is that SuperSplat can now throw around millions of splats and still maintain a silky smooth frame rate. Try it for yourself!

## PWA Support[](https://blog.playcanvas.com#pwa-support)

A Progressive Web App (PWA) is a web application that provides a native app-like experience, including the ability to install it on a user's home screen or desktop.

From today, SuperSplat is shipping with PWA support! 🎉

To install SuperSplat as a PWA:

- Visit
[https://playcanvas.com/supersplat/editor](https://playcanvas.com/supersplat/editor). - Hit the
`Install SuperSplat`

button in the address bar.

For your convenience, pin SuperSplat to the Taskbar (Windows) or add it do the Dock (macOS).

### PLY File Association[](https://blog.playcanvas.com#ply-file-association)

With SuperSplat installed as a PWA, your operating system can now open launch PLY files directly into the tool. Simply right-click on a PLY file and select SuperSplat to open it.

You can also set SuperSplat as the default tool to open your PLYs. Then, you can simply double-click a PLY file to open it instantly in SuperSplat!

## Your Feedback Matters[](https://blog.playcanvas.com#your-feedback-matters)

We hope you love today's update! ❤️

The SuperSplat community has grown a lot in recent weeks and we want to get your feedback. What other features would you like the PWA to get? Are you still experiencing any performance problems? What is still missing from SuperSplat? Let us know by heading over to the [forum](https://forum.playcanvas.com) or [ping us on X](https://x.com/playcanvas)!