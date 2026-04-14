---
tags: [source, rendering, grass, deferred, unity, tessellation, geometry-shader]
date: 2026-04-14
sources: 1
---

# Unity Deferred Grass Rendering（Steven Sell / Vertex Fragment）

[[steven-sell]] 2020 年 12 月发布的 Realms 项目支线产物：一个 Unity built-in 延迟管线下的草地着色方案，全部五个可编程着色器阶段都用上了，并把源码放在 GitHub: ssell/UnityDeferredGrass。

## 摘要

文章一开头就说它不是逐行教程而是高层走读，配套仓库有完整代码。方案从单一 mesh（地形 patch 或任意平面）开始，通过 tessellation 增密三角形；geometry shader 取每个源三角形第一顶点做原点生草 quad；vertex + fragment 处理后续变换与采样。延迟管线不支持半透明，所以用 `AlphaToMask On` + 把 `min(texture.a, cutAlpha)` 写入 `UnityStandardData.occlusion`（它在 G-Buffer diffuse 的 alpha 通道上）——`cutAlpha` 可被其它 pass 覆写以启用切割/消失效果。草的视觉参数包括：`Albedo Map`、`Base Color`/`Tip Color` 梯度、`Growth Map`（兼做高度图）、`Dimensions`（宽/高/密度）、`Wind Map` 风扰动图、`Disruption Map`（RGB A = flatten/cut/burn/grow）。三个亮点技巧：**perspective bend** 是把 quad 上方两顶点沿左/右本地轴做 shear 向相机倾倒，不是完全 billboard，避免高视角看穿空隙；**wind** 是在草根本地坐标系绕轴旋转上方顶点，方向来自 distortion map 采样、幅度来自 `_WindStrength`，超阈值时叠加 additive highlight 让风看得见；**density dropoff** 用 `_CameraTargetPos` 作中心，按距离采一张艺术家绘制的 dropoff map，近密远稀平滑过渡。互动效果（压草/割草/烧草/种草）的 shader 通路已经铺好但未完全接入游戏代码，作者明确说因为时间精力不足留给未来版本。

## 关键要点

- 延迟管线 + 草 = alpha cutout（`AlphaToMask`），没有 alpha blend 空间
- 五阶段流水线拆工明确：hull/domain 加密、geometry 生 quad、fragment 光照
- perspective bend 比纯 billboard 优雅：配合草的随机旋转产生自然的视角适应
- density dropoff 靠采样一张"距离 → 密度"曲线图，比硬编码线性衰减更可控
- disruption map 用 4 通道承载 4 种互动，让 shader 成为被贴图驱动的通用效果引擎
- 自我反思坦率：作者明确说自己没时间做成完整 tutorial、部分 feature 只写好 shader 还没游戏侧数据

## 链接到的概念

- [[deferred-grass-shader]]
- [[deferred-rendering]]
- [[fragment-shader]]
- [[alpha-compositing]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/unity-deferred-grass-rendering/
- 本地：`raw/articles/vertexfragment.com/2020-12-17_unity-deferred-grass-rendering.md`
