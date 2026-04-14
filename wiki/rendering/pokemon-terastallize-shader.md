---
tags: [shader, shadergraph, ddx-ddy, 法线重建, fresnel, emission, 游戏复刻]
date: 2026-04-14
sources: 1
---

# Pokémon 太晶化 Shader：DDX/DDY 法线重建 + 三角形随机反射

[[daniel-ilett|Daniel Ilett]] 2024 年的 Shader Graph 系列用《Pokémon 朱/紫》的 **Terastallize** 作为案例，把一个看起来很花哨的效果拆成三个技术独立的层：**基础 Lit 渲染 + Fresnel 边缘光 + 平面化面 + 三角形随机反射**。拆下来之后每一层都是可以独立复用的技术，尤其 DDX/DDY 的法线重建和"用贴图给每个三角形一个随机值"两个 trick 值得单独记下来。

## 思路：把观察到的效果翻译成三个可独立实现的层

在游戏里 Terastallize 看起来同时发生了几件事：Pokémon 的**基础形状还在**、外壳有**发光边缘**、外壳表面是**棱面状**而不是原来的光滑面、棱面在相机移动时**随机高亮**。Ilett 的推断：

- 基础形状 → 用普通 [[shader-graph-lighting-primer|Lit shader]] 画底层。
- 发光边缘 → `Fresnel Effect` 节点 × HDR Emission Color。
- 棱面外观 → 不改 mesh，在 shader 里**重建 flat-shaded 法线**。
- 随机高亮 → 给每个三角形一个随机向量，和相机方向做点乘后动画驱动。

## 关键 trick 1：DDX/DDY 重建 flat normal

这是全文最有价值的技术。**问题**：你想让 mesh 看起来是 flat-shaded（每个三角形一个恒定法线），但不想去修改美术的 mesh import 设置，也不想影响其它 shader 对同一个 mesh 的光滑法线需求。

**解法**：GPU fragment shader 处理 pixel 时是 **2×2 quad 一组同步执行**的（这也是 [[divergent-gradient-in-branches|derivative 不能在 divergent branch 里取]]的根本原因）。`DDX(v)` 返回当前像素和 quad 里左右邻像素的 `v` 之差，`DDY(v)` 返回上下邻像素之差。如果 `v = WorldPosition`，那么：

- `DDX(WorldPos)` = 沿表面水平方向的一个小切向量。
- `DDY(WorldPos)` = 沿表面垂直方向的另一个小切向量。
- `cross(DDY(WorldPos), DDX(WorldPos))` = 垂直于表面的法向量，在同一个 flat 面上所有像素**都得到相同的结果**——因为一个三角形面是平的。

最后 `Normalize` 再输出到 `Normal` 输出口。代价：每个像素两次 derivative + 一次叉积 + 一次 normalize，**远比改 mesh 便宜**，而且是纯逐像素的，不侵入任何全局 asset。[[hlsl-derivation-correctness|DDX/DDY 要保证 2×2 quad 内非发散]]这个限制这里自动满足——整张 mesh 都跑这套 shader 不存在分支。

叉积顺序是 `cross(DDY, DDX)` 不是 `cross(DDX, DDY)`——弄反了法线朝内，整个模型背面才被点亮，肉眼就能看出来。

## 关键 trick 2：用贴图为每个三角形分配随机值

**问题**：想让每个三角形独立反射光。Shader Graph 有 `Vertex ID` 和 `Instance ID` 节点，但没有 `Primitive ID` 或 `Triangle ID`——这是一个能让 shader 作者非常难受的缺失。代码 shader 里可以直接读 **`SV_PrimitiveID`**（fragment 入参），但 Shader Graph 不暴露。

**workaround**：**把随机值烘进一张贴图**。Ilett 写了一个 Unity 插件读 mesh 的 UV0，把每个三角形在 UV 空间上覆盖的像素全部填成同一个随机灰度值。这张贴图在采样时必须**关 mipmap、关压缩、用 Point 过滤、高分辨率（文章里用了 8192²）**——任何平滑/压缩都会把三角形边缘的"阶跃"变成渐变，破坏"一个三角形 = 一个值"的语义。而且贴图大小和 mesh 三角数严重耦合，这是工作流代价。

有了这张贴图，一个灰度值（0-1）可以通过三次 `Random Range`（分别加偏移 `0 / 3.14 / 96.07`）生成一个 `Vector3`，`Normalize` 后作为该三角形的"反射向量"。

## 反射驱动：点乘 + 时间动画

每个三角形的反射强度是 **`dot(normalize(CameraDirection), randVec)`**——相机朝不同方向时，不同三角形被"点亮"。为了不让玩家握着相机不动时反射看起来冻结，再加一个时间项：

```
reflection = remap( sin((dot + CycleSpeed * time) * PI), [-1, 1], [0, 1] )
```

`Smoothstep` 用一个 `Reflection Thresholds` Vector2 做下限 / 上限裁剪——下限之下全黑，上限之上全亮，中间平滑过渡。这步让屏幕上真正亮起来的三角形数量受 artist 控制。

## 上色与叠加

想给反射再加一点炫彩色，用 **HSV 色彩空间的 hue 随机化**——把随机向量的第一个分量当作 hue，saturation 和 value 全拉到 1，用 `Colorspace Conversion` 节点从 HSV 转 RGB。然后 `Lerp(baseReflection, colorful, ColorReflectionStrength) × smoothstepMask`。

最后把这个量乘 `Reflection Strength`（全局强度 slider），加上前面算好的 **Fresnel × FresnelColor**，结果塞进 [[shader-graph-lighting-primer|Emission 输出口]]。

## 为什么把它记下来

这个 shader 把三件独立的事缝在一起，每件都值得单独记：

- **DDX/DDY flat normal 重建**几乎是 shader 里唯一不改 mesh 就能切换 smoothing 模式的方法，也是一切"低多边形棱面风格化"的基石。
- **贴图编码 Triangle ID** 是 Shader Graph 缺失 primitive ID 时的唯一 workaround；未来 Unity 加了 primitive ID 节点就不需要这套绕圈。
- **"Fresnel + HDR Emission"** 是 Ilett 教程里反复出现的固定组合（见 [[mgs-stealth-camo-shader|Stealth Camo]]、[[godot-visual-shaders|Godot hologram]]），任何想让物体看起来有"能量场/灵气"的地方都能套。

## 相关

- [[daniel-ilett]]
- [[shader-graph-lighting-primer]] — Emission / Base Color 输出的前置
- [[hlsl-derivation-correctness]] — DDX/DDY 的数学意义与陷阱
- [[divergent-gradient-in-branches]] — derivative 必须在 2×2 quad 内非发散
- [[mgs-stealth-camo-shader]] — 同系列教程的另一个 Shader Graph 案例
- [[classic-shader-noise]]

## Sources

- [[sources/danielilett-pokemon-terastallize]]
