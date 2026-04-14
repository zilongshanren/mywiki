---
tags: [渲染, temporal, 运动矢量]
date: 2026-04-14
sources: 1
---

# Motion Vectors（运动矢量）

**屏幕空间每像素的二维位移矢量**，表示「当前帧的这个像素，上一帧在屏幕上的哪个位置」。是所有 temporal 技术——[[temporal-antialiasing|TAA]]、motion blur、temporal denoising、DLSS/FSR——的基础输入。

## 生成方式

典型做法是在顶点着色器里**算两次位置**：一次用当前帧的 MVP，一次用上一帧的 MVP。然后在像素着色器里做透视除法后相减，写入一张两通道 16-bit 浮点纹理。

```hlsl
// VS
vsOut.previousPosition = mul(PreviousMVP, worldPos);
vsOut.currentPosition  = mul(CurrentMVP, worldPos);

// PS
float2 prev = vsIn.previousPosition.xy / vsIn.previousPosition.w;
float2 curr = vsIn.currentPosition.xy  / vsIn.currentPosition.w;
float2 velocity = prev - curr;
// 转到 UV 空间，记得减去两帧的 jitter，因为 jitter 不属于真实运动
velocity = velocity * float2(0.5, -0.5) + 0.5;
velocity -= currentJitter;
velocity -= previousJitter;
```

对静态几何体——不动不变形的——可以跳过顶点那步，在全屏 pass 里用深度 buffer + 两帧的 view-projection 矩阵做 camera reprojection，效果等价。

## 替代方案

有些引擎会在每个顶点缓存一个 `previousPosition` 属性，每帧写入前一帧的结果——多 32 bit/顶点内存但省掉顶点位置的重复计算。只有在 skinning、tessellation、复杂 vertex shader 的情况下才值得这么做。

## jitter 的处理

**关键陷阱**：投影矩阵带了 TAA 的 sub-pixel jitter 时，velocity 里会混入这个 jitter。因为 jitter 不代表真实运动，必须显式减掉两帧的 jitter 偏移；否则 reprojection 会把 jitter 再放大一遍。

## 透明与 deformation

透明物体默认不写深度也不写 motion vectors——TAA 拿到的历史无法 reproject，只能被 color clamping 兜底。一些引擎让透明物体也写 blended velocity，或者对高频效果用「responsive AA」直接放弃 history。skinning、cloth、fluid 这些非刚性变形必须各自算自己的 velocity——从 skinned bone matrix 派生，或者从上一帧的 mesh 顶点 buffer 派生。

## Edge 处理：dilation

velocity 本身也是 aliased 的——它和深度、stencil 一样，在几何边界上会取到「错」的值。TAA reprojection 用 aliased velocity 反而会把边缘锯齿再引回来。解决方法是 **velocity dilation**：在 3x3 邻域里取最近深度对应的 velocity（depth dilation），或者取最大 magnitude 的 velocity。相当于把边缘的 velocity 往外扩一圈，覆盖掉因为 jitter 漂过来的「空洞」。

## 相关

- [[temporal-antialiasing]]
- [[taa-history-rectification]]
- [[mvp-transform]]
- [[coordinate-spaces]]

## Sources

- [[sources/elopezr-taa-holy-trail]]
