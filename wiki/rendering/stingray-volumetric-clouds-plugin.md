---
tags: [渲染, 体积云, raymarching, 时间重投影, 大气, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 体积云 plugin（Jp Guertin 2016）

[[jp-guertin|Jean-Philippe Guertin]] 2016 年 7 月发的 Stingray plugin，[开源在 GitHub](https://github.com/greje656/clouds)。它**不是**一个新方法——整套路子几乎照搬 [[horizon-zero-dawn-clouds|Andrew Schneider 的 *Real-time Volumetric Cloudscapes of Horizon: Zero Dawn*]] 和 Patapom 的 *Real-time Volumetric Rendering Course Notes*。价值在于：**把 HZD 那套方法落到一个工业引擎的 plugin 里、代码公开可读、并且作者老实地把每一处工程权衡写出来了**。和 [[cloudscape-sdf-volumetric|DCS 的 SDF-driven cloudscape]] 放一起，构成 2015-2016 业界体积云的两条主流分支。

## 建模：3D noise × coverage × 高度

- 低频 3D Perlin-Worley 噪声（64³ 左右）决定云的**宏观分布**；
- 高频 3D noise 雕**形状细节**；
- 2D noise 做**扰动 / 延展**；
- 一张 **2D weather map**（512×512，5 octaves 动画 Perlin）存 coverage / cloud type / wetness，每步 raymarch 采样一次以驱动当前位置的云属性；
- **curl noise** 给 sampling position 加动态扰动，既模拟气流也顺带隐藏 trilinear filter artifact。

> Jp 的吐槽：调那几个 noise 的**采样 scale** 比调 shader 参数更费劲——tiling vs 细节是个权衡，而且 scale 直接决定 GPU cache 命中率。"花时间才能建立直觉"。

对远处低空的 cumulus 云出现的"方格 tiling"，技巧是 **在低空强制更高 coverage**——让它们糊在一起，观众看不出 tiling。

## Raymarch：256 step、4×4 Bayer 插帧、1/16 pixel 重建

- 全分辨率 raymarch 太贵，所以**每 16 帧拼一张完整图**：每帧只采样一个 4×4 Bayer 格子里的 1 个像素。这条路子是 HZD 公开方案的直接搬运，Jp 做了一个微创新——**Bayer 而不是 blue noise**：
  - Mikkel Gjoel 在 *Rendering of INSIDE* 里推荐 blue noise（抗 banding 最好）；
  - Bayer 虽然肉眼容易看出结构，但每帧渲染的像素**都是同一个 Bayer 位置**，GPU cache coherency 明显更好——"一帧只打 16 分之一的 cache pattern 是重复的"。
  - 同时叠加 **8-value Halton 序列**做次级时间抖动，注意只吸收 75% 的第 16 帧来避免历史失效。

> 对比 [[volumetric-cloud-quarter-res-upsample|1/4-res + jitter + temporal upsample]]：两条路解决的是同一个问题（full-res raymarch 太贵），Stingray plugin 选的是**每帧稀疏 + 16 帧重建**，HZD 原始方案的路线；而 Sell 描述的 URP 方案选的是**每帧全屏 1/4 分辨率 + jitter 轮询**。两者的 GPU 微观 cost 不同，但都靠时间维度把采样摊开。

## Motion vector 的近似

Cloud 的"世界位置"没法像几何那样有严格 motion vector。Jp 的做法是在 raymarch 过程里**加权求和 absorption 位置**，用这个近似 3D 点去重投影到上一帧。对 invalidated pixel 做时间权衡时需要在"trackable 像素要平滑" vs "失效像素要快更新"之间调参——典型 temporal filter trade-off。

## 光照：Beer-Powder + 动态 ambient

- 体积透光用 HZD 描述的 **"Beer-Powder"** 模型——同时吃 Beer 律的指数衰减和模拟 out-scattering 的"粉"项，让云边缘发亮。
- 散射/消光系数**视点依赖**（近云和远云用不同值）——不物理，但可调出 artist 想要的样子。
- Ambient term 不用常数：每帧在**太阳矢量两侧**取几对大气样本平均，算出 bottom / top 两个 ambient 色，让 ambient 跟着大气状态走。
- Absorption 位置还用来**按高度改变 absorption 色**——黄昏时云底橙、云顶粉的效果就出来了。

## 天气系统

512×512 weather map 每步 raymarch 都被采样一次来取 coverage / cloud type / wetness。Jp 指出**每 ray step 重采样太浪费**——raymarch 是 instruction bound，一个 lerp 都省——理论上可以 ray 起止采两次再线性插值。wetness term 还要驱动一个 **"sunny/stormy"成对的参数结构**做 lerp，这是主要的 per-step 开销大头，"未来可优化"。

## 未被解决的问题

Jp 自己列出来的 future work：
- **Scale sense**：怎么让云看起来"大"？他的直觉是靠暴露更多高频细节，让小云朵成为远处大云团的比例尺；但高频细节就要更多采样。
- **Shadow / reflection**：初步尝试了 **512×512 opacity shadow map**。这张图非视锥依赖、更新频率可以远低于 16 帧，且采样粗度可以降。同样的思路可以生成 global specular cubemap。

## 相关

- [[horizon-zero-dawn-clouds]]
- [[volumetric-cloud-quarter-res-upsample]]
- [[cloudscape-sdf-volumetric]]
- [[volumetric-raymarching-intro]]
- [[temporal-antialiasing]]
- [[jp-guertin]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-volumetric-clouds]]
