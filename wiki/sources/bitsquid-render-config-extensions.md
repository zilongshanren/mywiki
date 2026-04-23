---
tags: [source, bitsquid, stingray, 渲染, 引擎架构, plugin]
date: 2026-04-19
sources: 1
---

# Render Config Extensions（Tobias Persson / Bitsquid）

[[tobias-persson|Tobias Persson]] 2016 年 8 月在 Bitsquid Blog 上介绍的 Stingray 1.5 新特性——给 [[stingray-data-driven-render-config|data-driven render config]] 加一套**命名扩展点**，让 plugin 可以不 fork 主 pipeline 就注入自己的 pass / resource。

## 摘要

文章开门见山：Stingray 的 render pipeline 完全由 `render_config` JSON 驱动，这个 Tobias 以前的 GDC 讲过（GDC 2011/2012 的 data-driven renderer 两篇 talk）。1.5 的新问题是**plugin 生态开始扩张**——Stingray 要服务游戏之外的行业（ArchViz、工业可视化），第三方/内部团队越来越想深度集成自己的渲染特性，但又不能每次都要整份复制 `renderer.render_config`。

解法是 `render_config_extension` 文件，两个 root block：
- **`append`**——顺序无关，给 `shader_libraries` / `render_settings` / `shader_pass_flags` / `global_resources` / `resource_generators` / `viewports` / `lookup_tables` 追加项。
- **`insert_at`**——按**主 config 显式声明的 `extension_insertion_points`** 精准注入 layer / modifier。文中给的例子是 [[stingray-volumetric-clouds-plugin|Jp 的体积云 plugin]]：在 `post_processing_development` 插一个 debug pass，在 `skydome` 插 `clouds_modifier`。

Extension 的加载顺序由 boot `.ini` 里 `render_config_extensions` 数组决定——这样一个 extension 可以在另一个 extension 之前或之后加载，形成分层的 plugin 生态。

Tobias 老实地列了**未做的工程债**：没有 name collision 检查（只靠约定前缀 namespace）、没有版本号、没有严格 validation。"这是一个实验性的机制"，1.5 先发出来解封 plugin 作者，未来再迭代——典型的 Bitsquid 节奏：**别为还没遇到的问题提前设计**。

## 关键要点

- `append` 是 **顺序无关** 的补充，允许新 shader library / GPU buffer / setting / render-target 声明。
- `insert_at` 只能插到**主 config 显式命名的 hook**——不允许按行号 / JSON-path 撞大运。这是主 pipeline 作者对"哪里可扩展"负契约责任。
- Extension 之间有**加载顺序依赖**（boot ini 的数组次序），后加的 extension 可以注入到前加 extension 的 hook。
- 当前版本**没有 name collision 检查**——靠 plugin 用前缀模拟 namespace，这是已知的工程债。
- 设计哲学：别让 plugin 在主 config 里到处挖洞；让主 pipeline 作者**显式声明可扩展点**，重构主 pipeline 只要保留命名 hook 就不破坏兼容。
- 1.5 把这个接口发出来的目的是**解封 plugin 作者和内部非游戏项目团队**的深度渲染集成需求；版本号 / 强制 namespace / validation 后续版本再加。
- 本质上是 [[engine-plugin-c-abi-versioned-api|Bitsquid C-ABI plugin system]] 的 **data-driven 对位**——一个管 C++ 侧 API 版本化扩展，一个管 render pipeline 的 JSON 扩展。

## 链接到的概念

- [[render-config-extension-points]]
- [[stingray-data-driven-render-config]]
- [[stingray-volumetric-clouds-plugin]]
- [[engine-plugin-c-abi-versioned-api]]
- [[data-driven-architecture]]
- [[tobias-persson]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/08/render-config-extensions.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-08-16_render-config-extensions.md`
