---
title: Graphics Programming Weekly - Issue 405
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-405/
author: Jendrik Illner
published: '2025-08-24'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- video explains the implementation of a tornado effect as found in Elden Ring
- shows the modeling, UV manipulation, and shader work in Godot

![](../../assets/ddb5a3102742ba4f.png)

- video tutorial covering optimization strategies when games are GPU-limited
- presents techniques for identifying GPU bottlenecks and performance issues
- demonstrates effects of lights, shadows, post-processing, as well as overdraw optimizations

![](../../assets/5c43a6e0c1d013e8.png)


- The author explores GPU point rendering performance bottlenecks
- investigates why millions of points cause dramatic slowdowns on Apple GPUs when heavily overlapped
- compares regular point rasterization vs compute shader approaches across 30+ GPU models

![](../../assets/eb922c3ec0e03f97.png)


- Arm releases a temporal super sampling model optimized for mobile Neural Accelerators
- enables upscaling from 540p to 1080p
- includes explanations on how to get started with the model as well as how to train and evaluate it

![](../../assets/ef11700617c2429b.png)


- comprehensive guide to automatic differentiation in machine learning from a practical perspective
- covers DAG computation graphs, dynamic graph building, and gradient computation using the chain rule
- includes toy AutoGrad implementation in Python, demonstrating forward and backward passes
- explores regularization techniques, skip connections, and gradient management in modern frameworks like PyTorch

![](../../assets/7b8e2b4bd03fcddb.png)


- interactive tutorial on Big O notation explaining algorithm complexity analysis
- covers O(1), O(log n), O(n), and O(n²) with practical examples including bubble sort and binary search
- demonstrates performance implications through visual demonstrations

![](../../assets/bed300145ae58ab3.png)


- trained neural cache storing visibility between lights and 3D positions for direct illumination
- integrates MLP with multi-resolution hash-grid encoding
- feeds light visibility data to weighted reservoir sampling

![](../../assets/ba23a71e611ab5c0.png)


- perceptually uniform color model based on OKLab color space, offering improved color manipulation
- enables consistent brightness across different hues by maintaining the same lightness value
- produces better gradients without muddy midpoints and predictable shades without hue drift
- supports wider Display-P3 gamut colors beyond sRGB

![](../../assets/880e334b08c7684c.png)


- Microsoft’s solution to shader compilation stuttering by moving shader compilation to cloud infrastructure
- creates State Object Database (SODB) from game data and Precompiled Shader Database (PSDB) for distribution
- initially launching on ROG Xbox Ally devices and later broader through the AgilitySDK

![](../../assets/0e9054dd9301ea77.jpg)


- major revision introducing ML-based neural rendering technologies, including AMD FSR 4 upscaling
- requires pre-built, signed DLL architecture with automatic hardware-appropriate fallback from FSR 4 to FSR 3.1.5
- enables automatic driver-based technology upgrades for FSR 4 upscaling and upcoming FSR ML Frame Generation

![](../../assets/7a5355f62460b327.png)


- Python tool for analyzing texture resolution requirements by examining mipmap level information distribution
- calculates per-pixel differences between consecutive mip levels to identify needlessly large textures
- helps to optimize texture memory usage and streaming performance by providing objective metrics for size reduction decisions

![](../../assets/716cb56f1d65e7dd.jpg)

Thanks to [Matt Pharr](https://pharr.org/matt/) for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.