---
title: Publish Your Gaussian Splats with SuperSplat 2.0 | PlayCanvas Blog
url: https://blog.playcanvas.com/publish-your-gaussian-splats-with-supersplat
author: Will Eastcott
published: '2025-02-13'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Today, we are announcing a major update of SuperSplat, the open source platform for editing and publishing 3D Gaussian Splats.

### 🏠 We've Moved[](https://blog.playcanvas.com#-weve-moved)

SuperSplat can now be found on a shiny new domain! From now on, point your browser at:

The SuperSplat Editor that you know and love can now be accessed at [https://superspl.at/editor](https://superspl.at/editor). Much easier to remember, don't you think?

### 🌐 Publish your Splats to the Web[](https://blog.playcanvas.com#-publish-your-splats-to-the-web)

Recently, we added the ability to export an HTML viewer of your splat from the SuperSplat Editor. Built on the powerful [PlayCanvas Engine](https://github.com/playcanvas/engine) and our open source [Compressed PLY format](https://blog.playcanvas.com/compressing-gaussian-splats#compressed-ply-format), it offers fast load times and high-performance rendering. However, *hosting* the HTML viewer was still your responsibility. And let's be honest, not everybody has the time or expertise to host their own website. So we've added a new feature to SuperSplat to make it easier to share your splats with others.

It's as easy as 1-2-3:

- Log in with your PlayCanvas account (or sign up if you don't have one).
- Select
`File`

>`Publish`

when you've finished crafting your splat. - Fill out the publishing options form and hit
`Publish`

.

That's it! Your splat will be published to the web and you'll be given a URL to share with others.

By default, your splat will be listed on the SuperSplat website. However, you can also choose to make it unlisted. This means it won't appear in the main gallery, but you can still access it via the URL.

### 🎥 Create Camera Flythroughs[](https://blog.playcanvas.com#-create-camera-flythroughs)

Sure, it's great to be able to share your splats with others, but for that extra 'wow' factor, why not add a camera flythrough? SuperSplat Editor 2.0 introduces the Timeline that makes it a breeze to author great looking camera animations. Simply select a frame in the timeline, position the camera, and set a keyframe. Do this for as many frames as you want and you've got a camera flythrough!

### 📄 Load and Save your SuperSplat Projects[](https://blog.playcanvas.com#-load-and-save-your-supersplat-projects)

With the ability to create camera animations, your splat projects are becoming more and more complex. To support this, we've added a new project file format so you can save your work between sessions. The extension of SuperSplat's new project file format is `.ssproj`

.

The `.ssproj`

file format is actually just a ZIP file containing project data in JSON format, along with a set of PLY files storing the Gaussian Splat data.

The introduction of the new project file format has also prompted us to reorganize the `File`

menu. `Open`

, `Save`

and `Save As`

now only operate on `.ssproj`

files. To import and export other file formats into your project (such as `.ply`

or `.splat`

) you can use the `Import`

and `Export`

options in the `File`

menu.

![File Menu](../../assets/1ad138881f6e4484.png)


### 👥 Explore Splats from the Community[](https://blog.playcanvas.com#-explore-splats-from-the-community)

With the ability to publish splats to the web, [superspl.at](https://superspl.at) has become a great place to explore the work of the Gaussian Splat community. Browse or search digitized reality from creators around the world.

![Community Scroll](../../assets/9e9e78d09e6b7d7e.gif)


#### View Splats in Immersive AR and VR[](https://blog.playcanvas.com#view-splats-in-immersive-ar-and-vr)

One of the coolest things about the PlayCanvas-powered web viewer is that it's fully integrated with WebXR, the browser-based standard for immersive experiences. Simply tap the viewer's AR button and you can spawn photorealistic 3D models directly into your environment.

Or dive straight into a splat in fully immersive VR.

🤳 AR mode has been tested on Meta Quest 2 and 3, and Android-based smartphones.

🥽 VR mode has been tested on Meta Quest 2 and 3, and Apple Vision Pro.

### 👨💻 Our Open Source Mission[](https://blog.playcanvas.com#-our-open-source-mission)

We are proud to bring SuperSplat to you as an MIT-licensed open source project. The 3D Gaussian Splat community has come a long way in the last 18 months and much of that progress is thanks to the OSS community. So it's important to us that we play our part. But we're stronger together, so please do consider joining our open source effort. Submit issue reports, open pull requests...or just help us out by starring [our repo](https://github.com/playcanvas/supersplat)! ⭐

### 👂 Your Feedback Matters[](https://blog.playcanvas.com#-your-feedback-matters)

We hope you love today's update! We put our heart and soul into this release and we're excited to share it with you.

The SuperSplat community has grown a lot over the last year and we want to get your feedback. What other features would you like to see added to the platform? Let us know on the [Discord](https://discord.com/invite/T3pnhRTTAY) or [ping us on X](https://x.com/playcanvas)!