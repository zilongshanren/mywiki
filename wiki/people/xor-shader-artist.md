---
tags: [人物, 作者, 渲染, shader, gamemaker]
date: 2026-04-14
sources: 5
---

# Xor（GM Shaders）

**Xor**（[@XorDev](https://twitter.com/XorDev)）是一位以 [Shadertoy](https://www.shadertoy.com/user/Xor) 和 [GameMaker](https://gamemaker.io/) 为主要阵地的 shader 艺术家和教程作者，个人博客 [mini.gmshaders.com](https://mini.gmshaders.com) 是一个面向**实践为主、学术味偏轻**的短篇 shader 技术站。文章通常以「一个可跑的小片段 + 一页纸讲清楚」的节奏发布，是入门 GPU 图形、程序纹理和 shader art 的友好入口。

## 风格

- **代码先行**。几乎每篇都配完整的 shader 代码，复制粘贴就能跑，很多直接链到 Shadertoy 或 GitHub 仓库。
- **从 2D 出发讲清概念**。很多 3D / 数学主题（旋转、光照、阴影）都会先从 2D 类比展开，再把维度升上去。
- **廉价优先 > 理论最优**。比起追求「最物理正确」，Xor 更在乎「8-bit 单通道够用就行」「3D 下 Worley 太贵，换个简单方法」这类权衡——非常典型的**美学导向 shader 思维**。
- **GameMaker 视角**。作为一门 2D 为主的引擎，GameMaker 里做 3D 图形其实挺折腾。Xor 的教程经常顺便填补「主流教程不覆盖 GM」的文档空白。
- **短篇为主**。「Mini」系列每篇都是几分钟读完的便笺，适合当参考手册或睡前小读物。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Mini: JFA | [[jump-flooding-algorithm]] — GPU 距离场的洪填算法 |
| Mini: OkLab | [[oklab-color-space]] — 感知均匀的色彩混合 |
| Mini: 3D Rotation | [[3d-rotation-math]] — Euler / Axis-Angle / 四元数的比较 |
| Efficient Chaos | [[layered-grid-noise]] — 用黄金角打破周期性的廉价噪声 |
| GM Shaders: Shadowmaps | [[shadow-mapping-basics]] — Shadow mapping 入门与软阴影采样 |
| Mini: Texels and Pixels | [[texel-pixel-conversion]] — 纹素与像素之间的换算 |
| Mini: Recursive Shaders | [[ping-pong-surfaces]] — 多趟 / 反馈 shader 的 ping-pong surface |
| Mini: Code Golfing | [[shader-code-golfing]] — shader 压缩技巧与数学恒等式 |
| Functions: Dot Product | [[vector-dot-product]] — 点乘的条纹 / 衰减 / Lambert 用法 |
| Mini: Creative Code | [[creative-coding-process]] — 创意编程的四步工作流 |

## 和其它作者的对比

- 相比 [[bartosz-wronski|Bart Wronski]] 的信号处理 / 数据驱动风格，Xor 更偏**视觉艺术和教学**。
- 相比 [[christoph-peters]] 的论文式推导，Xor 更重**最小可跑示例**。
- 和 [Inigo Quilez](https://iquilezles.org/) 算是同一个谱系——Xor 的 OkLab 页还直接引用了 iq 的优化 mix 版本。

## 相关

- [[jump-flooding-algorithm]]
- [[oklab-color-space]]
- [[3d-rotation-math]]
- [[layered-grid-noise]]
- [[shadow-mapping-basics]]
- [[fragment-shader]]
- [[texel-pixel-conversion]]
- [[ping-pong-surfaces]]
- [[shader-code-golfing]]
- [[vector-dot-product]]
- [[creative-coding-process]]

## Sources

- [[sources/xor-mini-jfa]]
- [[sources/xor-mini-oklab]]
- [[sources/xor-mini-3d-rotation]]
- [[sources/xor-efficient-chaos]]
- [[sources/xor-shadowmaps]]
- [[sources/xor-mini-texels-pixels]]
- [[sources/xor-mini-recursive-shaders]]
- [[sources/xor-mini-code-golfing]]
- [[sources/xor-mini-dot-product]]
- [[sources/xor-mini-creative-code]]
