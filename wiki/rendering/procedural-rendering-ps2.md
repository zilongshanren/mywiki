---
tags: [渲染, PS2, 主机硬件, 过程式几何, VU, DMA]
date: 2026-04-14
sources: 1
---

# PS2 上的过程式渲染（Procedural Rendering on PS2）

PS2 是一台「内存小、吞吐量大」的奇特主机——32 MB 主内存、4 MB VRAM、两颗可编程的 **VU（Vector Unit）**、一颗**超宽**的 GS 光栅器。它对**过程式几何**出乎意料地友好：只要你能让 VU 按 60 Hz 的节拍把顶点塞进 DMA chain 喂给 GS，你就可以在单帧里「绘制**比主内存容量还多**」的几何——因为没有一根三角形需要在内存里静态存活。

## 硬件拼图

PS2 的图形路径大致如下：

- **EE（Emotion Engine）**：主 CPU，但真正做 geometry transform 的不是它，是 VU；
- **VU0 / VU1**：两颗可编程向量协处理器，各自 16 KB code + 16 KB data。VU1 通常跑在「micro mode」里做顶点管线，VU0 常做物理/AI；
- **GIF / DMA chain**：VU1 的输出打成一段 GS 能消化的指令流，通过 DMA chain 连续喂给 GS；
- **GS（Graphics Synthesizer）**：没有 shader 的宽光栅器，以「傻快」见长——超高带宽访问 4 MB eDRAM。

VU 的汇编语言像一台小 DSP，没有 transcendental 指令——**连 `expf`/`sinf` 都得自己写**。这是 Robin Green 最后写 [[faster-math-functions|*Faster Math Functions*]] tutorial 的直接起因：他需要在 VU 上插值一个旋转，发现没办法调用 pow。

## 过程式策略的吸引力

在 PS2 这样的机器上，**几何生成速度 > 几何存储容量**是一个可达的点。如果你能让 VU 每秒生成超过 30M 顶点，那你就可以按过程式方式绘制任何规模的模型，而不需要把它全部放进主内存。典型思路：

- **分形 / 生成规则**：按一棵几何变换树（`rotate`/`sweep`/`horn`/`scale`）递归展开基本图元，每个变换都是 VU 上几条指令。
- **LOD 即生成深度**：远处的物体递归浅一点就行——LOD 不需要单独存多套网格，它就是生成算法的一个参数。
- **DMA chain reuse**：固定模板的 instancing 可以通过 DMA chain 的 `REF`/`REFS` 指令复用几何段。

## William Latham 的 Lifeforms

Robin 的 GDC 2001 demo 选了 [William Latham / Stephen Todd 的 Lifeforms](https://www.amazon.com/Evolutionary-Art-Computers-Stephen-Todd/dp/012437185X)——一组用几何变换树随机生成的有机形态，70 年代末到 90 年代在 IBM UK Research Center 产出，代表作是一批大幅面 Cibachrome 艺术印刷。Todd 和 Latham 的 1992 年的书 *Evolutionary Art and Computers* 给出了生成规则，但写得「时而极度详细、时而敷衍挥手」。Robin 把生成算法做成 PS2 实时版，在 60 fps 下每帧重新出一只生物。

副产品：当你能以 60 fps 输出 Latham 当年要花几天慢渲染的艺术，它就不再是艺术——算力消解了稀缺性。Robin 现场还得做一句免责声明：**随机生成的有机形态偶尔会出现一些过于「生殖」的造型，请观众见谅**。

## 为什么它还有意义

PS2 是特例，但「在 VRAM / RAM 紧的硬件上用生成算法代替静态资产」这个套路在：

- **移动 GPU**（紧 bandwidth、紧热预算）；
- **shadertoy 风格的程序化渲染**（零资产）；
- **世界规模的 voxel / mesh 生成**（Minecraft / No Man's Sky）

里都活着。Robin 的 GDC 2001 材料是这条路线在主机时代的一个早期公开样本，也是连向 [[faster-math-functions|*Faster Math Functions*]] 的因果链头——因为没有 `expf`，所以得学 minimax。

## 相关

- [[faster-math-functions]] — 被 VU 的「没有数学库」逼出来的续集
- [[robin-green]]

## Sources

- [[sources/green-procedural-rendering-ps2]]
