---
tags: [source, chipsandcheese, gpu, amd, rdna, overclocking]
date: 2026-04-19
sources: 1
---

# RDNA 1 Redux: Maximizing Performance With RX 5000 Series GPUs（Chips and Cheese）

[[chips-and-cheese]] 2021 年 4 月发表的 Navi 10 超频实操指南，署名为"Chips; Cheese"（集体作者），面向 2021 年 GPU 荒中仍握有 RX 5700/5700 XT/5600 XT 的用户。

## 摘要

文章把 Navi 10 超频拆成三层递进：Wattman 基础超频（+5% Firestrike / +19% 功耗）、跨型号 BIOS 刷写（累计 +14.57% 性能 / +70% 功耗）、以及 More Power Tool + VBIOS 修改（功率限制 +99%、2150 MHz core、1000 MHz memory、VRAM timing 从 1550 MHz block 下移）。作者自述用 RX 5700 风冷刷到 2150 MHz core + 1930 MHz VRAM 的 Timespy 成绩 9990，据其所知是当时最高风冷记录。讨论中最有意思的遗留悬念是"SOC Maximum Clock"参数——作者把它从 1350 推到 1500 MHz 拿到额外增益，但 AMD 未公开该参数控制的具体单元，作者原以为是 memory controller 到 L2 fabric 的时钟，但内存延迟数据不支持这一假说。

## 关键要点

- RX 5700 非 XT 版常因 yield（shader/logic 损伤）降级而非时钟瓶颈，超频余量大
- 跨型号 BIOS 刷写必须 PCB 相同，否则砖机
- VRAM timing 1550 MHz block 往下复制能改善带宽密集场景的 1% 低帧
- SOC Maximum Clock 参数功能未公开，实测把它拉高时功耗反而下降
- 2150 MHz 以上需 LN2 或极好 bin 才稳

## 链接到的概念

- [[rdna1-overclocking-navi10]]

## 原文

- 链接：https://chipsandcheese.com/p/rdna-1-redux-maximizing-performance-with-rx-5000-series-gpus
- 本地：`raw/articles/chipsandcheese.com/2021-04-23_rdna-1-redux-maximizing-performance-with-rx-5000-series-gpus.md`
