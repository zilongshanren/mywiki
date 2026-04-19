---
tags: [渲染框架, 跨平台, 开源, 引擎, gpu-driven]
date: 2026-04-19
sources: 2
---

# The Forge —— Confetti 的跨平台渲染框架

**The Forge** 是 [[people/wolfgang-engel|Wolfgang Engel]] 所在的 Confetti FX 在 2018 年初开源的跨平台实时渲染框架，覆盖 DirectX 12 / Vulkan / Metal 2 / Linux / 多平台主机。它不是一个完整的游戏引擎，而是一个**显式图形 API 之上的薄框架**——处理 pipeline / descriptor / 资源 / shader 编译 / 多线程提交这些跨 API 的脏活，再附带一套参考级别的渲染样例（[[visibility-buffer|Visibility Buffer]]、[[triangle-filtering-pipeline|Triangle Filtering]]、hybrid ray tracing、PBR、分簇光照……）。

Confetti 内部从 2015 年起就用一个类似的框架跑研究；2017 年决定推倒重写，直面新一代显式 API 的抽象，2018 年初开源。

## 定位：源码即知识

Engel 在 2020 年的回顾里把 The Forge 称为「**下一代 GPU Zen**」。他的理由值得引用：

> "Showing source code is the ultimate way to share graphics programming knowledge."

这句话有明确的针对性。他自己是 *ShaderX* / *GPU Pro* / *GPU Zen* 系列的长期编辑，但也看到这些书 / 会议 talk 的常见失败模式——一页伪代码 + 一个公式，读者拿回去很难复现。The Forge 的每个 release note 都像一篇博客，附带可编译、可在出货游戏上验证过的代码。Engel 把它视为**替代自己下一本书**的知识共享载体。

## 被生产线验证

最公开的案例是 Supergiant Games 的 *Hades*：Confetti 基于 The Forge 给 Supergiant 重写了一个**跨 PC / macOS / Switch** 的游戏引擎，*Hades* 就在其上出货。这是一次「框架→真实 shipping 游戏」的端到端背书。

出货清单（Engel 自述）：
- AAA 定制游戏引擎（*Hades* 级别的独立游戏 + 未公开 AAA）
- 编辑器 / 教育 app
- 商业框架的底座，预计装机量「上亿」

## 工程价值

从 wiki 其它条目反复引用 The Forge 来看，它的工程价值主要落在几个点：

- **[[visibility-buffer]] 的权威参考实现**——DX12 / Vulkan / Metal 2 / Linux 全平台可编译运行。Engel 的 *Triangle Visibility Buffer* 长文就是在此代码库上写的，文中所有 `.fsl` shader 链接都指向 The Forge GitHub
- **[[hybrid-raytraced-shadows-reflections|Hybrid RT]] 的跨平台示范**——2018 年与 [[kostas-anagnostou|Kostas Anagnostou]] 合作移植的 hybrid shadow，在 iOS / macOS / Xbox / PC 上全跑，iPhone 7 上跑 Sponza 都能接受。这是 Engel 在 DXR 之争（见 [[ray-tracing-api-debate]]）里的工程姿态落地
- **Forge Shader Language (FSL)**——一个跨 HLSL / MSL / GLSL 的 shader 前端，The Forge 的 demo 都用它写。wiki 其它条目引用过不少 `.fsl` 文件
- **开放源码的现代管线**——GPU-driven 剔除、[[async-compute]]、bindless 资源绑定、ExecuteIndirect——都有可跑的参考

## 关联贡献者与依赖

Engel 在致谢里提到的合作者与赞助方：

- 工程师：Leroy Sikkes、Jesus Gumbau、Max Oomen、Marijn Tamis、Manas Kulkarni、Volkan Ilbeyli、David Srour 等（2021 年时已累计 ~30 人）
- 厂商支持：Apple、AMD、INTEL、Google
- 依赖：AMD 的 **GeometryFX**（提供 triangle filtering 原型）、**Vulkan Memory Manager**
- 算法原作：Burns & Hunt（VB）、Schied & Dachsbacher（DAIS）、Olano & Greer（2DH 三角形判据）、Wihlidal（GeometryFX 的 GDC 2016 talk）

## 非工程角度的延伸

2020 年那篇 *Catching Up* 写得非常松弛——Engel 说明了为什么 2018 之后他自己写博客的频率明显下降：公司规模扩张意味着他要管 H1B / O1 签证、401k、房东、税务、IP 律师、假日晚餐……剩下做技术的时间反而不够。他把**发 release notes** 当作替代博客的渠道。这一点顺带解释了 wiki 上 Confetti 这条线为什么文章不多但每篇信息密度都很高——因为那不是随手写的博客，是 release-note 格式的系统总结。

## 相关

- [[visibility-buffer]]
- [[triangle-filtering-pipeline]]
- [[hybrid-raytraced-shadows-reflections]]
- [[ray-tracing-api-debate]]
- [[deferred-rendering]]
- [[async-compute]]
- [[bindless-rendering]]
- [[people/wolfgang-engel]]
- [[kostas-anagnostou]]

## Sources

- [[sources/wolfgang-engel-forge-history]]
- [[sources/wolfgang-engel-ray-tracing-without-api]]
