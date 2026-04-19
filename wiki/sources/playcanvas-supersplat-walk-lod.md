---
tags: [source, playcanvas, gaussian-splatting, supersplat, walk-mode, lod, 流式加载, voxel-collision, 3dgs]
date: 2026-04-19
sources: 1
---

# New in SuperSplat: Walk Mode, Streamed LOD and Easy Upload（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2026-03-11 发布于 blog.playcanvas.com 的 SuperSplat 功能更新：三项大能力 + PlayCanvas Engine 2.17.0 的 splat 渲染性能专项优化。

## 摘要

**Walk Mode**——第一人称 splat 探索。默认是 **click-to-walk**：点哪去哪，相机平滑飘过去；桌面按 WASD 切到 FPS 式控制；移动端 Settings 里可开 **pinch-to-move** 做全触屏导航。底层是**基于体素的碰撞系统**：场景里有 collision 数据就自动开第一人称。碰撞数据通过 [[splat-transform-cli|SplatTransform]] 生成（developer preview 阶段，先放一批创作者试用）。**Streamed LOD**——由于用户发布的 splat 越来越大（桌面典型支持 ~4M Gaussian，新作品常超 10M），引入**流式加载 LOD**。基于 [[sog-compression-format|SOG]] 格式把场景切成小块按需拉取——当前视点和设备能力决定加载什么，手机和桌面都能拿到各自能处理的版本。XGRIDS 设备捕获的 LCC 场景自带高质量 LOD；其他用户可以用 SplatTransform 从多份不同细节的 PLY 生成 streamed SOG。**Easy Upload**——SuperSplat 主页新加 Upload Splat 按钮，拖一个 PLY / SOG / Streamed SOG / LCC 文件直接发布，不必再进 Editor；Editor 发布流也统一到同一"details dialog"。**PlayCanvas Engine 2.17.0** 专攻 splat 渲染：WebGL2 和 WebGPU 都有大幅帧率提升、LOD 选择更精细、按设备能力自适应优化。

## 关键要点

- **Walk Mode 用 voxel collision**：体素化比 splat-level 精细 collision 便宜得多，也避开 3DGS 的"软边界"问题。
- **Click-to-walk 作为默认**：降非技术用户门槛——不用学 WASD 就能探索场景。
- **Streamed LOD 建在 SOG 之上**：SOG 的 Morton order 让"切片成块"有天然的空间局部性，切片流式加载得很自然。
- **XGRIDS LCC 一等公民**：SuperSplat 已经把外部捕获硬件的原生格式接入工具链。
- **LOD 生成链路**：用户喂多份不同精度 PLY → SplatTransform 输出 streamed SOG → viewer 自动按视点拉。
- **Easy Upload 降发布门槛**：从"必须进 Editor"变成"主页拖一下"。
- **Engine 2.17.0**：这一波渲染性能优化是 10M+ Gaussian 场景实用化的关键。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[sog-compression-format]]
- [[splat-transform-cli]]

## 原文

- 链接：<https://blog.playcanvas.com/new-in-supersplat-walk-mode-streamed-lod-and-easy-upload>
- 本地：`raw/articles/blog.playcanvas.com/2026-03-11_new-in-supersplat-walk-mode-streamed-lod-and-easy-upload-pla.md`
