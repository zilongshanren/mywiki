---
tags: [unity, 粒子系统, shader, shadergraph, 渲染]
date: 2026-04-14
sources: 1
---

# 粒子系统的 Custom Vertex Streams

Unity 传统的 CPU 粒子系统（Shuriken）和 [[fragment-shader|fragment shader]] 之间，默认只传一个 **Vertex Color**（每个粒子的最终颜色，由 Start Color、Color over Lifetime、Color by Speed 合并而来）。但几乎所有漂亮的粒子 VFX 都不止需要颜色——需要"此粒子现在的生命百分比"（做逐粒子溶解）、"此粒子的随机种子"（做逐粒子花纹变体）、一条曲线（做自定义淡入淡出）等等。Particle System Renderer 模块下的 **Custom Vertex Streams** 就是这条传输通道。

## 思路：把数据塞进未使用的 UV 分量

TEXCOORD（shader 层叫 UV）是 vertex attribute 里为数不多**带有多个空分量**的通道：TEXCOORD0 有 `(x, y, z, w)` 四个 float，粒子 quad 通常只用 `(x, y)` 做纹理采样，`z` 和 `w` 是闲着的。Custom Vertex Streams 让你在 Inspector 里添加任意数量的 per-particle 数据源，Unity 自动把它们**按顺序塞进** TEXCOORD0 的剩余分量，满了就溢出到 TEXCOORD1、TEXCOORD2 继续塞。

常用的数据源：

- **Lifetime → AgePercent**：粒子的归一化年龄 `[0, 1]`（0 = 刚生、1 = 即将销毁）。做 dissolve、fade、color ramp 都靠它。
- **Random → StableRandom.x**：每个粒子一个随机数 `[0, 1]`，粒子整个生命期内不变（VaryingRandom 每帧都变，另一种场景用）。做随机 sprite 选择、随机颜色抖动。
- **Speed, Position, Rotation, Velocity**：可以取各自分量。
- **Custom1 / Custom2**：来自 Particle System 的 **Custom Data** 模块——允许美术配置颜色或向量，再配合**曲线**让值随生命期变化。

在 Shader Graph 里读回来时，就是 `UV` 节点选对应通道 + `Split` 取分量。例如 AgePercent 塞到 TEXCOORD0.z，就是 `UV` 节点的 UV0 通道的第三个 split 输出。

## 顺序是硬约束

Cyan 反复强调：Custom Vertex Streams 列表里的**顺序**直接决定了 shader 读哪个分量的值。如果同时传 `AgePercent` 和 `StableRandom.xy`，默认顺序下 AgePercent 进 TEXCOORD0.z、StableRandom.x 进 TEXCOORD0.w、StableRandom.y 溢出到 TEXCOORD1.x——这种"横跨两个 UV 通道"的布局让 shader 很难清晰地读。美术端可以调整顺序让 StableRandom.xy 整体进 TEXCOORD0.zw，AgePercent 单独进 TEXCOORD1.x，虽然多用了一个通道但组织更清晰。

还有一个容易错过的警告：Vertex Streams **必须和 shader inputs 完全匹配**。如果列表里勾了 COLOR 但 shader 里没有 `Vertex Color` 节点，或者反过来，都会报 "Vertex Streams do not match the shader inputs" 警告——Unity 不会帮你容错。

## Custom Data：颜色、曲线、HDR

Custom Data 模块是 Custom Vertex Streams 的补充。它给你两个槽（Custom1、Custom2），每个槽可以是 Color 或 Vector。

- **Color**：支持 Constant / Gradient / Random Between Two Colors / Random Between Two Gradients。一个被普通粒子颜色系统忽略的能力是——Custom Data 的 Color **支持 HDR**（有 Intensity 调节），可以得到超出 `(1, 1, 1)` 的颜色值；这对 Bloom 后处理很重要。普通的 Start Color 没这个开关。
- **Vector**：最多 4 分量（用两个槽最多 8）。每个分量可以独立设为 Constant / Curve / Random Between Constants / Random Between Curves。**Curve 是杀手级特性**——AgePercent 只能线性推进，Curve 则允许任意形状，例如"前 20% 快速增大、中间稳定、最后 10% 急剧衰减"的淡入淡出曲线，美术端全部可调。

## 一个典型例子

Cyan 文中举的是烟雾粒子：

1. `StableRandom.x` → 喂给 **Flipbook** 节点的 Tile 输入，从一张 3×3 的云朵纹理里抽一个子格。每个粒子随机拿到不同的烟雾形状。
2. `StableRandom.x` 又 `Lerp` 到 `[0.9, 1.1]` 并乘到 Vertex Color 上，让每个粒子有轻微的颜色抖动。
3. `AgePercent` → `Step` 和纹理采样结果比对，做出 **[[texture-dissolve|texture dissolve]]** 效果——随着年龄推进，可见部分逐渐缩小。

这整套效果用 Vertex Color 的 alpha + Color over Lifetime 也能做，但 Custom Vertex Streams 让美术能把逻辑拆得更细——并且随着 Curve 的引入，可以表达非线性的时间函数，这是 Vertex Color 做不到的。

## 和 Visual Effect Graph 的分工

Cyan 顺带提到：Unity 还有一条 GPU 粒子路径——**Visual Effect Graph**（VFX Graph），运行在 Compute Shader 上，适合数万级别的粒子。但它在 URP 上早期处于 Experimental，而且 Shader Graph 的集成需要打开 "Experimental Operators/Blocks" 偏好和 `Output Particle Quad` 块上的 Shader Graph 选项。对低粒子数、和 CPU 游戏逻辑深度耦合的 VFX（例如依赖 AI 状态出粒子），Shuriken + Custom Vertex Streams 依然是实用选择。

## 相关

- [[uv-manipulation-nodes]] —— Flipbook 和 UV 通道的使用
- [[texture-dissolve]]
- [[fragment-shader]]
- [[alpha-blending]]
- [[cyanilux]]

## Sources
- [[sources/cyan-particle-custom-vertex-streams]]
- 相关：[[texture-driven-gpu-particles]] — Anno 1800 的 quad + 时间×粒子纹理方案
