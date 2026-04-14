---
tags: [哈希, 性能, simd]
date: 2026-04-14
sources: 1
---

# 非加密哈希函数（Non-Cryptographic Hash）

**非加密哈希**追求的目标和密码学哈希完全不同：要的是**雪崩性 + 雪片速度 + 低碰撞率**，不需要抗碰撞攻击或不可逆。它们是 hash table、checksum、内容寻址、数据去重等场景下的工作马，性能差异直接影响整个系统吞吐。

## 一段近 10 年的演进史

Aras Pranckevičius 在 2016 年做过一次大规模评测。十年后回看，主流玩家几乎全换了：

- **xxHash**（2014）→ **XXH3**（2020）：xxHash 几乎成了「现代非加密哈希」的代名词，XXH3 是它针对小输入和 SIMD 重写的版本。
- **wyhash**（2020+）→ **rapidhash**（2024+）：wyhash 一度在质量榜单上压过 XXH3；它的作者后来推出了 [[rapidhash]] 作为后继，是当前最快的通用 64 位哈希之一。

## 评测维度

非加密哈希的对比通常关注三类指标：

1. **吞吐**（GB/s）：分小输入（几个字节，常见于 hash table 键）和大输入（数 KB，常见于 checksum/blob）两段评估。
2. **统计质量**：常用 [SMHasher](https://github.com/rurban/smhasher) 套件检测雪崩、bias、bit-correlation 等。
3. **可移植性 / 实现复杂度**：核心代码越短越容易在多语言移植和审计。rapidhash V3 的核心可以压到 100 行左右 C# 代码。

## 性能测试的方法学坑

Aras 把 rapidhash 用 [Unity Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译成 C# 代码后，在两台机器上对照原生 C 的 rapidhash 与原生/Burst 的 XXH3：

| 机器 | rapidhash 原生 / Burst | XXH3 原生 | XXH3 Burst |
|---|---|---|---|
| Ryzen 5950X | ~38 GB/s | ~38 GB/s | ~24 GB/s（慢 30-40%） |
| Apple M4 Max | ~67 GB/s | ~50 GB/s | ~30 GB/s |

两个观察值得记住：

- **Burst 不总能逼近原生**。XXH3 的 Burst 移植掉了 30-40%，而 rapidhash 的 Burst 移植几乎贴齐原生。这暗示某些代码模式（比如特定的 SIMD 或 128 位乘法）在 Burst 下生成的指令显著不同——这是 [[bottleneck-analysis]] 的典型边界条件，原本以为是 GPU/驱动问题，实测才发现是 codegen 问题。
- **arm64 上 rapidhash 优势更大**。这又是 [[hennessy-patterson|架构差异]] 的实测体现：x86 与 arm64 的 ALU/调度不同，「最快哈希」的排名会换。

## 为什么 128 位乘法是关键原语

rapidhash 的核心循环依赖 64×64→128 的整数乘法（`umul128`/`__uint128_t`）。这条指令在硬件上只需要一两个周期，但 C# 等高级语言历史上都拿不到——必须借助像 Burst 这样的 native 编译器或 intrinsic。这就是「短 100 行核心」之所以能跑出 38-67 GB/s 的关键：所有数据都汇聚到一条 SIMD-级的硬件指令上。

## 相关

- [[rapidhash]]
- [[bottleneck-analysis]]
- [[cpu-performance-formula]]
- [[locality-principle]]

## Sources

- [[sources/aras-rapidhash-unity-port]]
