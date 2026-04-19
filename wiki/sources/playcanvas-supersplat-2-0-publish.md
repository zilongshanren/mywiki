---
tags: [source, playcanvas, supersplat, gaussian-splatting, webxr, 发布]
date: 2026-04-19
sources: 1
---

# Publish Your Gaussian Splats with SuperSplat 2.0（Will Eastcott / PlayCanvas）

[[will-eastcott]] 在 2025 年 2 月发表，宣布 SuperSplat 2.0 从"编辑器"扩张为"编辑 + 发布平台"，并搬到新域名 `superspl.at`。

## 摘要

SuperSplat 2.0 的核心变化是给作者提供**一键发布**：登录 PlayCanvas 账号、在 `File` 菜单里点 `Publish`、填基本信息、拿到一条可分享的 URL。底层是 [[supersplat-publish-platform|SuperSplat 发布平台]]——一个开源 [[gaussian-splatting-web|压缩 PLY]] + [[playcanvas-webgpu-editor|PlayCanvas 引擎]]驱动的 HTML viewer + 托管服务。发布后的 splat 默认出现在 `superspl.at` 的公共 gallery，也可以设为 unlisted 保留 URL 但不公开。2.0 同时引入 **Timeline** 关键帧相机动画（在时间线上选帧 → 移相机 → 打 keyframe，串成 flythrough），以及 **.ssproj 项目文件格式**——一个 ZIP 壳里装 JSON 元数据 + 一组 PLY——对应地把 `File` 菜单改成 Open/Save/SaveAs 只吃 `.ssproj`、Import/Export 处理 `.ply` 和 `.splat` 等交换格式。发布出来的 viewer 自带 WebXR，测试过 Quest 2/3、Vision Pro 和 Android 手机的 AR/VR 模式。

## 关键要点

- 发布流水线三步：登录 → `File > Publish` → 填表；结果是一条可发社群的 URL。
- **Timeline 关键帧**：把 splat 场景变成"有镜头脚本的短片"，是 3DGS 从"可交互 3D 资产"走向"视觉内容"的关键工具。
- **`.ssproj` 格式**：ZIP(JSON + PLYs)——工业标准打包思路，复用 PLY 作为内部 splat 存储，项目信息另存 JSON。
- `Open/Save` 与 `Import/Export` 语义分离：避免新手把"导入 PLY"当成"打开项目"的路径混淆。
- **WebXR 一等公民**：发布的 viewer 一键进入 AR/VR；不再需要专门写 XR 代码。
- 域名从 `playcanvas.com/supersplat` 迁到独立 `superspl.at`——品牌独立，信号意味着这个产品线已能脱离母体。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[supersplat-pwa]]
- [[gaussian-splatting-web]]
- [[will-eastcott]]

## 原文

- 链接：<https://blog.playcanvas.com/publish-your-gaussian-splats-with-supersplat>
- 本地：`raw/articles/blog.playcanvas.com/2025-02-13_publish-your-gaussian-splats-with-supersplat-2-0-playcanvas.md`
