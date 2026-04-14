---
tags: [source, rendering, webxr, volumetric-video, ar-vr, playcanvas]
date: 2026-04-14
sources: 1
---

# PlayCanvas 支持 Microsoft 体积视频回放（Steven Yau / PlayCanvas Blog）

PlayCanvas 工程师 Steven Yau 于 2023 年 2 月发布的项目复盘，记录如何在 PlayCanvas 中集成 Microsoft Mixed Reality Capture Studios（MRCS）的 `.hcap` 体积视频，并打通桌面、移动 AR、桌面/头显 VR 的统一体验。

## 摘要

文章围绕一个 showcase demo 展开：把 MRCS 录制的全息视频接入 PlayCanvas 引擎，做到同一个 URL 在桌面浏览器、支持 WebXR 的 Android AR、以及 Oculus Quest VR 头显上都能观看。核心集成通过 MRCS 提供的 `holo-video-object-umd.js` devkit 加上 PlayCanvas 端的 `holo-video-player.js` 实体脚本完成：运行时根据 `.hcap` URL 流式创建 mesh 和 material。真正的工程量集中在跨设备体验：一个 XR manager 脚本统一处理进入/退出 AR/VR、按设备能力显示按钮、切换相机与图层（AR 用透明画布 + 无天空盒层）、为带 `ar-relative` 标签的实体在 AR 中自动移动到用户正前方。VR 分支复用了 Starter Kit: VR 的传送、拾取与手部模型功能；UI 用世界空间按钮绑定在 pivot 实体上始终面向用户。作者还顺带用一个自定义 shader 把 cubemap 投影为平面地板，用 shadow catcher 材质让平面地板接收角色软阴影。结尾坦白了两个 bug：VR 下 clustered lighting 阴影严重掉帧、以及 AR 中投影矩阵和相机组件 FOV 不一致导致的 UI 命中不准——作者用第一帧反解投影矩阵写回组件的方式规避。

## 关键要点

- 体积视频必须独立 CDN 托管，不能和引擎资源混在一起
- 单 URL 跨平台 XR 的关键是一个中心化的 XR manager 脚本
- AR 需要独立第二相机 + 透明画布 + 移除天空盒层；实体位置要按进入/退出自动迁移
- VR 下唯一合理的 UI 布局是世界空间，用 pivot 实体朝向相机
- 投影天空盒（projected cubemap）+ 阴影接收器材质是在平面上"伪造无限地板"的廉价组合
- 暴露的 bug 指向"相机组件 vs 实际 projection matrix"抽象接缝未打磨平整

## 链接到的概念

- [[volumetric-video-playback]]
- [[shadow-mapping-basics]]
- [[rendering-api-depth]]

## 原文

- 链接：https://blog.playcanvas.com/playcanvas-now-supports-microsoft-volumetric-video-playback
- 本地：`raw/articles/blog.playcanvas.com/2023-02-01_playcanvas-now-supports-microsoft-volumetric-video-playback.md`
