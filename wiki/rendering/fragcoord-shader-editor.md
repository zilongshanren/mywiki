---
tags: [渲染, shader, 工具, 调试, 开发者体验]
date: 2026-04-19
sources: 1
---

# FragCoord.xyz：面向专业与业余的 Shader 编辑器

[[xor-shader-artist|Xor]] 2026 年推出的 [FragCoord.xyz](https://fragcoord.xyz) 是一个浏览器内的 shader 编辑 / 调试 / 分析工具。定位介于 ShaderToy 的"演示分享"和专业 GPU profiler 之间——想做「Xor 自己写 shader 需要的所有工具整合成一个环境」。

## 5 种 Inspector 模式

核心设计是把通常分散在不同工具里的功能并列在同一个 shader 预览下方：

1. **Tuner**：所有 uniform 实时显示当前值、被代码引用的高亮。可以选中一个数字字面量用滑块调——替代"改代码-重新编译-看结果"循环。
2. **Inspect**：选中任一**中间表达式**（不只最终颜色）单独预览到屏幕上，看它作为图像是什么、hover 能读出光标位置的精确值，下方有选中量的 histogram。类似于"在 shader 里随处下断点看变量"。
3. **Errors**：逐像素检测 **NaN / Inf / 超出 [0,1]**，用 checkerboard 可视化——NaN 红青、Inf 绿品、越界 蓝黄。一眼就看到哪里除以 0、哪里饱和。
4. **Frames**：CPU / GPU 时间、ms / fps 切换、stutter 点标记。基础性能监控。
5. **Heatmap**：**逐像素指令成本**。分支、条件 for 循环会造成 warp 内 divergence——heatmap 直接显示 divergence 的代价。还提醒用户注意 quad/warp 绑定，相邻像素成本差距大时会"被较贵的一方拖累"。

## 跨平台转换

内建 shader 代码转换：**ShaderToy** / **Twigl** / **WebGL** / **HLSL** / **Metal** / **WGSL** 之间一键互转。对做跨引擎 shader 移植非常省事——把 `gl_FragColor` 和 `gl_FragCoord` 的名字对等映射、头尾 boilerplate 自动添加。

自动格式化工具也能对齐各种约定，适合从 ShaderToy 等混合来源拷贝代码后统一风格。

## Code Library

内置常用函数库：hash、noise、rotation、color transformation 等。社区版 tab 共享片段，更新后所有引用自动跟进——消除"每个 shader 各自 copy 同一段 noise"的碎片化。

## 字符数 + 指令数双计数

- **压缩后字符数**：方便 code golfer 确认 tweet 限制。
- **估算指令数**：悬停看 line-by-line 估算。作为性能代理比 fps 稳。

## 设计哲学

Xor 在公告里强调"现有工具不够用"：ShaderToy 适合分享但没有调试；专业 profiler 门槛高且脱离浏览器。FragCoord 试图做**一个专业人和业余人都愿意用的中间地带**——**调试工具是 first-class、不是 afterthought**。

## 对 shader 教学的价值

对刚接触 shader 的人，`Errors` 和 `Inspect` 两个面板极有教育价值：

- 看见"为什么整个画面变黑" = 某处除以 0 产生 NaN 传染。
- 看见中间变量是什么颜色 = 具体理解抽象数学式。

这也是 [[common-shader-pitfalls|Xor 的 shader 常见陷阱]]一文里 NaN / Inf 章节的自然延续——这些工具把诊断流程**自动化**了。

## 相关

- [[xor-shader-artist]]
- [[common-shader-pitfalls]]
- [[shader-code-golfing]]
- [[shadertoy-basics]]
- [[webgpu-intro]]

## Sources

- [[sources/xor-fragcoord-editor]]
