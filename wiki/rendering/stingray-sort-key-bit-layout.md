---
tags: [渲染, 排序, sort-key, data-driven, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 的 64-bit sort_key 位布局

Walkthrough 系列第 4 篇。Tobias 坚持用 **显式 ordering + 单次 stable sort** 来解决渲染命令排序——不做 bucket，不做多阶段 sort。原因：实现简单、每个 renderable 只需 visit 一次、cost 容易 profile、并行天然（多个 [[stingray-render-context|RenderContext]] 的 Command 数组直接 concat 再 sort 就行）。

思想源自 Christer Ericsson 那篇经典的 ["Order your graphics draw calls around!"](http://realtimecollisiondetection.net/blog/?p=86) —— **所有 draw 排序条件塞进一个 64-bit 整数**，从高位到低位优先级递减。Stingray 的具体分配如下（**MSB 在左**）：

```
[ 2 | 7       | 3          | 32           | 1        | 16    | 3          ]
[ - | Layer   | Pass Deferr| User defined | Instance | Depth | Pass Immed |
    | System  | red        |              | bit      |       | iate       ]
```

## 字段含义

**2 bits Unused**——作者自己也承认不清楚为啥空着，可能是历史原因，目前恒为 0。

**7 bits - Layer System**：一帧的宏观阶段顺序，来自 `render_config` 里的 layer 声明。每声明一层 +1。下面的片段展示了 `gbuffer → decals → lighting → emissive` 的 sort_key 自增：

```
{ name="gbuffer" render_targets=[g0,g1,g2,g3] sort="FRONT_BACK" }
{ name="decals" render_targets=[g0,g1] sort="EXPLICIT" }
{ resource_generator="lighting" }
{ name="emissive" render_targets=["hdr0"] sort="FRONT_BACK" }
```

layer 是 [[stingray-data-driven-render-config|data-driven render pipeline]] 的中枢，由 `LayerManager` 管理。shader 声明 "我要渲进哪几层"，RC::render 录制时自动把 layer 的 sort_key 位 OR 进 final sort_key。

**3 bits - Shader System (Pass Deferred)**：shader（Stingray 叫 `ShaderTemplate::Context`，Nathan Reed 的 ["The Many Meanings of Shader"](http://reedbeta.com/blog/many-meanings-of-shader/) 里称为 "Effect"）可能是 multi-pass 且渲进同一 layer，这 3 位编码 pass 在 layer 内的顺序。

**32 bits - User defined**：一般由 [[render-config-extension-points|Resource Generator]] 系统使用，用户也可自由使用而不破坏 data-driven 兼容性。

**1 bit - Instance bit**：shader 实现了 "instance merging" 时置位。[[stingray-render-device-dispatch|RenderDevice dispatch]] 阶段用它配合高位相等性扫描出可合并的 draw 区间。

**16 bits - Depth**：`RenderContext::render()` 的 `job_sort_depth`（unsigned normalized [0,1]）量化后放这里。layer 声明 `BACK_FRONT` 时把这 16 位按位翻转即可——透明物体的 back-to-front 排序不需要特殊 code path。

**3 bits - Shader System (Pass Immediate)**：multi-pass shader 的另一种执行顺序。默认 Pass Deferred 模式下相同 sort 高位的 pass N draw 先全部执行，再到 pass N+1；Immediate 模式把 pass index 放到最低位，于是对同一个 object 的多个 pass 连发执行：

```
// Deferred: for pass, for draw  — 最少 state 切换
// Immediate: for draw, for pass — 某些 alpha blending 要求 per-object 顺序
```

## 排序实现

所有 Command 收齐后一次 **stable radix sort**。stable 很关键——两个 sort_key 完全相同的 command 保持录制顺序，避免帧间时序抖动。sort 的位置是 `RenderDevice::dispatch` 的第一步，RC 的 user 完全无感。

user 可以 bypass data-driven 系统：shader 里不 tag pass，sort_key 的高 bits 全零，完全由 `RenderContext::render()` 的 `interleave_sort_key` 参数控制。

## 为什么这种设计赢

Tobias 和 Christer 的赢点在于 **把"排序"变成一次纯算术操作**——没有 bucket、没有多阶段 sort、没有 "透明物体要不要 separate pipeline" 的分裂逻辑。所有排序规则（layer、pass、depth、instance-able）都编码在位里，sort 只知道 "这是一串 64-bit 数"。扩展规则时加 bit、挪 bit 就行。

## 相关

- [[stingray-render-context]] —— Command 是 RC 里跟 sort_key 成对的数组单元
- [[stingray-render-device-dispatch]] —— dispatch 里 stable radix sort + instance merging
- [[stingray-data-driven-render-config]] —— Layer System 在 render_config 里的声明
- [[render-config-extension-points]]
- [[triangle-plane-sort-translucency]]
- [[batching]]

## Sources

- [[sources/bitsquid-renderer-walkthrough-3-6-canonical]]
