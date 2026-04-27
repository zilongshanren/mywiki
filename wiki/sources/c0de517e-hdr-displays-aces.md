---
tags: [source, graphics, hdr, aces, 色调映射, 显示校准]
date: 2026-04-27
sources: 1
---

# Tonemapping on HDR displays. ACES to rule 'em all?（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2017 年 2 月的文章，批评游戏业在 HDR 显示时代跟风采用 ACES 的倾向，并提出更务实的 HDR TM 框架。

## 摘要

2016–2017 年 HDR 显示刚进入消费市场，业界快速形成了一个共识：用 ACES RRT（Reference Rendering Transform）做 tone mapping，再配上针对目标显示器的 ODT（Output Display Transform）。Pesce 对此表示怀疑，并逐条拆解。

他的主要论点：ACES 是为电影制作设计的，其目标是标准化多机构协作的色彩管线，并给电影人提供"胶片感"基准。这两个目标对游戏都不成立——游戏不混用多供应商素材，也不需要向电影调色师致敬。HDR 游戏面临的真正问题是**显示校准**：不同 HDR 屏的峰值亮度从 400 nit 到 1000 nit 差异极大，观看环境更是无法控制。ACES 的 ODT 把输出锁定到特定 nit 档，这对动态变化的观看条件并不合适。

更好的方案（Pesce 在更新中也同意）是：用一条简单的固定形状曲线把渲染输出压缩到便于 grading 的中间空间，由艺术家在这个空间完成所有外观决策（3D LUT），最后再用一条依赖显示能力和环境的小曲线做最终的 display-referred 输出。这与 Timothy Lottes 的 VDR color pipeline 思路一致。

## 关键要点

- HDR 显示需要 tone mapping，原因：TV 本身是 display-referred，而非 scene-referred
- ACES RRT 设计目标：电影标准化 + 胶片感，均与游戏无关
- HDR 游戏最紧迫的问题是**校准**：适应不同峰值 nit 和观看环境
- 正确架构：scene → 固定压缩（便于 grading） → 3D LUT grading → 自适应显示曲线
- 胶片曲线（S 曲线）有价值，但不应委托给 TM 算子；grading LUT 可以实现同样效果且更可控
- ACES 的社区评论澄清：ACES 对引擎的价值是资产共享标准化（Substance 等），与"好看"本身无关

## 链接到的概念

- [[aces-hdr-display-calibration]]
- [[local-tonemapping]]
- [[hdr-video-edr-metal]]
- [[color-lut]]
- [[filmic-post-processing-critique]]
- [[in-game-display-calibration]]

## 原文

- 链接：https://c0de517e.blogspot.com/2017/02/tonemapping-on-hdr-displays-aces-to.html
- 本地：`raw/articles/c0de517e.blogspot.com/2017-02-23_tonemapping-on-hdr-displays-aces-to-rule-em-all.md`
