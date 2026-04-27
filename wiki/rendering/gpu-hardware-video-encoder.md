---
tags: [gpu, 视频编码, nvenc, vcn, h264, vmaf, 固定功能硬件]
date: 2026-04-27
sources: 1
---

# GPU 硬件视频编码器：固定功能 vs 软件编码的权衡

现代 GPU 都搭载专用的硬件视频编码单元（Nvidia 称 NVENC，AMD 称 VCN/VCE），其设计目标是在不占用 CPU 和着色器资源的前提下完成实时编码。Chester Lam 在 2022 年用 Overwatch 和 Elder Scrolls Online 的实战录像对 Turing NVENC、Pascal NVENC、AMD VCN（RDNA 2）和软件编码 libx264 进行了系统比较，以 Netflix 的 **VMAF** 指标衡量主观质量。

## VMAF：感知质量的量化

VMAF（Video Multimethod Assessment Fusion）由 Netflix 开发，结合多个子指标，并以机器学习模型对各子指标加权——权重来自人类观看者对"极好/好/一般/差/很差"的主观评分。输出分数 0–100，100 对应"极好"，80 对应"好"，60 对应"一般"。实际使用中 90+ 才算视觉干净。

相比传统 PSNR/SSIM，VMAF 对运动和细节的权衡更符合人眼感知，尤其适合评估有 HUD 元素、快速摄像机移动的游戏录像。

## 三种场景下的表现对比

### 流媒体（固定码率，1080P）

流媒体要求码率不能超出带宽上限，且必须实时，给编码器留出的分析时间极少。

- **Turing NVENC** 在简单场景（Overwatch，快速镜头移动）可与 libx264 faster preset 持平甚至领先；在复杂场景（ESO raid，大量粒子特效）被软件编码反超。NVENC 倾向于码率轻微超出目标值，用多余 bit 换质量。
- **Pascal NVENC** 与 Turing 相近，整体略逊。
- **AMD VCN**（RDNA 2）在所有场景中垫底，尤其在运动剧烈时 blocking 更严重，UI 文字周围伪影更多。

### 录制（可变码率，4K）

录制无需严格控制码率，可以在更高码率下操作。CPU 在此场景受限于需要实时处理 4K——单 CCX Zen 2 @ 3.5 GHz 最快只能用 ultrafast preset，把灵活性全部牺牲掉。

- 硬件编码器全面反超软件编码：GPU 固定功能单元的吞吐碾压 CPU 的分析能力。
- **Turing** 依然领先，**Pascal** 和 **VCN** 同档，但与 Turing 差距小于流媒体场景，因为高码率下差异趋于消失。

### 转码（慢速离线，最高质量 preset）

转码不受实时限制，软件编码可以用 veryslow preset 充分展示其分析能力。

- **libx264** 以明显优势领先：在相同 VMAF 目标下需要更少的 bit，bitrate efficiency 明显更好。
- **Turing** 次之，**Pascal** 和 **VCN** 并驾齐驱。
- 高码率（>30 Mbps）时各编码器 VMAF 收敛，质量差异可忽略；低码率（<10 Mbps）时所有编码器输出均较差。
- VCN 的编码速度几乎不随 quantization parameter 变化（44–45 FPS），而 NVENC 和 libx264 随质量参数有明显速度变化。

## 核心权衡

| 维度 | 硬件编码器 | 软件编码（libx264）|
|------|----------|-----------------|
| 实时 4K 录制 | 优势显著 | 受 CPU 吞吐限制 |
| 流媒体（低码率质量） | NVENC 领先，VCN 弱 | 受 CPU 实时限制 |
| 转码 bitrate 效率 | 次于软件 | 最优 |
| 灵活性 | 固定功能，分析简单 | 可做复杂 rate control |
| 功耗影响 | 不占 shader | — |

硬件编码器的本质是**速度与灵活性的取舍**：固定电路极快，但分析逻辑简单，无法像软件那样做复杂的帧间预测和率失真优化。结论是：

- 实时流媒体/录制 → Turing NVENC 是最接近软件编码质量的硬件方案
- AMD VCN 在高码率录制时"够用"，但流媒体质量有差距
- 纯离线转码且有足够 CPU → 软件编码质量更好

## 参见

- [[video-codec-licensing-tradeoffs]] — H.264/HEVC/AV1 的 codec 选型
- [[jpeg-codec-pipeline]] — 图像编解码的固定功能 pipeline 对比
- [[async-compute]] — GPU 固定功能单元与 shader 的并行调度

## Sources

- [[sources/chipsandcheese-gpu-video-encoders]]
