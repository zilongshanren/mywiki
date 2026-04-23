---
tags: [渲染, 性能]
date: 2026-04-05
sources: 1
---

# 批处理（Batching）

**把多个对象合并成一次绘制，减少 Draw Call 或状态切换成本**。

## 批处理类型

### Static Batching

编译时合并**静态**对象的 mesh 到一个大 mesh。运行时零成本，但：
- 无法移动
- 合并后的 vertex buffer 更大，不能 instanced
- 内存成本高

### Dynamic Batching

运行时按帧合并小 mesh 到临时 vertex buffer。适合小对象（<300 顶点）。每帧 CPU 开销。

### GPU Instancing

**同一个 mesh + 同一个 material 的多个副本**在一次 DrawCall 画完，通过 per-instance data（位置/颜色/uniform）区分。**真正减少 DrawCall 数量**。适合草、树、粒子。

### SRP Batcher（Unity）

用**持久化 Constant Buffer**，不同 material 的对象只要使用同一个 shader 变体就能连续渲染，避免 CB 重新上传。**减少的是状态 setup 开销，不减少 DrawCall 数量**。

## 批处理的真正对象

批处理要规避的是：
1. DrawCall 本身（Instancing）
2. 状态切换开销（SRP Batcher、Texture Atlas）
3. CPU submission overhead（命令缓冲构建）

## 限制

- **不同材质**不能（不改）合批。
- **不同 shader 变体**打破 SRP Batcher。
- **Skinned Mesh** 通常需要专门路径。

## 相关
- [[draw-call]]
- [[rendering-pipeline]]
- [[culling]]
- [[gl-draw-accumulator-batching]] —— Supnik 的 GL 累加器：同状态合批 + 层重排 + 状态合并

## Sources

- [[sources/rtr-day02]]
