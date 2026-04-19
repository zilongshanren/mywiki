---
tags: [渲染, 云渲染, 云游戏, GPU, OTOY, 历史]
date: 2026-04-19
sources: 1
---

# OTOY 的早期云渲染架构（2010）

2010 年 OTOY 为 SolidWorks 在云端做 CAD 演示时公开的渲染/编码架构。Jules Urbach 当年接受媒体采访时讲过几个具体数字，是理解"云游戏"这个词早期工程约束的一个难得注脚。[[sam-lapere|Sam Lapere]] 在博客上转述了这些细节。

## 核心问题：延迟预算

客户端远离服务器时，用户可感的延迟 = 带宽 + 物理距离 + 图像分辨率/压缩率 + 服务器渲染速度。OTOY 的工程目标是把总延迟压到 **16 ms 以内**，对应服务器与客户端之间最大约 **1000 mile** 的物理半径。作为对照：

- SF ↔ NY（约 3000 mile）：85 ms
- SF ↔ 日本：约 100 ms

Urbach 同时强调**分发拓扑**才是真正的解——类似 Akamai 在全球部署边缘节点，只有把服务器推到用户 1000 mile 内才能满足游戏级体验。这一设计直觉在十多年后的 Stadia / GeForce Now / xCloud 中仍然成立。

## 硬件：AMD RV770

OTOY 在这一阶段的 GPU 选型是 AMD **RV770**——HD 4800 系列的核心：

- 800 个 stream processor
- 2 GB 显存，256-bit 总线，115 GB/s 带宽

Urbach 的说法是"每个 vector core 只要几分钱"，也就是用海量低成本并行核心摊薄单帧成本。这个经济学直接决定了之后所有云游戏厂商的设备选型思路——单位像素的 compute 必须比传统游戏 PC 便宜一个量级才撑得住多用户共享。

## 编码吞吐

OTOY 声称在该硬件组合上可以做到：

- 实时编码到 **3840 × 2160** 分辨率
- **1080p 每帧 1 ms**，即 1000 fps 的编码能力

1000 fps 的编码速度不是为了真的输出 1000 fps，而是**在渲染与编码之间腾出延迟预算**：渲染 + 编码 + 网络 + 解码 + 显示的总和必须塞进一个刷新周期。编码耗时被压到毫秒级后，整条流水线的瓶颈才会从编码转移回网络。

## 与当时 GPU 渲染潮的关系

OTOY 这条云渲染线与 [[gpu-unbiased-path-tracing|2010 GPU 非偏置渲染器大爆发]]是**同一波硬件红利**的两种兑现方式：一部分厂商把 GPU 算力拿去做**离线渲染器加速**（Octane、iray、V-Ray RT），OTOY 则把它拿去做**云端实时编码 + 远程呈现**。后来 Octane 本身也进了 OTOY，两条线合流。

## 相关

- [[sam-lapere]]
- [[gpu-unbiased-path-tracing]]
- [[nvidia-omniverse]]

## Sources

- [[sources/raytracey-otoy-solidworks-cloud]]
