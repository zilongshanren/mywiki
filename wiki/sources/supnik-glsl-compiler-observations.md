---
tags: [source, 渲染, shader, GLSL, 编译器]
date: 2026-04-19
sources: 1
---

# Fun With GLSL Compilers（Ben Supnik / hacksoflife）

[[ben-supnik|Supnik]] 2010-12-22 的文章。他用 AMD ShaderAnalyzer 把 GLSL 编译到 RV790 汇编，逐条记录驱动编译器帮他做了什么、没做什么，然后把结论反过来改造 X-Plane 10 的 shader 组织方式。

## 摘要

核心观察：**RV790 的 ALU 是 5-wide scalar、只有一条 slot 能跑超越函数**，所以 `pow(vec4, vec4)` 要 8 个指令组；编译器会 **inline 一切、折叠常量、砍掉 `*0.0` 以及编译期已知的条件分支**；但它**不做值域推理**——`if (max(0.6,x) > 0.3)` 这种恒真表达式还是全跑。结论：X-Plane 以前用大量 `#define` 手写 conditional shader，规模一大不可维护；改成**「每个阶段一个函数 + 函数内 `#ifdef`」**，由编译器把 `0.0` 常量沿数据流传下去并删掉无用 MAD。代价是会比手写 nicer shader 多泄露几条指令，但节省的时间可用在真正的热路径手调上。

## 关键要点

- RV790 ALU：5-wide scalar，仅一条 slot 支持 log/exp → `pow` 比你想象的贵。
- 编译器会激进 inline、折叠常量、`x * 0.0 = 0.0` 全路径消除、砍 compile-time 已知分支。
- 编译器**不**做值域推理；恒真条件还是会生成完整条件码。
- X-Plane 的 `#define` 组合在 DX9 时代是必需的（硬件没分支），但不随代码规模扩展。
- 更好的做法：`calc_spec()` 等阶段函数里放 `#ifdef`，返回 `0.0`，由编译器把后续 MAD 消掉。
- 热点仍要手调；「依赖编译器」是 90% 的省力策略，不是 100%。

## 链接到的概念

- [[glsl-compiler-optimization-reliance]]
- [[shader-instruction-cost]]
- [[common-shader-pitfalls]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/fun-with-glsl-compilers.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-22_fun-with-glsl-compilers.md`
