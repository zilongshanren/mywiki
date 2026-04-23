---
tags: [gpu, 内存延迟, 微基准, pointer-chasing, methodology]
date: 2026-04-19
sources: 1
---

# GPU 延迟微基准的方法学修正

Chester Lam 在 2021 年 4 月首次发布 GPU memory latency 测试（参见 [[gpu-memory-hierarchy-latency]]）之后，跨代跨厂测试中暴露了两个系统性偏差，于是在 5 月做了一次方法学修订。这次修订本身比结果更值得记住——它揭示了 GPU 缓存实测中"看似等价的访问模式其实不等价"的陷阱。

## 问题一：fixed stride 被 AMD 的缓存替换策略击穿

原测试用固定步长（stride）pointer chasing，跨度大于 burst read 即可落到内存延迟。这对 Nvidia 有效，但在 AMD 尤其 RDNA/RDNA2 上——即使数组区域超过缓存容量，AMD 仍然呈现高命中率。作者推断 AMD 使用了对固定步长"友好"的缓存替换策略（例如某种 LRU 变体无法识别大步长 eviction 模式），结果低估了 AMD 的真实缓存延迟曲线。

修复：改用 **Sattolo 算法** 生成随机置换，保证每个节点都在一个长环上出现且恰好一次。相对普通 shuffle，Sattolo 还避免生成短循环——任何循环都等于整个数组长度。换上随机访问后 AMD 的缓存层次一下子变清晰，Nvidia 曲线几乎不变（Nvidia 的替换策略对访问模式不敏感）。

功劳归属：TPU 论坛的 dragontamer5788 提醒了作者 Sattolo 这个细节。

## 问题二：loop overhead 与编译器 unroll

原测试循环体没手动展开。实测发现对 Nvidia 无影响（推测 Nvidia 编译器自动 unroll 或硬件能把 branch overhead 藏进延迟），但在 AMD 上造成系统性高估。修订：手动 ×10 unroll，AMD 的延迟曲线整体下移，得到更准确的 AMD 真实延迟。

## 修订后的结果差异

- RDNA 2 的三级缓存层次重新可见；Infinity Cache 的真实延迟修订为约 156 ns（比 Ampere L2 高 15 ns），而非此前估算的 86 ns——原估算严重低估
- RDNA 2 L1/L2 仍然快于 Ampere L2
- Nvidia 历代曲线与修订前基本一致

## 方法学启示

微基准的任何"看起来无关紧要的实现选择"——步长、loop 是否 unroll、访问是否顺序——都会与目标硬件的某个未文档化特性发生共振。对跨平台对比尤其致命：一种实现能在 A 家公平测到延迟、在 B 家被预取或替换策略掩盖真实值。给出负责任的 apples-to-apples 对比，必须分别验证每个平台对实现选择的敏感性。

这一经验延伸到 [[benchmark-methodology-end-to-end]] 的通用原则：任何跨平台数字都要先问"我测的是我以为的东西吗"。

## Sources

- [[sources/chipsandcheese-gpu-memory-latency-impact]]
