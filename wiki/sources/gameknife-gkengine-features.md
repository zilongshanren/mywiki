---
tags: [source, 引擎, 历史, 特性清单]
date: 2026-04-14
sources: 1
---

# gkENGINE 技术特性（gameKnife）

[[people/gameknife]] 于 2015 年 3 月 11 日发布的 [[gkengine|gkEngine]] 技术特性清单页，定位是"a cross-platform game engine"。内容是一份六个板块的 feature bullet + 一组编辑器与场景截图占位。

## 摘要

这篇短页是 2015 年时 gkEngine 对外展示的产品化 feature list，包含渲染、系统、物理与动画、工具链、编辑器、其他六个板块。渲染上提供延迟光照/延迟着色、"准"PBS、shader 条件编译、HDR/SSAO/DOF/GodRay/ColorGrading 等现代后处理、DX9/GL3/GLES2 多 API、多线程渲染、多 LOD 地形与全天候 Time of Day。系统层面主打跨平台（Windows / macOS / iOS / Android）、task 分发、lzma 压缩的 PAK 文件系统、组合式 GameObject。物理动画通过接口插件式接 Havok / PhysX；工具链涵盖 gmf 自研模型格式、gkMaxPort（3ds Max 插件）与资源编译器；编辑器基于 MFC。其他特性包括 Oculus DK1/DK2 与 3D 显示支持。这份清单十年后被作者自己承认是"稚嫩的 CryEngine 模仿者"，但也构成了他 2024 年 [[gknext-renderer|gkNextEngine]] 的经验底色。

## 关键要点

- 延迟光照 + "准 PBR" 是 2015 年那个时代独立引擎的合理技术选择，比 UE4 正式推出 PBR 晚了一两年。
- Shader 条件编译、多渲染 API（DX9/GL3/GLES2）显示出当时"一份代码多后端"的诉求。
- 跨平台通过"基础库 OS 特例化 + 部分模块完全重写"实现——这条路径十年后被作者自己评价为"笨重"，每个平台几乎都是一个独立渲染器。
- 物理与动画走插件化接 Havok/PhysX 而非自研，是典型的"先集成后自研"的独立引擎策略。
- 自研 gmf 模型格式是把 obj 做二进制优化 + 可逆互转，便于调试。
- gkMaxPort 把 3ds Max 作为主 DCC 入口，是那个时代中国独立引擎常见的选择。
- MFC 编辑器 + 3dsmax 工作流 + Oculus DK1/DK2 + 3D 显示，这份清单像一张 2013–2015 年代的时间戳。

## 链接到的概念

- [[gkengine]]
- [[gknext-renderer]]
- [[deferred-rendering]]
- [[physically-based-shading]]
- [[engine-evolution]]

## 原文

- 链接：<http://gameknife.github.io/tech/2015/03/11/tech-feature/>
- 本地：`raw/articles/gameknife.github.io/2015-03-11_gkengineji-zhu-te-xing.md`
