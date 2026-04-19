---
tags: [source, unity, urp, post-processing, underwater, caustics, flow-map]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders 2 - Underwater（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Snapshot Shaders 2* 撰写的 **Underwater** 后处理参数手册——一个屏幕空间的水下视觉效果，把 UV 波浪扭曲和 caustics 叠加在一次 Volume pass 里。

## 摘要

水下视觉由两部分构成：**UV 波浪扭曲**（画面像被水摇晃）和 **caustics**（阳光被水面折射后在水下物体上产生的亮斑）。Snapshot 2 把两者都做成 URP Volume override 的参数：

- **波浪扭曲**由一张 *Wave Flow Map* 驱动——R/G 通道编码 UV 位移的强度和方向（经典 flow map 格式）。*Wave Strength* 放大位移、*Wave Flow Tiling* 控制贴图平铺、*Wave Flow Speed* 决定贴图在屏幕上的滚动速度。
- **Caustics** 有三种模式：*Off*（不显示）、*Triplanar*——沿 XY / YZ / XZ 三个平面各采一次 caustics 纹理再按表面法线加权混合（正面朝哪个方向那张采样权重最大），消除单平面投影拉伸但 **贴图采样数 ×3**；*Light Aligned*——把 caustics 的采样坐标对齐到主光方向，成本较低。Caustics 关键参数包括 *Caustics Texture* + *Caustics Tint*（alpha = 全局强度）、**两套 Tiling/Scroll Velocity**（推荐两套数值接近但不同、滚动方向相反，两层叠加互相错位会产生丰富闪烁），以及 *Caustics Color Separation*（按 RGB 通道各偏移一次采样，产生色差感 —— 代价是**采样数又 ×3**，triplanar + color separation 就是 **×9**），以及距离衰减 *Caustics Start Fade* + *Caustics Fade Falloff*（远处 caustics 淡出避免渐远处的无效细节）。

## 关键要点

- **Flow Map 的 R/G 通道直接编码 2D 位移**——相当于给屏幕每个像素一个小箭头，是比 `sin(uv.y)` 更一般化的 UV 扭曲方式
- Triplanar caustics 采样成本的量级 warning 是真实的：1 次 → 3 次（triplanar）→ 9 次（triplanar + color separation），像素着色端会显著变慢
- **两套 caustics tiling/scroll 错位叠加**是 VFX 的经典 trick——单张纹理循环有明显重复感，两层异频叠加后周期显著拉长，视觉上变得"更像自然光斑"
- Color Separation 是 [[chromatic-aberration-post|色差]] 思路在 caustics 上的迁移——三通道错开采样位置，让亮斑边缘有彩虹感
- Start Fade + Falloff 距离衰减是**视觉优化也是性能优化**——远处 caustics 像素小到不可辨，衰减为 0 避免在 mip 层级里产生高频噪声
- Light Aligned 模式假定 caustics 方向一致（通常是太阳），适合开阔水面；Triplanar 适合室内水池等光线不定场景
- 本效果是典型的"Volume 后处理伪造三维光学现象"——真实 caustics 需 ray traced / photon mapped，这里是纯屏幕空间**贴图叠加**

## 链接到的概念

- [[underwater-post-effect]]
- [[chromatic-aberration-post]]
- [[urp-volume-post-processing]]
- [[triplanar-projection]]

## 原文

- 链接：https://danielilett.com/snapshot-shaders-2/underwater/
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-2-underwater.md`
