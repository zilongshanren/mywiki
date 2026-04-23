---
tags: [source, rendering, 调试, PIX, shader-debug, 迭代速度]
date: 2026-04-19
sources: 1
---

# PIX is great but...（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 3 月的一篇短文：**PIX 虽好，但屏幕上涂颜色有时候更快**。重点不是工具精度，而是**迭代时间**。

## 摘要

Pesce 在刚解掉一个涉及不同坐标空间、Z-buffer 解码的讨厌 bug 之后写下这篇笔记。他先用 PIX 做了很多工作，但**真正定位问题是在放弃 PIX 之后**——把从 Z-buffer 恢复出来的数据直接画到主画面角落，再改 main shader 让它输出希望比对的 ground truth 数据，几次修改就修好了。

这个工作流只在两个前提下成立：**渲染是脚本化的**（容易加 debug view），以及 **shader 能热编译在游戏里自动更新**。Pesce 把它类比到写动态语言的经验——一旦能 live-edit，debugger 反而用得少了，大家都回去**用 print 看运行时**。

他接着 tease 了下一步：在渲染画面上放**带精确数值读数的 color picker**，或者能把颜色解释成法线 / 向量的拾取探针。

## 关键要点

- **PIX vs 着色调试的本质对比**：PIX 给的是精确数值 + 单步，但代价是**切工具、切工作流、迭代慢**；屏幕涂色是粗糙可视化，但**迭代时间接近零**，很多 bug 的可定位性只要「粗糙但够多」就足够。
- Bug 定位法：**把中间数据画到画面角落** + **让 main shader 输出 ground truth** → 并排比对。
- 成立前提：**scripted rendering**（易加 debug pass）+ **shader live-reload**。
- 类比到脚本语言：**live-edit 让 debugger 用得少**，print / 可视化成为主力。
- 未来向：能在渲染画面上放数值探针（color picker + 法线解释器）——本质是把 Pesce 心里那张「数值版 debug view」做成一套复用工具。
- 评论补充（读者 dario）：把 FBO 写成 HDR 图保留浮点精度，再到 Photoshop 里读像素值——同种思路的另一变体。

## 链接到的概念

- [[pix-api-and-dxdmp]]
- [[debug-visualization]]
- [[gpu-printf-debugging]]
- [[binary-hot-reload]]
- [[live-editing-taxonomy-2010]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/03/pix-is-great-but.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-03-19_pix-is-great-but.md`
