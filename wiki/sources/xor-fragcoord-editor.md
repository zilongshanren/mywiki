---
tags: [source, 渲染, shader, 工具, 开发者体验]
date: 2026-04-19
sources: 1
---

# FragCoord: The Ultimate Tool（Xor）

[[xor-shader-artist|Xor]] 2026 年 3 月推出 [FragCoord.xyz](https://fragcoord.xyz)——他自己设计的浏览器内 shader 编辑 / 调试 / 分析 / 社群平台，整合 ShaderToy 的"分享"和专业 profiler 的"诊断"。

## 摘要

FragCoord 在单个 shader 预览下方提供 5 种 Inspector 模式：(1) **Tuner**：所有 uniform 实时值 + 代码里数字字面量的滑块调参；(2) **Inspect**：选任一中间表达式单独预览，hover 读光标值 + histogram；(3) **Errors**：逐像素标 NaN / Inf / 越界 `[0,1]` 的 checkerboard；(4) **Frames**：CPU/GPU ms、fps、stutter；(5) **Heatmap**：逐像素指令成本（显示分支 divergence 带来的 warp 代价）。跨平台 Import/Export 把 ShaderToy / Twigl / WebGL / HLSL / Metal / WGSL 一键互转——节省"跨引擎 shader 移植"上无数小时。Code Library 共享 noise / rotation 等常用函数，社区 tab 可 fork；引用能自动跟随作者更新。发布时配有字符计数（code golf）和指令估算（性能代理）。上线两周已有 500 成员 + 650 公开 shader。Xor 定位：为专业人和业余人都设计的**真正可调试**的 shader 环境。

## 关键要点

- **Inspect 模式**：任选中间表达式作为输出——类似"shader 版断点"。
- **Errors 模式**：NaN / Inf / 越界用 checkerboard 可视化——诊断黑屏的神器。
- **Heatmap 模式**：逐像素成本图，揭示 branch divergence。
- **多格式互转 + 指令统计**：跨引擎移植和 code golf 都照顾到。
- **Code Library 社区共享**：消除"每个 shader 各自 copy 同一段 noise"的碎片化。

## 链接到的概念

- [[fragcoord-shader-editor]]
- [[common-shader-pitfalls]]
- [[shader-code-golfing]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/fragcoord
- 本地：`raw/articles/mini.gmshaders.com/2026-03-07_fragcoord-the-ultimate-tool.md`
