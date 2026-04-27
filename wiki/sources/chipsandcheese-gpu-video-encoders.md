---
tags: [source, gpu, 视频编码, nvenc, vcn, vmaf, nvidia, amd]
date: 2026-04-27
sources: 1
---

# GPU Hardware Video Encoders – How Good Are They?（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 3 月的文章，以游戏录像（Overwatch、Elder Scrolls Online）为测试素材，对比 Nvidia Turing NVENC、Pascal NVENC、AMD VCN（RDNA 2）和 libx264 软件编码在流媒体、录制、转码三个场景下的质量表现，使用 VMAF 作为主观感知质量指标。

## 摘要

文章的核心结论是：Nvidia Turing NVENC 是目前最接近软件编码质量的硬件方案，在实时流媒体低码率场景下甚至超过 libx264 faster preset；AMD VCN 整体落后于上一代 Pascal NVENC，在流媒体场景中运动处理最弱。但所有硬件编码器在转码（无实时限制、使用最高质量 preset）中均无法达到软件编码的 bitrate 效率，因为其固定功能电路难以做复杂的帧间分析。4K 录制场景下，CPU 吞吐成为软件编码的致命限制，硬件编码器反而全面领先。

## 关键要点

- VMAF 比 PSNR/SSIM 更适合评估游戏录像，因为其权重来自人类感知训练
- Turing NVENC：流媒体低码率最佳，倾向超出目标码率（用多余 bit 换质量）
- AMD VCN：4K 录制高码率时与 Nvidia 差距小，但流媒体质量落后，blocking 更明显
- 软件编码（libx264 veryslow）：转码质量最优，但 4K 实时受 CPU 瓶颈
- Pascal NVENC 仍是稳健的流媒体选项，质量与 Turing 接近
- 所有编码器在 >30 Mbps 时质量趋同；<10 Mbps 时输出质量均偏差

## 链接到的概念

- [[gpu-hardware-video-encoder]]
- [[video-codec-licensing-tradeoffs]]

## 原文

- 链接：https://chipsandcheese.com/p/gpu-hardware-video-encoders-how-good-are-they
- 本地：`raw/articles/chipsandcheese.com/2022-03-30_gpu-hardware-video-encoders-how-good-are-they.md`
