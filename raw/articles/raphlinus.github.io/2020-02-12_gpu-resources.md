---
title: GPU resources
url: https://raphlinus.github.io/gpu/2020/02/12/gpu-resources.html
author: Raph Levien’s blog
published: '2020-02-12'
source_blog: Raph Levien’s blog
source_site: https://raphlinus.github.io/
category: game programming
fetched: '2026-04-13'
---

This post is basically a dump of resources I’ve encountered while doing a deep dive into GPU programming. I welcome pull requests against the [repo](https://github.com/raphlinus/raphlinus.github.io) for other useful resources. Also feel free to ask questions in issues, particularly if the answer might be in the form of a patch to this post.

## Understanding the hardware

### Intel

Intel is one of the best GPU hardware platforms to understand because it’s documented and a lot of the work is open source.

-
[Programmer’s Reference Manual](https://01.org/sites/default/files/documentation/intel-gfx-prm-osrc-kbl-vol07-3d_media_gpgpu.pdf)for Kaby Lake (Gen 9.5)

There’s also some academic literature:

One of the funky things about Intel is the varying subgroup width; it can be SIMD8, SIMD16, or SIMD32, mostly determined by [compiler heuristic](https://software.intel.com/en-us/forums/opencl/topic/564990), but there is a new [VK_EXT_subgroup_size_control](https://www.khronos.org/registry/vulkan/specs/1.1-extensions/html/chap44.html#VK_EXT_subgroup_size_control) extension.

### NVidia

There’s a lot of interest and activity around NVidia, but much of it is reverse engineering.

### AMD

## Understanding API capabilities

-
[vulkan.gpuinfo.org](https://vulkan.gpuinfo.org/)- a detailed database of what extensions are available on what hardware/driver/platform combinations. -
[Metal Feature Set Tables](https://developer.apple.com/metal/Metal-Feature-Set-Tables.pdf)has similar info for Metal.

## Subgroups

Subgroup/warp/SIMD/shuffle operations are very fast, but less compatible (nonuniform shuffle is missing from HLSL/SM6), and you (mostly) don’t get to control the subgroup size, so portability is a lot harder.

## Languages

### GLSL

-
[https://github.com/KhronosGroup/glslang](https://github.com/KhronosGroup/glslang)- reference implementation of GLSL, compilation to SPIR-V -
[shaderc](https://github.com/google/shaderc)- Google-maintained tools

### HLSL

-
[DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler)(DXC) - produces both SPIR-V and DXIL.

### Metal Shading Language

### OpenCL

-
[clspv](https://github.com/google/clspv)- compile OpenCL C (subset) to run on Vulkan compute shaders.- To me, this is evidence that Vulkan will simply eat OpenCL’s lunch. This is still
[controversial](https://github.com/KhronosGroup/Vulkan-Ecosystem/issues/42), but Khronos people are insisting there’s an “OpenCL Next” roadmap.

- To me, this is evidence that Vulkan will simply eat OpenCL’s lunch. This is still
-
[OpenCL 3.0](https://www.khronos.org/news/press/khronos-group-releases-opencl-3.0)is recently announced, and their plans do include clspv and related tools to run on a Vulkan.

### TensorFlow

### Exotic languages

-
[Julia on GPU](https://juliacomputing.com/industries/gpus.html)- layered on CUDA

## SPIR-V

-
[SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross)- transpile SPIR-V into GLSL, HLSL, and Metal Shading Language

## WebGPU

-
[Building WebGPU with Rust](https://fosdem.org/2020/schedule/event/rust_webgpu/)- FOSDEM talk -
[wgpu](https://github.com/gfx-rs/wgpu)- Rust WebGPU implementation -
[dawn](https://dawn.googlesource.com/dawn)- Google’s WebGPU implementation in C++ -
Work-in-progress

[specification](https://gpuweb.github.io/gpuweb/) -
[Get started with GPU Compute on the Web](https://developers.google.com/web/updates/2019/08/get-started-with-gpu-compute-on-the-web)- Google (Chromium/Dawn)

### WebGPU shader language

The discussion of shader language had been very [contentious](https://news.ycombinator.com/item?id=22020511). As of very recently there is a proposal for a textual language that is semantically equivalent to SPIR-V, and there seems to be agreement that this is the path forward.

The previous proposals were some profile of SPIR-V, a binary format, and Apple’s [Web High Level Shading Language](https://webkit.org/blog/8482/web-high-level-shading-language/) proposal, which evolved into [Web Shading Language](https://github.com/gpuweb/WSL). Both of these had disadvantages that made them unacceptable to various people. It’s not possible to use SPIR-V directly, largely because it has undefined behavior and other unsafe stuff. The Google and Mozilla implementations addressed this by doing a rewrite pass. Conversely, Apple’s proposal met with considerable resistance because it didn’t deal with the diversity of GPU hardware in the field. There’s a lot of ecosystem work centered around Vulkan and SPIR-V, and leveraging that will help WebGPU considerably.