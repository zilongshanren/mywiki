---
tags: [渲染, hdr, aces, 色调映射, 显示校准, color-grading]
date: 2026-04-27
sources: 1
---

# ACES 与 HDR 显示校准

随着 HDR 消费显示器（HDR10、Dolby Vision）的普及，游戏业在 2016–2017 年形成了一个快速共识：用 **ACES RRT**（Reference Rendering Transform）做 tone mapping，再用对应显示标准的 **ODT**（Output Display Transform）输出。[[angelo-pesce]] 和其他工程师（如 [[krzysztof-narkowicz]] 的博客分析）对此提出了质疑，推动了更系统的 HDR 色彩管线思考。

## ACES 的原始设计目标

ACES 由  AMPAS（电影艺术与科学学院）主导，核心目标是：

1. **多机构协作的色彩管线标准化**：不同摄影机、不同 VFX 机构的素材可以在同一个色彩空间里混合
2. **胶片感基准**：RRT 建模于 film stock，让电影人在数字工具上看到熟悉的"胶片感"输出

这两个目标对游戏都不成立：游戏不混用多供应商素材，也不需要向电影调色师提供熟悉的基准。评论区有人指出，ACES 在引擎里的真正价值是**资产共享标准化**——如果 Substance Painter 和游戏引擎都用 ACES，材质在两个工具里的外观会更一致。这是一个合理但有限的理由，远不足以支撑"ACES 是 HDR 游戏的正确 TM 方案"的宣称。

## HDR 显示的真正难题：校准可变性

SDR 时代虽然显示器质量参差不齐，但大家都在 100 nit 附近，sRGB 色域，差异相对可控。HDR 时代的问题更严峻：

- 峰值亮度从 400 nit（入门 HDR）到 1000 nit（HDR1000），差 2.5 倍
- 观看环境亮度影响感知对比度，暗室和阳光下的观感完全不同
- OLED 和 LCD 的黑场行为完全不同（HDR OLED 在黑色有真正零亮度，LCD 有光晕）

ACES 的 ODT 是为特定 nit 档（400/1000/2000/4000 nit）分别设计的，假设显示器能力已知且固定。但游戏上市后运行在用户家里，我们根本不知道用户屏幕的实际能力。把 TM 锁定到一个固定的显示能力目标，恰恰是 Pesce 认为的"cop-out"：把不确定性推给设备，而不是主动适配。

## 推荐架构：分离 look 与 calibration

Pesce 在文章更新中认同了 Timothy Lottes（VDR color pipeline，GDC 2016）描述的方案：

```
scene linear HDR
      ↓
[固定压缩曲线]   ← 目的：把高光卷肩到方便 grading 的中间空间，不承担 look 职责
      ↓
[3D LUT grading] ← 艺术家在这里做所有外观决策（对比、色调、风格化）
      ↓
[自适应显示曲线] ← 依赖目标显示器的 nit 能力和实际 headroom 动态调整
```

关键原则：**look 决策在 grading 层，校准决策在最后一步**。这让艺术家不需要为每种显示器重做 grading，只需要调整最后一步的校准参数（或让用户自己调）。

与此相对，把 ACES RRT 直接作为最终输出曲线，等于把 look（胶片感）和 calibration（适配 1000 nit 显示）混在了同一条曲线里，两者都做不好。

## 与 SDR 游戏的历史教训

Pesce 提到，SDR 时代大家也没认真对待显示校准——大量游戏有 gamma 校准界面，但几乎没有人认真设计这个校准流程。HDR 时代变化如此之大，继续用随意的方法不可接受。[[in-game-display-calibration]] 页面记录了这类实践的现状。

苹果的 [[hdr-video-edr-metal|EDR 方案]] 是另一种思路：把显示 headroom 的计算交给 OS，应用只需声明"我的 EDR 值 > 1.0 表示超白"，系统自动根据当前屏幕能力做适配。这避免了应用层硬编码 nit 目标的问题。

## 相关

- [[local-tonemapping]]
- [[hdr-video-edr-metal]]
- [[color-lut]]
- [[filmic-post-processing-critique]]
- [[in-game-display-calibration]]
- [[gamma-correction-srgb]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-hdr-displays-aces]]
