---
tags: [人物, 作者, 渲染, 路径追踪, disney-animation]
date: 2026-04-19
sources: 4
---

# Yining Karl Li（李一宁）

**Yining Karl Li** 是 Walt Disney Animation Studios 的渲染工程师，自 2013 年加入以来长期在 Hyperion Renderer 开发团队，参与了从《Moana》《Zootopia》到《Moana 2》《Zootopia 2》等 10 部以上影片的产线渲染。个人博客 [blog.yiningkarlli.com](https://blog.yiningkarlli.com/)（Code & Visuals）以制作人员视角记录生产级路径追踪渲染器的演进与具体工程问题，是少有能从影片里指出「这一帧某个效果是我写的代码」的一手叙述。

## 背景

- 宾夕法尼亚大学 CGGT 出身，早年参与过 Pixar Undergraduate Program 与 Optix 路径追踪预览（RTP）。
- 在 Disney Animation 主要负责 Hyperion 的核心渲染算法与生产支持；包括 shadow terminator 修正、many-lights 重要性采样、volume rendering、水面渲染等。
- 以合著者身份署名多篇 Disney Animation 关于 Hyperion 的 SIGGRAPH/TOG 论文与 course notes（Burley et al. 2018、Chiang et al. 2019、Huang et al. 2021、Li et al. 2024、Reichardt et al. 2025、Lee et al. 2025）。

## 风格

- **从制作视角讲技术**：每篇博客都以影片上映后个人回顾为主线，技术细节指向对应的论文与 course notes，而不是重写一遍。
- **强调「第二次做一遍的价值」**：引 Mythical Man-Month 第 11 章，把 Moana→Moana 2 的水渲染、一代到二代 path guiding、RTP→GPU Ptex 纹理流送都视为「第一次写完是用来扔掉的」。
- **写生产细节**：例如 Moana 2 第三幕风暴为单镜头提供定制 Hyperion build，Zootopia 2 渲染团队在资产建模阶段就介入性能审查，这类细节只有产线内部才写得出来。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Moana 2（2024-12） | [[hyperion-renderer]]、[[wavefront-path-tracing]]、水渲染 CSG、photon mapping、二代 denoiser |
| SIGGRAPH 2025 Talk — A Texture Streaming Pipeline for Real-Time GPU Ray Tracing（2025-08） | [[ptex-gpu-streaming]]、LRU 纹理缓存、cuckoo hash |
| SIGGRAPH 2025 Course — Path Guiding Surfaces and Volumes in Hyperion（2025-08） | [[path-guiding-production]]、OpenPGL、wavefront 下的 path guiding |
| Zootopia 2（2025-12） | [[nested-dielectrics]]、[[path-guiding-production]] 首次大规模上线、Chiang 毛发模型在续集上的维护 |

## 相关

- [[hyperion-renderer]]
- [[wavefront-path-tracing]]
- [[path-guiding-production]]
- [[ptex-gpu-streaming]]
- [[nested-dielectrics]]

## Sources

- [[sources/yiningkarlli-moana-2]]
- [[sources/yiningkarlli-texture-streaming-siggraph2025]]
- [[sources/yiningkarlli-path-guiding-siggraph2025]]
- [[sources/yiningkarlli-zootopia-2]]
