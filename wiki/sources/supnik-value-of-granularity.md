---
tags: [source, opengl, driver-compat, engine-architecture]
date: 2026-04-19
sources: 1
---

# The Value Of Granularity（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2010 年 3 月的博客文章，用 X-Plane 的真实经验讲「为什么不应把 OpenGL 扩展死死绑定为整桶」。

## 摘要

OpenGL 是典型的 leaky abstraction：它承诺「画 3D」但绝口不提代价。X-Plane 为应对十余年的硬件差异，把硬件切成 2.5 个桶——固定管线、现代着色器、以及第一代着色器（R300/NV25）。桶内扩展本可以整体启用以减少组合爆炸，但现场调试证明这种打包会反咬一口：当 FBO 在某台机器上坏掉，用户崩溃，只有把「GLSL 开但 FBO 关」这种理论上不需要的组合临时开出来，才能远程隔离故障。X-Plane 9 因此把 FBO、GLSL、VBO、PBO、point sprite、occlusion query、线程化 OpenGL 全部做成可单独关闭的命令行开关，每一个都精确对应一次驱动翻车事件。随着驱动稳定，这些开关会被「卷起来」——9.45 起线程化 OpenGL 变成硬依赖。判断何时可卷入，不看规范而看技术支持电话的数量。

## 关键要点

- 桶分类只是编码省力的近似，不是真实设备能力的反映
- 细粒度扩展开关的首要价值是现场二分调试，不是长期配置模式
- 何时把一个扩展从可选变为必需，由真实 field 反馈决定
- 作为前瞻：越新的扩展越需要保留单独开关，因为驱动稳定需要时间

## 链接到的概念

- [[opengl-extension-bucket-strategy]]
- [[opengl-loader]]
- [[pc-gpu-driver-compat-qa]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/03/value-of-granularity.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-03-10_the-value-of-granularity.md`
