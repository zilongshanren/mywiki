---
tags: [nvidia, gpu, microarchitecture, maxwell, 28nm, compute, gaming, static-scheduling]
date: 2026-04-27
sources: 1
---

# Maxwell 架构

Maxwell 是 Nvidia 2014 年在 28 nm 工艺上推出的 GPU 架构，继承自 [[kepler-architecture]]，在不换节点的前提下实现了大幅代际性能提升，核心策略是：**削减 Kepler SM 中低利用率的执行资源，换取更高的 SM 数量与更高的时钟频率**。

GM204 是中端代表（16 SM，2048 个 FP32 通道），GM200 为旗舰（24 SM，3072 通道）。Pascal 直接建立在 Maxwell 的微架构基础上，继承其静态调度控制码格式和 SM 四分区划分。

## 对 Kepler 的精简

Maxwell 的改动逻辑是"去除 Kepler 中游戏不会利用的功能"：

- **砍 FP64 高比例配置**：Kepler 可配置 1:3 FP32/FP64 比例（GK210）；Maxwell 将所有 SKU（含数据中心 Tesla M60）统一降至 1:32，彻底放弃高性能 FP64
- **去除 Shared FP32 单元**：Kepler 的 SMSP 可调用另一 SMSP 的 32-wide 共享 FP32，但需双发射且受寄存器带宽制约，实际利用率低；Maxwell 删除共享单元，每 SMSP 只保留私有 32-wide FP32，并发吞吐无需 dual issue 即可达到峰值
- **缩小 Shared Memory bank 宽度**：从 Kepler 的 64-bit 降至 32-bit，游戏均使用 32-bit 类型，64-bit 宽度浪费硅面积

## SM 结构（SMSP 四分区）

Maxwell SM 仍保持 Kepler 的四分区（SMSP）结构，每分区含：
- 16 entry 调度队列
- 64 KB 寄存器文件（4 个单端口 bank）

Shared Memory 容量从 Kepler 的 64 KB 扩至 **96 KB**，且不再兼任 L1 缓存（Kepler 需动态划分 L1/Shared Memory）。这让 Maxwell 可以追踪更多活跃 workgroup，进一步隐藏内存延迟。

Maxwell 还向 Shared Memory 引入了**原生整数原子 ALU**（atomic compare-and-swap），Kepler 需要 load-with-lock + store-with-unlock 序列，延迟极高；Maxwell 的 CAS 延迟大幅下降，超越 AMD GCN（AMD 自 Terascale 2 起就有原子硬件支持但延迟较高）。

## 静态调度改进

Maxwell 延续 Kepler 的编译器静态调度方案，但扩展控制码密度：每 3 条指令前置一个 64-bit 控制字（Kepler 为每 7 条）。每条指令的控制信息从 8 bit 增至 **21 bit**，新增：

- **精细粒度 barrier**：每条指令可关联自己的 barrier，相关指令只等待对应 barrier，而非等待整类内存访问排空。每线程 6 个条目的记分板实现该机制
- **编译器管理寄存器重用缓存**：4 位掩码标记操作数是否写入 2-entry × 4-operand 的重用缓存，后续指令如能命中则避免 bank 冲突。缓存在调度分区切换线程时失效

## 缓存层次

| 层级 | 变化 |
|------|------|
| L1 向量缓存 | 移交给两个 24 KB 纹理缓存（每 SM，每个覆盖 2 SMSP），Kepler 的 SM-级 L1 被删除 |
| Shared Memory | 96 KB，专用（不再做 L1），纯原子操作改善 |
| L2 | GM200 为 3 MB（GK210 为 1.5 MB），带宽提升但实测利用率低于 AMD |
| VRAM | GDDR5，带宽与 Kepler 相近；通过**基于瓦片的光栅化**降低对带宽的依赖 |

L2 延迟低于 GCN，且 Maxwell 引入 ISCADD 指令减少地址计算中的依赖链。

## 性能特征与竞争格局

GM200（GTX 980 Ti）在游戏中明显超越 GK110（GTX 780 Ti）和 AMD R9 390，尽管使用相同 28 nm 工艺。核心原因：更多 SM × 更高时钟 × 每 SM 执行效率改善。

计算方面，Maxwell 在非 FP64 场景（如 FluidX3D 流体模拟、FFT）表现出色，但丢失了 FP64 市场，数据中心线（Tesla M60）在 FP64 下远逊 Kepler Tesla K80。直到 Pascal P100 才补上这一缺口。

AMD 在带宽上保持优势（R9 390 用 512-bit 总线，Fury X 用 HBM），但 Maxwell 用更大 L2 + 瓦片光栅化减少了对原始 VRAM 带宽的依赖，在大多数游戏场景中扳平。

## 遗产

- Pascal 沿用 Maxwell 的控制码格式（至少延续至 Turing）
- AMD RDNA 2、Nvidia Ada Lovelace 均延续了"用更大末级缓存替代宽内存总线"的策略
- Maxwell 的 SM 四分区方案成为后续多代 Nvidia 架构的基础
- Pascal 直接继承 Maxwell 微架构 + 更先进工艺节点，产生了持续热销 7 年以上的 GTX 1080 Ti

## Sources

- [[sources/chipsandcheese-maxwell-nvidia]]
