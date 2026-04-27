---
tags: [cpu, qualcomm, arm, mobile, microarchitecture, snapdragon]
date: 2026-04-27
sources: 1
---

# Qualcomm Kryo 微架构

Kryo 是高通历史上第一款也是最后一款自研 64 位 ARM 移动处理器核，搭载于 Snapdragon 820/821（2016 年），随后被定制化的 ARM Cortex 核取代。

## 背景

在 Kryo 之前，高通使用 Scorpion 和 Krait 等自研 32 位 ARM 核积累了丰富经验。64 位时代的 Kryo 是高通在移动 CPU 设计上最雄心勃勃的尝试：试图用类桌面级的乱序核宽度主导安卓生态。Snapdragon 821 配置了两个大核（Kryo big）和两个小核（Kryo little），两者使用相同微架构，仅时钟频率和缓存配置不同——这比 ARM 的 big.LITTLE 方案（使用完全不同的核心）更"大胆"，可视为 Zen 4c 异构配置思路的早期实践。

## 核心架构

Kryo 是 4-wide 乱序流水线，在 2016 年移动端实属激进：

- 4 个整数 ALU（媲美同期桌面核，而 Cortex-A72 仅有 2 个）
- 2 个 128-bit 向量/FP 执行单元，FMA 延迟 5 周期（优于 A72 的 7 周期）
- 4-wide 解码/前端，可连续处理 taken branch（零泡沫机制）
- 大型 flag 寄存器文件和整数物理寄存器文件，支持高 branch 密度代码

## 前端与分支预测

Kryo 的分支预测处理方式独特：采用 L0 指令缓存（~8 KB）+ 快速跳转地址计算的混合机制，而非传统的多层 BTB 结构。在小于 8 KB 代码范围内可实现零泡沫跳转。间接分支预测支持单个分支 16 个目标，或 64 个总目标（每分支 2 目标）。16-entry 返回地址栈，与当时 Intel Core 2 相同深度。

## 弱点：内存子系统

Kryo 最致命的缺陷在于内存子系统：

**Store forwarding 延迟极高（13 周期）**，几乎等同于 forwarding 失败（14–15 周期），意味着几乎所有 store→load 依赖都会产生严重停顿。相比之下，Cortex-A72 的 forwarding 仅需 7 周期。

**无二级 TLB**：Kryo 仅有 192 entry 的单层 L1 TLB。超过 768 KB 的数据集访问会触发完整 page walk，惩罚高达 28+ 周期。Cortex-A72 有多层 TLB，处理大数据集更得心应手。

**L2 缓存小且慢**：大核 768 KB（小核 512 KB），延迟 25/23 周期。换算成实际时间，大核 L2 延迟约 10.9 ns，与 Intel 大容量 L3 相当——相当于用小容量 L2 承担末级缓存的角色，效果自然不理想。此外，大核 L2 的多核扩展带宽良好（私有 L2 设计使每 cluster 只需仲裁 2 个核心）。

## 热功耗瓶颈

Kryo 的大核面积在同代移动核中最大（仅次于 Apple Hurricane），功耗相应偏高。在持续负载下，散热压力迫使频率降至 ~1 GHz，严重抵消了其宽度优势。

## 历史遗产

Snapdragon 821 的继任者 835 采用定制 A73，Kryo 品牌名被沿用但实质已变质（"Kryo 280" 实为定制 A73）。直到 2021 年高通收购 Nuvia，自研 CPU 核才重新提上日程（即后来的 Oryon 核）。Kryo 证明了高通有能力设计激进的移动核，但也暴露了端到端系统协同设计（缓存、TLB、散热）的短板。

## 相关

- [[rendering/adreno-640-architecture]] — Adreno 640 是 Snapdragon 855 的配套 iGPU，继任 Snapdragon 821（Kryo 时代）的 Adreno 530

## Sources

- [[sources/chipsandcheese-qualcomm-kryo]]
