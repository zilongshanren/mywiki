---
title: glTF Viewer Arrives on Mobile with AR Support | PlayCanvas Blog
url: https://blog.playcanvas.com/gltf-viewer-arrives-on-mobile-with-ar-support
author: Elliott Thompson
published: '2022-10-05'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Today we’re excited to announce the next major release of our glTF viewer. This version makes the viewer an ideal tool for reviewing how glTF models render on mobile as well as in augmented reality!

### View Models in AR on Mobile[](https://blog.playcanvas.com#view-models-in-ar-on-mobile)

Once a model has been loaded into the viewer on mobile, you’ll be given the option to drop into an augmented reality experience. The mode you get currently differs based on the operating system you’re using.

![glTF Viewer AR on iOS](../../assets/8c877a134264793b.gif)

![glTF Viewer AR on Android](../../assets/2c9621a0fc660c80.gif)

*Quick Look mode on iOS (left) and WebXR mode on Android (right)*

On iOS, the model will be loaded with Apple’s AR Quick Look mode (above left), while on Android the model will be placed into your environment using WebXR (above right).

### Mobile-Optimized Design[](https://blog.playcanvas.com#mobile-optimized-design)

![glTF Viewer Mobile Start](../../assets/e8b82af27e4736e8.png)

![glTF Viewer Mobile Controls](../../assets/96f57fd446f43f31.png)

![glTF Viewer Mobile Hierarchy](../../assets/e2f55165de1eb4fc.png)

It’s now possible to verify the content and rendering of your assets no matter which device you’re working on. The viewer has been redesigned using mobile-first principles, so you can explore glTF content just as well on mobile as you can on desktop. The UI scales up or down depending on the device screen size and takes an uncluttered approach to ensure you can focus on the glTF content itself even on very small screens.

### Quickly Load Models on Mobile Devices[](https://blog.playcanvas.com#quickly-load-models-on-mobile-devices)

When loading PlayCanvas viewer v3.0 on desktop, you’ll be presented with the option to load a glTF model from a URL.

![glTF Viewer Start Screen](../../assets/c22390e14a9364ba.png)


When this is used, the application will generate a QR code you can scan to share the current viewer scene between your devices or others:

![Share with QR Code](../../assets/68337ec6cb6db8b7.png)


### New PlayCanvas Theme[](https://blog.playcanvas.com#new-playcanvas-theme)

The latest release of [PCUI (v2.7.0)](https://github.com/playcanvas/pcui/releases/tag/v2.7.0) enables the use of additional themes in applications built using it. This allowed us to apply a new color theme to the model-viewer:

The new muted gray tones of this theme should allow users to more readily focus on their model content. Over the coming months, you’ll begin to see this new theme applied to more applications in the PlayCanvas ecosystem! Be sure to pass any feedback onto us using the [issue tracker](https://github.com/playcanvas/pcui/issues) of the PCUI library.

### Open Source[](https://blog.playcanvas.com#open-source)

PlayCanvas is fully committed to an open source strategy and our glTF viewer is therefore made available to you on [GitHub](https://github.com/playcanvas/model-viewer). It is a TypeScript application built on PlayCanvas [PCUI](https://github.com/playcanvas/pcui) front-end framework and, of course, the [PlayCanvas Engine](https://github.com/playcanvas/engine) runtime.

These open source projects have been years in the making and would not have been possible without the amazing OSS community. So why not explore our various GitHub repositories and consider making some contributions of your own. We also appreciate feature requests and bug reports, so don’t be shy!

We hope you find the new and improved glTF viewer useful for your projects. Stay tuned for further updates to it in the coming months!