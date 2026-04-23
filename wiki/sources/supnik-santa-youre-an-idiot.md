---
tags: [source, gpu, command-buffer, parallelism]
date: 2026-04-19
sources: 1
---

# Santa to Ben: You're An Idiot（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2010 年 3 月的博客文章，自我打脸前一年对「OpenGL 并行命令派发」的许愿。

## 摘要

他原本的想法是：CSM 多级阴影图彼此独立，若 GPU 能同时吞 8 条命令流就能把阴影准备阶段并行化。一次与 CUDA 开发者的对话把他拉回现实——CUDA 的多 kernel 并不是为了把更多核心喂给同一任务，而是为了在 batch 间切换时保持 GPU 不空闲。因为即使有几百个着色器单元，单次 kernel 的数据点仍以万计，GPU 早已饱和。把结论搬回图形领域：一张 256×256 的环境贴图就是 65k 像素加 overdraw，现代 GPU 的几百个着色器数量仍远小于任何 draw 的 fragment 数，串行派发已足以让卡忙个不停。图形仍是 *embarrassingly parallel*。真正剩下的疑问是 CPU 端——若 batch 小但驱动判断开销大，多 context 多核填 command buffer 是否能避免 GPU 饿死？Supnik 承认无法从应用层区分「判断是否要改配置」与「真的改 GPU 程序」两种成本的占比。

## 关键要点

- 图形 / GPGPU 的并行粒度天然远大于硬件核心数，无需应用再叠一层并行派发
- 并行 kernel 在 CUDA 的价值是填 batch 间隙，不是线性加速
- 小 batch 反而适合 CPU——驱动开销 + 本地性双重惩罚
- 区分「决策开销」vs「切换开销」是命令流调优的核心，且应用层很难看清

## 链接到的概念

- [[gpu-embarrassingly-parallel-serial-dispatch]]
- [[gpu-latency-hiding]]
- [[gpu-queues-vs-dispatch-execution]]
- [[cached-shadowmaps]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/03/santa-to-ben-youre-idiot.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-03-16_santa-to-ben-you-re-an-idiot.md`
