---
title: PlayCanvas Feature Update | PlayCanvas Blog
url: https://blog.playcanvas.com/playcanvas-feature-update
author: Dave Evans
published: '2015-09-21'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

New features have dropped: Entity Materials and Shader Assets!

## Entity Materials[](https://blog.playcanvas.com#entity-materials)

Have you ever been bothered by changes to your materials affecting all Entities with that model? You no longer need to worry. With the new Entity Materials feature you can customize which materials are applied on a per Entity basis.

Simply drag a material onto your model to create new Entity material. Or manage it from the model component interface.

## Shader Assets[](https://blog.playcanvas.com#shader-assets)

We now let you upload and create GLSL shader code as an asset in your project. Simply drop a **.glsl** file into the scene. Or create a new file from scratch in the asset panel.

Also, if you're smart, you can use the `asset.on('change')`

event to automatically update your materials whenever the shader changes.

**Live editing of material shaders anyone?**

These are just two of the new features we've added over the past few months. If you haven't visited PlayCanvas in a while, now is the perfect time to get back to building.