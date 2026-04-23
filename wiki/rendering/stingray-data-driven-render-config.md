---
tags: [渲染, 引擎架构, 数据驱动, stingray, bitsquid, render-graph]
date: 2026-04-19
sources: 1
---

# Stingray 的数据驱动渲染配置

Bitsquid 把 gameplay 层的 **[[data-driven-architecture|数据驱动]]** 纪律扩展到了整条渲染管线——在 Stingray 里，渲染管线的**几乎所有结构性决策**都在 `.render_config` / `.shader_source` 这类配置文件里，C++ 代码只负责通用的解释器和 GPU API 抽象。渲染程序员调一次 shader、改一次 post-process、换一套 CSM 实现，不再需要重编引擎——**改 config、live link、画面立刻变**。这是 Bitsquid 2015 年底对"渲染器也该热迭代"这件事给出的工业答案。

## 三个关键文件

Ben Mowery 在 2015 年底的一篇短文里拆出了三层配置：

1. **`settings.ini`** —— 项目级入口。`render_config` 字段指向 `.render_config` 文件，另有一节用来覆盖默认设置。一条项目可以在这里切换整条渲染管线。
2. **`core/stingray_renderer/renderer.render_config`** —— 真正的渲染"脚本"。里面三件事：
   - 指向若干 `.shader_source` 库；
   - `global_resources` 段**声明**所有 GPU buffer（CSM scratch、G-buffer、主 framebuffer 等）；
   - `resource_generators` 段把**每一次 draw / dispatch / clear** 都表达成命名结点——整个 frame graph 就是这份配置。
3. **`*.shader_source`** —— shader 库。可以直接写 HLSL，也可以让美术在节点化 shader 编辑器里搭（导出为同一语义的 node graph），以及吃 Max/Maya 的 ShaderFX 材质。

作者强调，仅靠 grep config、改值、看效果这套 workflow 就能自学绝大多数渲染改动，"完全不用开 Visual Studio"。

## 为什么 renderer 也要 data-driven

传统做法是把 render pipeline 硬编码在 C++：加一个 post 就要改引擎源码、重编、重启。Bitsquid 的论点是：
- **迭代闭环压到秒级**——和 gameplay live-link 一样的体验。
- **更便携**——切平台只是换 config，pipeline 的结构性声明和平台特定 C++ 解耦。
- **让渲染程序员更像内容作者**——实验性 shader / cascaded shadow 变体、tonemapping 曲线这些本来就是"数据"。

代价是需要一整套配置解释器和 live-reload 基础设施，这也是 Bitsquid 花好几年工程债才换来的东西。

## 与同时代方案对照

- **Guerrilla / Frostbite** 的 frame graph 是 2017 年之后才作为开放论文出现的工业实践；Stingray 的 data-driven renderer 在 2015 年就有了同形结构，只不过声明在配置文件而不是 C++ builder 里。
- **UE4** 的 renderer 本体是硬编码的 C++ + pass 宏，只有 post-process volume 这一层偏向数据驱动；调 shadow 实现一般需要引擎修改。
- **Bitsquid Flow** 做过 gameplay 层的可视化数据驱动（[[flow-graph-data-oriented-runtime]]），render_config 把同一哲学推到更硬的 GPU 层。

## 相关
- [[data-driven-architecture]]
- [[flow-graph-data-oriented-runtime]]
- [[render-pass-orchestration]]
- [[niklas-frykholm]]
- [[bitsquid-foundation-library-concept]]
- [[render-config-extension-points]] —— Stingray 1.5 的 plugin 扩展接口：append + insert_at 命名 hook
- [[stingray-renderer-three-stage-pipeline]] —— Stingray 渲染 Cull/Render/Dispatch 三阶段数据并行架构
- [[stingray-render-resource-context]] —— RenderResource 抽象与 RRC 的跨 API 资源分配
- [[stingray-resource-override-suffix]] —— 同样的 data-driven 思路在资源系统里的应用

## Sources
- [[sources/bitsquid-stingray-data-driven-rendering]]
- [[sources/bitsquid-render-config-extensions]]
