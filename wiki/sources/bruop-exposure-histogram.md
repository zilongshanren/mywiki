---
tags: [source, rendering, hdr, exposure, compute-shader]
date: 2026-04-27
sources: 1
---

# Automatic Exposure Using a Luminance Histogram（bruop.github.io）

[[bruno-opsenica|Bruno Opsenica]] 2019 年 4 月的文章，解释为什么 PBR 管线需要色调映射，并给出用 compute shader 构建 [[luminance-histogram-exposure|亮度直方图]] 来计算自动曝光的完整实现（基于 Alex Tardif 的方法）。

## 摘要

文章以 FlightHelmet glTF 模型的过曝截图开篇，说明物理光照单位（lumens、lux）产生的辐亮度值可以相差数个数量级，而显示器只能接受 [0, 1]。作者给出一个五步流水线：浮点 HDR 帧缓冲 → 求平均亮度 → 曝光缩放 → 色调曲线 → sRGB 变换。本文专注于第二步。对比两种平均亮度方案：几何平均（mip 下采样）易受极端值影响；亮度直方图更稳定。实现使用两趟 compute：第一趟 16×16 线程组借助 shared memory 局部累加、再 atomicAdd 合并到 256-bin 全局 buffer；第二趟单组 256 线程做并行归约加权平均、排除 bin0 纯黑像素、反查对数空间获得实际亮度，并用 timeCoeff 做帧间插值防闪烁。曝光公式参照 Frostbite / Filament：`exposure = 0.18 / L_avg`。完整 BGFX 示例代码开源。

## 关键要点

- 直方图 256 bin 覆盖对数亮度范围 `[minLogLum, maxLogLum]`，bin 0 专存低于阈值的像素
- Shared memory 局部累积 + atomicAdd 合并：减少全局写竞争
- 并行归约：O(log 256) 步求加权和，最后除以非零像素数
- 帧间插值 `adaptedLum = prev + (cur - prev) * timeCoeff`：防曝光闪烁
- 全文注意到一个 barrier 类型的 bug（`groupMemoryBarrier` 应为 execution+memory 两用），后来被 Graphics Programming Discord 用户修复

## 链接到的概念

- [[luminance-histogram-exposure]]
- [[tone-mapping]]

## 原文

- 链接：https://bruop.github.io/exposure/
- 本地：`raw/articles/bruop.github.io/2019-04-19_automatic-exposure-using-a-luminance-histogram.md`
