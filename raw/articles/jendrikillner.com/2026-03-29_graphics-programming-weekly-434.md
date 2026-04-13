---
title: Graphics Programming Weekly 434
url: https://www.jendrikillner.com/post/graphics-programming-weekly-issue-434/
author: Jendrik Illner
published: '2026-03-29'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

- analyzes the rendering techniques used in Tomb Raider III, running on hardware without T&L or programmable shaders
- covers portal-based room traversal for visibility culling, texture atlases with 256×256 palettized tiles, and distance fog to mask geometry cutoffs
- describes how static lighting was baked into vertex colors, and how color-key transparency and flipbook texture animations achieved dynamic-looking effects on constrained hardware

![](../../assets/ba044ba1baf241a9.png)


- compares the three hardware lossy image compression formats: Apple’s Metal lossy, ARM’s AFRC, and ImgTec’s PVRIC4
- benchmarks quality and throughput against Spark across R8, RG8, and RGBA8 formats

![](../../assets/030b9fa03e3c0b47.png)


- Digital Foundry tests the upgraded PSSR upscaler across various games
- revisits previously contentious PSSR-supported games using the new “Enhance Image Quality” dashboard mode and evaluates the improvements, remaining problems, and any regressions
- discusses whether Sony should have enabled the new PSSR by default and whether it qualifies as the definitive upscaling solution on PS5 Pro

![](../../assets/47563d667fea84c9.png)


- article and prototype implementation explaining how to build data inheritance, where derived data inherits from a base, and overrides are explicitly tracked per property
- covers how to extend the concept from simple scalar fields to collections
- discusses the associated UI challenges such as visualizing override indicators, handling removed items, and providing granular revert controls

![](../../assets/ddffd0083d92138e.png)


- new part of the Terrain Shaders series, showing how to add puddle effects to landscapes in Unreal Engine
- follows on from the previous episode, which covered rain effects on terrain in Unity
- demonstrates how to blend puddle wetness and reflections into a landscape material shader

![](../../assets/04bcb20438f1d548.png)


- tutorial on using Signed Distance Field (SDF) textures to drive shadow placement on anime-style face shading
- SDF face textures encode where shadows should appear on the face relative to light direction

![](../../assets/7ce9fd676ad68bf9.png)


- follow-up to part 1 on what constitutes a clean mesh in 3D modeling
- walks through specific examples of how to clean up meshes for film, games, and other use cases

![](../../assets/cb4e3258fe7cf8df.png)


- explains how LLM quantization works, covering how floats are stored and why smaller formats (float16, bfloat16, float8, float4) can replace float32 for model weights
- describes symmetric and asymmetric quantization as more effective alternatives to simple rounding

![](../../assets/ce470d513d956903.png)


- explains the Vision Transformer (ViT) architecture
- covers patch embeddings, learnable positional encodings, the class token, and the encoder-only classification head
- walkthrough for a hands-on fine-tuning example

![](../../assets/c3ce38a69be58012.png)


- personal statement on why SIGGRAPH Asia 2026 should be boycotted due to Malaysia being chosen as the host country
- criticizes the official SIGGRAPH for framing LGBTQ+ inclusion as a matter of cultural opinion rather than membership safety
- calls on SIGGRAPH leadership to relocate the conference and to introduce a structural venue review process that consults at-risk communities

![](../../assets/4e694e781a19f5de.png)

Thanks to Stephen Hill for support of this series.

Would you like to see your name here too? Become a [Patreon](https://www.patreon.com/jendrikillner) of this series.