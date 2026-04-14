---
tags: [人物, 作者, 中文博客, 游戏引擎]
date: 2026-04-14
sources: 5
---

# 云风（Cloud Wu）

云风（吴云洋），中国游戏引擎程序员，长期活跃于 blog.codingnow.com。早期在网易任职多年，主导过《大话西游》等 MMO 引擎与底层系统，后期创立 simplegame / ejoy，是开源 actor 模型游戏服务器框架 **skynet**（Lua/C 混合）以及 2D 游戏引擎 **ejoy2d** 的主要作者。

他的文章偏好用纯 C 写底层、用 Lua 做脚本层，反感 C++ 过度的 template 与 all-in-one 哲学，长期围绕模块化、接口设计、对象模型、资源管理、虚拟文件系统、内存管理、序列化、GC 这些朴素而核心的工程问题展开思辨。写作风格务实，多为边做边写的设计笔记，对中文游戏程序员社区影响较大。

## 主要工作

- 网易早期 MMO 引擎 / 大话西游系列
- skynet：面向游戏服务器的 Lua/C actor 框架
- ejoy2d：2D 游戏引擎
- 十余年的个人博客 blog.codingnow.com，系统性的工程思考输出

## 关联概念

- 偏爱 C + Lua 混合编程的哲学，反对用 C++ 宏来"模拟"对象模型
- 从模块化 / 接口先行 / 生命期隔离出发设计底层

## 相关

- [[modular-design]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[c-opaque-struct-modules]]
- [[c-interface-oop]]
- [[simple-cpp-mark-sweep-gc]]
- [[c-serialization-metadata]]
- [[game-engine-vfs]]
- [[malloc-wrapper-debug]]

## Sources

- [[sources/cloudwu-c-module-interface]]
- [[sources/cloudwu-cpp-mark-sweep-gc]]
- [[sources/cloudwu-c-serialization-and-c-oop]]
- [[sources/cloudwu-game-engine-vfs]]
- [[sources/cloudwu-malloc-wrapper]]
