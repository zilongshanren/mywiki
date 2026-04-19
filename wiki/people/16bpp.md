---
tags: [人物, 作者]
date: 2026-04-19
sources: 3
---

# 16BPP.net（Benjamin / define-private-public）

16BPP.net 的博主，身份在公开署名里只露出「Ben / Benjamin」，GitHub 用户名 `define-private-public`。他的长期副业 [PSRayTracing](https://github.com/define-private-public/PSRayTracing) 是基于 *Ray Tracing in One Weekend* 系列的 C++ 重写版，也是他几乎所有性能文章的测试床。

写作上最鲜明的特征是**用实际测量代替道听途说**：`final` 关键字、`noexcept`、贪心 vs 解析采样、free function 对性能的影响、Padé 近似、Nvidia Cg `asin()`、Estrin's Scheme——每一次都跨 Intel / AMD / Apple M 系列三种 CPU、三种编译器、多组 `-O` 级别做全矩阵测试，并把数据表、Jupyter notebook、Google Sheet 一并挂出来。他反复强调「**代码的运行时间永远比数指令、比读汇编更重要**」和「没有 benchmark 支撑的性能主张就是噪声」。

## 相关

- [[rejection-vs-analytical-sampling]]
- [[free-vs-member-functions-performance]]
- [[asin-cg-approximation]]
- [[estrin-scheme]]
- [[pade-approximants]]
- [[psraytracing]]

## Sources

- [[sources/16bpp-greedy-vs-analytical]]
- [[sources/16bpp-free-functions-hypothesis]]
- [[sources/16bpp-quicker-trig-asin-cg]]
