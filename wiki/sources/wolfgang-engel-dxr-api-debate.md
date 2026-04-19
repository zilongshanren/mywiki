---
tags: [source, graphics, 光线追踪, dxr, 图形api, 行业观点]
date: 2026-04-19
sources: 1
---

# Ray Tracing with the DirectX Ray Tracing API (DXR)（Wolfgang Engel）

[[people/wolfgang-engel|Wolfgang Engel]] 2018 年 4 月针对微软 DXR 公开提案写的观点文章。定调是**质疑**而非介绍技术——他在文章开头放了一整段自嘲式的不同讽刺版本（"推销冰箱到南极"），然后认真展开论据。

## 摘要

Engel 的核心问题：**为什么 ray tracing 需要一套独立 API？这对游戏开发者和发行商真的有利吗？**

他把利益方拆成三类并分别代入立场推演：(1) 硬件厂商想把 ray tracing silicon 的复杂度藏在 API 之后，这样一旦 RT 真的起飞就能卖专用硬件；(2) 操作系统厂商想把 RT 绑到自己平台上，提高迁移成本；(3) 游戏开发者 / 图形程序员想要**视觉上的差异化**，没有任何 RT 技术能替所有游戏通用，把 BVH / material sort / ray sort 黑盒化等于让大家用同一套视觉模板。他认为这会重演「一个 metal pixel shader、一个 skin pixel shader」那种被驳回的标准化提议。

经济论据同样尖锐：PC 上发售游戏本来就要先跟硬件厂商谈驱动修复——多一套 RT API 就多一个发售日"驱动坏了"的故障点。发行商能预估这笔 QA 账单，Bethesda / EA / R* 之类会反对；小开发者在这套体系里几乎没有议价权。维护成本远高于初次实现成本，中间件公司（如 Confetti）尤其受冲击。

他的替代建议：**扩展已有 API 而不是新增 API**——给 compute 加一个 ray tracing feature level，硬件专用 silicon 用 extension 暴露；opt-in 的高层 API 可以叠在上面，但别让它成为唯一入口。文末 Addendum 补上驱动经济学的完整推演。

评论区三条都支持他的立场：一位做 CUDA path tracer 的读者说自己真正缺的是跨平台 compute；MJP 提议硬件应暴露 BVH intersection + 一个管理 divergent shader micro-dispatch 的硬件 sorter（GPGPU 广泛受益）；另一位指出 Apple 的 Metal Performance Shaders ray tracing 就走的是这条路。

## 关键要点

- **反对黑盒化 BVH / shader binding**，因为它压缩了视觉差异化空间
- 「双重驱动 QA」经济论证：一款 ship 游戏现在要同时赌两套 API 的驱动稳定性
- 替代方案：compute feature level + extension，**黑盒化是可选项而不是强制项**
- Apple Metal Performance Shaders ray tracing 被视为更合理的抽象层级
- MJP 补充：硬件真正应该加速的是 (1) BVH/triangle intersection (2) 管理 divergent micro-dispatch 的 sorter
- 文章实际上是 [[ray-tracing-api-debate]] 概念页和 [[hybrid-raytraced-shadows-reflections]] Forge 移植的**动机文档**

## 链接到的概念

- [[ray-tracing-api-debate]]
- [[hybrid-raytraced-shadows-reflections]]
- [[hybrid-raytracing-pipeline]]
- [[the-forge-renderer]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2018/04/ray-tracing-with-directx-ray-tracing.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2018-04-05_ray-tracing-with-the-directx-ray-tracing-api-dxr.md`
