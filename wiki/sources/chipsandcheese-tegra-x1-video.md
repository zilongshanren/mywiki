---
tags: [source, gpu, nvidia, tegra, video-encode, hevc, h264, nintendo-switch, maxwell]
date: 2026-04-27
sources: 1
---

# Examining the Nintendo Switch (Tegra X1) Video Engine（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 6 月的文章，通过 Linux 环境下的 ffmpeg 测试，对比 Tegra X1 与桌面 Maxwell（GTX 980 Ti）及 Intel QuickSync（Skylake）的硬件视频编解码能力。

## 摘要

Tegra X1 采用与桌面 Maxwell 完全不同的视频引擎——这一细节令人意外。桌面 Maxwell 支持 HEVC 编码但不支持 HEVC 解码；Tegra X1 反而两者都支持，且 HEVC 编码速度在考虑实际码率后甚至反超 Maxwell。文章通过 H264 和 HEVC 的可变码率转码测试（VMAF 质量评估 + 实测帧率），发现三个编码器各有特点：Maxwell NVENC 低码率效率最好但倾向于欠射码率目标；Tegra X1 能精准命中码率目标；Intel QuickSync 速度最快但 HEVC 质量最差。视觉比较显示 Tegra X1 倾向于保留细节（但有边缘光晕），Maxwell 倾向于平滑处理，QuickSync 则出现明显块状失真。文章认为，NVIDIA 为一个 10W 移动 SoC 专门设计了全新视频引擎而非复用桌面版本，体现了当时 NVIDIA 的庞大工程资源。

## 关键要点

- Tegra X1 H264 解码性能足以处理 4K@60fps 单流，但单流速度低于桌面 Maxwell
- Tegra X1 HEVC 编解码完整支持，Maxwell 桌面版无 HEVC 解码
- Tegra X1 码率控制精准度优于 Maxwell（Maxwell 欠射约 20%）
- 两款 NVIDIA 编码器在高码率下与软件编码质量接近
- L4T 特定的 ffmpeg 编解码器参数与主流 NVENC/cuvid 不兼容

## 链接到的概念

- [[tegra-x1-video-engine]]
- [[gpu-hardware-video-encoder]]
- [[video-codec-hevc-av1-vvc]]

## 原文

- 链接：https://chipsandcheese.com/p/examining-the-nintendo-switch-tegra-x1-video-engine
- 本地：`raw/articles/chipsandcheese.com/2024-06-28_examining-the-nintendo-switch-tegra-x1-video-engine.md`
