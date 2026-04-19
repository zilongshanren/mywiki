---
tags: [渲染, gaussian-splatting, supersplat, pwa, playcanvas, 工具]
date: 2026-04-14
sources: 4
---

# SuperSplat：开源 3DGS 编辑器与 PWA 化

**SuperSplat** 是 PlayCanvas 团队开源的 3D Gaussian Splatting 编辑与优化工具，运行在浏览器里。它解决的是 3DGS 工作流里**"训练完拿到一坨 PLY 之后怎么清洗/对齐/瘦身"**的问题：原始扫描结果里不可避免地会有背景飞点、错位的坐标、冗余的 splat，SuperSplat 让用户在几分钟内把它们收拾成一个干净、可发布的 3D 资产。作为 [[gaussian-splatting-web]] 工作流的第二站，它是整条管线里最容易被忽视但又最必要的一环——没有清洗，splat 场景的观感会差一大截。

## 2×: compute shader 带来的性能跃升

2024 年 5 月发布的 v0.17.1 把 SuperSplat 的 GPU 耗时压了一半多：bike 场景从 **32ms 降到 13.5ms**。幕后驱动力是底层 [[playcanvas-webgpu-editor|PlayCanvas Engine v1.71.0]] 对 splat 处理的整套重写——借 [[webgpu-intro|WebGPU]] 的 compute shader 把原本用 fragment shader 凑出来的排序/混合改成了原生并行任务。结果是 SuperSplat 现在可以流畅地编辑**上百万个 splat** 而不掉帧，这对实际的博物馆/文物扫描场景至关重要：随便一件展品重建出来都在几十万到几百万级。

这条升级路线揭示的模式值得记录：**3DGS 的性能瓶颈往往在"处理 splat 元数据和排序"而不在"画 splat 本身"**。只要有 compute shader 就能把这段逻辑写成真正的并行算法，而 WebGL 时代只能靠 fragment GPGPU 的 workaround 凑性能。

## PWA：安装到桌面的浏览器应用

v0.17.1 的第二大变化是 **PWA（Progressive Web App）支持**。Progressive Web App 的核心意义是让网页应用"看起来像原生应用"：可以安装到桌面/开始菜单/Dock，有自己的图标和窗口，脱离浏览器标签页的生命周期。SuperSplat 把这层壳做好后，带来两个具体的体验改进：

1. **安装后独立运行**：用户从地址栏点 "Install SuperSplat" 就能把它钉到任务栏（Windows）或 Dock（macOS），像本地 DCC 工具一样启动。
2. **PLY 文件关联**：PWA 安装时向操作系统注册了文件类型，右键 PLY 文件可以直接选 SuperSplat 打开，甚至设置成默认程序后双击 PLY 就能开编辑器。

第二条是实打实的可用性跃迁——在此之前，用户要编辑 PLY 得先打开浏览器、找到 SuperSplat 地址、上传文件，如今只要双击。这把 SuperSplat 的定位从"在线 demo"升级为"本地工具链的一环"。对 web 工具来说，PWA + 文件关联是**从"网页"变成"软件"的关键一步**。

## 启示

SuperSplat 的这次更新是一个典型的「基建升级解锁业务跃迁」案例：WebGPU compute shader 让底层有了 2×性能，再靠 PWA 让工具的使用路径和本地软件对齐，两项加起来才让 SuperSplat 真正可以用到生产场景里。对想做 web 工具链的人，这是一条很值得参考的双线升级路径：**性能线（compute）+ 交付线（PWA / 文件关联）**。

## 相关

- [[gaussian-splatting-web]] —— 整条 3DGS web 工作流
- [[playcanvas-webgpu-editor]] —— 引擎侧的 WebGPU 支持
- [[webgpu-intro]]
- [[will-eastcott]]
- [[supersplat-publish-platform]] —— SuperSplat 从编辑器走向发布平台的 2025 年三版演进

## Sources

- [[sources/playcanvas-supersplat-pwa]]
- [[sources/playcanvas-supersplat-2-0-publish]]
- [[sources/playcanvas-supersplat-2-2-video]]
- [[sources/playcanvas-supersplat-viewer-oss]]
