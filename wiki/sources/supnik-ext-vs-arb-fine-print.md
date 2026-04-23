---
tags: [source, opengl, driver, fbo, mrt]
date: 2026-04-19
sources: 1
---

# EXT vs ARB - The Fine Print（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 6 月 1 日的博文。X-Plane 在 Linux/ATI 上用 RGBA8 + RG16F 混合做 MRT 时被 FBO 拒绝，Supnik 最初以为是驱动 bug，追下去发现是 `GL_EXT_framebuffer_object` 与 `GL_ARB_framebuffer_object` 的完整性规则不同：EXT 要求所有 color attachment 同 internal type，ARB 放宽。

## 摘要

驱动并非对单个 FBO 对象应用统一规则，而是按客户端调用的入口点（`*EXT` 与 ARB）跟踪对象「变体」并套用不同的 completeness 检查。这意味着 DX10 级 MRT 的灵活性只能在 ARB 路径拿到，EXT 路径上混格式就是合法地被驳回。Supnik 的感慨是同情驱动写手——为了同时向后兼容旧扩展语义和暴露新硬件能力，驱动必须维护两套规则。工程启示：不要跨入口点混用同一 FBO；扩展版本是语义差异，不是别名。

## 关键要点

- DX10-class 硬件 MRT 要求 bit plane width 相同（客户端假设）
- `GL_EXT_framebuffer_object`：所有 color attachment internal type 必须一致
- `GL_ARB_framebuffer_object`：放宽，允许 RGBA8 与 RG16F 共存
- 驱动按入口点区分对象变体，混用入口行为未定义
- X-Plane 需在「桶」级别整体切换到 ARB 入口，不在 FBO 内部混

## 链接到的概念

- [[opengl-ext-vs-arb-fast-path-leak]]
- [[opengl-extension-bucket-strategy]]
- [[xplane-gbuffer-format]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/06/ext-vs-arb-fine-print.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-06-01_ext-vs-arb-the-fine-print.md`
