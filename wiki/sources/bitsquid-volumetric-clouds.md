---
tags: [source, bitsquid, stingray, 渲染, 体积云, raymarching]
date: 2026-04-19
sources: 1
---

# Volumetric Clouds（Jp Guertin / Bitsquid）

[[jp-guertin|Jean-Philippe Guertin]] 2016 年 7 月在 Bitsquid Blog 发表的 Stingray 体积云 plugin 开发日志，对应开源仓库 [github.com/greje656/clouds](https://github.com/greje656/clouds)。文章开篇点题："这**不是**体积云入门"——而是把业界当时的公开方法（Schneider HZD 2015、Hillaire Frostbite 2016、Patapom 2013 course notes、Egor Yusov GPU Pro 6）在一个真实引擎里实现时踩到的每一个坑都记录下来。

## 摘要

Jp 的实现跟 *Horizon Zero Dawn* 的 Nubis 是一条路：低频 3D Perlin-Worley + 高频细节 + 2D weather map + curl noise 扰动。光照用 HZD 的 Beer-Powder + 一个动态 ambient（每帧在太阳矢量两侧取几对大气样本取平均）。raymarch 每帧只采样 1/16 像素（4×4 Bayer 模式），16 帧拼一张完整图——作者特地解释为什么他不用 Mikkel Gjoel 推荐的 blue noise：**Bayer 的好处是同一帧渲的像素都落在同一个 Bayer 位置上，cache coherency 明显更好**。再叠一个 8-value Halton 做次级时间抖动，并只吸收第 16 帧的 75% 来容忍历史失效。

motion vector 用 "weighted absorption position" 近似——在 raymarch 过程中加权记录吸收最多的位置，当作这团云的"代表 3D 点"去重投影。天气系统用 512×512 的动画 Perlin 噪声（5 octaves）驱动 coverage / cloud type / wetness，每步 raymarch 重采样一次——作者标注这是优化空间。

作者最后列了 future work：**sense of scale**（怎么让云看起来大）、**shadow / reflection**（初步方案是 512×512 opacity shadow map，可以远低于每 16 帧的速率更新）。

## 关键要点

- Noise 采样 scale 是最难调的参数，直接决定 tiling vs 细节 + GPU cache 命中率。
- 低空强制高 coverage 可以隐藏远处 cumulus 的方格 tiling artifact。
- **Bayer 4×4 比 blue noise 省 cache**——16 帧中每一帧都是"同一个 Bayer 位置"，这是 pattern 重复性带来的收益，跟 HZD 选 Bayer 的理由一致。
- Beer-Powder 模型让云边缘发亮，对远近云用**不同的散射 / 消光系数**（不物理，但艺术上更好控制）。
- Ambient term 每帧在太阳矢量两侧采几对大气样本动态合成——云的环境光随日落自动变暖。
- Absorption position 还兼任 "云的体重心"——用来按高度调 absorption 色和做重投影。
- Weather map 每步重采样贵；理论上可以 ray 起止采两次线性插；wetness driven 的参数结构 lerp 是主要 per-step 代价。
- Opacity shadow map 的更新周期可以比 raymarch 本身更慢，属于"空间一致但时间低频"资源——同思路可生成 global specular cubemap。

## 链接到的概念

- [[stingray-volumetric-clouds-plugin]]
- [[horizon-zero-dawn-clouds]]
- [[volumetric-cloud-quarter-res-upsample]]
- [[cloudscape-sdf-volumetric]]
- [[volumetric-raymarching-intro]]
- [[temporal-antialiasing]]
- [[jp-guertin]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/07/volumetric-clouds.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-07-31_volumetric-clouds.md`
