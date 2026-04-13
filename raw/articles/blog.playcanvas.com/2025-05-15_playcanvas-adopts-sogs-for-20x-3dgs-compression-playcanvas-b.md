---
title: PlayCanvas Adopts SOGS for 20x 3DGS Compression | PlayCanvas Blog
url: https://blog.playcanvas.com/playcanvas-adopts-sogs-for-20x-3dgs-compression
author: Will Eastcott
published: '2025-05-15'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Today, we are releasing [PlayCanvas Engine 2.7.5](https://github.com/playcanvas/engine/releases/tag/v2.7.5) that introduces a new and advanced compression format for 3D Gaussian Splatting (3DGS) called Self-Organizing Gaussians (SOGS). **SOGS can reduce 3DGS data by over 20x.**

To showcase PlayCanvas' support for SOGS, we have collaborated with [Christoph Schindelar](https://www.linkedin.com/in/christoph-schindelar-79515351/) to build a technical demo:

The church scene above was originally a **1GB PLY file containing 4 million Gaussians** - not at all suitable for the web or mobile! **Using SOGS, we can serve up the scene in just 55MB!** Read on to find out how.

### Introduction to Self-Organizing Gaussians[](https://blog.playcanvas.com#introduction-to-self-organizing-gaussians)

3D Gaussian Splatting has taken the real-time graphics world by storm, offering breathtaking photorealism. But as many developers have discovered, the incredible detail comes at a cost: massive file sizes. A typical high-quality scene can easily run into hundreds of megabytes, making them challenging for web delivery, mobile experiences, and quick load times.

This is precisely the problem that [Self-Organizing Gaussians](https://github.com/fraunhoferhhi/Self-Organizing-Gaussians), a groundbreaking compression technique from [Wieland Morgenstern](https://wieland.morgenst.de/) at [Fraunhofer HHI](https://www.hhi.fraunhofer.de/en/index.html), sets out to solve.

### The Core Challenge: Taming the Data Deluge[](https://blog.playcanvas.com#the-core-challenge-taming-the-data-deluge)

Each individual Gaussian in a 3DGS scene stores multiple parameters:

- Position (XYZ)
- Scale (3 values)
- Rotation (4 quaternion values)
- Opacity
- Base Color (RGB)
- Spherical Harmonics (SH) coefficients for view-dependent effects (often 45+ values, contributing a huge portion to file size – up to 75%!)

Storing all of these as high-precision floats is what leads to those hefty files.

### Enter SOGS: Reshape, Reorganize, Compress[](https://blog.playcanvas.com#enter-sogs-reshape-reorganize-compress)

Instead of just quantizing individual values or creating simple codebooks for attributes (which are valid but more traditional compression steps), SOGS takes a far more innovative approach, directly inspired by how image compression algorithms work best:

**Grid Reorganization:**The fundamental idea is to take all the Gaussians and their attributes and reshape this data. Imagine "unrolling" all the Gaussians and laying their parameters out into a series of 2D grids or "attribute images." For instance, all X positions could form one 2D image, all Y positions another, each SH coefficient its own image, and so on (e.g., 59+ such images if you have 59 attributes per Gaussian). Initially, these images would look like random noise.**The "Self-Organizing" Sort (PLAS Algorithm):**Here's the magic. SOGS employs a sophisticated sorting algorithm ([Parallel Linear Assignment Sorting - PLAS](https://github.com/fraunhoferhhi/PLAS)) to reorder the Gaussians themselves within these 2D grids. The goal is to arrange them so that Gaussians with similar properties (especially position, scale, and base color) become neighbors in the 2D grid. This process transforms the noisy, random-looking attribute images into much smoother, more structured images with lower frequency content.**Why sort?**Compressing highly organized, smooth data (like a sorted image) is vastly more efficient than compressing noisy, random data. The difference can be dramatic (e.g., a 9x reduction for a sorted vs. random image with JPEG).

**Exploiting Smoothness:**By sorting based on primary attributes (position, scale, base color), SOGS leverages the insight that Gaussians similar in these aspects are also likely to have similar secondary attributes (opacity, rotation, and those bulky SH coefficients). This "co-sorting" makes all the attribute images smoother.**Leveraging 2D Image Compression:**Once these attribute images are smooth and organized, SOGS applies standard, highly optimized 2D image compression codecs to each one. In PlayCanvas, we have opted to use WebP. This is where the massive compression gains come from – the WebP codec is perfect for compressing smooth, predictable image data. Check out the image set for the church:![SOGS Textures](../../assets/e31e88c012ffb594.jpg)


### The Impact for Splat Developers[](https://blog.playcanvas.com#the-impact-for-splat-developers)

Integrating SOGS into PlayCanvas is a game-changer for web-based 3DGS:

- 🗜️
**Massive File Size Reduction:**We're talking serious compression! The church scene above, for example, was reduced from ~1GB to 55MB (a**~20x reduction**). - ⚡
**Lightning-Fast Loading:**Smaller files mean your immersive 3DGS experiences load significantly faster, keeping users engaged. - 📱
**Mobile Feasibility:**This level of compression makes deploying rich 3DGS content practical even on bandwidth or memory-constrained devices. - ✨
**Exceptional Visual Quality:**SOGS is designed to maintain the high visual fidelity that makes 3DGS so compelling, and can even improve it by reducing artifacts. - 🖼️
**Simple Decoding:**The compressed format is essentially a set of WebP images, which are trivial and fast to decode using standard browser capabilities.

With SOGS support, PlayCanvas can deliver stunning, performant, and accessible 3D Gaussian Splat-based experiences directly in the browser. This is **huge news** for e-commerce, architectural visualization, education and entertainment industries.

### What's Next[](https://blog.playcanvas.com#whats-next)

PlayCanvas Engine support is just the first step. Here's what's coming next:

**Editor Support**- Support SOGS data as a first-class citizen in the Asset Panel**SuperSplat Support**- Add SOGS as an export format**Performance Optimization**- Now that we can quickly load vast numbers of Gaussians on mobile, we will turn our attention to boosting frame rates

### 👨💻 Our Open Source Mission[](https://blog.playcanvas.com#-our-open-source-mission)

We proudly provide the PlayCanvas Engine as an MIT-licensed open source project. The 3D Gaussian Splat community has made impressive strides over the past 18 months, largely due to open collaboration. Join us in shaping the future by submitting issues, creating pull requests, or simply starring [our GitHub repo](https://github.com/playcanvas/engine)! ⭐

### 👂 Your Feedback Matters[](https://blog.playcanvas.com#-your-feedback-matters)

We hope you approve of this latest update to our open source journey! The SuperSplat community has grown tremendously, and your feedback is invaluable. What features would you love to see next? Share your thoughts on our [Discord](https://discord.com/invite/T3pnhRTTAY) or [ping us on X](https://x.com/playcanvas)!