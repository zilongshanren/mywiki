---
tags: [渲染, msaa, 延迟渲染, 边缘检测, light-prepass, 超采样]
date: 2026-04-27
sources: 1
---

# MSAA 延迟渲染边缘检测（MSAA Deferred Edge Detection）

在[[rendering/deferred-rendering|延迟渲染]]和 Light Pre-Pass 管线中，MSAA 的最大挑战是：G-Buffer 以全分辨率存储，但光照 pass 通常在解析后的单像素粒度执行。边缘处的像素包含来自多个几何体的 MSAA 采样点，若不做区分一律按单样本着色会产生锯齿。标准解法是**先检测哪些像素跨越了几何边缘，对边缘像素做 per-sample 着色，非边缘像素维持 per-pixel 着色**。

## 基于采样差的 POINT/LINEAR 检测

Benualdo（首发于 Light Pre-Pass 论坛，Engel 2010 年整理）的方案：

对 normal buffer 同时采样两次——一次用 **POINT 滤波**（拾取 MSAA 表面的某个采样点），一次用 **LINEAR 滤波**（对该像素所有采样点的法线取均值）：

```hlsl
float3 normalPoint  = normalBuffer.SampleLevel(samplerPoint,  uv, 0).xyz;
float3 normalLinear = normalBuffer.SampleLevel(samplerLinear, uv, 0).xyz;
clip(-abs(normalLinear - normalPoint) + eps);
```

当 MSAA 采样点之间法线一致（内部像素）时，LINEAR 值近似等于 POINT 值，差值趋近零，clip 通过。当差值显著（边缘像素）时，clip 剔除当前像素，触发 per-sample 着色路径。LINEAR 值同时用于非边缘像素的光照着色，避免多一个 pass。

**深度校正**：法线相同但深度不连续同样是边缘（例如一个物体正好与背景法线平行）。深度值必须打包进同一纹理的 w 通道，或使用独立深度纹理并同样做差值检验，否则会漏检此类边缘。

## 基于体积纹理 Mipmap 的颜色边缘检测

评论者 Benualdo 另外分享了一种用于 PS3 前向渲染器的变种——用颜色缓冲做边缘检测，避免法线缓冲在前向管线中不可用的限制：

将一张小型 DXT1 体积纹理的 mip 0 设为全黑（0）、更高 mip 设为全白（1），用颜色缓冲的 `rgb` 作为 3D 纹理坐标采样两次（相邻像素）：

```hlsl
half edge1 = tex3D(volumeTex, color1.rgb);
half edge2 = tex3D(volumeTex, color2.rgb);
clip(-edge1 - edge2);   // 任一为 1 则丢弃（开启高质量路径）
```

原理：颜色变化越快（相邻像素 rgb 差距越大），硬件 mip 选择就越高，返回值越大。这把 ddx/ddy 的梯度计算转嫁给了纹理单元的 LOD 计算逻辑，比 ALU 指令更省。

## Stencil 复用模式

检测过一次的边缘信息可以写入 stencil buffer，供后续多个光源 pass 复用，避免每盏灯重新检测：

1. 渲染 Normal + Depth
2. 对全屏 quad 做边缘检测，将边缘像素 stencil 标记为 `0x01`
3. 每盏灯：先绘制光源代理体写入 `stencil = 0x02`（与 `0x01` 合并），再按 `stencil == 0x01`（仅边缘）路由到 per-sample 着色，按 `stencil == 0x02`（仅光照范围内非边缘）路由到 per-pixel 着色

这样边缘检测的纹理读取开销（4xMSAA 可能达 8 次采样）只发生一次，而非随光源数线性增长。

## 与 centroid sampling 的关系

上述方法的前提是平台支持 MSAA 表面的 linear filtering。若不支持（部分控制台），centroid sampling 是替代方案：渲染法线时启用 centroid 插值，对比有/无 centroid 的值差判断边缘，只需 1 次纹理读取，但误检率约 33%（centroid 坐标偶尔位于三角形内部时与普通插值一致）。

## 相关

- [[rendering/msaa-ssaa]] —— MSAA 基础原理
- [[rendering/deferred-rendering]] —— MSAA 在延迟管线下的整体挑战
- [[rendering/tiled-light-prepass]] —— Light Pre-Pass 变体，此技巧的原始语境
- [[rendering/sobel-edge-detection]] —— 颜色梯度边缘检测的另一路线（用于风格化描边）

## Sources

- [[sources/humus-edge-detection-trick]]
