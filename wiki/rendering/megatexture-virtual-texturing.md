---
tags: [渲染, 纹理, 虚拟纹理, streaming, id-tech, doom-2016]
date: 2026-04-27
sources: 1
---

# Mega-Texture / Virtual Texturing（虚拟纹理）

Mega-Texture（又称 Virtual Texturing，VT）是一种让 GPU 使用远超显存容量的纹理数据集的技术。核心思想是：只在显存中保留当前帧实际可见的纹理区域（tiles），其余数据留在磁盘或主内存，按需流式加载。

该技术最初由 id Software 的 John Carmack 在 id Tech 5（RAGE）中引入，DOOM 2016（id Tech 6）中进一步完善。

## 工作原理

显存中分配若干张巨大的物理纹理（DOOM 2016 中为 16k × 8k），每张由 128 × 128 像素的小 tile 拼接而成。场景中的几何体引用"虚拟纹理"，虚拟纹理的坐标在着色时被重新映射到物理 tile 的位置。

渲染流程包含一个**反馈机制**：在前向渲染 pass 中同时输出一个低分辨率的"feedback buffer"（DOOM 中为 160 × 120），记录每个像素所需的虚拟纹理地址和 mipmap 级别。CPU 读取这张 feedback buffer，确定哪些 tile 尚未加载，发起流式请求。下帧开始时通过 `vkCmdCopyBufferToImage`（或 DX 对应 API）将新 tile 数据上传到物理纹理中。

这一系统是**被动反应式**的：引擎先渲染、后发现缺失、再加载，因此存在 1-2 帧的 tile 缺失窗口，缺失时降级使用低分辨率 mipmap 填充。

## 优势与局限

优势在于理论上可实现无限多的不重复纹理，整个世界可覆盖以唯一纹理，无需手工平铺；适合大型开放世界或逐场景唯一纹理的风格。

局限在于：流式延迟导致偶发 texture pop-in；feedback buffer 读回需要跨 GPU/CPU 同步；mipmap 边界的各向异性过滤在 tile 边缘需要特殊处理（border texels）；实现复杂度高。

## 与普通纹理流式的区别

传统纹理流式以整张贴图为单位加载/卸载，Mega-Texture 粒度更细（tile 级别），且将所有纹理合并为少数几张物理纹理，减少了 GPU 纹理切换和 sampler 状态变更。

## Sources

- [[sources/adrian-doom-2016-graphics]]
