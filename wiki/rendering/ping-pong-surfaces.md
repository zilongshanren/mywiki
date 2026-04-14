---
tags: [shader, 后处理, 多趟渲染, 显存]
date: 2026-04-14
sources: 1
---

# Ping-Pong Surfaces：多趟 shader 的显存救命术

**Ping-Pong**（乒乓）是一种只用**两块** surface / render target 在它们之间反复倒腾数据，以实现任意多趟 shader 的技术。它的价值在于：一旦你的效果不得不走**多趟**（multi-pass），朴素做法会线性吞显存，而 ping-pong 可以把显存占用**钉死在两倍 surface 大小**。

## 为什么要多趟

最典型的动机是[[msaa-ssaa|大尺度模糊]]。一个 9×9 盒模糊要 81 次采样；但是把它拆成两次 5×5 模糊，总采样数是 `2 × 25 = 50`，少了一半。放到 17×17（289 次）vs 四趟 5×5（100 次）的时候差距更夸张。也就是说，把一次贵的 shader 拆成几次便宜的 pass，本身就是性能优化——[[gpu-latency-hiding|算力]]和带宽都能受益。不光模糊，**描边、光晕（bloom）、辉光**等多层卷积效果都吃这一招。

## 朴素做法 vs Ping-Pong

**朴素做法**：N 趟就建 N 个 surface，`A→B→C→D…`。如果你写过 10 趟的 bloom，全分辨率下 10 张 surface 会占掉大量[[virtual-memory|显存]]；而且如果开了 surface depth，每张还要再配一个 depth buffer，雪上加霜。

**Ping-Pong**：只要两张 surface `A`、`B`，任意多趟都是 `A→B→A→B…` 交替写。每一趟，当前的"目标"就是下一趟的"源"，循环复用。

## Feedback Shader：跨帧乒乓

Ping-pong 的另一个变体是**反馈 shader**：把**上一帧的输出**作为**这一帧的输入**，就能得到随时间演化的图形——粒子场、流体、生命游戏、残影轨迹。实现方式是维护一个布尔值 `surface_swap`，每帧取反，用它挑选当前帧的读写目标：

```gml
surface_swap = !surface_swap;
var _surf1 = surface_swap ? A : B;  // 这一帧写入
var _surf2 = surface_swap ? B : A;  // 这一帧读取
```

两张 surface 的角色每帧对调一次——跟[[taa-history-rectification|TAA 历史缓冲]]的逻辑完全一致，只是这里的"历史"是玩家能直接看到的视觉效果。

## 相关

- [[fragment-shader]]
- [[render-graph]]
- [[taa-history-rectification]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-recursive-shaders]]
