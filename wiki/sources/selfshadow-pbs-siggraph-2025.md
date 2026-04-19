---
tags: [source, 渲染, pbr, brdf, siggraph, openpbr, neural-materials]
date: 2026-04-19
sources: 1
---

# Physically Based Shading at SIGGRAPH 2025（Stephen Hill）

[[stephen-hill|Stephen Hill]] 和 Stephen McAuley 合办的 2025 年 SIGGRAPH 课程主页，距 2012 年首届已过了 13 年。Hill 本人此时已在 Lucasfilm Advanced Development Group 做 Principal Rendering Engineer（*Carne y Arena*、*The Mandalorian*），McAuley 则是 Sony Santa Monica 的 Technical Director。这一届的侧重从「游戏怎么落地 PBR」彻底转向了三条新战线：**[[openpbr|OpenPBR]] 标准化**、**neural materials 把离线质量塞进实时**、**色彩科学 / HDR tone mapping 的感知保真**。

## 摘要

- **Naty Hoffman** — Fundamentals of Physically Based Shading。这是 Hoffman 职业生涯的告别演讲——他在 Meta、Lucasfilm、2K、Activision、SCE Santa Monica、Naughty Dog、Westwood、Intel 工作数十年后正式退休，这一届是他最后一次在 SIGGRAPH PBR 课里讲「开篇」。
- **Peter Kutz（Adobe）** — OpenPBR: A Closer Look at Novel Features and Implementation Details。讲 [[openpbr|OpenPBR]] 里新加的一些特性（coat darkening、thin film、subsurface 参数化）和参考实现细节，附课程 notes 已更新到 v1.3（含 coat darkening 代码 Listing 2 的视角相关吸收修正）。
- **Peter Kutz & Stephen Hill** — EON: Advancing Rough Diffuse Reflection with Energy Preservation and Clipped LTC Sampling。把 Oren-Nayar 粗糙 diffuse 用能量守恒和裁剪 LTC 采样做成可直接替换 Lambert 的新缺省。
- **Laurent Belcour（Intel）** — Spectral Rendering in a Non-Spectral Renderer: How Can we Author and Render Fluorescence in RGB。讨论在 RGB 渲染器里作出并渲染荧光效果。
- **Alain Hostettler（ILM）** — Strand: A Production Model for Shading Hair, Fur and Feathers。ILM *Lama* 材质系统里的统一毛发 / 羽毛着色模型。
- **Andrea Weidlich（NVIDIA）** — Bridging the Gap Between Offline and Real Time with Neural Materials。NVIDIA 在 [[neural-materials|神经材质]] 上的最新进展，把 Manuka 级复杂 shader graph 压进实时可用的神经网络。
- **Yasutomi / Suzuki / Uchimura（Polyphony Digital）** — Driving Toward Reality: Physically Based Tone Mapping and Perceptual Fidelity in Gran Turismo 7。*GT7* 的物理 tone mapping 管线，附完整 C++ 参考实现 `gt7_tone_mapping.cpp`，还讲了对比敏感度函数（CSF）怎么指导 tone curve 设计。

## 关键要点

- **OpenPBR 是主线叙事**：2025 这一届的 course notes 反复勘误更新（OpenPBR notes 已到 v1.3），显示这一开放标准正在被社区严肃对待——coat darkening 的解析推导、金属参数拟合表（新增 brass / steel）都是可直接拿去实现的工程材料。
- **Neural materials 进入主会场**：Weidlich 带 NVIDIA 把「离线级别材质实时化」作为独立 session——暗示 Hoffman 那代 analytical BRDF 的路线图在走向融合。
- **GT7 的 tone mapping** 是罕见的由游戏开发商公开完整源码 + 速记 notes 的 case，对比 [[aces]] / filmic 风格有完全不同的感知驱动方法论。
- **Hoffman 退休** 是一个时代的象征——他是 1998 年以来 real-time rendering 数学基础的主要布道者之一。
- 从 changelog 看，Hill 对 course notes 的勘误节奏依然高：2025 年首次发布到 2026 年 2 月仍在持续修订（OpenPBR v1.3），继承了 [[stephen-hill]] 一贯的坦率勘误风格。

## 链接到的概念

- [[physically-based-shading]]
- [[openpbr]]
- [[neural-materials]]
- [[stephen-hill]]

## 原文

- 课程主页：https://blog.selfshadow.com/publications/s2025-shading-course/
- Changelog：https://blog.selfshadow.com/publications/s2025-shading-course/changelog/
- 本地：`raw/articles/blog.selfshadow.com/2026-01-01_siggraph-2025-course-physically-based-shading-in-theory-and.md`
