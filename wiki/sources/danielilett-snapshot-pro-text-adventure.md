---
tags: [source, 渲染, unity, urp, 后处理, ascii, atlas, retro]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Text Adventure（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Text Adventure ASCII 终端后处理的五个参数。

## 摘要

Text Adventure 把屏幕当字符终端：把画面按 `Character Size` 切成格子，每个格子取平均亮度，用亮度去**索引一张字符图集**选中一个字符，再把字符贴回格子——最终得到 ASCII 墙式的风格化输出。概念细节见 [[text-adventure-terminal-postfx]]。参数：`Character Size`（格子像素大小）、`Character Atlas`（`(n·x, y)` 形状的字符图集）、`Character Count`（`n`）、`Background Color` / `Character Color`（最终 lerp 的底色与字色）。页面注明 **Character Atlas 必须设置**，没有默认 fallback——产品把"字符要按亮度排序"的约束留给用户，atlas 排错就会出现亮度跳变。

## 关键要点

- `Character Atlas` 必须是 `(n·x, y)` 的横向字符条，按亮度从低到高排序
- `Character Count = n`（atlas 里的字符数），不能多不能少
- `Character Size` 决定画面分辨率牺牲量——越大越 ASCII，越小越接近原图
- 单色设计：字符只被染成 `Character Color`，想保留原色需要自改 shader
- 没提配合 `FilterMode.Point`——但 atlas 不用 point sampler 会把字符糊成渐变（[[color-quantization-retro|同复古量化链的约束]]）
- 典型用法：复古终端切镜、"hack 进入系统"过场、CRT + ASCII 组合

## 链接到的概念

- [[text-adventure-terminal-postfx]]
- [[color-quantization-retro]]
- [[crt-shader-effects]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/text-adventure/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-text-adventure.md`
