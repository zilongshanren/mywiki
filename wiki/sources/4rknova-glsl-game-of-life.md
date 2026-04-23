---
tags: [source, glsl, shadertoy, cellular-automata, conway]
date: 2026-04-19
sources: 1
---

# Conway's Game of Life（Nikos Papadopoulos / 4rknova.com）

[[nikos-papadopoulos]] 2013 年 1 月的短文，给出 Conway 生命游戏的 GLSL/ShaderToy 实现。

## 摘要

文章先复述生命游戏的四条规则（邻居少于 2 死、多于 3 死、2-3 活、死细胞恰 3 邻居复活），然后贴出 [[shadertoy-basics|ShaderToy]] 风格的 fragment shader 实现：利用 [[ping-pong-surfaces|多缓冲 ping-pong]] 把上一帧状态采样到 `iChannel0`，当前 frag 根据 8 邻居判断下一代。作者还给了个可以用的 bit-mix 哈希函数 `hash(uint)`，通过操控 IEEE 754 mantissa bit 从 UV 坐标快速生成伪随机初始占位。代码另一个小亮点：活细胞的输出值不是简单的 0/1，而是 `1.0 / count`，把 2 和 3 邻居的活细胞编码成不同的"生命点数"，便于后续可视化。整篇文章是教学级别的最小 demo，没涉及性能优化。

## 关键要点

- GLSL 生命游戏的经典写法：一帧一步、上一帧为纹理输入、当前帧写回 fragment。
- 8 邻居用 `vec3(0,1,-1)` 的排列组合去偏移采样坐标，避免 9 次独立 swizzle。
- bit 操作哈希：`floatBitsToUint` + 整数散列 + 写回 mantissa，一行生成 `[0,1)` 均匀随机数。
- 该实现是**朴素版**——每 frag 九次纹理采样，完全依赖 GPU L1 缓存；与 [[gpu-gol-optimization-ladder|Boris 的优化阶梯]]（PyTorch → Triton → CUDA 位打包，330× 提速）形成典型"naive vs optimized"对照。

## 链接到的概念

- [[shadertoy-basics]]
- [[ping-pong-surfaces]]
- [[gpu-gol-optimization-ladder]]

## 原文

- 链接：<https://www.4rknova.com/blog/2013/01/27/game-of-life>
- 本地：`raw/articles/4rknova.com/2013-01-27_conway-s-game-of-life.md`
