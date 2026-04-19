---
tags: [source, 渲染, 路径追踪, hyperion, disney-animation]
date: 2026-04-19
sources: 1
---

# Moana 2（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 于 2024 年 12 月发表的《Moana 2》回顾文章，从制作人员视角回溯 Disney Animation 第 63 部动画长片、也是 Hyperion 的第 10 部影片；重点在 Moana（2016）到 Moana 2 之间这十年 Hyperion 与产线的演化。

## 摘要

作者以「用 Hyperion 做 Hyperion 处女作的续集」为切口，列出一份非常长的技术差量清单：体积渲染整套重写为 state-of-the-art delta tracking；traversal 支持世界级尺度几何；ray self-intersection 彻底抛弃 bias；photon mapping 从太阳↔水面扩展到全部光源 + 光谱色散；SSS 从 normalized diffusion 换成 brute-force 路径追踪；眼睛用 manifold NEE 虹膜焦散；引入 path guiding；降噪换成获 2025 奥斯卡科技奖的二代深度学习降噪器。整个管线从自研数据格式换到了 USD。作者个人在 Moana 2 上主导了两件事：水渲染从 levelset-compositing 换成 ray-intersection-time CSG，把一个需要半打工程师维护的系统瘦身到他一人兼职维护；以及第三幕风暴的体积渲染，甚至为单镜头提供定制 Hyperion build。

## 关键要点

- Hyperion 内部版本号：Moana 3.x → Moana 2 16.x，每个整数都是一次重大改造。
- Moana 2 水渲染：抛弃 levelset compositing + meshing + 夜间预缓存这套重型管线，改用 ray-intersection-time CSG，零预处理、零磁盘缓存、对 ray tracing 性能影响可忽略，且几何 LOD 不再受世界级 levelset 网格分辨率限制。
- 基于下一代交互式 GPU ray tracing 灯光系统在 Moana 2 上首次广泛部署，其中 GPU Ptex 是关键组件（参见 [[ptex-gpu-streaming]]）。
- Chiang 毛发模型自 Zootopia 2016 诞生以来几乎没动过，已成行业事实标准；体现「好算法十年不用改」。
- Disney 做 R&D 的哲学：造轮子但要发论文；APIC 流体方法、FAB 流体边界方法已被 Houdini stock SOP 收编，让 Moana 2 能在更高抽象上做水特效。

## 链接到的概念

- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[path-guiding-production]]
- [[ptex-gpu-streaming]]

## 原文

- 链接：https://blog.yiningkarlli.com/2024/12/moana-2.html
- 本地：`raw/articles/blog.yiningkarlli.com/2024-12-18_moana-2.md`
