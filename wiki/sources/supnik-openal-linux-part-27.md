---
tags: [source, linux, abi, openal, 共享库]
date: 2026-04-19
sources: 1
---

# OpenAL on Linux, Part 27（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2010 年 9 月的 ABI 管理吐槽：Linux 发行版用一个 **complete rewrite** 的 OpenAL 替换原实现，升了 SONAME major、又删除了旧 `.so`，给 X-Plane 8/9 带来安装崩溃问题。

## 摘要

新 libopenal 实现相对旧版丢掉的大部分是 `_LOKI` 结尾的扩展符号——而扩展符号本来就不是 link-time ABI 的一部分（应用通过 `alGetProcAddress` 运行时解析，而不是静态链接），所以因为它们消失而升 major 并不合理。真正有问题的是一个 `alBufferAppendData` 符号：历史上曾被提议为 streaming 接口、后被挪进扩展、再被规范移除，但旧实现**以未装饰的名字错误地导出**到了核心。新实现删掉它是"把错误改回对的"。

Supnik 的不满不是升级本身，而是**发行版同时做了两件互斥的事**：升 SONAME（暗示不兼容、可共存）+ 删除旧 `.so`（逼所有应用重新编译）。正确的选择应该是二选一：要么保持兼容不升 major、要么升 major 让 `.so.0` / `.so.1` 并存。X-Plane 的兜底是 `dlopen` 两个 SONAME 自适应。

## 关键要点

- Extension 符号不计入 ABI——应用运行时查字符串、解析函数指针，编译期不依赖其存在。
- 升 SONAME major **必须**伴随让旧库留下来，否则等价于直接 break。
- "实现 bug 导出了不该有的符号"是真实问题，但单独升 major 去清理它代价过大。
- 应用自保只能走 `dlopen` + 动态函数指针表。

## 链接到的概念

- [[shared-library-soname-versioning]]
- [[opengl-extension-bucket-strategy]]
- [[function-vs-data-pointer-portability]]
- [[linux-graphics-stack-dri]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/09/openal-on-linux-part-27.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-09-03_openal-on-linux-part-27.md`
