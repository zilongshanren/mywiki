---
tags: [渲染, hdr, 后处理, bloom, 色彩]
date: 2026-04-19
sources: 1
---

# Fake HDR via Half-Brightness Rendering（半亮度渲染 + 后期乘 2 的伪 HDR）

2010 年前后不少旧硬件上开 fp16 render target 的代价仍然不可忽略——带宽翻倍、alpha blend 变慢、一些老 GPU 甚至压根不支持 MRT 上的 fp16。[[joost-van-dongen|Joost van Dongen]] 在 *Proun* 里想要 HDR 模糊（亮物体模糊后应该"胀"到暗区里、把黑描边吃掉那种效果）但不想吃 fp16 的开销，于是做了一个工程取巧：

1. 渲染时所有物体的颜色都乘 **0.5**，写进**普通 8-bit UNorm RGBA** render target。
2. 景深 / bloom 等模糊 pass 照常跑在这张 8-bit 图上。
3. 最后合成时再乘 **2** 把亮度还回来。

8-bit 通道的值域仍然是 `[0, 255]`，但在被模糊之前，原本"超出 255 的超亮区"现在存在 `[128, 255]` 这一段里没被 clamp，模糊能把这段"可用超亮"扩散到邻居、造成符合物理的 bloom / glow。最后乘 2 之后，亮区回到视觉预期位置。

## 代价与收益

- **收益**：完全不动 render target 格式，带宽、alpha blend、老 GPU 兼容性全部保留 8-bit UNorm 的最优状态；HDR bloom 视觉效果基本拿到手。
- **上限是 2×**：能"伪装"的最大亮度是 `255 × 2 = 510`——因为前期就乘了 0.5，原始亮度超过 2.0 的区域仍然会被 clamp 到 2.0。不是真 HDR，是"0–2 stop HDR"。
- **暗部精度减半**：所有颜色在存进 framebuffer 前被压缩到 `[0, 127]` 这一段（127 级而非 255），暗部 banding 风险翻倍。van Dongen 承认在隧道场景里刻意做更极端的 bloom 时，这套 trick 放大了量化伪影（但 Proun 的抽象纯色风格让这些伪影大多不可见）。
- **混色副作用**：两个不同色的亮物体（比如亮红 + 亮绿）在模糊重叠后，后期乘 2 会得到**非预期的高饱和混色**。van Dongen 观察到这是个"意外好看"的副作用——球体重叠处自然出现彩色光晕。

## 和其他 HDR 近似的关系

- 严格路线：用 fp16 / R11G11B10F 浮点 render target + 物理 tone map。代价是带宽和 blend 开销。
- 这一套：把"超亮"编码到 UNorm 的高半段，代价是上限 2× 和暗部精度折半。
- 相邻思路：[[bloom-threshold-blur-composite|bloom threshold]] 其实是另一种"把超亮区挑出来单独模糊"的 UNorm-only 折中，和这套路线解决的是同一类问题的两个角度。
- 真正的 HDR 合成类方法见 [[exposure-fusion]] / [[local-tonemapping]]。

## 把它放进 2024 的光里看

这个 trick 今天几乎没有人再用——R11G11B10F 在所有现代 GPU 上都快且免费，srgb / linear 工作流 + fp16 bloom buffer 已经是标配。但它作为**"2010 年一个独立工作室 solo 技美怎么在 8-bit 硬件上榨出 HDR 视觉"的样本**仍然有参考价值：核心是"把 visual space 和 storage space 解耦"的思路——如果你知道最终要乘某个常数，就可以提前对除它降低存储量化范围。类似思路后来出现在 [[gpu-data-packing|GPU data packing]]、[[unorm-snorm-hardware-conversion|UNorm 硬件转换]] 等完全不同的场景。

## 相关

- [[bloom-threshold-blur-composite]] —— 另一条 8-bit-friendly 的 bloom 思路
- [[gamma-correction-srgb]] —— UNorm 暗部精度相关
- [[exposure-fusion]] —— 真 HDR 世界的 tone mapping 方向
- [[local-tonemapping]]
- [[unorm-snorm-hardware-conversion]]
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-overbright-fake-hdr]]
