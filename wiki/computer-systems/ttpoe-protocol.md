---
tags: [networking, tcp, transport-layer, tesla, dojo, low-latency, ethernet, hpc]
date: 2026-04-27
sources: 1
---

# TTPoE：Tesla 超算传输协议

TTPoE（Tesla Transport Protocol over Ethernet）是 Tesla 为其 Dojo 超算研发的定制传输层协议，于 Hot Chips 2024 大会公开。其核心目标是在普通以太网基础设施上实现微秒级延迟的主机到超算数据传输，同时将实现复杂度控制在可由廉价硬件完全卸载的范围内。

## 动机

Dojo 训练视频模型时，单个张量可达 1.7 GB，主机侧的 IO 带宽往往成为超算整体吞吐的瓶颈，哪怕主机只做数据复制。常规超算网络方案（如 Infiniband）虽性能优秀，但成本高、交换机专有，不适合大规模扩容。TTPoE 的策略是：保留以太网的成本与通用性，仅对传输层动手术，将 TCP 的若干高延迟状态机精简掉。

## 对 TCP 的简化

TCP 的连接开销在微秒场景中显得笨重：

- **握手**：TCP 需要 SYN→SYN-ACK→ACK 三次往返，TTPoE 缩减为两次。
- **关闭**：TCP 四路握手加 TIME_WAIT 等待被替换为两次交互（发送 close opcode + 收 ACK），TIME_WAIT 完全删除，使端口可在微秒内复用。
- **拥塞控制**：TCP 使用 AIMD（加性增乘性减）算法动态缩放拥塞窗口，TTPoE 改为固定大小的 1 MB SRAM 发送缓冲区充当窗口。所有在途数据保存在 SRAM 中，丢包则直接重传缓冲内数据，无需复杂的窗口算法。

按 Little's Law，1 MB 在途数据配合约 80 µs 网络延迟，对应约 97.65 Gbps——恰好接近 100GbE 线速。

## 硬件实现：TTPoE MAC

TTPoE MAC 硬件块由一名 CPU 架构师设计，大量借鉴了处理器设计思路：包报由仲裁器乱序处理，但按序"退休"（在收到 ACK 后按顺序释放 SRAM）——与 CPU 乱序执行但顺序提交的 ROB 机制形同一辙。

这块 MAC 被集成进 **Mojo 卡**，一张廉价的 NIC：PCIe Gen3 x16 接口 + 8 GB DDR4 + 该 TTPoE MAC。Mojo 卡刻意使用低规格元件，目的是降低大规模扩容成本。当超算需要更多 IO 带宽时，工程师只需从服务器池中拉入更多安装了 Mojo 卡的主机机器。

## 与 Infiniband 的对比

Infiniband 在交换机侧用**信用系统**管理拥塞，不丢包，延迟极低，但需要专用交换机基础设施。TTPoE 的拥塞控制完全在端点独立运行，可在标准以太网交换机上部署，代价是丢包时需重传。对于 Tesla 的受控超算内网（丢包率极低），这是合理的权衡。

TTPoE 不适用于公网环境，因为其固定拥塞窗口在高延迟高丢包的公网链路上会造成大量重传与带宽浪费。

## Sources

- [[sources/chipsandcheese-ttpoe]]
- [[sources/chipsandcheese-tesla-dojo]]
