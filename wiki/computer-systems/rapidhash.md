---
tags: [哈希, 性能, simd, 算法]
date: 2026-04-14
sources: 1
---

# rapidhash

**rapidhash** 是 Nicolas Shevchenko 从 wyhash 演化出的非加密 64 位哈希函数（2024+ 起步），目前在多数评测里是「同时满足质量过关与速度最快」的代表。它继承了 wyhash 的极简风格：核心算法主要由 64×64→128 的整数乘法和异或拼接组成。

## 关键特征

- **核心代码短**：V3 版本即使含三种变体加可调参数也只 500 行 C；只取核心的话 100 行级别就能跑（Aras 的 [SmolRapidhash3.cs](https://github.com/aras-pranckevicius/UnitySmolRapidhash) 是个范例）。
- **依赖一条原语**：64×64→128 整数乘法（`umul128`、`__uint128_t`）。这是吞吐能拉到 38-67 GB/s 的根本来源。
- **API 简单**：和 `Unity.Collections.xxHash3` 类似的接口，但直接返回 64 位值，避免了 `int2` 的拆装开销。

## 实测吞吐

| 平台 | rapidhash | XXH3（参考） |
|---|---|---|
| Ryzen 5950X / Win / MSVC 2022 | ~38 GB/s | ~38 GB/s（小输入更慢） |
| Apple M4 Max / macOS / Clang 16 | ~67 GB/s | ~50 GB/s |

对照之下，把 XXH3 用 [Unity Burst](https://docs.unity3d.com/Packages/com.unity.burst@latest) 编译成 C# 后，吞吐掉到原生的 60-65%；而 rapidhash 的 Burst 移植几乎不掉。这是个有意思的 [[bottleneck-analysis|瓶颈定位]] 案例：同一段代码、同一个编译器、同一台机器，性能差距完全来自指令选择和寄存器分配的差异。

## 在 Unity 里的位置

Unity 自带的 `Unity.Collections.xxHash3` 是早年的封装，已经显著落后于原生 C 实现。Aras 的 SmolRapidhash 演示了如何把现代哈希原语带回 Unity Burst 生态：用 `[BurstCompile]` 标注 + 手写 SIMD 友好代码，在 IL2CPP/Burst 下逼近原生 C 性能。对游戏引擎来说，这意味着资源指纹、内容寻址 cache、ECS 哈希查找等场景都有一次「免费提速」的空间。

## 相关

- [[non-cryptographic-hash]]
- [[bottleneck-analysis]]
- [[cpu-performance-formula]]

## Sources

- [[sources/aras-rapidhash-unity-port]]
