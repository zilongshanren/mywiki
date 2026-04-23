---
tags: [source, bitsquid, 字符串, utf-8, 哈希]
date: 2026-04-19
sources: 1
---

# Strings Redux（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 6 月的文章，把游戏引擎字符串处理压成三句口号：UTF-8 everywhere、别做 string class、运行时尽量不要字符串。

## 摘要

作者面试喜欢考编码题是为了区分候选人是否区分"数据本身"和"数据表示"。但他写代码只用一种编码：**UTF-8**——统一、无歧义、可直接复用所有 ASCII 工具链。常见两种反对（更费内存、随机访问 O(n)）都站不住：游戏里字符串占内存比例极小，压缩后更几乎抹平差异；随机 glyph 访问是罕见操作，顺序遍历与 UTF-32 等速。

对 string class 也持极端反对态度：静态字符串场景（数据编译、脚本 callback）应直接用 `const char *`；动态场景（格式化、log）则用 `vector<char>` + 一组 `string::append` 函数——把"能否增长"显式写进类型系统。

最后，**runtime 里几乎不应出现字符串**。合法用途只剩 UI 文本（走本地化用 hash key 查表）和 debug（只活在 debug build）。其它所有命名——资源名、对象名、bone 名——**在数据编译阶段就 hash 成 32/64-bit 整数**（全局用 64-bit，局部用 32-bit，hash 冲突算编译错误，"还没碰到过"）。debug 时靠数据编译产出的反查表 + 资源内嵌 32 字节 `debug_name[]` 两重兜底。

## 关键要点

- **UTF-8 everywhere**：内外统一一种编码就不用再讨论；
- UTF-8 反对意见的两条都是误解（内存可压缩抹平、随机访问极少发生）；
- **不要 string class**；静态路径用 `const char *`，动态路径用 `vector<char>` + append 函数族；
- **runtime 只在 UI 和 debug 两处用字符串**；
- **所有命名走 hash**（Murmur 64 全局 / 32 局部），冲突视作编译错误；
- debug 可读性靠 **反查表（tool 用）** + **资源内嵌 `debug_name[32]`**；
- 源码约定：C++ 源文件严格 7-bit ASCII，所有非 ASCII 走本地化 JSON。

## 链接到的概念

- [[string-handling-game-runtime]]
- [[static-hash-value-debug-assert]]
- [[non-cryptographic-hash]]
- [[flow-graph-data-oriented-runtime]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/06/strings-redux.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-06-10_strings-redux.md`
