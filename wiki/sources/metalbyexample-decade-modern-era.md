---
tags: [source, metal, apple, 历史, 空间计算, raytracing]
date: 2026-04-19
sources: 1
---

# A Decade of Metal: The Modern Era (2020–Today)（Warren Moore / Metal by Example）

[[warren-moore|Warren Moore]] 发表于 2024 年 9 月 13 日，Metal 十周年的下半段：2020–2024 的几次重量级迭代——核心 raytracing、MetalFX upscaler、mesh shader、资源加载 API、visionOS、residency set。

## 摘要

- **2020 / Metal 2.3**（A14 + Apple M1 开启 Mac 转 Apple Silicon）：**核心 raytracing**（取代 MPSRayIntersector）；新 function 修饰 `[[visible]]` 让非 entry point 函数也能被 API 拿到，配合函数指针做更灵活 pipeline；visible function table / dynamic library / incremental pipeline compilation / binary archive；`MPSGraph`（ML DAG）；hardware counter API
- **2021 / Metal 2.4**（iOS 15）：增量版本。raytracing 加 instance 动画、triangle motion key frame、bounding box motion → 运动模糊；A15 起 lossy texture compression（私有存储最多省 50%）；stitched function（`[[stitchable]]` 让运行时拼接多个 shader 函数）
- **2022 / Metal 3**（版本号跳到 3）：argument buffer 3.0——资源用 `gpuResourceID` / `gpuAddress` 直接写进 buffer 不再要 encoder；mesh shader（object/mesh 两段，做 meshlet culling / 细节几何生成）；**MetalFX**（spatial + temporal upscaling）；`MTLIOCommandQueue` 资源加载 API（文件直接解压进 buffer / texture，ZLib/LZBITMAP/LZFSE + custom codec）
- **2023 / Vision Pro 年**：Metal 作为 visionOS 的底层；vertex amplification / layered rendering / rasterization rate map 终于显出设计意图——foveated / 立体渲染；raytracing 加 curve primitive（头发 / 毛皮 / 植被），multi-level instancing 支撑超大场景；MPSGraph 加序列化 / CoreML ONNX 导入
- **2024 / Metal 3.2**：RealityKit 加"低层" API（`LowLevelTexture` / `LowLevelMesh` 让引擎与自定义 Metal 代码高效互操作）；Compositor Services 加 passthrough immersive 渲染 API（AR 游戏空间打开）；资源统一协议 `MTLAllocation`，配套 **residency set**（一次 call 把一组资源标记 resident，是 Metal 4 里上升为唯一方式）；`mathMode` 属性替代 `fastMathEnabled`；PVRTC 正式标 deprecated（让位 ASTC + BC(n) + UASTC HDR）

这篇文章的主线是：**Metal 从 2020 年之后彻底对齐现代 GPU 范式**——核心 raytracing、mesh shader、GPU-driven argument buffer、资源加载命令队列、residency set——同时承担 Apple 新形态硬件（Apple Silicon Mac、Vision Pro）底层渲染基石的角色。

## 关键要点

- Metal 2.3 用核心 raytracing 取代 MPS-based 版本——visible function + 函数指针解开复杂 pipeline
- Metal 3 的 argument buffer 改走 `gpuResourceID` / `gpuAddress`，真正 bindless
- Mesh shader 接替 tessellation / vertex amplification 作为现代几何路线
- `MTLIOCommandQueue` + 内置压缩格式支撑资源流式加载（配合 sparse texture）
- Vision Pro 的 foveated / 立体渲染建立在 2019 的 rasterization rate map + vertex amplification 上
- Residency set 是 3.2 引入、Metal 4 后成为标记资源常驻**唯一**方式——显式内存管理加重
- 2024 年 RealityKit 低层 API 打破了"引擎黑盒"——自定义 Metal 代码可直接参与场景
- PVRTC 落日，ASTC + BC(n) + Binomial UASTC HDR 接棒

## 链接到的概念

- [[metal-decade-history]]
- [[metal-api-overview]]
- [[metal-4-api-redesign]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/a-decade-of-metal-the-modern-era/
- 本地：`raw/articles/metalbyexample.com/2024-09-13_a-decade-of-metal-the-modern-era-2020-today.md`
