---
tags: [渲染, gaussian-splatting, 压缩, webp, 球谐, morton-order, 3dgs]
date: 2026-04-19
sources: 2
---

# SOG / SOGS：3DGS 的"WebP"级压缩格式

**3D Gaussian Splatting 的爆炸性体积**是把它塞进 web 和移动端的核心瓶颈——一个典型高质量场景的原始 PLY 动辄 1GB、包含几百万个 Gaussian，每个点要存位置（XYZ）、尺度（3 个值）、四元数旋转（4 个值）、不透明度、基础色 RGB，以及一大串 view-dependent 的**球谐系数**（通常 45+ 个浮点，能占到总文件的 75%）。把这些都存成高精度 float 就是这么重。PlayCanvas 在 2025 年走了两步，拿出 3DGS 压缩格式 **SOGS → SOG** 这条迭代路径：压缩比从 ~20× 提升到 ~23×（1GB → 42MB，~95% 缩减），并把它开源，称自己是"3DGS 的 WebP"。

## SOGS：把 3DGS 当图片压

SOGS（**Self-Organizing Gaussians**）由 Fraunhofer HHI 的 Wieland Morgenstern 提出。它的核心观察是：**压缩平滑、有序的数据远比压缩噪声高效**——一张按像素排好序的图片 JPEG 后能比随机噪声图小 9×。那么如果 Gaussian 的属性可以被"排序"得像图片一样平滑，就可以直接套用高度优化的 2D 图像编码器。

SOGS 的三步：

1. **Grid reorganization**——把所有 Gaussian 的每个属性分别摊平成一张 2D 图。有 59 个属性就得到 59 张"属性图"。直接看它们是随机噪声。
2. **Self-organizing sort（PLAS 算法）**——用 **Parallel Linear Assignment Sorting** 重排这些 Gaussian 在 2D 网格上的位置，让属性相近的 Gaussian（主要是位置、尺度、基础色）在网格里也成为邻居。以这三个主属性为排序键时，次要属性（opacity、旋转、SH 系数）也大概率跟着变平滑——这就是"co-sorting"。
3. **WebP 编码**——把每张已经平滑的属性图交给 **WebP**。浏览器原生支持、解码飞快。

PlayCanvas Engine 2.7.5（2025-05）首先把 SOGS 作为引擎端一等公民引入：Christoph Schindelar 的教堂场景从 1GB PLY 压到 55MB，约 **20× 减小**。

## SOG：把 SOGS 再拆两步

SOG（**Spatially Ordered Gaussians**）是 2025-09 PlayCanvas 推出的迭代版，与 SOGS 共享"属性图 + WebP"的框架，但改进了四处：

- **Morton order 存储**：splat 数据按 Z-order 曲线铺排，加载时**不需要再做一次排序预处理**——数据本身就是 GPU-ready 的。"faster to load"。
- **单文件打包**：引入 `.sog` 格式（ZIP 壳，里面装 `meta.json` + 多张 `.webp`），分发一个文件即可；也可以选择不打包、输出零散 `.json` + `.webp`（但 Editor 只认打包版）。
- **压缩端从 CUDA 换到 WebGPU**：SOGS 的压缩流水线依赖 CUDA，门槛高；SOG 只需 WebGPU 就能跑，compute 在哪个平台都行。
- **精度更高**：同样比特预算下最小化压缩 artifact，把精度花在更值钱的属性分量上。

结果：同一个 4M Gaussian 的 skate park 场景，SOG 版 42MB，原始 PLY 1GB（**~95% 压缩**）；比 Compressed PLY 进一步缩 2-3×。

## 为什么"WebP of Gaussian Splatting"

把 SOG 跟传统 3DGS 压缩路线对比，它的定位像 WebP 对 JPEG：

- **借图像编码的车**：SOG 的最终容器就是 WebP。任何支持 WebP 的浏览器都可以直接解码，不用写定制解码器——这是它"简单解码"的核心理由。
- **把排序作为压缩的一级构件**：传统方案是量化每个 splat 独立属性或做 codebook；SOG 是在空间上把 Gaussian 先排成有序网格，再让通用图像编码器去吃这份有序性。
- **开源规范**：SOG 的规范文档、SplatTransform 的参考写入实现、PlayCanvas Engine 的参考读取/渲染实现都是 MIT 开源的。目的是让其他引擎和工具商也能接入、形成事实标准。

## 与 3DGS 工作流的集成

SOG 已经被做成 3DGS 工具链的各处默认选项：

- **生成**：[[splat-transform-cli|SplatTransform]] 一条命令：`splat-transform input.ply output.sog`。
- **引擎**：PlayCanvas Engine 2.11.0+ 原生支持；[[playcanvas-react-declarative|PlayCanvas React]]、PlayCanvas Web Components 同步更新。
- **编辑器**：PlayCanvas Editor 把 `.sog` 作为一等资产（`.json` + `.webp` 散包不支持）；拖进场景自动生成 `GSplatComponent`。
- **SuperSplat**：[[supersplat-publish-platform|SuperSplat]] 默认用 SOG 压缩发布，比 Compressed PLY 小 2-3×。
- **下游**：Reflct 切到 SOG 后包体减半（3SH vs 2SH 一比），关键资源显存用量降 95%+；Voxelo 的 SOG 文件大小只有原先"已压缩"格式的 1/3，相对原始 AI 重建 PLY 减 95%+。

## 注意事项

- **不一定是最优方案**：SOG 偏"通用"且易解码，但特定场景下（如超稀疏 / 动态 splat）可能有更针对性的压缩方案。
- **Unbundled 变体兼容性**：散包 `.json` + `.webp` 不被 PlayCanvas Editor 支持，只能用 `.sog`，这是个小的部署陷阱。
- **精度与感知质量的 trade-off**：SOG 相比 SOGS 在同比特下精度更高，但文章给的评估是"compression artifacts 更少"，没有给 PSNR/SSIM 等量化指标。

## 相关

- [[gaussian-splatting-web]] —— Web 3DGS 的完整工作流
- [[supersplat-publish-platform]] —— 下游编辑/发布平台
- [[splat-transform-cli]] —— 生成 SOG 的 CLI
- [[compute-vs-raster-points]]
- [[webgpu-intro]] —— SOG 的压缩端依赖 WebGPU
- [[will-eastcott]]

## Sources

- [[sources/playcanvas-sogs-20x-compression]]
- [[sources/playcanvas-sog-opensource]]
