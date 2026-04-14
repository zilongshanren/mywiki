---
tags: [source, C++, API设计, 类型系统, 防御性编程]
date: 2026-04-14
sources: 1
---

# Avoid unsigned types by default（Matthäus G. Chajdas / anteru.net）

[[matthaeus-chajdas]] 2010 年 5 月在 anteru.net 上发表的一篇 C++ 设计随笔，重新讲解 Scott Meyers 1995 年 *C++ Report* 专栏中提出的「默认避免 unsigned」原则。

## 摘要

作者观察到 C++ 程序员（尤其是从 Java 转来的）倾向于到处使用 `unsigned` / `size_t`，把它当成「正数语义」的类型标注。他认为这是个错误：**unsigned 类型让 sanity check 失效**——一旦签名上是 unsigned，函数内部就无法用 `assert(size >= 0)` 这种最基本的契约检查发现负数 / 大小算错的情况。文章给出一个生动的反例：用 `memset(&pod, 0, sizeof(Pod) - sizeof(Vector4))` 清结构体时，作者模糊记错 `Pod` 包含 `Vector4` 但实际是 `Vector3`，差值为 -3；如果 `memset` 第三参数是 `size_t`，这个 -3 变成 `18446744073709551613`，64 位机上等于尝试 wipe 整个地址空间。如果是 signed，一次 assert 就抓住。作者承认 unsigned 在两个场景里仍合理：interop（边界上转换，转换前 sanity check）、I/O（按位处理）。除此之外都应当 default to signed。文末特别强调这并不意味着「signed 就是安全的」——signed 同样会溢出，只是错误更容易暴露和拦截，建议配合 SafeInt 之类的库使用。

## 关键要点

- **核心论点**：unsigned 的最大代价是「负数 / 算错的数无法被 assert 抓住」。
- **`memset` 反例**：`sizeof(pod) - sizeof(Vector4)` 在 `Vector3` 字段下是 -3，转换为 `size_t` 后变成接近 `2^64`，立刻 segfault 但完全无法定位。
- **唯二合理使用 unsigned 的场景**：interop（边界转换）与 I/O / bit pattern 操作。
- **「省一个 bit」论点反驳**：现实里几乎没人单次 `malloc` / `fwrite` 2³¹ 元素，更别说 2⁶³。
- **API 设计建议**：尤其是公开 API 不要用 unsigned 参数，否则调用方失去 sanity check 能力。
- **不是银弹**：signed 也会溢出，仍需 `SafeInt` / 范围检查保护中间运算。
- **被引用文章**：Scott Meyers, *Signed and Unsigned Types in Interfaces*, C++ Report 1995。

## 链接到的概念

- [[avoid-unsigned-types]]
- [[red-flags]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/blog/2010/avoid-unsigned-types-by-default
- 本地：`raw/articles/anteru.net/2010-05-17_avoid-unsigned-types-by-default.md`
