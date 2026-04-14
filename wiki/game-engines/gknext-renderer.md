---
tags: [游戏引擎, 渲染器, 开源, 光线追踪]
date: 2026-04-14
sources: 1
---

# gkNextRenderer / gkNextEngine

[[people/gameknife|gameknife]] 2024 年五一期间在 _Ray Tracing in One Weekend_ 的基础上启动的开源项目，定位是"**一个征战 15 年的老兵，回到初心，重新学习现代渲染**"。2025 年 5 月的 YearOne 总结里，作者已经把它发展成了一个中等规模的 Vulkan 实时光追引擎，tag 也从 _Realtime PathTracer_ 演进到 _gkNextEngine_。

## 动机

作者坦言自己的渲染知识停留在 DX11 / PS3 晚期 / PS4 早期时代：硬件光追、bindless、temporal jitter、样本重用等 2018 年之后的革命他都"错过了"。买了一台 M3 Max 笔记本后，从苹果官方例子入手理解硬件光追，再转到 Vulkan + RayTracingInOneWeekend 的阅读，一路做到了完整的实时路径追踪与混合渲染器。

## 技术栈

- **图形 API**：Vulkan（通过 MoltenVK 跑在 macOS/iOS，靠 Android 原生 Vulkan 跑在骁龙 8 Gen 2 / 865）。
- **Shader 语言**：glsl → hlsl → slang，一次迁移几乎"一行不用改"，换来泛型、module、interface 与自动微分。
- **包管理**：vcpkg + CMake，让跨平台自编译近乎零成本。
- **CI**：GitHub Actions 每个 PR 跑跨平台编译。作者每周用 Mac / Android / SteamDeck 跑一次阶段产物做运行时验证。
- **脚本**：quickjs（而不是 V8——后者"比 gkNextRenderer 还大几倍"）。
- **加速结构**：tinybvh 单头文件 CPU/GPU BVH，和 GPU 的加速结构完全同构，支持 ARM NEON。
- **UI / 编辑器**：ImGui，作者"之前对它不齿"，结果做出一个具备 Outliner / Content Browser / Property Editor / 节点材质编辑面板的 UE5-like 编辑器。

## 渲染管线

- **纯路径追踪**：RTIO 式朴素实现 + 重要性采样 + NEE，初期的 reproject 结构已接近时空样本复用（第二年计划啃 reservoir sampling）。
- **Hybrid Renderer**：[[visibility-buffer|VB]] 替代 primary ray，硬件光追处理短距离 secondary ray，远距离走 probe / cache。详见 [[hybrid-raytracing-pipeline]]。
- **Reverse-Hybrid Renderer**：primary ray 直接写 VB，后续走 compute shading，"整体渲染只有几个 compute shader"。
- **Bindless**：渲染资源访问几乎完全跑在 GPU 内部。见 [[bindless-rendering]]。
- **Probe Generation**：基于 tinybvh 的 CPU/GPU 共享 ambient cube 生成，异步 shadow map 更新。

## 工程价值观

作者多次强调：

- **不重复造轮子**：能用成熟开源库就用。
- **跨平台是第一公民**：不是事后适配，而是初始需求。
- **长期主义**：目标像 Spartan Engine 那样以年为单位持续贡献与分享。
- **拥抱 AI**：YearOne 里大量代码与 Claude 3.7 Sonnet 协作完成，Ambient Cube Probe 等系统是典型案例。作者认为"通用人工智能可能在语言大模型上出现"。

## 与旧作的关系

gkNextEngine 与作者 2013–2015 年主导的 [[gkengine]] 一脉相承又完全重写——后者是"稚嫩的 CryEngine 模仿者"，前者则"不刻意模仿和树立目标，以尽量优雅的方式实现"。

## 相关

- [[people/gameknife]]
- [[gkengine]]
- [[visibility-buffer]]
- [[hybrid-raytracing-pipeline]]
- [[bindless-rendering]]
- [[engine-evolution]]

## Sources

- [[sources/gameknife-gknextrenderer-yearone]]
