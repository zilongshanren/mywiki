---
tags: [source, opengl, driver-bug, glsl]
date: 2026-04-19
sources: 1
---

# I've Got the Blues（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月发表的 debug 笔记。与社区贡献者 alpilotx 联调实验性 instancing 代码时，NVidia Linux 驱动下 instanced 几何全错、场景其余部分被涂成蓝色——这篇文章诊断了病因。

## 摘要

OpenGL 2.1 规范承诺 conventional attribute（`gl_Normal` 等内置顶点属性）与 `glBindAttribLocation` 指定的 generic attribute 之间不存在别名，应用可以同时写满所有 slot。但 NVidia 的 GLSL release notes 清楚说明其实现**违反规范**：内置 attribute 占据固定 slot（`gl_Normal` = 2），如果你用 `glBindAttribLocation` 把自定义 generic attribute 也指到同一 slot，数据会被互相覆盖。驱动代码和规范对不上，bug 就这么浮上来。Supnik 的结论既务实又有点怒气：让 linker 自己分配 attribute index，不要手动 bind。他还解释了 X-Plane 8/9 为什么全部 shader 都只用 built-in attribute——牺牲语义清晰度换来 scene graph / mesh / buffer 的统一代码路径，并保持 OpenGL 1.2.1 向下兼容。

## 关键要点

- OpenGL 2.1 规范明确「无别名」，NVidia 实现存在别名，两者冲突有明文文档
- `gl_Normal` 固定映射到 attribute index 2，与手动绑定的 generic attribute 相撞会彩票
- 症状：instanced 几何错乱、颜色通道串到法线通道导致场景变蓝
- 工程对策：让 linker 自动分配 index，或统一只用 built-in attribute
- X-Plane 的设计选择：统一代码路径 + 向下兼容 > 语义清晰

## 链接到的概念

- [[opengl-builtin-attribute-aliasing]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/01/ive-got-blues.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-28_i-ve-got-the-blues.md`
