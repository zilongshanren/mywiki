---
tags: [shader, 透明度, dither, 渲染, urp]
date: 2026-04-14
sources: 1
---

# Dither 透明度（alpha clipping 伪透明）

在实时渲染里要让一个物体"看起来半透明"有两条路：**真正的 alpha blending**（标准的 source-over 混合，和所有透明物一起排序、禁止写深度），和 **dither alpha clipping**——把"半透明"解释成"按一张 dither 图案丢掉一部分像素的不透明物"。后者常被叫作 *screen-door transparency*、*stipple transparency*，或 *dithered alpha*。

## 为什么要用 dither 替代真透明

真 alpha blending 带来一堆代价：

- **排序地狱**——透明物必须从后往前画才能得到正确合成，而一个物体自己和自己之间也没法正确排序；
- **禁深度写**——透明物自身不能遮挡后面的物体，也不能被 SSAO / motion blur / DOF 等依赖深度的后处理正确处理；
- **和延迟渲染冲突**——延迟管线的 G-buffer 只给不透明物准备，透明物必须在额外的 forward pass 里单独处理。

Dither clipping 把透明物彻底当成不透明物——shader 里调用 `clip(col.a - threshold)`，`threshold` 按像素位置从一张 dither 图里采样——丢掉的像素是"像素级别的洞"，留下的像素是完整的不透明渲染。因为是不透明物，它可以参与 depth prepass、写深度、走 SSAO、被 deferred 管线接受，而视觉上（只要 dither 分辨率足够高）看起来仍然像半透明。

## Bayer 矩阵：阈值图从哪来

最经典的 dither pattern 是 **Bayer 矩阵**——一种递归构造的、保证空间上"低频能量最小"的有序阈值矩阵。对 `n × n` Bayer 矩阵，每个 cell 的阈值是 `(i / n²)` 的一个规整排列。Daniel Ilett 的 *Dither Transparency* shader 在运行时**在 shader 内部生成** Bayer 矩阵，也可以替换成一张外部贴图——只要这张贴图的**红通道**存的是阈值就行。

参数上还有两个实用旋钮：

- **Dither Scale**——按几个像素一个 dither 单元；整数值下视觉最干净（非整数会和像素格产生 beating）；
- **Opacity**——对最终 alpha 做一次乘法，等价于在 clip 前移动整条阈值曲线。

## 何时不要用 dither

Dither clipping 最大的视觉代价是**密度较低的情况下会看到明显的点阵图案**——40% 不透明度的物体在近距离看是一盘斑点，不是半透。它不适合玻璃、烟雾、粒子、边缘羽化的 UI 这些需要真正连续 alpha 的场景。它真正擅长的场合：

- **LOD 渐入渐出**（[[fizzle-lod-fading]]）——角色走近时 impostor 到 full mesh 的切换；
- **靠近相机的遮挡物淡出**——第三人称相机遇到近处墙壁；
- **植物 / 头发的 alpha cutout**——传统 alpha test 的升级版，保留 TAA 友好性；
- **忍者隐身、幽灵化**等风格化状态。

所有这些场景的共同特征是**"半透明效果本身是短暂的或风格化的"**，dither 伪影反而成了一种可接受的视觉语言。

## 和其他 dither 的关系

Dither 在 shader 里还有两个相邻用法：

- **颜色量化 dither**（见 [[retro-rendering-techniques]]）——在把 8-bit 颜色压到 5-bit 时加入噪声阈值，结果是色带被打散成高频噪点；
- **[[taa-history-rectification|TAA 相关的 blue-noise dither]]**——把抖动分散到低频看不见的频段。

本质都是"用高频换低频"的同一个信号处理技巧——只不过这里被应用在 alpha 通道上。

- **[[color-banding|去色带 dither]]**——以量化步长的幅度叠加 Interleaved Gradient Noise 到渐变上，打散深色大面积 posterization。和 alpha dither 完全对称：这里是把量化阶梯恢复为连续感知，那里是把连续 alpha 量化成二值 discard。
- **[[floyd-steinberg-dithering|Floyd–Steinberg 误差扩散]]**——真正解决**颜色量化**的经典 dither，顺序扫描每个像素并把量化误差 7/3/5/1 分配给右下邻居，视觉质量显著好于有序 Bayer，但不可并行。和 alpha dither 的区别在于作用通道（颜色 vs alpha）和输出形态（连续像素 vs 二值 discard），共享的是同一个"高频换低频"信号处理直觉。

## Sources

- [[sources/danielilett-dither-transparency]]
- [[sources/simonschreibt-diablo3-trees]] —— Blizzard 用两张贴片 + alpha8 做 Diablo 3 树的案例，典型的 alpha cutout 替代高多边形几何
