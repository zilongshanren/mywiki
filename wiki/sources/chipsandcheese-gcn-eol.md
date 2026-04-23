---
tags: [source, chipsandcheese, gpu, amd, gcn, driver, eol]
date: 2026-04-19
sources: 1
---

# The End of an Era: AMD Discontinues Pre-2016 GCN GPU Support（Apex / Chips and Cheese）

[[apex-chipsandcheese]] 2021 年 6 月的社区向复盘文章，回应 AMD 在 Radeon Driver 21.6.1 里把 Hawaii（GCN 2）和 Fiji（GCN 3）踢出支持列表的事件。

## 摘要

文章逐条证伪 AMD 隐含的技术理由：(a)"架构太旧"不成立——同驱动仍支持 GCN 1 的 Oland/Cape Verde 甚至 HD 7790 的 rebadge RX 455；Fiji（GCN 3）架构上反而更接近仍受支持的 GCN 4 Polaris；(b)"性能不够"不成立——R9 290X 仍与 RX 480/580、GTX 1060 在 1080p 上相当；(c)"为 Windows 11 让路"不成立——Windows 11 沿用 WDDM；(d)"为 FSR 优化"不成立——FSR 是 shader-level，不依赖驱动。真正原因被作者还原为市场份额：AMD dGPU 在 Steam 硬件调查约占 1/6（含集显），真实更低，已不足以支持专门 QA 投入；仍支持的低端 400 系列多是 OEM，且驱动代码路径与 500 系共享——"免费顺带"。作者把这一处理的最大问题定位在**零预告**：Nvidia 把 Kepler 转 legacy 时提前公告，AMD 同一周既上 FSR 又砍卡，让正面新闻被吞。

## 关键要点

- 21.6.1 砍掉 200/300/Fury 系列，保留更老的 GCN 1 Oland/Cape Verde
- R9 290X 在 1080p 仍对标 RX 480/580/GTX 1060
- Kepler 老 Nvidia 卡在 Windows 11 上仍受支持，Win11 非理由
- FSR 是 shader-level，21.5.2 驱动也能跑
- 真实原因：AMD dGPU 市场份额 <<1/6，QA 投入不划算
- PR 教训：砍硬件本身可以，零预告不行
- 对 Polaris 用户的推断：12–24 个月后或同样被砍

## 链接到的概念

- [[gpu-driver-support-lifecycle]]
- [[gcn-wave-occupancy]]
- [[samsung-8n-vs-tsmc-n7]]

## 原文

- 链接：https://chipsandcheese.com/p/the-end-of-an-era-amd-discontinues-pre-2016-gcn-gpu-support
- 本地：`raw/articles/chipsandcheese.com/2021-06-23_the-end-of-an-era-amd-discontinues-pre-2016-gcn-gpu-support.md`
