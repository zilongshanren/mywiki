---
tags: [opengl, vertex-attributes, glsl, driver-bug]
date: 2026-04-19
sources: 1
---

# OpenGL 内置顶点属性与 generic attribute 的别名

OpenGL 2.1 规范明确规定：所有 `MAX_VERTEX_ATTRIBS` 个 generic attribute 与全部 conventional attribute（`gl_Vertex`、`gl_Normal`、`gl_Color`……）之间**不存在别名（aliasing）**，应用可以同时把它们全部写满而无需担心互相覆盖。

但 NVidia 在 Linux 下的 GLSL 实现选择了相反的语义：内置顶点属性与 `glBindAttribLocation` 绑定的 generic attribute **会在同一 slot 上互相覆盖**。例如 `gl_Normal` 的 slot 固定为 2，如果你用 `glBindAttribLocation` 把某个 generic attribute 也指到 2，那里装的是谁的数据就是彩票。Supnik 与 alpilotx 联调时遇到的现象是：实验性 instancing 代码里 generic attribute 撞上 built-in 之后，实例几何错乱，场景剩余部分全部涂成蓝色——颜色被当成法线、法线被当成颜色，渲染结果立刻崩坏。

这条和规范不符的实现细节在 NVidia GLSL release notes 里有明文，但一般人不会去读。Supnik 的结论是实用主义的：**让 linker 自己给 attribute 分配 index**，不要去手动 `glBindAttribLocation`，也不要在同一个 shader 里混用 `gl_Normal` 这类 built-in 与自定义 generic attribute。这样即便驱动与规范在别名问题上有分歧，也不会踩坑。

这一事件也解释了为什么 X-Plane 8/9 的所有 shader 都只通过 built-in attribute 传每顶点数据——即便需要把不同语义硬塞进 `gl_Color` / `gl_MultiTexCoord` 这种「被严重污染」的通道里。它保留了 scene graph / mesh / buffer 管理一个统一代码路径，只有 shader setup 感知硬件能力，其他部分一路跑到 OpenGL 1.2.1 都成立。

## Sources

- [[sources/supnik-ive-got-the-blues]]
