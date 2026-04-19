---
tags: [source, gpu, architecture, mcm, nvidia]
date: 2026-04-19
sources: 1
---

# NVIDIA's Next Generation GPU: MCM?（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2020 年 12 月的文章，结合 Nvidia 2017 年一篇 MCM GPU 研究论文，分析把下一代服务器 GPU 做成多 die 拼装的可行性、互连功耗代价与优化手段。

## 摘要

文章以 Nvidia 2017 年 MCM 研究论文为骨架，结合 2020 年外界对下一代 server GPU 的泄漏，讨论 MCM GPU 的三大工程挑战：跨 die 通信的功耗（28nm GRS 约 0.54 pJ/bit，对比片内约 80 fJ/bit）、如何在调度与缓存层面减少跨 die 流量、以及图形 workload 的带宽现实。论文配置为 4 颗 die × 64 SM @ 1 GHz，总 64 TFLOPs。通过加入 16 MB L1.5 缓存（拦截跨 die 访问）、把 CTA 调度改成 die-by-die 填充、以及 first-touch 页映射，跨 die 带宽被削减约 5 倍。作者再用 GTX 1080 跑 FFXIV 4K 的实测 L2/VRAM 利用率外推 4K 144 fps 场景，结论是 768 GB/s 的全双工跨 die 链路已足以覆盖图形负载。但文章也强调两个隐藏成本：整卡功耗会把散热推到极限；很多 workload（论文 48 个里有 15 个）根本填不满 256 SM，上层软件并行度成了瓶颈。

## 关键要点

- **互连能耗的数量级差**：片内约 80 fJ/bit vs. 跨 die GRS 约 540 fJ/bit @ 20 Gb/s，差约 7 倍，是 MCM 所有优化的共同出发点。
- **L1.5 缓存**：放在跨 die 链路前专门吸收跨 die 访问，单这一项就少 28% 流量；传统 L2 容量被压到 32 KB，仅保留原子操作加速角色。
- **CTA 调度局部化**：把线程组调度从 round-robin 改为 die-fill 策略，利用相邻 CTA 间的数据局部性，再减 33%。
- **first-touch 页映射**：由驱动实现——SM 第一次访问的页会被绑到它所在 die 的 VRAM，把访存锁在本地。
- **图形 workload 的外推**：FFXIV Shadowbringers 4K 基准在 GTX 1080 上用了 33.7% L2 带宽、45% VRAM 带宽，换算到 4K@144 fps 约需 2.6 TB/s L2、1.14 TB/s VRAM——768 GB/s 级跨 die 链路即可胜任。
- **未解的问题**：散热随 SM 规模线性涨；应用侧 28% 左右的 workload 连 256 SM 都填不满，扩展性受上层制约。
- **同期印证**：同网站《NVIDIA's Enterprise》提到 server GPU 延期，疑因"让多 die 对 OS 呈现为单一 GPU"的固件/驱动未打通——系统软件抽象才是真正难的工程部分。

## 链接到的概念

- [[mcm-gpu-design]]
- [[cuda-memory-hierarchy]]
- [[gpu-latency-hiding]]
- [[dennard-scaling]]

## 原文

- 链接：https://chipsandcheese.com/p/nvidias-next-generation-gpu-mcm
- 本地：`raw/articles/chipsandcheese.com/2020-12-28_nvidias-next-generation-gpu-mcm.md`
