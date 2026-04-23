---
tags: [source, chipsandcheese, cpu, zen4, genoa, amd]
date: 2026-04-19
sources: 1
---

# Details on the Gigabyte Leak（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 8 月发表于 [[chips-and-cheese]] 的短文，基于某勒索组织从 Gigabyte 泄露的 Zen 4（Genoa 服务器 / AM5 客户端）处理器编程参考（PPR）摘取的技术细节。文章本身立场偏"新闻 + 数据解读"，但提取的 PMU event 掩码、IBS 字段、缓存/TLB 参数具有一手技术价值，因此仍收录。此文一些预测与 [[chipsandcheese-zen3-bottlenecks|Zen 3 bottlenecks]] 文末对 Zen 4 的推测可交叉验证。

## 摘要

核侧：Zen 4 保留 Zen 3 的 4 个整数调度队列与两级 BTB 结构，未见基础取舍变化；L2 从 512 KB 翻倍到 1 MB（保持 8-way，只加 set 数而非提 associativity，换取更低延迟、代价是稍差 hitrate）；L2 DTLB 从 2048 扩到 3072，配合 page coalescing 理论可覆盖 48 MB。Genoa 支持 AVX-512F/VL/BW/CD/IFMA/DQ/VPOPCNTDQ/BITALG/VNNI/VBMI/VBMI2/BF16，featureset 对标 Ice Lake Server。L1D 自然对齐从 32 字节提到 64 字节，IBS 字段可跟踪 64 字节（512-bit）µop，推测 512-bit 数学未被拆两半；retired FLOP 每周期上限 64 对应 2×512b FMA，bfloat16 仅 1×512b。作者个人倾向 Zen 4 走 Sunny Cove 式单 512b FMA 复用（可作 2×256b），两 FMA + 两 FADD 管道。内存子系统：Storage-Class Memory（SCM）在 PMU 侧成为一等数据源，新出现 "Extension Memory"（含 GenZ）与 "Peer Agent Memory" 类别；AMD 明言 Zen 4 不做内存池化。IO 侧：每 CCD 两个 Scalable Data Port 到 Infinity Fabric、LCLK +53% 且双 IO hub、新 MPIO/MPDMA 微控制器把更多原属主板 BIOS 的职责上收进 CPU。AM5 新增 4 条 PCIe Gen4、内置 USB BIOS 更新、iGPU 大概率全系标配。作者收束观点：Zen 4 核心微架构与 Zen 3 类似，主要靠 TSMC 5nm + 扩大 L2/DTLB + AVX-512 + IO 换代拉 IPC 与生态。

## 关键要点

- L2 翻倍到 1 MB，8-way 不变（低延迟 > 高命中率的取舍）
- L2 DTLB 3072 条目 + page coalescing → 最多覆盖 48 MB
- Genoa AVX-512 featureset 对标 Ice Lake Server（含 BF16、VNNI）
- L1D 对齐从 32→64 字节；单 µop 可访问 64 字节
- retired FLOP 上限 64/cycle → 2×512b FP32 FMA，但 bfloat16 只 1×512b
- 作者猜测：单 512b FMA（可拆 2×256b）方案，更省面积
- SCM 作为一等 PMU 数据源；Extension / Peer Agent Memory 新类别
- IO：双 IO hub、LCLK +53%、MPIO 收回 BIOS 职责、MPDMA 用于页迁移
- AM5：+4 PCIe Gen4、内置 USB BIOS 刷写、iGPU 推测全系

## 判断

这是"news with technical substance"：来源不是作者自己的实测而是泄露的 PPR。许多结论（尤其 AVX-512 throughput 假设）是推断而非已证。作为技术参考需保留作者的"推测"限定词。与 [[chipsandcheese-zen3-bottlenecks]]对 Zen 4 的前瞻可形成双向印证：扩大 L2、改进 BPU、扩后端队列方向一致。

## 链接到的概念

- [[zen2-microarchitecture]]
- [[dispatch-stall-breakdown]]
- [[op-cache-decoded-uop-cache]]

## 原文

- 链接：https://chipsandcheese.com/p/details-on-the-gigabyte-leak
- 本地：`raw/articles/chipsandcheese.com/2021-08-22_details-on-the-gigabyte-leak.md`
