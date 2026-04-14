---
tags: [gpgpu, parsing, 并行算法, prefix-sum, monoid]
date: 2026-04-14
sources: 1
---

# GPGPU 上的字符串反转义：状态机作为 monoid 同态

[[raph-linus]] 2018 年在一篇 sketch 里回答了一个看似反直觉的问题：像 JSON 字符串反转义这种"后面每一步都依赖前面所有字符"的任务，能不能在 GPU 上并行算出来？他的回答是可以，关键工具是把状态机表达成 **monoid 同态**，再用 **parallel prefix sum**（扫描）把 O(n) 的串行推进压到 O(log n) 的并行深度。

## 问题的表面"串行性"

字符串反转义的朴素状态机只有四个状态：0 = 字符串外、1 = 字符串内、2 = 刚遇到反斜杠、3 = 错误。规则极简：`"` 切换 0↔1、`\` 在 1 里进入 2、在 0 里是错误。要留下状态 1 里的字符，丢掉其余。

直觉上必须从左到右扫：开头多一个 `"` 或 `\` 会让后面所有字符的状态整体翻转——靠近末尾的字符看起来像是"依赖无限长的前缀"。GPU 最讨厌这种依赖链。

## 把字符映射成"状态到状态"的函数

突破口来自 Dan Piponi 关于"用 monoid 做增量正则匹配"的经典观察：**不要把字符映射成状态转移，而是映射成从状态到状态的函数**。

四个状态只有 4⁴ = 256 种可能的函数。考虑到错误状态 3 总映射回 3，实际只有 64 种，可以用一个字节编码为三元组 `(s0, s1, s2)`（当前 s3 已固定）。于是：

- 普通字符 `a` → `(0, 1, 1)`：0 留原地、1 留原地、2 回到 1
- 引号 `"` → `(1, 0, 1)`
- 反斜杠 `\` → `(3, 2, 1)`：0 出错、1 进入 2、2 退回 1
- 空串 → `(0, 1, 2)`（identity）

函数复合写起来是 `compose(a, b)[i] = b[a[i]]`——关联但不交换。例如 `aa = a`，但 `\a = (3, 1, 1)`、`a\ = (3, 2, 2)`，顺序敏感。这正是构造一个 [[functions-as-vectors|函数作为元素的 monoid]] 所需的全部条件：有单位元、有关联操作。

## Prefix sum 就是一次并行扫描

一旦 "字符 → 函数" 的映射建立，整个输入的每个位置的"当前状态机状态"就等于它所在位置的**函数复合 prefix scan** 的结果作用在起始状态上。标准的 work-efficient 并行 prefix sum 算法在 2n 次操作、log n 并行深度内完成这一计算——和最朴素的串行版本同阶总功，却能在 GPU 上真正跑满带宽。

> 这个技巧在 Raph 的工具箱里不是孤例：xi-editor 的 rope 数据结构用完全同款的 monoid homomorphism + prefix sum 在 O(log n) 内把文本偏移换算成行号——那边求的是**增量**（编辑后只重算受影响子树），这里求的是**并行**（GPU 上一次全量扫）。同一抽象，两种性能目标。

## Stream compaction 丢掉被转义吃掉的字符

算出每个字符所在状态还不够——题目要求**只保留** state 1 的字符。通用招式是 **stream compaction**：给每个字符打 0/1 标签（是否保留），对标签做 prefix sum 得到目标下标，然后用一次 **scatter** 把每个保留下来的字符写到新数组。scatter 吃全局内存带宽，是瓶颈，但现代 GPU 硬件直接支持。

## 实测数据与瓶颈

Raph 的 CUDA 原型（Thrust 库的 `transform_inclusive_scan` + `copy_if`）在 GTX 1060 上跑到约 **4 GB/s**，对比他的 scalar CPU 版本 200 MB/s 约 20 倍加速。他自己的判断是瓶颈在全局内存带宽，更聪明的做法是把输入切成 tile、在 shared memory 里做大部分工作，最后再拼接——但那要深入 GPGPU 性能细节的"一大坑"。

他也诚实承认：这远未到"实用"——CPU scalar 版本显然还能用 SIMD 打大，两边都没打到极限，GPU 的 20 倍只是证明这个问题**能**被并行化，不是证明**应该**被放到 GPU。

## 为什么值得记住

这个 sketch 的智识价值不在数字，而在方法论：

- **"串行"是表面现象，本质只看依赖是不是能写成 monoid**。只要能，就存在并行算法。
- **状态机的通用并行化套路**：map 到"状态到状态的函数"→ 复合作为 monoid → prefix scan。
- **Parsing 不是 GPU 禁区**。它后来被 [[gpgpu-json-parsing|Towards GPGPU JSON parsing]] 进一步扩展到括号结构提取。

## 相关

- [[gpgpu-json-parsing]] — 同一系列的后续，把技巧推到完整 JSON 树结构
- [[raph-linus]]
- [[functions-as-vectors]]
- [[cuda-memory-hierarchy]]

## Sources

- [[sources/raphlinus-gpu-unescaping]]
