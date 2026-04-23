---
tags: [渲染, 深度缓冲, shader]
date: 2026-04-19
sources: 1
---

# 线性 Z 小把戏（`hPos.z *= hPos.w / far`）

[[angelo-pesce|Pesce]] 在 2010 年的《Know your Z》给出一个顶点着色器小技巧：在把裁剪空间位置送往光栅化之前，做

```
hPos.z *= hPos.w / farPlaneViewZ;
```

因为深度缓冲最终写入的是 `z/w`，投影后 `z` 在 `[0, far]`，所以经过这次乘除，写入深度缓冲的值就变成 `z / far`——**一个在视空间线性的 `[0, 1]` 深度**。相当于把 W-buffer 的效果用一行 VS 指令塞进了 Z-buffer。

## 它不动 `w`，所以不破坏透视插值

关键点：这个技巧**只改 `z`，不碰 `w`**。因此纹理坐标的透视校正插值完全不受影响——不像直接 `hPos /= hPos.w`（《Know your Z》里的 Option A）那样把整个齐次坐标压扁、禁掉透视插值。

## 代价：Z 在屏幕空间不再线性

Pesce 一开始漏掉了同事提醒的坑：**做完这个变换，`z/w` 在屏幕空间不再沿三角形平面线性插值**。光栅化对 `z` 做的是屏幕空间线性插值——但线性视深度 / w 并不落在一个平面上。后果：

- 三角形内部的 Z 会**沿曲面弯曲**，可能和相邻三角形对不齐，出现新的 Z-fighting。
- 粗粒度 **Hi-Z / Z 压缩**会失效或变差——它们依赖 `z/w` 的屏幕空间线性。
- 近平面裁剪在某些卡上会出怪异行为（Pesce 自己没复现，但有读者报告）。

**什么时候能用**：物体**细分足够密**、不存在近距平行墙面、且你明确需要线性深度做阴影 / 重建。比如角色 shadowmap——Pesce 原文里专门点了这个场景。

## 与同类方案的关系

- **W-buffer**：硬件原生的线性深度方案。在 DX9 后基本被弃，现代硬件不直接支持；这个 shader 小把戏算是 W-buffer 的软件模拟。
- **[[reversed-z|Reversed-Z + float]]**：当下主流方案。用 float 精度分布抵消投影矩阵的远处稀疏，不需要线性化，也不破坏屏幕空间线性。
- **Logarithmic / Linear view-space depth**：在 PS 里从 `z/w` 反算或 VS 里单独输出 `viewZ` 插值，和本 trick 的思路一致，但把线性化推到 PS 或插值器，避免 Hi-Z 失效。

评论区有读者贴了 [Humus 的 linear depth 分析](http://www.humus.name/index.php?page=News&ID=255)；Pesce 对其中「线性 z 让 Hi-Z 容易算 tile 深度范围」的说法持保留意见——Hi-Z 从 quad 的插值结果里拿边界，不依赖 `z/w` 的屏幕空间线性。

## 结论

一个有用的小工具，但不是万能药。大多数场景用 [[reversed-z]] 就够了；这个 trick 只在**需要线性 view-space Z 且能接受精度代价**的窄场景下亮相（角色阴影、某些 deferred 重建路径）。

## 相关

- [[z-buffer]]
- [[reversed-z]]
- [[z-fighting]]
- [[hierarchical-z-buffer]]
- [[coordinate-spaces]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-know-your-z]]
