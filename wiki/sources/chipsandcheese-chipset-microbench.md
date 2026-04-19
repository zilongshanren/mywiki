---
tags: [source, pcie, chipset, platform]
date: 2026-04-19
sources: 1
---

# Microbenchmarking Chipsets for Giggles（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2026 年 3 月的主板 chipset 对 PCIe 延迟/带宽影响的实测。

## 摘要

chipset 自从内存控制器和 PCIe 都被集成进 CPU 后已退出性能关键路径。但通过把 GPU（Nvidia T1000，单槽 PCIe Gen3 x16）分别插 CPU 直连与 chipset 下挂的槽，用 Nemes Vulkan benchmark 让 GPU 访问 host memory，可以测出 chipset 带来的额外延迟——每级 chipset chip 增加约 500–600 ns。AM5 X670E 挂两颗 PROM9 惩罚翻倍（+921 ns），老 Skylake Z170 反而最好（+338 ns）。文章还揭示 `HOST_COHERENT_BIT` + cache hit 会引发异常 probe 流量，probe 吞吐成为 GPU cache hit 带宽的隐蔽瓶颈。

## 关键要点

- AMD AM5 B650：CPU 650 ns → chipset 1221 ns（+570）
- AMD AM5 X670E 双 PROM21：+921 ns
- Intel Arrow Lake Z890：+550 ns
- Intel Skylake Z170：+338 ns
- AMD AM3+ 990X + SB950：+602 ns（架构老但单级 hop）
- GPU cache hit 带宽被 chipset 压住（25 GB/s，T1000 本地 132+ GB/s）
- probe 粒度貌似 512 B 而非 64 B——未解之谜
- 未来 chipset 不会优化延迟，因为服务的设备都是 µs/ms 级

## 链接到的概念

- [[chipset-pcie-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/microbenchmarking-chipsets-for-giggles
- 本地：`raw/articles/chipsandcheese.com/2026-03-22_microbenchmarking-chipsets-for-giggles.md`
