---
tags: [source, rendering, 程序化几何, 3ds-max, maxscript, 艺术]
date: 2026-04-19
sources: 1
---

# Solid Motion（Joost van Dongen，2011-07-30）

[[joost-van-dongen]] 2011 年 7 月发的一篇技术美术文章，描述了他 2006 年首次写、2009 年大量出图的自创 MAXScript 技术——**Solid Motion**：把一个带动画的 3D 物体沿时间轴「扫掠」成一个静态的高面数实体，把运动本身变成雕塑。

## 摘要

Joost 读了一本 Futurism 艺术史书后——未来主义者痴迷于**用单一静态画面或雕塑捕捉运动和速度**（Boccioni 最出名）——他开始想：用 3D 软件可以怎么做这件事？结果是 Solid Motion：**对一个 3ds Max 动画，逐帧复制物体；再用「相邻两帧对应 edge 之间生成 polygon」的方式把帧与帧之间的空间封成一个连续的实体表面**。算法极其简单，本质上是 3D 版本的 POV-Ray `sphere_sweep`，但不限形状，对任何 mesh animation 都可用。

输出是一个**高度图形化、介于具象和抽象之间**的 4D-to-3D 产物。茶壶从空中弹落、柱子倒塌、球体打穿神庙这些场景生成的 Solid Motion 完全看不出原来的物体，却仍隐约保留运动方向和轨迹。代价是面数爆炸：一个 "Solid Motion J" 的黑白实例有超过 400 万三角形，MAXScript 生成要跑很久。

Joost 不在乎性能——这脚本只用来出图。脚本仍可下载（`SolidMotion v13.ms`），在 3ds Max 里选中带动画的物体、运行脚本即可为整个时间轴生成 Solid Motion，但他警告：长动画 + 高面数大概率让 3ds Max 崩溃，先用几个立方体和一百帧试手。

评论区提到两个有意思的观察：一是结果和 POV-Ray 的 `sphere_sweep` 同构；二是看得见 "scales"（鳞片状伪像）——当物体**同时旋转和平移**时，两帧之间 edge 到 edge 的直插值偏离真实扫掠体，表面出现一层规则的锯齿。Joost 回应：**fix 要 10M+ 面数做自适应采样，但他反而喜欢这些伪像**——它们给表面加上了有趣的纹理图案，刻意保留。

## 关键要点

- **Solid Motion = 沿动画时间轴扫掠 mesh 形成的体积实体**。每帧复制一份物体 + 把相邻帧对应 edge 连成 polygon 封面。
- 算法朴素到 10 行伪代码能写完，但输出的视觉语言很强：**具象动作变成抽象雕塑**。
- 起源是 Futurism 的艺术命题（Boccioni 式「运动即形式」），不是工程需求——**艺术史 → 3D 脚本**的反向启发。
- 对「时间-变形」类扫掠问题而言，它是比 sphere sweep 更通用的 poor man's 4D→3D 投影——代价是无曲面拟合，直接 edge 插值带来**子采样鳞片伪像**，尤其在旋转 + 平移复合运动下明显。
- Joost 把这些伪像视为**美学特性**而非 bug——符合他 [[games-as-expression]] 路线里「作者审美高于技术正确」的原则。

## 链接到的概念

- [[solid-motion-sweep]]
- [[joostdevblog-games-as-expression]]——同一周内的姊妹帖，思路上同源（艺术史驱动技术）

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/07/solid-motion.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-07-30_solid-motion.md`
