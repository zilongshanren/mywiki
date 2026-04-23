---
tags: [playcanvas, asset-pipeline, html5, web-engine, tooling]
date: 2026-04-19
sources: 1
---

# PlayCanvas 云端资产管线（2013）

2013 年 6 月，PlayCanvas 推出**浏览器端资产导入**功能：开发者直接把 FBX 或 COLLADA 文件拖进浏览器，转码全部在云端完成，再不用本地下载安装命令行工具链。这在 2013 年是一次相当激进的产品判断——当时 Unity / Unreal 的做法还是本地 Editor 里跑导入器，把 .fbx 扔进 `Assets/` 文件夹触发 reimport。PlayCanvas 把这一步搬到 server 端，顺理成章地兼容了 Mixamo 这类 web-first 素材源：创作者在 Mixamo 里挑好模型与动画，几分钟内就能出现在 PlayCanvas 游戏里。

这一步是 PlayCanvas 作为**"纯 web 引擎"**定位的关键伏笔：如果要让整个开发循环都在浏览器里完成（见后来的 [[playcanvas-webgpu-editor|PlayCanvas Editor]] 与 [[supersplat-pwa|SuperSplat PWA]]），资产管线就不能要求本地工具链。十二年后，同样的哲学延伸到 3DGS 工作流（[[playcanvas-editor-gaussian-splat]]、[[sog-compression-format]]）——所有 asset 操作都在浏览器 / 云端完成，本地只需要一个现代浏览器。

原文很短，主要是发布声明 + 5 分钟演示视频，没有披露云端转码栈的实现细节（是否使用 FBX SDK、是否排队调度、是否缓存转码结果等均未说明）。技术细节是一处空白。

## Sources

- [[sources/playcanvas-cloud-asset-pipeline]]
