---
tags: [渲染, 延迟渲染, g-buffer, x-plane, 2010]
date: 2026-04-19
sources: 1
---

# X-Plane 10 的 G-Buffer 布局（Supnik 2010）

[[ben-supnik|Supnik]] 在 2010 年 12 月记录了 X-Plane 10 初版延迟渲染管线的 G-Buffer 格式，是一份**结构足够简单、但把权衡讲清楚**的实战样本——没有 PBR 的 roughness/metallic，只有一个 shininess 比例；没有 material index 的野心，因为模拟器本来就没有复杂的「多材质 shader 联邦」。16 字节分成四张 RT：

- **RT0: RGBA8 albedo + alpha** —— alpha 用于前向叠加透明元素的 replace 语义；
- **RT1: RG16F** —— 法线 X/Y，Z 由眼空间方向重建（不存 Z 符号，见下文）；
- **RT2: RG16F** —— 一通道存 16F 的眼空间深度，另一通道打包 shadow + shine；
- **RT3: RGBA8 emissive + alpha** —— X-Plane 十年来用 additive emissive 贴图驱动动画灯效，这条保留。

合计 4 张 MRT、16 字节——见 [[multiple-render-targets]] 与 [[deferred-rendering]] 的通用讨论。

## 关键权衡

### Shadow 与 shine 打包进一个 16-bit 通道

两个都需要 ~8 bit 精度，直觉上 16 位整数正好塞两个 8 位字段——但**硬件不配合**：NV 的某些平台不允许 render 到 16-bit 整数；ATI 没暴露 float↔int 的 bitcast。换 RGBA8 也不行，因为 alpha 通道会被 GL 的混合语义吃掉，而 extended blend 在 OS X / MRT 场景都不可用。

Supnik 的解法是直接做浮点算术打包：`packed = 256.0 × shadow + shine`。用浮点的指数位当「两个字段之间的位分配器」——shadow 满时 shine 降到约 2 bit 精度、shadow 为 0 时 shine 回到 8 bit。单看 shine 通道能见到条带，但合成时 shadow 把条带遮住，视觉上看不见。这是一条典型的「利用 float 指数做两字段软打包」的小技巧。

### 法线不存 Z 符号

这个选择依赖两条假设：(1) 后向面被 culling 剔除；(2) 艺术家的 normal map 不会「极度外推」到让切线空间法线实际指向后向。Supnik 在评论里承认 Crytek best-fit normal 更准，但他的产品里尚未见到真实 artifact，等出事再加复杂度——标准的 [[cheat-by-solving-less]] 做派。

### 16F 深度在行星尺度下不够

眼空间深度用 16F 能撑住近距离（阴影尚可），但做 O'Neil 大气散射那种**从深度重建世界位置**的技术会崩。Supnik 给的候选方案是：不再用 G-Buffer 的深度去重建——**直接用模型视图空间里原始行星球面的数学方程去求交**。如果你知道 fragment 来自球面，绕开 G-Buffer 的深度精度回头走解析几何，是更便宜的路。

### emissive 通道的 alpha 被浪费

emissive 理论上可预乘 RGB 后丢掉 alpha——但 X-Plane 需要「非发光物体覆盖发光物体」的 replace 行为，这必须靠 alpha blending 实现：不发光 fragment 要输出 `alpha=1, RGB=0` 来把 G-Buffer 里既有的亮像素抹掉。GL 没有 3 通道可渲染格式，alpha 通道白白占用但无法复用。这是格式约束 > 带宽愿望的现实例子。

### OS X 10.5 后备方案

老 OS X 不支持 RG 纹理，只能退化到 4 张 `RGBA_16F`——VRAM 翻倍，8800 卡上 fill rate 至少降 20%。跨代 OpenGL 环境的老生常谈。

## 配套 GLSL 片段

Supnik 几天后在 *FMTT, GLSL Edition* 贴了对应的片元着色器输出代码：`gl_FragData[0..3]` 分别按上面布局写入，其中 `cut_pos` 做 discard 代理、`shiny_ao * cut_pos` 打包、`position_eye.z/-1024.0` 归一深度。这是前述格式表的直接实现样本。

## 相关

- [[deferred-rendering]]
- [[multiple-render-targets]]
- [[yuv-gbuffer-layered]] —— DCS 的 5×R8G8 层化 G-Buffer，与本文的 16B 宽格式形成对照
- [[tangent-space-normal-mapping]]
- [[ben-supnik]]
- [[cheat-by-solving-less]]

## Sources

- [[sources/supnik-gbuffer-format]]
- [[sources/supnik-fmtt-glsl-edition]]
