---
tags: [source, unity, shadergraph, ddx-ddy, emission, 游戏复刻]
date: 2026-04-14
sources: 1
---

# Pokémon's Terastallize Effect in Shader Graph（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 4 月的 Shader Graph 教程，复刻《Pokémon 朱/紫》的 **Terastallize**（太晶化）的晶体外壳效果。作者选了一只加拿大鹅 mesh 作为测试 model（"until Gen 10 is based on Canada"）。

## 摘要

作者承认没看过 Game Freak 的实现，整个复刻是纯粹凭肉眼观察倒推的：底层 Pokémon mesh 还在、外壳有 emissive Fresnel 光晕、外壳是**棱面化**的（不是原来的光滑面）、不同棱面**随机高亮反射**。实现建在 URP Lit 模板上，分四块：(1) **Base Color + Metallic + Smoothness 底层**——和普通 Lit shader 一样；(2) **Fresnel 边缘光**——`Fresnel Effect` 节点 × HDR `Fresnel Color`；(3) **flat-shaded 法线重建**——关键 trick，用 `DDX(WorldPos)` 和 `DDY(WorldPos)` 得到沿面的两个切向量，叉积（`cross(DDY, DDX)`——**顺序不能反**）得到法线，由于同一个三角形每个像素 world position 的梯度相同，整个三角形得到同一个法线；(4) **三角形随机反射**——因为 Shader Graph 没有 `Primitive ID` 节点，作者写了一个 Unity 插件把每个三角形在 UV0 空间覆盖的像素填成同一个随机灰度值生成一张贴图（必须关 mipmap / 关压缩 / Point 过滤 / 高分辨率），采样后用三次 `Random Range`（偏移 `0 / 3.14 / 96.07`）生成随机向量，和 `Camera.Direction` 做点乘，加时间动画，过 `Smoothstep` 阈值，最后乘 HSV 随机色，累加到 Fresnel 结果，塞进 Emission。

## 关键要点

- **DDX/DDY 叉积法**是 shader 端重建 flat normal 的标准套路：`cross(DDY(WorldPos), DDX(WorldPos))` → `Normalize` → Normal 输出。叉积顺序弄反法线朝内。
- GPU 是 **2×2 pixel quad** 同步执行，所以 `DDX`/`DDY` 就是当前像素和 quad 内邻居像素的差——对平坦面来说每个像素得到的结果都一样。代价远小于修改 mesh import 或 artist 手动标 flat。
- Shader Graph **没有 Primitive ID / Triangle ID 节点**——有 `Vertex ID` 和 `Instance ID`，但没有 primitive 级别。代码 shader 里可以用 `SV_PrimitiveID`。作者的 workaround 是烘一张"每三角形一个随机灰度"的贴图。
- 这张随机贴图必须 **关 mipmap、关压缩、Point 过滤、高分辨率**（作者用了 8192²），否则任何平滑都会把三角形边界变模糊。分辨率严重耦合 mesh 三角数，这是工作流代价。
- 一个灰度值生成随机 `Vector3` 的技巧：用三次 `Random Range`（加不同偏移）+ `Normalize`；偏移值 `3.14 / 96.07` 是作者随手挑的魔法数。
- HSV → RGB 着色技巧：把随机向量的第一个分量作为 hue，saturation 和 value 都硬编 1，`Colorspace Conversion` 节点转回 RGB。
- 反射阈值用 `Vector2 Reflection Thresholds` 配 `Smoothstep`——下限之下全黑、上限之上全亮、中间平滑过渡，控制屏幕上亮三角形的数量密度。
- 相机静止时避免反射冻结：加 `Cycle Speed * Time` 项，过 `sin(· * PI)` + `Remap` 到 [0, 1]。
- 最终结果全塞进 Emission（要 HDR + Bloom 后处理配合），基础 Lit 走 Base Color/Metallic/Smoothness 通道独立渲染，两条通路自然叠加。

## 链接到的概念

- [[pokemon-terastallize-shader]]
- [[hlsl-derivation-correctness]]
- [[divergent-gradient-in-branches]]
- [[shader-graph-lighting-primer]]
- [[classic-shader-noise]]

## 原文

- 链接：<https://danielilett.com/2024-04-10-tut7-10-terastal-effect/>
- 本地：`raw/articles/danielilett.com/2024-04-10_pokemon-s-terastallize-effect-in-shader-graph.md`
