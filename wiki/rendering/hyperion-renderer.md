---
tags: [渲染, 路径追踪, 离线渲染, disney-animation, hyperion, 生产渲染器]
date: 2026-04-19
sources: 4
---

# Hyperion Renderer

**Disney's Hyperion Renderer** 是 Walt Disney Animation Studios 的自研生产路径追踪器，自 *Big Hero 6*（2014）起为所有迪士尼动画长片服务，到 *Moana 2*（2024）已经是第 10 部，到 *Zootopia 2*（2025）是第 11 部。名字源自土星的卫星 Hyperion，早年以「批处理 wavefront 渲染器」的架构闻名。

## 架构要点

- **Wavefront 风格**：不把一整条 ray 路径顺着跑到底，而是把同一 bounce 的大量样本分批处理，便于 shader sort 与缓存友好（Eisenacher et al. 2013，Sorted Deferred Shading）。见 [[wavefront-path-tracing]]。
- **Ptex 为底座**：表面纹理一律用 per-face Ptex（Burley & Lacewell 2008），避免 UV 拆分；这也是 [[ptex-gpu-streaming]] 讨论的约束来源。
- **光照侧**：按需使用 [[path-guiding-production]]，many-lights 重要性采样（Li et al. 2024），photon mapping 用于焦散，delta-tracking 异构体积渲染（Kutz et al. 2017、Huang et al. 2021）。
- **BSDF**：Disney BSDF 系列，包括 Chiang 毛发模型、Chiang 次表面散射（brute-force path traced SSS）、Chiang & Burley 2018 眼虹膜焦散（manifold NEE）、Zeltner 2022 LTC sheen。
- **降噪**：第二代深度学习降噪器，由 Disney Research Studios、Disney Animation、Pixar、ILM 合作开发，获 2025 奥斯卡科技奖（Vogels et al. 2018、Dahlberg et al. 2019）。
- **管线**：Moana 时期依赖大量自研数据格式，Moana 2 起已全量迁到 USD（Miller 2022、Vo 2023、Li 2024、Zhuang 2025），灯光工作流甚至换到 Houdini DCC 也没伤到管线。
- **内部版本号**：Moana（2016）时 Hyperion 3.x，Moana 2 时 16.x——每个整数版本号都代表一次重大改造。

## 从 Moana 到 Moana 2 的十年演进

*Moana 2* 是首次用 Hyperion 做 Hyperion 处女作的续集，Yining Karl Li 的博客里列了一长串十年内的改进：

- **体积渲染**：整套从头重写，变成 state-of-the-art delta tracking 系统。
- **遍历**：改造成线程可扩展 + rebraiding，专门应对 Moana 一代在海面和岛屿几何上遇到的世界级尺度问题（Burley et al. 2018）。
- **Ray self-intersection**：新系统彻底抛弃 bias 值，解决 Maui 羽毛这类疑难。
- **Photon mapping**：从只在太阳↔水面之间的受限版本，扩展到支持全部光源类型、主要光照功能、甚至包含光谱色散。
- **SSS**：从 normalized diffusion 迁移到 brute-force 路径追踪 SSS。
- **眼睛**：从 ad-hoc shader 升级到物理合理的眼模型 + manifold NEE 虹膜焦散。
- **Path guiding**：从无到有，并在 Moana 2 做了二代的原型研究，到 *Zootopia 2* 大规模部署——12% 镜头采用（[[path-guiding-production]]）。
- **Fractured mesh / 细分**：Burley & Rodriguez 2022 的 fracture-aware tessellation，让大规模破碎特效容易做。
- **GPU 实时预览**：Hyperion 并非 GPU 渲染器，但团队开发了基于 GPU ray tracing 的下一代交互式灯光系统，Moana 2 是首次广泛部署；它用 [[ptex-gpu-streaming]] 解决纹理瓶颈。
- **Moana 2 水渲染重做**：把一代基于 levelset 合成 + meshing + 夜间预缓存的重型系统，替换成「交点时 CSG」：运行时不预处理、无磁盘缓存、无性能负担，也终结了需要半打工程师维护的局面。

## Moana 2 存留下来的东西

并非所有都改了——Chiang 毛发模型（Chiang et al. 2016）自 *Zootopia*（2016）引入后几乎没动过，已成行业事实标准。

## 相关

- [[wavefront-path-tracing]]
- [[path-guiding-production]]
- [[ptex-gpu-streaming]]
- [[nested-dielectrics]]
- [[yining-karl-li]]

## Sources

- [[sources/yiningkarlli-moana-2]]
- [[sources/yiningkarlli-zootopia-2]]
- [[sources/yiningkarlli-texture-streaming-siggraph2025]]
- [[sources/yiningkarlli-path-guiding-siggraph2025]]
