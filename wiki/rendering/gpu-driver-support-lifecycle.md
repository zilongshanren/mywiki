---
tags: [gpu, amd, driver, gcn, eol, legacy]
date: 2026-04-19
sources: 1
---

# GPU 驱动支持生命周期：AMD 砍 GCN 2/3 的理由

2021 年 6 月 AMD 在 Radeon Driver 21.6.1 里悄悄把 Hawaii（GCN 2）和 Fiji（GCN 3）踢出支持列表——包括 R9 290/290X、R9 390/390X、Fury/Fury X。时机正好是 Windows 11 公布和 FSR 上线前夜，社区骂声不小。Apex / Chips and Cheese 的这篇复盘把厂商给出的技术理由逐一证伪，指向一个更赤裸的答案：市场份额。

## 技术理由都站不住

- **"架构太老"**：21.6.1 里**仍支持** GCN 1 的 Oland / Cape Verde（R5 430/435、R7 430/435/450）和 Bonaire（RX 455，HD 7790 的 rebadge）。GCN 1 比 GCN 2/3 更老；Fiji 架构上反而更接近仍然被支持的 GCN 4（Polaris）
- **"性能不够"**：R9 290X 至今在 1080p 下约等同 RX 480 / RX 580 / GTX 1060，仍是主流 1080p 卡。R5 430 被砍的对象远远超过
- **"为 Windows 11 让路"**：Windows 11 用同一 WDDM 驱动模型，Kepler 这代 Nvidia 旧卡仍受支持
- **"为 FSR 优化"**：FSR 是 shader-level，不依赖驱动，Fury X 实测跑得动

## 真实原因

Apex 的结论简洁：AMD dGPU 在 Steam 硬件调查里约占 1/6（含集显），真实独立显卡份额更低。200/300/Fury 系列的持卡用户是"fraction-of-a-fraction-of-a-fraction"，继续投入 QA 不划算。仍保留支持的低端 400 系列大多是 OEM 模型，且驱动与仍在售的 500 系共用代码路径——"免费顺带"。

这与 [[samsung-8n-vs-tsmc-n7]] 所揭示的更大背景一致：AMD 对手 Nvidia 有近 5 倍市值，能承担更长的 legacy 支持。AMD 在组织资源上无法同时做好新架构推进 + 老架构 QA。

## PR 层面的教训

作者强调问题不在砍，而在**零预告**。Nvidia 把 Kepler 转 legacy 时提前公告；AMD 同一周既推 FSR 又砍老卡，让正面新闻被负面反噬。对行业从业者的启示是显而易见的：硬件 EOL 的时间点和话术都可以设计得更温和，成本为零。

## Polaris 用户的警示

作者在结尾留给 RX 480/580 用户一句话："expect 12–24 months"——事实上 Polaris 之后也确实走完同路。这一节奏给游戏开发者评估"最低支持硬件"提供了粗略参考：以 AMD 的现行节奏，发布日起向后推 6–7 年就是驱动支持底线，游戏若要跑满这个区间就不能依赖驱动级修复。

## 延伸：FSR 作为 legacy 卡的救济

讽刺的是 GTX 980 Ti（Maxwell）同期接受 FSR，被媒体用作正面案例——AMD 自家 Fury X 却被切掉驱动支持。FSR 在 shader 层实现无关驱动版本的事实让老卡用户还能再榨 1–2 年，这也是 [[rdna1-overclocking-navi10]] 所在社区（把老卡吃到骨髓）的共同语境。

## Sources

- [[sources/chipsandcheese-gcn-eol]]
- [[sources/asawicki-gpu-state-2025]] —— 2025 年底 D3D12 硬件覆盖率调查：AMD RDNA1/2 进入独立驱动分支，Turing EOL 暂不临近，Intel Xe 时间线最难预测
