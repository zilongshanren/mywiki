---
tags: [shader, 折射, glass, fresnel, unity, urp]
date: 2026-04-19
sources: 1
---

# 折射玻璃 Shader（URP）

**折射玻璃**的最小配方是「读背景像素 + 按表面法线偏移 UV + Fresnel 权重合成」。在内建管线里这件事用 [[unity-grabpass-blur|GrabPass]] 实现，URP 下用内置的 `_CameraOpaqueTexture` 替代。[[daniel-ilett|Daniel Ilett]] 在 *Shader Toolbox for URP* 的 Glass shader 是这个配方的参数化版本——只暴露四个核心参数，把复杂度压到极限。

## `_CameraOpaqueTexture`：URP 版的 GrabPass

URP 的 Forward Renderer 可以 opt-in `_CameraOpaqueTexture`：它会在不透明队列渲完之后把当前 color attachment 拷贝成一张纹理，透明 pass 就能读到「背景」。这比 GrabPass 的优势是：

- **一次拷贝**覆盖所有透明物体，不是每个 GrabPass 物体一次——O(1) 而非 O(N)。
- **由 SRP 显式管理**生命周期，不会每个 shader 重新声明一次。
- **缺点**：只包含 opaque，透明物体之间互相看不见（后面的透明物体不在前面的透明物体的折射里）。Shader Toolbox 因此额外提供一张自定义的 `_CameraTransparentTexture`，把到当前为止已绘制的全部物体拷进去——用 *Camera Texture Mode* 切换（默认读 opaque）。

## 折射：法线偏移 UV

最简单的折射算法就是用表面法线的 `xy` 分量偏移屏幕空间 UV，再从 camera texture 采样：

```hlsl
float2 refractUV = screenUV + normal.xy * refractStrength;
half4 behind = SAMPLE_TEXTURE2D(_CameraOpaqueTexture, sampler_..., refractUV);
```

参数暴露两个：

- **Refractive Index**：控制偏移强度。名字虽然是物理量（n = c_vacuum / c_medium），但 shader 里只是一个线性系数，不做 Snell 的 `sin` 运算——廉价的物理外观。
- **Glass Strength**：折射结果以多大权重混入最终颜色。0 时完全透明（只看背景），1 时完全透明且不显示自身 Base Color；中间值做线性混合。

值得注意 *Base Color* 仍然在公式里——玻璃本身可以带颜色（彩色玻璃），乘到折射结果上就是染色后的背景。

## Fresnel：边缘高光 + 视角相关混合

Fresnel 在玻璃里有两种经典用途：

- **边缘高光（rim light）**：掠射角下玻璃最亮。*Fresnel Power* 和 *Fresnel Color* 就是 [[fresnel-edge-highlight|Fresnel Highlight]] 那套直接搬过来。
- **正视/掠射反射权重**：真实玻璃正看时几乎全透明、掠视时更像镜子。虽然 Ilett 的 shader 没显式实现镜面反射，但 Fresnel 值确实可以作为折射 vs. 表面色的混合权重——让玻璃边缘更不透明、中心更透明。

*Use Emission* toggle 决定 Fresnel 层写到 Base Color 还是 Emission——和 [[iridescent-bubble-shader|Bubble shader]] 同一套设计。写到 Emission 就和 [[bloom-threshold-blur-composite|Bloom 后处理]]叠加成发光玻璃。

## 和 GrabPass 折射的实质差异

[[unity-grabpass-blur|Linden Reid 的毛玻璃]]用 GrabPass + 可分高斯模糊，Ilett 的 URP 版用 `_CameraOpaqueTexture`——但 Ilett 这个 shader 不做 blur。本质差别：

| 差异点 | GrabPass foggy window | URP glass (Ilett) |
|--------|----------------------|-------------------|
| 背景纹理 | 每物体一次 grab | 一次拷贝复用 |
| 模糊 | 可分高斯 | 无 |
| UV 偏移 | 基于物体 UV | 基于表面法线 xy |
| 透明物体互相看见 | 看情况 | 需切 `_CameraTransparentTexture` |

换言之，Ilett 的 Glass 是**清澈玻璃**（refraction-only），不是**毛玻璃**（refraction + blur）。要做后者需要在这个基础上再叠一层 blur——一般的路径是渲到一张 RT，做模糊再采样。

## 相关

- [[unity-grabpass-blur]] —— 内建管线的 GrabPass 实现与对比
- [[iridescent-bubble-shader]] —— 同一套 camera texture 折射机制 + 彩虹 ramp 的肥皂泡版本
- [[fresnel-edge-highlight]] —— Fresnel 作为玻璃边缘高光的通用做法
- [[bloom-threshold-blur-composite]] —— 玻璃 + bloom 的发光效果
- [[env-mapping-cubemap-shader]] —— 完整的反射需要 cubemap 采样，不止折射
- [[daniel-ilett]]

## Sources

- [[sources/danielilett-toolbox-urp-glass]]
