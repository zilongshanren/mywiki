---
tags: [source, rendering, raytracing, aaa, complexity, innovation, industry]
date: 2026-04-27
sources: 1
---

# Why Raytracing Won't Simplify AAA Real-Time Rendering（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2020 年 12 月的文章，论证光线追踪不会使 AAA 渲染引擎变简单，核心论点是"复杂度源自人与产品，而非技术"。

## 摘要

文章以 Carmack 2001 年展示 Doom 3 时关于"统一光照"的承诺开篇——彼时的统一技术是 stencil shadows，结果引擎并没有变简单。作者援引 Clayton Christensen 的创新周期理论指出：AAA 渲染从未进入商品化阶段，仍处于激烈的差异化竞争中。每项新技术（可编程着色器、compute shader、光追）不会删除旧技术，而是叠加在已有复杂度之上，因为 AAA 工作室愿意花一个月工程师时间换一毫秒的帧时间。复杂度的真正驱动力是组织结构与竞争压力，与技术本身无关。作者同时强调，渲染的另一面——低端市场（Unity、Unreal 免费版、Roblox、Three.js）已高度商品化，人人都能做 3D 游戏，这是真正的进步，只是 AAA 不会因此简化。结论：光追只会在顶端加更多复杂度，而在低端，技术变化永远隐藏在工具层之下。

## 关键要点

- 每次渲染硬件跃迁（3dfx → vertex shader → compute → RT）都带来更多代码量，非更少
- Christensen 创新周期：AAA 处于去商品化竞争阶段，工程投入会自然填满可用计算预算
- "一个月工程师 = 一毫秒帧时间"是 AAA 复杂度的经济驱动根本
- 光追不消除旧的阴影/反射技巧，而是增加混合路径；hybrid pipeline 是必然结果
- 低端渲染（Unity/Unreal 免费版、Three.js、Roblox）已商品化，与 AAA 轨道平行运行
- 预测窗口约十年：AAA 不会简化，但非 AAA 市场会持续扩大

## 链接到的概念

- [[rendering/hybrid-raytracing-pipeline]]
- [[rendering/rendering-pipeline-taxonomy]]
- [[rendering/realtime-quality-vs-quantity]]
- [[rendering/rendering-roi-philosophy]]

## 原文

- 链接：https://c0de517e.blogspot.com/2020/12/why-raytracing-wont-simplify-aaa-real.html
- 本地：`raw/articles/c0de517e.blogspot.com/2020-12-27_why-raytracing-won-t-simplify-aaa-real-time-rendering.md`
