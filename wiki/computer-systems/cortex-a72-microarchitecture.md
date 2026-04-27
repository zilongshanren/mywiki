---
tags: [arm, cpu, microarchitecture, aarch64, out-of-order, server, sbc]
date: 2026-04-27
sources: 1
---

# Cortex-A72 微架构

Cortex-A72 是 Arm 2015 年发布的 ARMv8-A 乱序核，3 宽，峰值约 2.3–2.4 GHz。虽已被 [[cortex-a710-microarchitecture]] 等后代取代，但凭借 Raspberry Pi 4、AWS Graviton 一代等广泛部署，仍是 2022 年最易获取的 AArch64 乱序核之一。

## 前端

**分支预测**：方向预测性能合理，能识别较长的重复模式，比同期的高通 Kryo 稍好。BTB 容量约 2K–4K 条目，取决于跳转距离（远/近分支区别存储）。BTB 速度偏慢，即便是 64 条目微 BTB 也有 2 cycle 延迟，无法做到零气泡分支。返回栈 31 条目，比 Kryo（16 条目）深。

**取指与解码**：48 KB L1i，3 路组相联，16 bytes/cycle 取指带宽；A72 与 L1i 紧密耦合 BTB，L1i 缺失时无法继续生成取指地址，导致 L2 代码场景性能很差（两核都不足 1 IPC）。

## 乱序引擎

- ROB：128 条目（对低功耗核偏大）
- 整数寄存器文件：64 重命名条目（约 ROB 的一半）
- FP 寄存器文件：128-bit NEON 向量占用多个 64-bit FP 寄存器（5 个），因此 FP 重命名容量充足，但 128-bit 向量的 in-flight 深度受限
- 分布式调度器：每个执行端口独立队列，整数每队列 8–10 条目，结构简单低功耗

**与 Kryo 比较**：Kryo 4 宽、有 4 个基础 ALU，整数吞吐明显占优；A72 双 ALU、单乘法器，但 scalar FP 吞吐与 Kryo 相当（双 64-bit FP 管道各可每周期执行）。

## 内存子系统

- L1d：32 KB，2 路，4 cycle；128-bit load/cycle，store 半速
- L2 TLB：1024 条目，4 路；L2 TLB 缺失附加 7 cycle
- Store forwarding：7 cycle（含部分重叠情形），无内存依赖预测——等待所有先序 store 地址已知后再放行 load，实现简单但可能引入额外延迟

在 Graviton 一代中，4 颗 A72 共享一个 2 MB L2（21 cycle 延迟）。集群内 L2 带宽约 16 bytes/cycle 总量，4 核分摊后极为有限。跨集群延迟超过 200 ns，接近服务器 NUMA 延迟。

## 定位与历史评价

A72 在手机、Raspberry Pi、SBC 和网络设备等"轻 CPU 负载"场景中表现良好。其最大弱点是 L2 带宽与多核扩展性。服务器场景中 AWS 已经用 [[neoverse-n1-microarchitecture]] 取代 Graviton 一代。

作为 AArch64 乱序执行进入主流的标志性核心，A72 的影响深远，也是许多微架构研究的基准参照。

## Sources

- [[sources/chipsandcheese-cortex-a72]]
