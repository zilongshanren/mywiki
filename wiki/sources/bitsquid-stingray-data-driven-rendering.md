---
tags: [source, bitsquid, stingray, 渲染, 引擎架构]
date: 2026-04-19
sources: 1
---

# Data Driven Rendering in Stingray（Ben Mowery / Bitsquid）

Ben Mowery（Stingray 渲染工程师）2015 年 12 月的一篇短文，配套一条 Stingray Render Config Tutorial 视频——[[niklas-frykholm|Bitsquid]] 把 gameplay 层玩熟的[[data-driven-architecture|数据驱动]]哲学推广到**整条渲染管线**的工业宣言。

## 摘要

文章开局抛出主张：gameplay 层的数据驱动（component、live link、热更新）有同等价值的**渲染版本**——Stingray 的 renderer 就是这么做的。改一个 shader、加一个 post、切一种 CSM 实现，**全都靠改配置文件**，不动 C++、不重编；引擎运行中就能看效果。这对渲染程序员意味着"编辑 / 编译 / 运行 / 调试"四段式循环坍缩成一个"改 config / 看画面"的单步循环。

配置分三层：`settings.ini` 指向 `.render_config` 入口；`renderer.render_config` 声明 shader library、`global_resources`（CSM scratch、G-buffer、main framebuffer 等 GPU buffer 分配）、以及 `resource_generators`（实际的每条 render pass / draw）；`.shader_source` 存 shader 代码——HLSL 直写 / 节点化 shader 编辑器 / ShaderFX 三种前端都吃。作者推荐的上手方式是"grep 配置 + 改值 + 看效果"，文末指向 Bitsquid YouTube 的 Stingray Render Config Tutorial，但评论区有人反馈视频里没挂 PowerPoint 链接（只能找到一版旧的 gamedevs.org 版）。

文本身非常短、也没有完整 config 例子，主要功能是把概念打标、指路 YouTube。真要学会这套架构得跟视频一起消化。

## 关键要点

- Stingray 的 render pipeline 是一份**声明式的 config 图**——`global_resources` + `resource_generators` = frame graph 的 data-driven 版本。
- 这比业界主流 frame graph（Guerrilla 2017 等）要早两年，只是表达介质是 config 文件而不是 C++ builder API。
- Shader 来源多元：HLSL 文本、节点化编辑器、Max/Maya ShaderFX——data-driven 不强制任何一种。
- **改 shader / 改 pipeline / 换 CSM 实现 = 改 config**；live link 让改动即时反映到运行中的 game instance。
- 这条路的工程债是"一整套 config 解释器 + live reload 基础设施"——Bitsquid 用多年时间才攒起来。
- 本文偏宣言性，缺完整 config 例子，最好配合 YouTube *Stingray Render Config Tutorial* 一起看。

## 链接到的概念

- [[stingray-data-driven-render-config]]
- [[data-driven-architecture]]
- [[flow-graph-data-oriented-runtime]]
- [[render-pass-orchestration]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/12/data-driven-rendering-in-stingray.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-12-18_data-driven-rendering-in-stingray.md`
