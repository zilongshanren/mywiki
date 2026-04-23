---
tags: [source, bitsquid, cpp, compile-time, tooling, include-graph]
date: 2026-04-19
sources: 1
---

# Caring by Sharing: Header Hero（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2011 年 10 月的博文，发布了一款分析 C++ include 图与 rebuild 解析量的工具 Header Hero（C# 源码附），并附一份打破 header 依赖的实操清单。

## 摘要

C++ 编译时间只会单调恶化：加 include 容易，删 include 没人做。作者写了个小工具给项目扫 `.cpp`/`.h`，用简化的 `#include` 字符串解析（非真 preprocessor）快速算出 Total Lines、Total Parsed 和 Blowup Factor（每行被平均解析多少次）。然后按「贡献 = 自身行数 × 被 include 次数」排序、点击详情看双向传染图，就能定位真正该砍的中间 header。作者给出四招打破依赖：前向声明（含模板、typedef）、pimpl、placement new 到内嵌 buffer、把「小 type + 大量 inline」拆成两个 header。一天半把项目 Total Parsed 从 6M 降到 4.3M 行，完整 rebuild 37 秒。

## 关键要点

- Blowup Factor 是 include 卫生的量化体检指标。
- 增量扫描用缓存 + 字符串匹配，秒级反馈，让「改 header → 看影响」进入内循环。
- 占榜单前列的未必是 STL 容器——具体业务 header（`shader.h`、`file_system.h`）上榜往往是中间头污染。
- 简化解析的代价：注释掉的 `#include` 仍被计入，需真删；boost 风格的 `# include` 空格要额外适配（评论反馈）。
- 和 unity build（[[unity-build-macro-renaming]]）是两条方向相反的路线。

## 链接到的概念

- [[header-hero-compile-analysis]]
- [[header-file-vs-pub-export]]
- [[header-as-user-manual]]
- [[information-hiding]]
- [[orthodox-cpp]]
- [[dependencies]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/10/caring-by-sharing-header-hero.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-10-08_caring-by-sharing-header-hero.md`
