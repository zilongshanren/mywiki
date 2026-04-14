---
tags: [渲染, 可见性, 剔除, z-buffer]
date: 2026-04-14
sources: 1
---

# Hierarchical Z-Buffer（HZB）

**HZB** 是 Greene、Kass、Miller 在 1993 年 SIGGRAPH 提出的数据结构：从一张深度图出发建一个类似 mipmap 的金字塔，但每层用 **`max` 降采样**（2×2 texel 取最远值），而不是普通 mipmap 的加权平均。越往上越保守：上层的一个 texel 记录了底下一整片区域里最远的那个深度。

它是现代 [[occlusion-culling|遮挡剔除]] 的基础——能把「屏幕空间上一个矩形是否完全被现有场景挡住」的问题压到 **O(1) 次纹理采样**。

## 查询流程

给一个物体：

1. 取它的 world-space AABB，顶点着色器里投影到屏幕，得到屏幕矩形 `sbox` 和最小（最近）深度 `min_z`。
2. 根据屏幕矩形长宽选一个**足够粗**的 HZB mip 层 level，使这个矩形最多覆盖 2×2 或 4×4 个 texel：
   ```hlsl
   float2 size = sbox_vp.zw - sbox_vp.xy;
   float level = ceil(log2(max(size.x, size.y)));
   ```
3. 像素着色器对 4 个（或 4×4）corner texel 做 `max`，得到**屏幕矩形下整个场景的最大深度**。
4. 如果 `min_z > max_z`，物体完全在场景后面 ⇒ 被遮挡。否则保守判可见。

因为是 max 降采样，第 3 步从粗层读一个值就保守地覆盖了整片区域；如果采更细的层会更精确但不会更保守。

## 构建

逐层做 quad pass，从上一层读 2×2 texel、输出 max 到下一层：

```hlsl
out = max(max(src[0], src[1]), max(src[2], src[3]));
```

Conviction 里的分辨率是 **512×256**（四分之一主相机分辨率），典型预算约 0.10 ms 在 Xbox 360 上完成 mip chain 构建。为了避免 non-power-of-two 的麻烦通常强制 POT 分辨率；非 POT 时要小心「最右 / 最下」一列 texel 要额外 `max` 一次以防漏测。

## 为什么 max 降采样

mipmap 的加权平均是在**重建连续信号**，想让远处的 texel 平均地代表一小块。HZB 的目的正相反：**保守地代表一小块里最难穿过的那个**。只有取最大值（在「深度越大越远」约定下）才能保证「如果 HZB 说你过得去，你原 z-buffer 也肯定过得去」。这是一种保守近似，和 AABB 对几何体的保守近似是同构思路。

## 最小 HZB 的双面

对称地，如果把降采样换成 `min`，就得到一个「这一片区域里最近的深度是多少」的金字塔——可以用来做**保守的 early-Z** / tile culling / 光照 / AO 预处理。现代引擎往往同时维护 min-max 金字塔：max 用来遮挡剔除，min 用来 light culling / SSAO / [[temporal-antialiasing|TAA]] 的 reprojection 验证。

## 和硬件 Hi-Z 的区别

GPU 硬件里的 **Hi-Z** 是固定功能路径上的加速结构，外部着色器一般读不到。HZB 是**应用层**自己构建的 mip 金字塔，完全可控，能在任意分辨率、任意自定义输入上用。

## 应用面

除了 [[occlusion-culling|遮挡剔除]]，HZB 还可以：

- 做 **contribution culling / LOD 选择**：屏幕 bounds 是 bypass 产物
- 做 **shadow caster culling**：用 light-space HZB 剔 caster、再用主相机 HZB 剔 caster 的 shaft bounds
- 做 **SSAO / SSR 采样预处理**：跳过明显没有近处表面的区域
- 做 **GPU-driven culling**：UE5 Nanite / Frostbite 等把整条 HZB build + query 全搬到 compute shader，CPU 端只发一个 indirect draw

## 相关

- [[occlusion-culling]]
- [[culling]]
- [[z-buffer]]
- [[reversed-z]] — 深度约定会影响 max / min 的含义
- [[sparse-shadows-cone-tracing]] —— Karis 2012 列出的屏幕空间 trace 友好结构之一（min/max depth mipmap）
- [[gpu-based-occlusion-culling]] —— HZB 在 GPU-driven instance culling 里的典型用法

## Sources

- [[sources/selfshadow-practical-visibility]]
