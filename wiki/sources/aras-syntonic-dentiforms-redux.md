---
tags: [source, 软件设计, 渲染, 代码简化]
date: 2026-04-14
sources: 1
---

# Syntonic Dentiforms redux（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2026 年 4 月的一篇 demoscene 考古 + 代码反思文章。作者把自己 2004 年在 nesnausk! 做的 demo《Syntonic Dentiforms》的源代码挖出来，移植到今天的平台，并顺手把 22 年前那一堆过度抽象的 C++ 扫得干干净净。

## 摘要

原 demo 是 Windows 32 位 + Direct3D 9 + D3DX Effects Framework + Visual Studio 6，用了当时新鲜的 pixel shader 2.0，还留了 ps 1.4 / 1.1 的降级路径。这次重构把图形后端换成 **sokol_gfx**、音频换成 **sokol_audio + stb_vorbis**，一口气支持 Windows/DX11、Linux/GL、macOS/Metal 和 Web/WebGL2（均为 64 位）；同时把基于 Object-ID 的阴影换成常规 [[shadow-mapping-basics|shadow map]]（Castaño 的 5×5 PCF 滤波），灯光一律 per-pixel、法线正确归一化、反射做了抗锯齿处理。更值得记录的是作者对旧代码的自我批评：「2004 年的我写的东西按今天的标准真的很糟——指针、抽象、设计模式、继承一大堆毫无意义的东西」。他把 `animator` 目录里 16 个文件、`IAnimChannel`/`CAnimChannel<T>`/`IAnimStream<T>`/`CAbstractTimedAnimStream<T>`…… 一长串模板接口，重写成两个文件里的 `AnimCurve`/`SampledAnimation`/`AnimationBunch`，Graphics 与资源加载也做了同样治疗。整个项目从 **216 文件 24k 行** 变成 **49 文件 6k 行**，可执行文件还小了约 1 MB——因为 D3DX 那堆大而全的东西被更专注的 sokol 家族库替代。作者顺便回忆：2004 年他们深受 Andre Weissflog 的 Nebula Device 引擎影响（那是 OOP/抽象的样板），而今天 Weissflog 的 [sokol](https://github.com/floooh/sokol) 则是「几乎完全相反」的极简风格，作者说自己「爱死了这种反转」。

## 关键要点

- **API 抽象层的时代迁移**：从 D3D9 + D3DX 专用封装迁到 sokol_gfx 这种跨后端的薄抽象，是过去十年游戏/demo 引擎层设计的一次典型品位转变。
- **代码体量塌缩**：同一个 demo，216 → 49 文件、24k → 6k 行——作者的结论是大部分旧代码里的「抽象」其实没有换来任何灵活性，纯粹是 2000 年代 C++ 模板/OOP 文化的副产品。这是 [[classitis]]（Ousterhout 的「类炎症」）在图形/引擎代码里的一个具体案例。
- **动画子系统的重灾区**：`IAnimChannel`/`CAnimChannel<T>`/`CAnimContext`/`CAnimCurve<T>`/`CAnimImmediateMixer<T>`/`IAnimListener<T>`/`IAnimStream<T>`/`CAbstractTimedAnimStream<T>`/`CAnimStreamMixer<T>`/`traits::anim_type<T>`/`IAnimation<T>`/`CAnimationBunch`/`CSampledAnimation<T>`/`CTimedAnimStream<T>` 被压成 3 个具体类型——接口/listener/traits/templates 层层套娃的代价，最终体现为「打开一个文件找不到任何真实行为」。
- **阴影与光照的升级**：Object-ID 阴影换成常规 shadow map + 5×5 PCF；顶点光照改成 per-pixel；反射法线正确归一化并做抗锯齿。这些都是 2004→2026 实时渲染默认做法的增量。
- **可执行文件更小**：D3DX 体量大是因为它兼任 effects framework、texture loader、数学库；换上几个「只做一件事」的小库反而省下 1 MB。这是 [[deep-modules|深模块]] 反面论据之一：不一定非要通用才有价值，专注且小反而更常见地赢。
- **Nebula Device → sokol 的反讽**：同一个作者（Weissflog）在两个时代写出了风格完全相反的引擎/库——2004 年的 Nebula 影响了包括年轻 Aras 在内一批人走向「接口/继承/traits」，2020 年代的 sokol 则回归极简 C 风格。一种隐性的 [[taste-development|品位养成]] 纪录。

## 链接到的概念

- [[classitis]]
- [[aras-pranckevicius]]
- [[shadow-mapping-basics]]
- [[deep-modules]]
- [[shallow-modules]]
- [[false-abstraction]]
- [[taste-development]]
- [[cpp-multi-paradigm-discipline]]

## 原文

- 链接：https://aras-p.info/blog/2026/04/13/Syntonic-Dentiforms-redux/
- 本地：`raw/articles/aras-p.info/2026-04-13_syntonic-dentiforms-redux-aras-website.md`
