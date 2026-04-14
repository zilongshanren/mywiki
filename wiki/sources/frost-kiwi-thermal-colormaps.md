---
tags: [source, 渲染, 颜色, color-lut, 可视化]
date: 2026-04-14
sources: 1
---

# Thermal Camera LUTs and colormaps for DaVinci Resolve（Frost / frost.kiwi）

[[frost-kiwi|Frost]] 发表于 2024 年 3 月的一篇工具型短文：在写完 [[color-lut|游戏 LUT 长文]] 之后，他发现 DaVinci Resolve 并没有内置把灰度热成像着色的 colormap，于是写了段 Python 脚本把 matplotlib 所有 colormap 一次性烘成 Iridas/Adobe `.cube` 1D LUT，直接挂进 Resolve 的 Color 页。

## 摘要

文章主题是**把 matplotlib 的 colormap 搬到视频调色工作流**——[[perceptual-colormaps]] 这条路的工具化落地。作者指出 Resolve 和大多数 NLE 都缺少感知均匀 colormap，于是用 `colour-science` Python 包里的 `LUT3x1D` + `write_LUT_IridasCube` 写了个 ~30 行的 CLI 脚本：命令行给出 `--colormap viridis --lutsize 256` 就吐出一个 `viridis.cube`。DaVinci Resolve 的 `.cube` 原生支持 1D LUT，无需额外包装。整套流程是：Resolve Preferences 里加一个 LUT 目录 → 把烘好的 `.cube` 塞进去 → Color 页的 LUTs 面板选中 → 直接拖到节点上。文章同时附了所有 matplotlib colormap 的预览视频和下载包。作者再三提醒：**除非有明确艺术意图或特殊数据布局，否则选感知均匀的那一组**（viridis / inferno / plasma / magma / cividis），不要用 `jet` / `rainbow`，和他上一篇 LUT 长文里「选 colormap 要考虑人眼响应」的结论一致。

## 关键要点

- DaVinci Resolve `.cube` 格式支持 1D LUT，正好对应一维 colormap
- `colour-science` 包内置 `LUT3x1D` 和 `write_LUT_IridasCube`，无需手写文件格式
- 默认 `lut_size = 256` 足够 8-bit 输入，也对齐常见像素格式
- 感知均匀 colormap（viridis 族）才是数据可视化的默认正解
- `jet` / `rainbow` 在绿色附近挤压、青色附近平台，会制造虚假边界
- 整条流程同样适用于任何支持 `.cube` 的其他软件（Premiere、Affinity、OBS 插件等）

## 链接到的概念

- [[perceptual-colormaps]]
- [[color-lut]]
- [[frost-kiwi]]

## 原文

- 链接：<https://blog.frost.kiwi/Davinci-Resolve-thermal-luts/>
- 本地：`raw/articles/blog.frost.kiwi/2024-03-01_thermal-camera-luts-and-colormaps-for-davinci-resolve.md`
