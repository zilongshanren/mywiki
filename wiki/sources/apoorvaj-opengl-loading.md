---
tags: [source, 渲染, OpenGL]
date: 2026-04-14
sources: 1
---

# What is OpenGL loading?（Apoorva Joshi / apoorvaj.io）

[[apoorva-joshi|Apoorva Joshi]] 2016 年 8 月发表的入门长文，从 OpenGL「为什么不能直接 include + link 就用」讲起，最后给出一个 ~180 行的手写 loader 取代 GLEW。

## 摘要

文章先把 OpenGL「不是库、是规范，函数集合取决于硬件 + OS + 驱动」这件事掰碎讲清楚：在 Windows 上 OpenGL 实现是随驱动发的 `opengl32.dll`，Windows SDK 里的 `GL/gl.h` 还停留在 OpenGL 1.1，所以现代函数既没有头声明也没有静态符号，必须在运行时 `LoadLibrary` + `wglGetProcAddress` 自己拉出来。GLEW 这类 loader 把这件事自动化了，但 Joshi 拿 [[papaya-image-editor|Papaya]] 做对照实验：GLEW 文件夹 37,393 行，比 Papaya 整个应用还大；删掉换成 ~180 行手写 loader，构建时间从 6.9 秒降到 5.5 秒。手写 loader 借鉴 Fabian Giesen 的 X-macro 模式：用一个 `PAPAYA_GL_LIST` 宏列举要用到的函数，宏被定义两次分别用来 typedef 函数指针类型和定义 / 加载全局指针。文章把「代码复杂度」明确摆成与性能并列的优化轴。

## 关键要点

- OpenGL 是规范不是库，函数集合 = 硬件 ∩ OS ∩ 驱动版本，所以无法静态链接所有函数。
- Windows SDK 的 `GL/gl.h` 只到 OpenGL 1.1，需要自己补齐 `GL_ARRAY_BUFFER` 等常量和 typedef。
- Loader 三步：`LoadLibrary`/`dlopen` → `wglGetProcAddress`/`dlsym` → 填全局函数指针。
- GLEW 必须支持「所有 OpenGL 函数」，因此体量很大（37k+ LOC）；真实程序只用一小撮。
- X-macro 模式把函数列表写一次、宏展开两次，新增函数只加一行。
- 复杂度是和性能并列的优化轴：删掉用不上的代码本身就是收益。

## 链接到的概念

- [[opengl-loader]]
- [[apoorva-joshi]]
- [[calling-conventions-x86]]

## 原文

- 链接：<https://apoorvaj.io/loading-opengl-without-glew>
- 本地：`raw/articles/apoorvaj.io/2016-08-20_what-is-opengl-loading.md`
