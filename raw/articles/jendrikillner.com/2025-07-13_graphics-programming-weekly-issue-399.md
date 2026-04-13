---
title: Graphics Programming Weekly - Issue 399
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-399/
author: Jendrik Illner
published: '2025-07-13'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- presents the argument that rendering industry is shifting from technology-driven growth to content delivery and user-generated content as primary revenue drivers
- discusses the role of machine learning in rendering, noting its effectiveness in post-processing but limited impact on core algorithms due to existing analytical solutions
- predicts future trends toward “more real-time, less baking” approaches and advances in dynamic data structures for optimal signal representation

![](../../assets/879e97861482c689.png)


- explores the technical foundations of digital display technology
- covers the evolution from electron guns to modern displays
- examines how pixels and color systems work in todays screens

![](../../assets/f2cfff6755a1a57f.png)


- explains how to use Wave Matrix Multiply Accumulate (WMMA) operations on AMD RDNA 4 GPUs
- covers the simplified VGPR layout compared to RDNA 3 and the new intrinsics for 16x16 matrix operations
- provides practical examples including multi-layer perceptron (MLP) implementation using WMMA for neural network inference

![](../../assets/be30c2dc309eac3a.png)


- announces the launch of Skia Graphite as Chrome’s new rasterization backend
- explains how Graphite improves upon the previous Ganesh backend with better multithreading and depth testing for 2D graphics
- details performance improvements and future development plans

![](../../assets/0be8e8f75ed1bed2.png)


- comprehensive guide to efficiently packing various data types commonly used in graphics programming
- covers techniques for normalized data, floating point formats, bitfields, and specialized encoding methods for normals and world positions
- provides HLSL code examples and GPU instruction analysis on RDNA hardware

![](../../assets/26c211f44846e714.png)


- compares lossless compression techniques for multi-layer floating point images
- evaluates OpenEXR, JPEG-XL, and a custom approach using mesh optimizer with zstd
- presents that mesh optimizer combined with zstd provides really good performance-to-compression ratio results

![](../../assets/b0fbe96fd7f76947.png)


- presents a new approach to color quantization using the HyAB distance formula in CIELAB color space
- compares results against exisitngs methods
- demonstrates how a hybrid distance metric (absolute difference in lightness, Euclidean in chromaticity) improves color fidelity in quantized images

![](../../assets/a9351bf6fd76309a.png)


- addresses visual artifacts that occur with transparent textures have unintetional RGB values in transparent areas during mipmapping
- presents a Python tool that pads transparent textures by bleeding opaque pixels outward to fix rendering issues
- explains the difference between premultiplied and straight alpha workflows and their impact on texture processing

![](../../assets/4e0927ff7ed45b81.png)


- video exploring the mathematical relationship between matrices and tensors
- covers tensor algebra concepts that extend beyond traditional matrix operations
- presents mathematical foundations useful for understanding advanced graphics and machine learning algorithms

![](../../assets/02113b4b592bcc35.png)


- detailed explanation of physarum-inspired algorithms for creating organic-looking simulations and visual effects
- provides implementation details including GPU shader techniques, interactive experiments, and artistic applications for real-time organic pattern generation

![](../../assets/a9891d77bc68d252.png)


- video recording of research paper presentations from the Interactive 3D Graphics and Games (I3D) 2025 conference
- features cutting-edge research on neural rendering techniques and Gaussian splatting methods
- showcases the latest developments in neural graphics and real-time rendering technologies

![](../../assets/722b727205606b27.png)


- research presentations from I3D 2025 conference focusing on advanced filtering and reconstruction techniques
- covers state-of-the-art methods for image and signal processing in real-time graphics applications
- presents novel approaches to improving quality and performance in interactive 3D rendering

![](../../assets/b7099501a34ab4d2.png)

Thanks to [Aras Pranckevičius](https://aras-p.info/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.