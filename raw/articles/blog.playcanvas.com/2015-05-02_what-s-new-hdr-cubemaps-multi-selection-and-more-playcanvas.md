---
title: 'What''s New: HDR Cubemaps, Multi-selection and more | PlayCanvas Blog'
url: https://blog.playcanvas.com/whats-new-hdr-cubemaps-multi-selection-and-more
author: Will Eastcott
published: '2015-05-02'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

It's been another busy week for the PlayCanvas team. Here's a quick run down of the coolness we've deployed for you!

## HDR Cubemaps[](https://blog.playcanvas.com#hdr-cubemaps)

We've taken lighting to a whole new level of realism in PlayCanvas. The Editor now supports the import of HDR images to build HDR cubemaps.

HDR image formats supported are .hdr and .exr. When a texture is selected in the Inspector, there is now a property called HDR which is either true or false. So the workflow to construct an HDR cubemap for image based lighting is now:

-
Upload 6 HDR images

-
Create a new cubemap asset and select it so that it is shown in Inspector

-
Assign the six images as cubemap faces

-
Hit the Prefilter button in Inspector

-
Open the Scene Settings (the cog in the bottom left of the Editor UI)

-
Assign the HDR cubemap asset to the Skybox property in Scene Settings


Now, physical materials will use the HDR cubemap as the source for image based lighting.

## Multi-selection: Phase 1[](https://blog.playcanvas.com#multi-selection-phase-1)

We've deployed the first phase of a really useful new feature: multi-selection. Initially, this works for texture and cubemap assets. In the Assets panel, you can now SHIFT or CTRL click multiple textures or cubemaps. This allows you to do several things:

- Delete multiple assets simultaneously
- Change shared properties once for all assets in the selection
- Display the summed size all assets in the selection

Stay tuned for multi-selection support for other asset types and entities too!

## Material Duplication[](https://blog.playcanvas.com#material-duplication)

If you right click a material asset, you can now duplicate it via the context menu:

## Audio Preview[](https://blog.playcanvas.com#audio-preview)

Now you can play back your audio assets directly from the Editor. Select the audio asset in the Assets panel and the Inspector now shows a play button:

That's all for this week, folks. Now get back to making great games!