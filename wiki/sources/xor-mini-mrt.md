---
tags: [source, 渲染, shader, mrt, gpu, gamemaker]
date: 2026-04-14
sources: 1
---

# GM Shaders: MRT（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 1 月 6 日的新年开篇，一页纸讲清楚 GameMaker 下如何使用 **Multiple Render Targets**。

## 摘要

MRT 的核心改动只有一行：把 `gl_FragColor` 换成 `gl_FragData[0..3]`，每个下标对应一张额外的 surface；宿主端通过 `surface_set_target_ext(slot, surface)` 把 4 张 surface 绑进去，一次 `draw_self()` 同时输出到全部目标。Xor 先给出一份红 / 绿 / 蓝 / 白的测试 shader，然后用两个典型用例说明为什么这个功能值得掌握——**[[deferred-rendering|延迟渲染]]**（G-Buffer: normal、albedo、position、specular 同时写出）和他自己 idle game *Constructor* 里的 **Object ID buffer**（每个物体输出 `vec3(i,0,0)/255`，outline shader 凭 ID 画描边）。最后他点出几个必须注意的陷阱：HTML5 根本不支持 MRT、低端设备可能反而更慢、surface 格式和数量会严重影响 VRAM（不用时别开 `rgba32float`，单通道用 `r8unorm` 就好）、所有 RT 共享一次 rasterization（`discard` 会 kill 全部 output）。

## 关键要点

- **MRT = 一次 draw 写多张附件**：GLSL 里用 `gl_FragData[i]`，GM 侧 `surface_set_target_ext(i, surf)`，上限 4 张。
- **最经典用途是 G-Buffer**：延迟渲染把 albedo/normal/position/depth 在几何 pass 里一次写出，光照 pass 再读回。
- **Object ID outline**：每物体一个 ID 色，outline shader 读 ID 图比较邻域即可画描边；一次几何提交产出"画面 + 索引图"。
- **自建 depth**：GameMaker 没开放 depth buffer，但可以用 `gl_FragData[1]` 手写一份 depth 供 SSAO / shadow map 消费。
- **VRAM 是真正的代价**：4 张 full-HD RGBA8 ≈ 32 MB，换成 float4 立刻 4×；按需选格式是重点。
- **平台限制**：HTML5 完全不支持，低端 GPU 未必受益；上线前要早测。
- **rasterization 状态共享**：所有 output 共用相同 vertex / viewport / discard；想要 RT 之间独立剔除是办不到的。

## 链接到的概念

- [[multiple-render-targets]]
- [[deferred-rendering]]
- [[xor-shader-artist]]
- [[fragment-shader]]
- [[rendering-pipeline]]

## 原文

- 链接：https://mini.gmshaders.com/p/mrt
- 本地：`raw/articles/mini.gmshaders.com/2024-01-06_gm-shaders-mrt.md`
