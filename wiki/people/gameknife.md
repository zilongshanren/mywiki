---
tags: [人物, 作者, 中国, 引擎开发]
date: 2026-04-14
sources: 4
---

# gameKnife

中国独立引擎开发者，拥有约 15 年图形与游戏开发经验。博客站点 `gameknife.github.io`，早期有博客园与 cnblogs 的发布记录。

作者自述长期深耕移动平台渲染与系统嫁接工作，知识边界一度停留在 DX11 时代。2024 年前后借 M3 Max 笔记本重新接触硬件光追，从 _Ray Tracing in One Weekend_ 起步，开源自研 Vulkan 实时光线追踪引擎 [[gknext-renderer]]。作者早年（2013–2015）在团队中主导开发过另一款跨平台商业化探索引擎 [[gkengine]]。

## 技术取向

- 渲染技术路线：从传统延迟着色、[[tbdr-vs-imr|Tile-Based 架构]] 优化，到硬件光追、[[visibility-buffer|Visibility Buffer]]、[[bindless-rendering|Bindless]]、[[hybrid-raytracing-pipeline|混合光追管线]]。
- 强调跨平台工程化：Vulkan + vcpkg + GitHub Actions CI，覆盖 Windows / macOS (MoltenVK) / Android (骁龙 8 Gen 2) / SteamDeck。
- 对 shader 语言、包管理、编辑器架构等"现代化"基础设施持积极态度（slang、imgui、quickjs、tinybvh）。
- 年度总结式的博客风格，擅长从"一个从业者重新学习"的视角串联新旧技术栈。

## 相关

- [[gknext-renderer]]
- [[gkengine]]
- [[engine-evolution]]
- [[tbdr-vs-imr]]

## Sources

- [[sources/gameknife-gknextrenderer-yearone]]
- [[sources/gameknife-tbdr-performance-tuning]]
- [[sources/gameknife-pathfinding-review]]
- [[sources/gameknife-gkengine-features]]
