---
tags: [渲染, 性能, profiling, gpu-counter, 工具链]
date: 2026-04-19
sources: 1
---

# 把 GPU 性能计数器织进引擎自己的 profiler

[[ben-supnik|Supnik]] 2013 年在 7970 上跑 X-Plane 的 *Moving the Needle* 里，一边感叹「IHV 每次 GDC 开场都说多数游戏是 CPU bound，我仿佛能感觉到他们在瞪我」，一边把一个具体的工具链痛点写清楚：外部 GPU profiler（当时用的是 AMD **GPU PerfStudio 2**）虽然能按 GPU 时间排序全部 draw call，但**不 sniff call stack**——同一个云团子系统在不同子场景里各出一次，profiler 只会显示 N 个孤立的 draw，不会告诉你「这 N 个都来自 `render_cloud_puffs()`」。当引擎是由若干通用子系统合成一帧、而某个子系统拖了后腿时，这种数据挖掘缺失让"定位到代码"这一步得靠人手。

他给的下一步方案就是本条目命名的做法：**把 NV / AMD 的 performance counter API 直接集成到 sim 里**——在"按逻辑设计而非 call stack 划分"的 instrumentation 段里读 GPU counter，就能构建一个 HUD 风格的、逐子系统的 GPU 耗时面板。这和他们以前为 CPU 侧写过的多代 timing 工具是同一个思路（"Shark 好用到那几年我们根本没自己写"），只是现在延伸到 GPU 侧。

关键是"按逻辑 vs 按 call stack"这个对立：call-stack 采样 profiler 和外部 GPU profiler 都只能按**调用结构**聚合，而引擎开发者真正需要的维度是**子系统／pass**，两者不总是重合。引擎内建的 probe 在每个有意义的逻辑边界上手动插桩，读一次 GPU 时间戳 / counter，就把 call stack 换成了领域语义。代价是每个新平台都要写一遍 counter 绑定——但对于一个跨 NV / AMD / Intel / Apple 的长生命周期 sim，这笔工程被 Supnik 认为值得。

顺带一个具体发现：同一个 *Moving the Needle* profile 里他抓到**单个云团 batch 在 1080p+4×SSAA 下要 32 ms**（一万顶点覆盖大半屏），后面几个 batch 几 ms，其余 batch 是噪声——这种"一个 draw 吃掉全部预算"的分布，没有一张 GPU 时间直方图是看不出来的。外部工具帮他看见了分布，但要追到**云系统代码的哪一条路径**，他就必须回头走本条目说的引擎内 probe 这条路。

## 相关

- [[bottleneck-analysis]] —— 先判断瓶颈在哪，再决定要不要写 probe
- [[frame-profiler-overlay]] —— HUD 风格逐 pass 时间可视化的另一面
- [[xplane-headlight-perf-teardown]] —— Supnik 手术式性能定位的另一个案例
- [[cpu-gpu-pipelining-input-lag]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-moving-the-needle-7970]]
