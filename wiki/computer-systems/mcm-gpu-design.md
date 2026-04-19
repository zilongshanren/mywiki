---
tags: [gpu, architecture, mcm, chiplet, interconnect]
date: 2026-04-19
sources: 1
---

# MCM GPU 设计

MCM（Multi-Chip Module）GPU 指的是把一颗"巨无霸"单片 GPU 拆成若干颗小 die，再通过封装级互连拼成一个对外表现为单一 GPU 的系统。思路与 AMD 第一代 Epyc/Threadripper 用多颗 Zeppelin die 组 CPU 如出一辙：单片面积逼近光罩极限、良率随面积指数下滑、功耗墙与 [[dennard-scaling]] 失效一起卡死单片扩展，MCM 因此成为绕过这堵墙的主要方向。

[[chester-lam]] 在 2020 年底的文章中围绕 Nvidia 2017 年的 MCM 研究论文做了拆解，核心矛盾非常清晰：**跨 die 数据传输比片内传输贵一个数量级**。Nvidia 在 28nm 上的 Ground Referenced Signaling（GRS）达 0.54 pJ/bit @ 20 Gb/s，而片内互连只需约 80 fJ/bit——差距接近 7 倍。在一颗 256 SM、1 GHz、64 TFLOPs 的假想配置下，这意味着若不额外优化，跨 die 带宽开销足以把功耗预算吃掉，迫使整机要么降频、要么用超规格散热。

论文给出的三板斧都围绕"减少跨 die 流量"展开：

- **L1.5 缓存**：在跨 die 链路前加一层 16 MB 缓存，专门拦截会出 die 的访问；平均削减 28% 的跨 die 带宽。传统 L2 容量反而被压到 32 KB，仅保留在内存控制器前加速原子操作。
- **CTA 调度局部化**：把传统 SM 间 round-robin 的 CTA 分发改成"先填满一颗 die 再填下一颗"，让相邻 thread group 共享 L1.5 里的数据，再减 33%。
- **First-touch 页映射**：由驱动接管——SM 第一次访问某个页时，把该页绑定到所属 die 的 VRAM，尽量让访存留在本地。

叠加三项优化后，跨 die 带宽削减约 5 倍。Lam 又做了一个图形 workload 的外推实验：GTX 1080 跑 FFXIV Shadowbringers 4K 基准，L2 带宽利用 33.7%、VRAM 33.7%、45%；若线性放大到 4K@144 fps，需要约 2.6 TB/s L2 与 1.14 TB/s VRAM 带宽。切成 4-die MCM、L2 分区跟着内存控制器走时，768 GB/s 的全双工跨 die 链路就够用——说明在图形场景下 MCM 的互连带宽压力并非不可解。

但 MCM 不是银弹。文章也点出两个遗留问题：**功耗与散热**随总 SM 数线性增长，单卡整板功耗会冲破现有风冷/水冷的常规设计（RTX 3080 已经 320 W）；**应用侧并行度**不足——Nvidia 自己在论文里承认 48 个测试 workload 里有 15 个无法把 256 SM 填满，上层算法需要重写才能吃下这种规模的并行。

同日 chipsandcheese 的姊妹文章《NVIDIA's Enterprise》则从另一侧证实了工程落地的难度：Nvidia 下一代 server GPU 被传因"让多颗 die 对 OS 表现为单一处理器"的固件与驱动问题而延期。系统软件必须隐藏 die 边界，而这套抽象的难度正是文献里常被低估的部分。

## 相关

- [[cuda-memory-hierarchy]]
- [[gpu-latency-hiding]]
- [[dennard-scaling]]
- [[cache-coherence-cross-cluster]]
- [[chester-lam]]

## Sources

- [[sources/chipsandcheese-nvidia-mcm-gpu]]
