---
title: Create 3D Gaussian Splat Apps with the PlayCanvas Editor | PlayCanvas Blog
url: https://blog.playcanvas.com/create-3d-gaussian-splat-apps-with-the-playcanvas-editor
author: Will Eastcott
published: '2024-06-05'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

[CLICK HERE](https://playcanv.as/e/p/cLkf99ZV/) to open in a new tab. Credits: Splats scanned at the [V&A Museum](https://www.vam.ac.uk/). HDRI from [Poly Haven](https://polyhaven.com/a/sepulchral_chapel_rotunda).

We have big news for the 3D Gaussian Splat community - the PlayCanvas Editor now has fully integrated support for splats! Learn how to quickly build stunning, interactive 3DGS applications today.

🤳 A smartphone

💻 A computer with a web browser

⏱️ A small amount of time

The application above shows several splats assembled in a single application, with animation and post effects spicing up the visuals. Let's check out how it was built.

### Step 1: Clean in SuperSplat 🧹[](https://blog.playcanvas.com#step-1-clean-in-supersplat-)

After [capturing the statues](https://developer.playcanvas.com/user-manual/graphics/gaussian-splatting/#creating-splats) to PLY format, our first stop is [SuperSplat](https://playcanvas.com/supersplat/editor?load=https://raw.githubusercontent.com/willeastcott/assets/main/statues/narcissus.compressed.ply), the open source tool for editing and optimizing 3D Gaussian Splats. Here, in a little over a minute, we can isolate the statue from the background and align it with the origin:

Once we are done, we can download the splat using our [compressed PLY format](https://blog.playcanvas.com/compressing-gaussian-splats). In this case, our downloaded PLY is **only 1.56MB**!

### Step 2: Import into the Editor 🚧[](https://blog.playcanvas.com#step-2-import-into-the-editor-)

Now that we have a clean, compressed PLY, we simply need to drop it into the Editor's Asset Panel. And from there, drag it into the viewport to add it to the scene. Let's do that (along with a cube map for a photographic backdrop):

The PlayCanvas Editor is a powerful visual environment for building and publishing 3D scenes. You can:

- Grab useful scripts (and other assets) from the Asset Store. Here, we import an Orbit Camera script.
- Create beautiful user interfaces, using either HTML or PlayCanvas' built-in UI system.
- Add sound, physics, VR/AR support and much, much more.

### Step 3: Add Animation and Post Effects ✨[](https://blog.playcanvas.com#step-3-add-animation-and-post-effects-)

What really makes the demo pop is the transitions that fade the statues in and out.

With the Editor, you can customize the shader code that renders your splats to apply stunning animation effects. For the transition between statues, individual splats are transformed and recolored over time, while a full-screen bloom effect is ramped up and down.

### Resources[](https://blog.playcanvas.com#resources)

Today's release makes working with 3D Gaussian Splats both easy and fun! We've shown you how to build a virtual gallery or museum but the possibilities are endless. With 3D Gaussian Splats in the PlayCanvas Editor, you can target many verticals: product visualization (furniture, clothing, consumer electronics), automotive, education, travel and so much more.

To get started, here is an useful list of resources:

[Statue Project](https://playcanvas.com/project/1224723/overview/3d-gaussian-splat-statues)- feel free to fork it, explore and experiment.[3D Gaussian Splatting](https://developer.playcanvas.com/user-manual/graphics/gaussian-splatting/)User Guide[SuperSplat](https://playcanvas.com/supersplat/editor)(don't forget to[install the PWA](https://blog.playcanvas.com/a-faster-supersplat-with-pwa-support#pwa-support))

### Go Forth and Create[](https://blog.playcanvas.com#go-forth-and-create)

We hope you love today's update as much as we do! ❤️

But let us know what you think by heading over to the [forum](https://forum.playcanvas.com) or [ping us on X](https://x.com/playcanvas)!