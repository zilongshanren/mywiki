---
tags: [渲染, 反走样, 综述, deferred-rendering]
date: 2026-04-19
sources: 1
---

# 2011 年抗锯齿方案分类（Supnik 综述）

Ben Supnik 2011 年 4 月写的一篇「AA 菜单」，把当时（延迟渲染刚成为 AAA 主流、MSAA 在 G-Buffer 上失灵、MLAA/FXAA 刚落地）能用的反走样方案按**决定权从哪一层得到**排成五档。这份分类不是学术正交分解，而是工程师在做引擎选型时实际要先问的问题：我画的是 forward 还是 deferred？我有 G-Buffer 可复用吗？我能接受后处理盲猜边缘吗？

## Supnik 的五档

### 1. Universal —— 任何管线都能用

**[[msaa-ssaa|SSAA]]**：最老也最暴力，在更高分辨率下渲染再下采样。它同时给 [[aliasing|几何走样]]、alpha test 和纹理各向异性都加 buff——代价是 fill rate 至少 4×。

### 2. Hardware FSAA —— 驱动给、你不管

**[[msaa-ssaa|MSAA]]**：帧缓冲 N× coverage，pixel shader 只在 1× 跑一次；省 shader 开销但仍吃带宽。**shader 内部的走样（alpha cutout、高频高光）不会被 MSAA 修复**，因为 shader 没多跑。MSAA 在[[deferred-rendering|延迟渲染]]下不能用——光照决策在 resolve 之后做。

**CSAA（NVIDIA）**：shader 1×、framebuffer 4×、光栅化 16×，在 MSAA 基础上进一步细化 coverage 信号，中间混合色更细。只是一个 NVIDIA 独家增强项。

### 3. 2D —— 不要 Z-buffer 的做法

**OpenGL antialiased primitives**：规范没强制，现代硬件不支持，等于不能用。

**Texture AA**：画带一圈透明像素的贴图四边形，靠双线性插值在屏上自然得到 1 像素的软边。必须走 alpha blending，不能 alpha test。X-Plane 的仪表 UI 大量用这个——便宜、最高画质，但跟 Z buffer 不兼容，不能事后改造。

### 4. Post-process —— 只看最终图的滤镜

**MLAA / FXAA**：分析输出图找阶梯状 pattern 再模糊掉。不依赖任何几何信息，**插在渲染末端即可**。驱动厂（ATI）甚至把 MLAA 做成全局开关，因为 deferred 流行后 MSAA 驱动按钮卖不动了——厂商要把 GPU cycle 的销售点重新找回来。MLAA 放在驱动层的代价：**应用层无法控制开启时机，2D UI 会被误模糊**。Supnik 承认他分不清 MLAA 和 FXAA 的实现差异，读者在评论里补充：Intel 原始 MLAA 是慢 CPU 版；Jimenez 的 GPU MLAA、Sony SPU 版、AMD 驱动版各不相同。

**TAA**：把「更多样本」的维度从空间换到时间——相机每帧亚像素抖动，当前帧和上一帧混合。当相机快速运动时需要禁用混合（否则鬼影）。Supnik 把它列在 post-process 档，对后来 TAA 发展成最主流 AA 方案是一个早期信号。

### 5. Deferred-only —— 吃 G-Buffer 的方案

**Edge detection + blur**：用 G-Buffer 的 depth/normal 不连续处当边，对这些像素做窄带模糊。GPU Gems 2 的老路子，**最便宜**。

**[[subpixel-reconstruction-antialiasing|SRAA]]**：Chajdas / McGuire / Luebke 同年在 I3D 发的新方案——MSAA 只做 depth+normal G-Buffer，着色仍 1×，用 bilateral kernel 把几何边重建回来。

## 分类背后的判断轴

- **得到 coverage 信息的路径**：rasterizer（MSAA/CSAA） vs. 高分辨率几何 buffer（SRAA） vs. 颜色图反推（MLAA/FXAA） vs. 时间维度（TAA）。
- **对 alpha 的处理**：SSAA 全面覆盖；MSAA 完全放弃；Texture AA 反而最干净。
- **是否吃 Z buffer**：Texture AA 不行；其余都可。
- **是否要求 G-Buffer**：SRAA / edge-blur 要；其余不要。
- **驱动 vs 应用控制**：MLAA 给驱动的代价是 UI 误伤——一个被忽视的工程细节，后来 DLSS/FSR 的 UI mask 机制就是在还这笔债。

## 时代背景

这篇写在 MLAA/FXAA 刚刚铺开、SRAA 论文刚发、TAA 还没成主流之前的窗口。Supnik 列完之后承认自己没深究 MLAA vs FXAA 差异——后来的答案是：**形态学/SDF 风格的后处理 AA 是一个松散的家族**（MLAA / FXAA / SMAA / DLAA / CMAA），差异在边缘检测和重建 kernel 细节，但共享同一个基本假设「颜色图本身就是信息足够」。真正从这一代胜出的是 [[temporal-antialiasing|TAA]]，因为它引入了一个外源信息通道（历史帧），而这份通道的信息带宽远超纯色图像。

## 相关
- [[aliasing]]
- [[msaa-ssaa]]
- [[subpixel-reconstruction-antialiasing]]
- [[analytical-antialiasing]]
- [[temporal-antialiasing]]
- [[fwidth-derivative-antialiasing]]
- [[deferred-rendering]]
- [[ben-supnik]]
- [[ogssaa-fxaa-non-square]] —— 2012-10 Supnik 把 SSAA（Universal 档）与 FXAA（Post 档）在 X-Plane 拼起来：非方形竖向偏置 + FXAA 跑在 SSAA 空间
- [[gradient-based-post-aa]] —— Pesce 2011 给出的梯度驱动 post-AA 配方，属 Post-process 档中「纯本地滤镜」子类

## Sources

- [[sources/supnik-aa-techniques-survey]]
