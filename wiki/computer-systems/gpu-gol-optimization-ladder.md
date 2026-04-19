---
tags: [cuda, triton, gpu-优化, 带宽瓶颈, 位打包, 共享内存]
date: 2026-04-19
sources: 2
---

# GPU Game of Life 优化阶梯

Boris The Brave 用 Conway 的 [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) 当作练手案例，做了一份 GPU kernel 优化的**阶梯式对照**：同一算法（2D 邻域求和 + 三条规则），在 A40 上把 step 时间从 PyTorch 的 **223 ms** 逐步压到 **0.68 ms**，快了约 **330 倍**。这个系列的价值不是最终数字，而是把每一个优化动作、它攻击的瓶颈、以及预期收益量级一一对齐。

## 带宽下限作为标尺

整个练习以 A40 的 DRAM 带宽 **696 GB/s** 当作第一把尺子。N=2¹⁶ × N 的 int8 网格约 4 GB，每步至少读一次、写一次，理论下限 **11.5 ms**。这个数字让每一版本都有「吃掉多少 peak 带宽」的刻度——优化从 17% 起步（torch.compile）爬到 78%（grouped CUDA），和 CUDA 工程师的经验一致：60% 算好，80% 算优秀。

这个下限不是最终物理极限。后文会看到它被「多步融合 + SRAM」和「位打包」两种手段**共同击穿**。

## 阶梯一：框架抽象税

- **PyTorch eager（223 ms）**：每次算子都单独派发，中间结果往返 DRAM；框架 overhead 直接把实际带宽压到 5%。
- **torch.compile（38.1 ms）**：前端 Python 跟踪 → fuse → 生成 [[gpu-gol-optimization-ladder|Triton kernel]]，单次直降 5×。这一档揭示了「写 ML 框架代码而没 compile」是最容易的慢因。

## 阶梯二：手写 CUDA / Triton naive

- **Naive CUDA（26 ms）**：一个线程一个 cell，九读一写，看似要 55+ ms 的带宽，但 SM 的 L1 缓存自然把邻域读复用，实际 44% peak。block size 的最优是 `1×128`——不是正方形最小周长，而是「宽行拿连续内存 + 够一个 warp」的经验值。block 选型因素交织（perimeter / 连续访问 / register 预算 / occupancy），Boris 的结论是「放弃解析推导，直接 benchmark 网格扫」。见 [[cuda-memory-hierarchy]] 的 occupancy 讨论。
- **Naive Triton（22.5 ms）**：`tl.load` + 多个重叠指针，一个线程算一个 cell。Triton 的贡献是**自动**帮你做向量化 load/store、每线程算多 cell、以及（在这里没发挥）shared memory 规划。比等价 naive CUDA 略快，因为 Triton 默认一个线程就算了 8 个 cell。

## 阶梯三：每线程处理更多 cell

在 CUDA 里手工加一层 `ROW_GROUP/COL_GROUP` 循环，让单线程算 2×4 cell。循环展开 + 寄存器复用 + 乱序执行合力把带宽利用率抬到 **78% peak（14.7 ms）**。Boris 坦言这一档收益比预期大——没有显式 shared memory 也没多拉 128-bit load。

这一阶梯的道理和 [[gpu-latency-hiding]] 里 ILP 路径相通：减少在飞线程总数、让每线程做更多事，反而比最大化 occupancy 更划算。

## 阶梯四：打碎 byte-per-cell 抽象——位打包

一个 cell 只有 1 bit 的状态信息，却用 1 byte 存，直接浪费 8× 带宽。改成位打包后，带宽下限降到 **1.4 ms**：

| 变体 | 时间 |
|---|---|
| Bitpacked 8-bit Triton | 14.9 ms |
| Bitpacked 32-bit Triton | 5.21 ms |
| Bitpacked 8-bit CUDA | 8.04 ms |
| Bitpacked 64-bit CUDA | **1.84 ms** |

64 位 CUDA 版本用「按位同时算 64 个 cell」的 SWAR 风格（Boris 让 ChatGPT 写的内核），离 1.4 ms 的新下限已经很近，开始吃到计算边界而非带宽边界。CUDA 在位打包这一档持续超过 Triton——Boris 猜是 Triton 对这种极端手写内核的优化不够，没深究。

## 阶梯五：多步融合击穿 DRAM 下限

续篇里 Boris 采纳读者评论：**一步一往返 DRAM 浪费掉了 L1 的 67 TB/s 带宽**。方案：每个 threadblock 一次性把一个矩形载入 shared memory，在 SRAM 上跑 8 步，再把缩小 8 cell 的内部矩形写回 DRAM。

需要配套的工程点：

- **双缓冲**：同一 block 内线程并发，shared array 要两份，每步交换，避免读写同址。
- `__syncthreads()` 每步一次，确保所有线程看到上一步结果。
- **borders 会被污染**，每 threadblock 的有效输出矩形缩小 8 cell，相邻 block 得重叠覆盖。

跑 8 步共 **5.4 ms**，均摊到单步 **0.68 ms**——比位打包的 1.84 ms 再快 **2.7×**，而且已不再受 DRAM 带宽约束。继续把步数加到 > 8 没收益：SM 的计算资源被吃满了。

进一步优化：展开 `ROW_GROUP` 后**跨行共享 1×3 子和**（3×3 可以分解为 3 个 1×3 预和 + 3 次列求和），几个指令省下去；寄存器数组替代部分 shared memory 的尝试反而掉速，可能是占用太多寄存器压了 occupancy。

## 可迁移的判断

这串阶梯把几条朴素经验压成数字证据：

- **先做框架编译器能自动给你的（torch.compile），再考虑手写 kernel**——门槛 5× 之内。
- **存储格式比 kernel 巧思更能打**——把 1 bit 当 1 bit 存，8× 带宽立刻还给你。
- **多步融合 + 共享内存是真正击穿带宽墙的武器**，前提是算法允许局部重复计算 boundary。
- **block / group size 没有解析最优**，benchmark + profiler 比猜强。

这条路线本来还可以继续走：Hashlife（缓存重复区域）、多 GPU、以及 tensor core 上的 boolean matmul——Boris 也提到但没展开。

## 相关

- [[cuda-memory-hierarchy]] —— 位打包对应 global，多步融合对应 shared
- [[gpu-latency-hiding]] —— ILP vs occupancy 的取舍
- [[gcn-wave-occupancy]] —— register 预算压 occupancy 的同类陷阱
- [[locality-principle]]
- [[latency-vs-throughput]]

## Sources

- [[sources/boristhebrave-gol-cuda-triton]]
- [[sources/boristhebrave-gol-multistep]]
