---
title: Build WebGPU Apps Today with PlayCanvas | PlayCanvas Blog
url: https://blog.playcanvas.com/build-webgpu-apps-today-with-playcanvas
author: Will Eastcott
published: '2024-04-18'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

It's here! 🥳 Today, we're excited to announce that WebGPU support has officially arrived in the PlayCanvas Editor.

![Editor with WebGPU Scene](../../assets/2c1f0490a7b4a2a3.png)


## WebGPU on the Rise[](https://blog.playcanvas.com#webgpu-on-the-rise)

Since its inception back in 2010, PlayCanvas has been layered on top of WebGL. In 2017, we were proud to launch support for [WebGL 2.0](https://blog.playcanvas.com/mozilla-launches-webgl-2-with-playcanvas/) in partnership with our friends at Mozilla. April 2023 marked the beginning of a new era for web graphics when Google enabled WebGPU by default in Chrome 113. Since then, WebGPU adoption has exploded and today, [Web3D Survey](https://web3dsurvey.com/webgpu) reports that **62.19% of end users can now run WebGPU**. With [Firefox and Safari due to launch their WebGPU support](https://caniuse.com/webgpu) in the not-too-distant future, expect this number to rise dramatically in 2024.

## Why WebGPU Matters[](https://blog.playcanvas.com#why-webgpu-matters)

If you enable WebGPU for your PlayCanvas project, you may not notice much difference to begin with. In fact, we have put a great deal of effort into ensuring your WebGL projects look identical under WebGPU. But over time, there is are a great deal of opportunities to achieve performance improvements due to WebGPU's reduced driver overhead.

Another key feature unique to WebGPU is support for Compute Shaders which allow for general computation on the GPU. Support for Compute Shaders landed in [Engine v1.70.0](https://github.com/playcanvas/engine/releases/tag/v1.70.0). Here you can see Computer Shaders in action simulating 1 million particles on the GPU:

[Click here](https://playcanvas.github.io/#/compute/particles) to run it for yourself in a WebGPU-enabled browser (i.e. Chrome or Edge).

In short, WebGPU represents the future for PlayCanvas and you can expect some incredible advances in performance and functionality over the coming months.

## Getting Started with WebGPU[](https://blog.playcanvas.com#getting-started-with-webgpu)

WebGPU support in PlayCanvas is still considered 'Beta'. There are still some unimplemented features (for example, the run-time lightmapper is still not supported). Therefore, you have to currently 'opt in' to WebGPU support. To do this, open your Project's Settings in the Inspector and expand the `RENDERING`

section. Then update `Graphics Devices`

to include `WebGPU (beta)`

.

Once we are satisfied WebGPU support has matured enough, it will become the default.

## Your Feedback is Important[](https://blog.playcanvas.com#your-feedback-is-important)

Since WebGPU support is new, we rely on the community for feedback. What works and what doesn't? Please [submit an issue](https://github.com/playcanvas/editor/issues) if you discover any problems or kick off a new thread on the [forum](https://forum.playcanvas.com/) if you want to discuss WebGPU support in more detail. We want to hear what your opinions! 👂