---
tags: [source, chipsandcheese, gpu, 内存延迟, warp, ampere, rdna2]
date: 2026-04-19
sources: 1
---

# GPU Memory Latency's Impact, and Updated Test（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 5 月的续作，分两部分：(1) 用 Nsight 在 Unigine Superposition 上量化 GPU 工作集确实受 memory latency 限制；(2) 对原 pointer chasing 微基准做方法学修订。

## 摘要

第一部分针对 Ampere（RTX 3090）和 Pascal（GTX 1080），实测 SOL（Speed of Light）显示两张卡的 VRAM/compute 利用率都远未饱和，top warp stall reason 都是 Long Scoreboard——即等待 cache/VRAM 返回数据。Nvidia 官方判定标准（`sm__issue_active_per_active_cycle_sol_pct` < 80% 且 top stall 为 long scoreboard → TEX-latency limited）成立。Pascal 更胜 Ampere：64-way SMT vs 48-way SMT 让 Pascal 在 warp stall 时有更多备用 warp 可调度；Ampere 还存在 5.61% 的 SM 活跃时间不均（Pascal 仅 0.71%），大 shader array 暴露负载均衡问题。

第二部分披露原测试的两处偏差：固定步长被 AMD 缓存替换策略"友好处理"导致低估延迟，改用 Sattolo 算法生成随机置换后 RDNA/RDNA2 的缓存层次重新可见；循环未展开对 AMD 带来高估，手动 ×10 unroll 后 AMD 延迟曲线下移。修订后 Infinity Cache 真实延迟约 156 ns（比 Ampere L2 高 15 ns），此前估算严重低估。还验证了 Nvidia 的 constant memory 专用 2 KB L1 / 32–64 KB L1.5 缓存层次（Fermi → Ampere），AMD 则无此独立层次。

## 关键要点

- Unigine 8K Optimized 下 RTX 3090 的 shader 和 VRAM 利用率都不到 60%
- Long Scoreboard（等 cache/VRAM）是两代旗舰的首要 warp stall 原因
- Pascal 反超 Ampere：每 SM 64-way vs 48-way SMT
- Ampere 负载均衡 delta 5.61% vs Pascal 0.71%
- Sattolo 算法生成的随机置换是测 AMD GPU 延迟的正确姿势
- Loop ×10 unroll 对 AMD 必要，对 Nvidia 无影响
- Infinity Cache 真实延迟 ~156 ns，比 Ampere L2 高 15 ns
- Constant memory L1（2 KB）延迟比 Ampere global L1 还低

## 链接到的概念

- [[ampere-warp-stall-utilization]]
- [[gpu-latency-microbench-methodology]]
- [[gpu-constant-memory-cache]]
- [[gpu-memory-hierarchy-latency]]
- [[gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/gpu-memory-latencys-impact-and-updated-test
- 本地：`raw/articles/chipsandcheese.com/2021-05-13_gpu-memory-latencys-impact-and-updated-test.md`
