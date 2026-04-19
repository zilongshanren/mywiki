---
tags: [source, playcanvas, gaussian-splatting, cli, 工具链, 3dgs]
date: 2026-04-19
sources: 1
---

# Introducing SplatTransform CLI（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2025-07-15 发布于 blog.playcanvas.com 的工具公告：PlayCanvas 开源了 **SplatTransform**——一个把 3DGS 数据的格式转换 / 空间变换 / 过滤 / 合并 / CSV 导出汇到一条 CLI 命令的工具，定位是 [[supersplat-publish-platform|SuperSplat]] 的命令行补丁。

## 摘要

SuperSplat 适合可视化单场景清洗；脚本和 CI 流水线需要的是命令行版。SplatTransform 填这个空位：`npm install -g @playcanvas/splat-transform` 后以 `splat-transform` 调用。格式互转覆盖 PLY / SPLAT / KSPLAT / SOGS / CSV；空间变换支持一条命令里边 translate / rotate / scale 边转换；最有意思的是**多文件合并**语法——参数紧跟在各自输入后面，`inputA.ply -r 0,90,0 inputB.ply -s 2 merged.ply` 形成一个小型场景图。过滤侧支持 `--filterNaN`、`-c opacity,gt,0.3` 属性过滤、`--filterBands 2` 砍 SH 阶次（占 SH 系数 75% 的空间大头）。CSV 导出把 splat 从二进制黑盒变成可读表格，可以喂给 Excel / Pandas / ML 流水线做分布统计、离群点检测、聚类。后续（2026-03）又加入生成 walk mode 的体素碰撞数据和从多份 PLY 生成 streamed SOG。

## 关键要点

- **目标格式**：生成 Compressed PLY 或 SOG，和 PlayCanvas Engine / Editor / SuperSplat 无缝打通。
- **迁移路径**：别家的 `.splat` / `.ksplat` 一键转成 PlayCanvas 家族的格式。
- **SH 瘦身旋钮**：`--filterBands` 是最直接的体积控制手段（SH 占比 75%）。
- **多文件合并**：参数局部作用域化的 CLI 语法——一条命令装一个微场景图。
- **CSV 作为中间层**：把 splat 当数据集做分析，而不只是当资产做渲染。

## 链接到的概念

- [[splat-transform-cli]]
- [[sog-compression-format]]
- [[supersplat-publish-platform]]
- [[gaussian-splatting-web]]

## 原文

- 链接：<https://blog.playcanvas.com/introducing-splat-transform-cli-tool>
- 本地：`raw/articles/blog.playcanvas.com/2025-07-15_introducing-splattransform-the-ultimate-cli-tool-for-3d-gaus.md`
