---
tags: [人物, 作者, 可视化]
date: 2026-04-14
sources: 3
---

# Bartosz Ciechanowski

**Bartosz Ciechanowski** 是波兰软件工程师 / 可视化作者，个人博客 [ciechanow.ski](https://ciechanow.ski/) 以**高度交互的长文** 闻名——每一篇都在浏览器里跑实时 WebGL/Canvas 模拟，读者可以拖动参数、观察物理过程。

## 风格

- **第一原理推导**：从最简单的观察一步步推出完整模型，不跳步骤。
- **交互优先**：每一个抽象概念都配一个可玩的 demo，而不是静态图。
- **工程美学**：文章本身也是优秀的前端工程样本——他在博客里甚至有专门讲 [how the site is built] 的文章。
- **主题横跨物理 / 数学 / 计算机图形**：色彩空间、alpha compositing、薄透镜、GPS、内燃机、机械表、帆船、双足自行车……

在 2014 年前后（他博客刚开始的时期），Ciechanowski 还经历过一段**硬核低层挖坟**的阶段——Transform Feedback 滥用 GPGPU、`class-dump` + Hopper 逆向 Foundation 的 `__NSArrayM` 和 `__NSDictionaryI`、手工翻译 ARM64 汇编。这些文章没有后来那种 WebGL 交互 demo，但同样是「从第一原理问一个问题：这东西真正怎么工作？」的一脉——只不过问题对象从「光在哪里折射」变成了「循环缓冲区在 ARM64 上长什么样」。Bezier 曲线那一篇是博客上**第一篇带交互 demo** 的文章，可以视为他后来风格的雏形。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Color Spaces | [[color-space]] |
| Alpha Compositing | [[alpha-compositing]] |
| Cameras and Lenses | [[pinhole-camera]]、[[thin-lens-model]] |
| Exploring GPGPU on iOS | [[gpgpu-transform-feedback-ios]] |
| Drawing Bézier Curves | [[bezier-curve-triangulation]] |
| Exposing NSMutableArray | [[nsmutablearray-circular-buffer]]、[[objc-runtime-internals]] |
| Exposing NSDictionary | [[nsdictionary-linear-probing]]、[[objc-runtime-internals]] |

三篇都属于「**图形学基础必读清单**」——比任何教科书都更直观。

## 相关

- [[color-space]]
- [[alpha-compositing]]
- [[pinhole-camera]]
- [[thin-lens-model]]
- [[gpgpu-transform-feedback-ios]]
- [[bezier-curve-triangulation]]
- [[nsmutablearray-circular-buffer]]
- [[nsdictionary-linear-probing]]
- [[objc-runtime-internals]]

## Sources

- [[sources/ciechanow-color-spaces]]
- [[sources/ciechanow-alpha-compositing]]
- [[sources/ciechanow-cameras-and-lenses]]
- [[sources/ciechanow-exploring-gpgpu-ios]]
- [[sources/ciechanow-drawing-bezier-curves]]
- [[sources/ciechanow-exposing-nsmutablearray]]
- [[sources/ciechanow-exposing-nsdictionary]]
- [[sources/ciechanow-nsdictionary-objectforkey-assembly]]
