---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/build_tool/
published: '2021-05-08'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 构建工具从 Make 到 Ninja

最近，我们把自研游戏引擎的构建工具从 GNU Make 迁移到了 [Ninja](https://ninja-build.org/) 。

迁移动机是这样的：

我为引擎编写了最初的 Makefile ，它可以很好的工作在 MinGW / MacOSX / iOS 平台。把基本框架搭好以后，用起来也比较方便。但是，参与开发的同事一直有用 MSVC 开发的需求，而我们迟迟没有在 Makefile 的框架里增加 MSVC 的支持。用 MSVC 的同事一直在手工维护一个 MSVC 的项目。

渐渐的，同时维护 Makefile 和 MSVC 的工程成了一个负担。

实际上，现在惯用的方法都是用一个高阶的语言去描述项目构建流程，再翻译成不同平台下的构建脚本。即使用 GNU Make ，通常我们也是先用 Make 本身设计一个框架，在这个框架下去描述构建脚本，再让 Make 在不同平台下生成不同的流程。

如果不介意引入新的工具，那么 Autoconf ，CMake ，Premake 都可以解决这个问题。