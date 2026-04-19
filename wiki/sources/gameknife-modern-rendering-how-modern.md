---
tags: [source, 渲染, 引擎, 光追, vulkan, 中文]
date: 2026-04-19
sources: 1
---

# 现代渲染能有多现代？（gameknife / gkNextEngine）

[[gameknife]] 发表于 2025 年 10 月的一篇反思性长文，以"一个古董级 OpenGL ES 渲染工程师的重新学习"视角，回答"现代渲染到底现代在哪"——本质上是对自家开源项目 [[gknext-renderer|gkNextEngine]] 一年半演化的一次系统总结。

## 摘要

文章用自问自答的形式覆盖五个层面。**Shader 层面**：[[slang-shader-language|Slang]] 的泛型、模块、namespace 让 shader 能写得像 C++——一个 `FPathTracingRendererV2` 可以通过模板参数组合 raycaster/tracer/illuminator，每个 pipeline 最终只剩几十行"装配代码"。**资源管理层面**：[[zero-bind-gpu-resource-management|零 bind]]——通过 Vulkan BDA（Buffer Device Address）+ bindless 纹理数组 + PushConstant 三件套，整个管线不再绑任何 descriptor，所有资源都通过一个 `GPUScene*` 指针偏移访问，改管线从一晚上缩到几分钟。**Drawcall 组织**：GPU-driven（当下还是"传统"的 indirect draw + GPU cull 的空绘制版本，未来要转 mesh shader 或其软件模拟版）。**光照层面**：[[ambient-cube-probe-pathtrace-exit|AmbientCube 探针]]作为 PathTracing 提前退出缓存 + [[hybrid-voxel-software-raytracing|混合体素软件光追]]作为无硬件 RT 设备的 fallback——同一份探针数据在 HardwarePT / SoftwarePT / SoftTracing / SoftModern 4 种渲染器里都有用。**时域渲染**：TAA + reprojection + 多帧样本累积，配合 120–240Hz 高刷屏幕可以实现"人眼补帧"——截图画质远低于肉眼所见画质。最后他把 gkNextRenderer 升级为 gkNextEngine，目标只有一个："just for fun"；原则是"永远用最新技术 / 拥抱第三方库 / 保持小体积可读"。

## 关键要点

- 零 bind 需要 BDA + bindless 数组 + PushConstant 三件套，pipeline 拿到整个世界的访问权。
- Slang 可以写出"看起来像 C++"的 shader：泛型、模块、namespace、自动微分，全平台编译。
- PathTracing 提前退出 + AmbientCube 探针缓存是朴素而高效的 GI 加速，16 spp 下不带降噪器已有可接受画质（累积 16 帧 ≈ 128 spp）。
- 同一份 AmbientCube 数据是 4 种渲染器的共享"hybrid context"：既是 PathTracing 的 exit cache，又是软件 ray tracing 的空间结构，又是 SoftModern 的漫反射来源。
- 移动端可通过探针距离做 sphere-tracing 式的软件光追近似，无需完整 BVH。
- 120Hz+ 时域累积配合高刷屏，能达成"截图差但肉眼好"的视觉体验。
- 引擎小体积+拥抱第三方库（SDL、glm、tinybvh、quickjs、lzav、miniaudio、tinygltf、meshoptimizer、joltphysics、ozzAnimation、spdlog、stb、imgui）。

## 链接到的概念

- [[zero-bind-gpu-resource-management]]
- [[slang-shader-language]]
- [[ambient-cube-probe-pathtrace-exit]]
- [[hybrid-voxel-software-raytracing]]
- [[bindless-rendering]]
- [[hybrid-raytracing-pipeline]]
- [[valve-ambient-cube]]
- [[taa-history-rectification]]
- [[temporal-supersampling]]
- [[gknext-renderer]]

## 原文

- 链接：http://gameknife.github.io/tech/2025/10/28/how-modern-rendering-modern/
- 本地：`raw/articles/gameknife.github.io/2025-10-28_xian-dai-xuan-ran-neng-you-duo-xian-dai-2.md`
