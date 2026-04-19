---
tags: [渲染, gaussian-splatting, 3dgs, 点云, web, playcanvas, supersplat, pwa]
date: 2026-04-14
sources: 5
---

# 3D 高斯溅射在 Web 上的工作流

**3D Gaussian Splatting（3DGS）** 是近年兴起的一种新型场景表达：用一堆各向异性的三维高斯分布替代网格，通过 rasterizer 把每个高斯"溅射"到屏幕空间做 alpha 合成，从而以极快的速度渲染出近乎照片级的真实场景。作为一种同时面向**扫描重建**与**实时渲染**的表示，它天然适合从手机拍一圈就得到可交互 3D 场景的消费级应用。而一旦要把 3DGS 塞进浏览器里跑，就必须解决三件事：**数据格式与压缩**、**GPU 渲染管线**、**编辑器/工具链**。PlayCanvas 团队 2024 年中前后在这三条线上同时发力，把整个 web 3DGS 流程串了起来——这篇条目把他们的工作拼成一个整体工作流。

## 数据：PLY 与压缩 PLY

原始 3DGS 训练输出一般是 **PLY** 格式：每个 splat 带位置、法向（可选）、球谐系数（通常 48 个浮点）、尺度、旋转四元数、不透明度——单个场景动辄上百万条记录、几十到上百 MB。直接丢进浏览器既下载慢、又吃显存。PlayCanvas 因此设计了一套**压缩 PLY 格式**：把球谐和尺度量化到低比特，大幅减小体积，同时保留足够的视觉质量。案例里 V&A 博物馆扫描的雕像压缩后只有 **1.56MB**，对于 web 场景已经完全可接受。压缩 PLY 是跑通 web 3DGS 工作流的**基础条件**——没有它，前端连下载都扛不住。

## 工具：SuperSplat 编辑器

[[supersplat-pwa]] 是 PlayCanvas 开源的 3DGS 编辑/优化工具，运行在浏览器里，支持把原始 PLY 拖进来做**背景裁剪、对齐原点、批量编辑 splat、导出压缩 PLY**。它本质是一个"3DGS 版的 Photoshop + 轻量 DCC"，是扫描数据进入渲染管线前的清洗工位。v0.17.1 之后 SuperSplat 靠 [[webgpu-intro|WebGPU]] 的 compute 能力与 [[playcanvas-webgpu-editor|PlayCanvas v1.71]] 引擎的 splat 处理改写，把 bike 场景的 GPU 耗时从 32ms 降到 13.5ms——**GPU 侧快了超过 2 倍**。同时加入 **PWA 支持**：用户可以把 SuperSplat "安装"到桌面和任务栏/Dock，把 PLY 文件关联给它，实现双击 PLY 直接打开的本地原生体验。这两条改动让 SuperSplat 摆脱了"演示 demo"的定位，成为真正可以日常用的扫描后处理工具。

## 引擎与编辑器：PlayCanvas 集成

第三块拼图是 PlayCanvas Editor 2024 年 6 月宣布的 **Gaussian Splat 一等公民支持**。SuperSplat 导出的压缩 PLY 可以像普通资产一样拖进 Editor 的 Asset Panel，再拖到场景里就变成一个可变换、可脚本化的实体。更重要的是，Editor 允许**自定义 splat 的渲染 shader 代码**——这意味着 splat 可以像普通 mesh 一样参与动画、过渡、bloom 等后处理。文章示范的"雕像虚拟展厅"里，多尊雕像用淡入淡出切换、单个 splat 被 shader 随时间重定位重上色、全屏 bloom 再叠一层——这在 NeRF/3DGS 早期工具链里完全做不到：传统 splat viewer 往往只能"显示"，不能"合成到游戏世界里"。

## 工作流全貌

把三块拼起来，就得到 PlayCanvas 给 web 3DGS 应用开发者的**标准工作流**：

1. **采集**：用智能手机围着目标拍一圈，上传到任意 3DGS 训练服务得到原始 PLY。
2. **清洗**：在 [[supersplat-pwa|SuperSplat]] 里隔离前景、对齐坐标、导出压缩 PLY。
3. **集成**：把压缩 PLY 拖进 PlayCanvas Editor，加环境贴图、轨道相机脚本、UI、音效、物理。
4. **合成**：编辑 splat shader 做动画/过渡/变色，叠 bloom 等后处理。
5. **发布**：一键生成 WebGL/WebGPU 应用链接，手机电脑都能跑。

整条链路的意义在于：3DGS 从「研究输出的 PLY」变成了「可以像任何 3D 资产一样被编辑/组合/发布的 web 内容」。它对商品展示（家具、服饰、汽车、电子产品）、博物馆教育、文旅、房地产等垂直场景特别友好——那些「真实感比建模成本更重要」的业务线，现在只要一个手机加一个浏览器就能跑完整个管线。

## 注意事项与待填的坑

- **球谐 LOD**：高阶球谐对视觉质量有贡献但也是压缩后最大的成分，具体量化策略与感知质量的 trade-off 文章未详细展开。
- **WebGPU 依赖**：SuperSplat 的 2× 加速强依赖引擎的 splat 处理重写和 compute shader；纯 WebGL 回退下的性能上限要差一截。
- **渲染正确性**：splat 做 alpha 合成时的排序/深度可见性在动画、遮挡、透明物体叠加时仍是活跃的研究议题。

## 相关

- [[webgpu-intro]] —— compute shader 与显式资源绑定是 splat 加速的基础
- [[playcanvas-webgpu-editor]] —— PlayCanvas Editor 里打开 WebGPU beta
- [[will-eastcott]] —— PlayCanvas 联合创始人，三篇文章的作者
- [[compute-vs-raster-points]] —— 点类原语用 compute vs raster 渲染的比较
- [[alpha-compositing]]
- [[supersplat-publish-platform]] —— 编辑完之后的发布、视频、embed、WebXR、viewer 开源整套基础设施

## Sources

- [[sources/playcanvas-supersplat-pwa]]
- [[sources/playcanvas-editor-gaussian-splat]]
- [[sources/playcanvas-supersplat-2-0-publish]]
- [[sources/playcanvas-supersplat-2-2-video]]
- [[sources/playcanvas-supersplat-viewer-oss]]
