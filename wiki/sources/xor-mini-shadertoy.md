---
tags: [source, 渲染, shader, shadertoy, gamemaker]
date: 2026-04-14
sources: 1
---

# Mini: ShaderToy（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 10 月的一篇，讲 **ShaderToy 的格式约定以及如何把 ShaderToy 上的 shader 移植到 GameMaker**。是一份标准化的移植清单，其思路对任何做 2D/混合引擎 shader 的人都有直接参考价值。

## 摘要

ShaderToy 本质是浏览器里的单 fragment shader 沙箱。它有几个隐含约定：入口叫 `mainImage(out fragColor, in fragCoord)`；uniform 以 `i*` 为前缀（`iResolution`、`iTime`、`iMouse`、`iChannel0..3` 等）；alpha 不参与合成；假设每张贴图独占 sampler。移植到 GM 要做五件事：(1) 加 varying；(2) `mainImage` → `main`，`fragColor` → `gl_FragColor`、`fragCoord` → `gl_FragCoord.xy`；(3) 显式设置 alpha；(4) 把所有 `i*` 接到 `shader_set_uniform_f`；(5) 补 WebGL 2 → WebGL 1 的语法差（`texture` → `texture2D`、不支持位运算 / switch / 动态数组 / 非方阵 / `round()`）。贴图必须独占 texture page（参考 Xor 上一篇两纹理教程）。多 Buffer pass 要分别对应 surface，并**注意 ShaderToy 的 Buffer 是 float 纹理而 GM surface 是 8-bit unorm**——输出值必须落在 0–1 内才能移植成功。`Common` tab 复制到每个 buffer shader 顶部。文末强调许可和归属——默认 CC-BY-NC-SA，商业使用要联系作者。

## 关键要点

- **入口与输出**：`mainImage(out, in)` → `main()`，`fragColor` → `gl_FragColor`，`fragCoord` → `gl_FragCoord.xy`。
- **uniform 映射表**：`iResolution`（vec3，z=1）、`iTime`、`iTimeDelta`、`iMouse`（xy 当前 + zw 按压位置带符号）、`iFrame`、`iChannelN` + `iChannelResolution[]`。
- **ShaderToy 假设每张贴图独占 sampler**——atlas 引擎必须先保证 sprite 独占 page 或用归一化套路（上篇）。
- **WebGL 2 → 1 的替换**：`texture` → `texture2D`；GM 不支持位运算、switch、动态数组、非方阵、`round()`。
- **多 Buffer 移植的坑**：ShaderToy 的 intermediate 是 float，GM 的 surface 是 8-bit——**输出必须 0–1**，否则 clamp 丢数据。
- **`Common` tab 是共享代码**——没有 include，要手工拷进每个 buffer。
- **许可**：CC-BY-NC-SA 3.0 是默认；商业项目要联系原作者并保留 license header。
- 推荐工具：[Shadertoy2GM](https://iarri.github.io/Shadertoy2GM/) 自动化版（基本用途够用，复杂的还是要懂手工移植）。

## 链接到的概念

- [[shadertoy-basics]]
- [[two-texture-sampling-tricks]] — 前置：atlas UV 归一化
- [[ping-pong-surfaces]]
- [[fragment-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-shadertoy-1392217
- 本地：`raw/articles/mini.gmshaders.com/2022-10-07_mini-shadertoy.md`
