---
tags: [source, chipsandcheese, computer-systems, networking, tesla, ttpoe, tcp, hot-chips, dojo]
date: 2026-04-27
sources: 1
---

# Tesla's TTPoE at Hot Chips 2024（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，报道 Tesla 在 Hot Chips 2024 大会上展示的 TTPoE（Tesla Transport Protocol over Ethernet）——一种为低延迟超算内网设计的自研传输层协议，用以替代 TCP，同时保持对标准以太网交换机的兼容性。

## 摘要

Tesla 的 Dojo 超算在训练视频模型时，一个张量可达 1.7 GB，IO 带宽往往成为瓶颈。既有解决方案（Infiniband）成本高昂，Tesla 转而在以太网上开发定制传输层协议。TTPoE 通过简化连接握手（3 次变 2 次）、取消 TIME_WAIT 状态、采用固定大小 SRAM 拥塞窗口等手段将延迟降至微秒级，并设计成可完全由硬件卸载执行。这块 MAC 由一位 CPU 架构师设计，内部借鉴了 CPU 的乱序退休与仲裁思路。承载 TTPoE 的主机卡叫 Mojo，成本低廉，可按需池化扩容以增强 Dojo 超算的 IO 带宽。

## 关键要点

- 握手从 SYN-SYN/ACK-ACK 三次握手简化为两次，关闭序列同样减为两次
- 取消 TCP TIME_WAIT 状态，支持微秒级端口复用
- 拥塞控制不使用滑动窗口缩放，而是固定 1 MB SRAM 发送缓冲区作为拥塞窗口；报文丢失则直接重传 SRAM 内保留的数据
- 按 Little's Law：1 MB × 80 µs 延迟对应约 97.65 Gbps，恰好能满足 100GbE 网卡
- 各端点独立管理拥塞（对比 Infiniband 在交换机侧用信用系统管理），不依赖特殊交换机
- 可在标准以太网交换机上运行，仅需替换端点 NIC 的 MAC 层
- Mojo 卡集成 TTPoE MAC + PCIe Gen3 x16 + 8 GB DDR4，刻意采用廉价规格以降低大规模部署成本
- 设计不适用于公网（固定拥塞窗口在高丢包场景表现差），专为受控的超算内部网设计

## 链接到的概念

- [[computer-systems/ttpoe-protocol]]
- [[computer-systems/tesla-dojo-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/teslas-ttpoe-at-hot-chips-2024-replacing-tcp-for-low-latency-applications
- 本地：`raw/articles/chipsandcheese.com/2024-08-27_teslas-ttpoe-at-hot-chips-2024-replacing-tcp-for-low-latency.md`
