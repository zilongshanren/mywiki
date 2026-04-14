---
tags: [游戏引擎, 历史, 跨平台, 中国]
date: 2026-04-14
sources: 2
---

# gkEngine（2013–2015 时期）

[[people/gameknife|gameknife]] 早年（约 2013–2015）开发的跨平台商用向引擎，定位是"a cross-platform game engine"。这一代 gkEngine 在 2015 年 3 月的博客里有一份技术特性清单，代表了那个时代一个中国独立引擎开发者对"商业引擎该长什么样"的理解。十年后被作者的 [[gknext-renderer|gkNextEngine]] 继承与重写。

## 技术特性（2015 年清单）

### 渲染

- 延迟光照与延迟着色管线（[[deferred-rendering]]）
- "准" 基于物理的着色（[[physically-based-shading|PBS]] 早期阶段）
- Shader 条件编译系统
- 现代后处理：HDR、SSAO、DOF、God Rays、Color Grading
- **多线程渲染**：渲染提交在独立线程
- **多渲染 API**：DX9 / GL3 / GLES2 可切换
- 多 LOD 层级地形系统
- Time of Day：全天候环境参数插值

### 系统

- 跨平台基础库：通过 OS 特例化实现平台无关层
- Windows / macOS / iOS / Android 四平台
- Task 分发系统：任意独立事务包装为 task 做多线程执行
- PAK 文件系统：lzma 压缩打包，接管文件系统
- GameObject + GameObjectLayer 组合式扩展

### 物理 & 动画

- 物理通过接口抽象，插件式接 Havok / PhysX
- 骨骼动画接 Havok，自研模块"筹划中"
- 内建 TrackBus 动画模块，用于 cutscene 等

### 工具链

- **gmf 模型格式**：对 obj 做二进制优化，支持 obj ↔ gmf 互转
- **gkMaxPort**：3ds Max 插件 + 脚本，用于整理模型、处理纹理材质、导出到引擎
- 资源编译器：针对多平台做纹理/材质/模型的特定生成处理
- 基于 MFC 的编辑器框架，含场景开发、模型预览、材质编辑、动画编辑、角色编辑

### 其他

- Oculus Rift DK1/DK2 支持
- 3D 显示支持（左右分割 / 上下分割）

## 历史评价

作者自己在 2025 年的 YearOne 回看时承认："**当时 CryEngine 就是我的学习目标**，当时略显稚嫩的我，当然是以模仿目标为第一要义。" 早年博客园也曾有人批评它"和 CryEngine 太像了，抄袭 CryEngine"，作者的回应是"所有技术点都是一个个实现调试出来的，每一行代码也是自己一行行敲出来的"。

这一代 gkEngine 的"跨平台"在作者自述里是**笨重的**：几乎在每个平台上实现了一个渲染器，只有场景接口保持一致。这个教训驱动了 [[gknext-renderer|gkNextEngine]] 里 **Vulkan + CI 一次编译处处运行** 的架构选择。

## 相关

- [[people/gameknife]]
- [[gknext-renderer]]
- [[engine-evolution]]
- [[deferred-rendering]]
- [[tbdr-vs-imr]]

## Sources

- [[sources/gameknife-gkengine-features]]
- [[sources/gameknife-gknextrenderer-yearone]]
