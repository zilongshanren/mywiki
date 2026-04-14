---
tags: [source, 计算机系统, 哈希, 性能]
date: 2026-04-14
sources: 1
---

# Rapidhash Unity port（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2026 年 3 月的文章，把 [[rapidhash]] 这个非加密哈希函数移植到 Unity Burst（C# + 编译时优化），并在 x86 与 arm64 两个平台上对照原生 C 实现与 Unity 自带的 XXH3。

## 摘要

文章先回顾近十年非加密哈希演进——xxHash → XXH3、wyhash → rapidhash——然后把 rapidhash 用 Unity Burst 重写为 100 行级的 C# 代码，发布为 `SmolRapidhash3.cs`。基准测试显示：在 Ryzen 5950X 上 rapidhash 的 Burst 移植达到 38 GB/s，与原生 C 持平；在 Apple M4 Max 上达到 67 GB/s，比原生 C 的 50 GB/s 还快。对照之下，Unity 自带的 XXH3 Burst 移植掉了 30-40%。这个差距引出一个有趣的工程结论：**Burst 不总能逼近原生**，要看代码是否击中 codegen 的「甜区」。

## 关键要点

- rapidhash 核心算法只依赖 64×64→128 整数乘法，所以在任何能拿到这条原语的语言里都能跑出极高吞吐。
- 使用 `[BurstCompile]` 标注后，Burst 会调用 `Unity.Burst.Intrinsics` 里的 128 位乘法 intrinsic，绕开 C# 标准库的限制。
- API 形态故意贴近 `Unity.Collections.xxHash3`，但直接返回 `ulong`，省掉 `int2` 拆装。
- 同一份算法在 arm64 上比 x86 优势更大——架构差异会改变「最快哈希」的排名。
- XXH3 在 Burst 下的 30-40% 性能损失暗示某些原语（特定 SIMD 模式）翻译效果不好——这是 [[bottleneck-analysis|瓶颈定位]] 的一个不显眼的子类。

## 链接到的概念

- [[rapidhash]]
- [[non-cryptographic-hash]]
- [[bottleneck-analysis]]
- [[cpu-performance-formula]]
- [[hennessy-patterson]]

## 原文

- 链接：https://aras-p.info/blog/2026/03/07/Rapidhash-Unity-port/
- 本地：`raw/articles/aras-p.info/2026-03-07_rapidhash-unity-port-aras-website.md`
