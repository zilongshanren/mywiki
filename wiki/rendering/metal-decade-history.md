---
tags: [metal, apple, api, 历史]
date: 2026-04-19
sources: 2
---

# Metal 十年演进史（2014–2024）

Apple 2014 年在 WWDC 上宣布 Metal 时，图形 API 生态仍由 OpenGL 主导，但 DirectX 12 / Vulkan 的低开销方向已经成型。苹果选了**闭源专有 API**这条路，目的是让软硬件同步演进、摆脱外部委员会的节奏。[[warren-moore|Warren Moore]] 十周年时做的两篇回顾把十年切成**早期（2014–2019）和现代（2020–2024）**两段，既是 API 版本的时间线，也是"Apple 想用 Metal 承载哪些硬件形态"的注脚。

## 早期 2014–2019：从 OpenGL 替代品到 GPU-driven 主力

- **2014 / Metal 1.0**（iOS 8 独占）：fixed state + multi-thread command encoding 把 draw call 成本降下来；一上来带 compute shader（MSL 是 C++ 加 GPU 扩展）；缺 indirect draw / tessellation / dual-source blending
- **2015**：Metal 上 Mac，随 MetalKit（`MTKView`、纹理 / Model I/O）+ MPS（预编译 compute kernel，埋伏 ML 未来）；加 indirect dispatch / draw 追上 OpenGL 4.0
- **2016**：tessellation（**用 compute shader 代替 OpenGL 的 TCS**，灵活性 > 标准管线）；heap（资源子分配 + aliasable）；Mac 上 dual-source blending
- **2017 / Metal 2** —— GPU-driven 路线的真正起点。A11 Bionic 解锁 imageblocks + tile shader（render / compute 一个 encoder 里交错）；第一代 argument buffer；nonuniform threadgroup
- **2018**：raytracing v1（`MPSRayIntersector`）；indirect command buffer（类似 DX12 bundle）
- **2019 / Metal 2.2**（A13）：sparse heap；GPU 端 argument buffer set pipeline；**rasterization rate map + vertex amplification**——当时不起眼，后来是 Vision Pro foveated / 立体渲染的基础

## 现代 2020–2024：对齐现代 GPU，承载新硬件形态

- **2020 / Metal 2.3**（A14 + Apple Silicon 转换开始）：核心 raytracing 取代 MPS 实现；`[[visible]]` + 函数指针 + visible function table + dynamic library + incremental pipeline compilation + binary archive；`MPSGraph` 做 ML DAG；hardware counter API
- **2021 / Metal 2.4**：raytracing 加 motion（triangle keyframe / bounding box / instance transform）→ motion blur；A15 起 lossy texture compression（私有存储省 50%）；**stitched function**（`[[stitchable]]` 运行时拼 shader）
- **2022 / Metal 3**（版本号跳 3）：argument buffer 3.0——`gpuResourceID` / `gpuAddress` 直接写 buffer 不再要 encoder；**mesh shader**；**MetalFX**（spatial + temporal upscaling）；`MTLIOCommandQueue` 资源加载 API（直接解压进 buffer/texture）
- **2023**：Vision Pro 首秀，Metal 作为 visionOS 底层；raytracing 加 curve primitive + multi-level instancing；MPSGraph 加序列化 / CoreML / ONNX 转换
- **2024 / Metal 3.2**：RealityKit `LowLevelTexture` / `LowLevelMesh`；Compositor Services passthrough；**`MTLAllocation` 协议 + residency set**（Metal 4 里升级为唯一方式）；`mathMode` 替代 `fastMathEnabled`；PVRTC 标 deprecated（让位 ASTC + BC(n) + UASTC HDR）

## 贯穿主线

- **从 driver overhead 降 draw call 起步** → 演进到 GPU-driven rendering → 现在是 bindless + concurrent
- **Apple Silicon 统一 GPU 架构**（iOS / iPadOS / macOS / visionOS 同一套）让 Metal 的设计有长期一致性
- **抛弃早期实验**：argument buffer v1、MPSRayIntersector 都被后代 feature 取代——[[metal-4-api-redesign|Metal 4]] 是又一次大清洗（特别是显式 residency + command allocator）
- 一些"埋伏" feature 要等硬件 / 新产品才显出设计意图（rasterization rate map → foveated rendering、vertex amplification → 立体渲染）

## 相关

- [[metal-api-overview]]
- [[metal-4-api-redesign]]
- [[hdr-video-edr-metal]]
- [[slug-gpu-glyph-rendering]]
- [[meshlets-and-mesh-shaders]]
- [[bindless-rendering]]
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-decade-early-years]]
- [[sources/metalbyexample-decade-modern-era]]
