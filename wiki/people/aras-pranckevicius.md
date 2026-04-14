---
tags: [人物, 作者, 引擎工程师]
date: 2026-04-14
sources: 8
---

# Aras Pranckevičius

**Aras Pranckevičius** 是立陶宛图形工程师，2006-2022 年在 Unity 担任图形/渲染相关核心岗位（最长一段时间是 graphics tech lead）。离开 Unity 后转向开源项目，目前主要在 Blender 的 Video Sequence Editor（VSE）模块做性能与代码质量改进，并以「模块负责人」身份带 3-4 人小团队。

他长期维护博客 [aras-p.info](https://aras-p.info/)，写作风格务实、动手第一：哈希函数对比、点云光栅化的微观瓶颈、图像滤波的「半像素偏差」考古、Burst/SIMD 代码生成检查等等。多数文章都附带可重现的基准测试或 webgpu demo，是「先量化再下结论」的典范。

## 主要贡献

- **Unity 渲染管线**：长期参与 Unity 的渲染管线、shader 编译器、平台后端工作。
- **Blender VSE**：从 4.1 开始持续推动 VSE 的性能、滤波质量、scopes 可视化等改进；将 waveform/vectorscope 从 CPU 搬到 GPU compute shader（见 [[compute-vs-raster-points]]）。
- **基准与对比**：长年维护非加密哈希函数评测系列，并把 [[rapidhash]] 移植到 Unity Burst（见 [[non-cryptographic-hash]]）。
- **图像滤波考古**：详细复盘了 Bilinear/Bicubic 在不同软件里「同名异义」的混乱，以及 DirectX 9 时代遗留的「半 texel 偏移」问题（见 [[image-resampling-filters]]）。
- **2004 demo 考古**：把 nesnausk! 时代的《Syntonic Dentiforms》从 D3D9 + D3DX 移植到 sokol_gfx 跨后端，并对着 22 年前的过度抽象（`IAnimChannel`/`IAnimStream<T>`/traits/listeners……）做了一次 [[classitis]] 级别的大砍，216 → 49 文件、24k → 6k 行（见 [[sources/aras-syntonic-dentiforms-redux]]）。

## 相关

- [[non-cryptographic-hash]]
- [[compute-vs-raster-points]]
- [[image-resampling-filters]]
- [[rapidhash]]
- [[pcg3d-hash]]
- [[worley-voronoi-noise]]
- [[lossless-float-image-compression]]
- [[openexr-format]]
- [[meshoptimizer-vertex-codec]]
- [[classitis]]
- [[shadow-mapping-basics]]

## Sources

- [[sources/aras-rapidhash-unity-port]]
- [[sources/aras-gpu-point-rasterization]]
- [[sources/aras-blender-vse-image-filtering]]
- [[sources/aras-more-hash-function-tests]]
- [[sources/aras-voronoi-hashing-osl]]
- [[sources/aras-lossless-float-image-compression]]
- [[sources/aras-openexr-vs-tinyexr]]
- [[sources/aras-syntonic-dentiforms-redux]]
