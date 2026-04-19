---
tags: [2d渲染, sprite, instance-draw, storage-buffer, 顶点压缩, batching]
date: 2026-04-19
sources: 1
---

# Sprite 批渲染：instance draw 与 storage buffer 压缩

2D sprite 批渲染的经典做法是把多个矩形的四角顶点写进同一个 vertex buffer，一次 draw call 提交。顶点属性至少含 `vec2 pos; vec2 uv;`。当需要支持 sprite 的旋转/缩放，一条 2×3 仿射矩阵会让每顶点负载膨胀到 10 个浮点，且 4 个顶点共享同一条矩阵——出现大量冗余。[[cloudwu]] 在 Soluna 框架里沿着"砍掉重复"的主线做了一轮优化。

## 去掉 mat2 重复：storage buffer + index

`mat2 sr` 在一个 sprite 的 4 个顶点上完全相同；且绝大多数 sprite 是单位矩阵，有旋转的角度也很有限。把唯一的 SR 矩阵表放进 storage buffer，顶点只保留一个 index，冗余就压下来了。`vec2 t`（translation）每个 sprite 不同但顶点间重复，暂时保留，稍后由 instance 机制处理。

## 去掉 per-sprite 重复：instance draw

`index` 和 `vec2 t` 仍在 4 顶点间重复。改用 [[draw-procedural-gpu|instance draw]] 就把它们从顶点流中抽出，放到 per-instance buffer。附赠收益：可以用三角条带描述矩形，省掉 index buffer。

一个小设计点：instance draw 原本是为"同一组顶点数据重复渲染"设计的，这里每个 instance 其实是不同矩形。所以顶点着色器不再用真的 vertex buffer，而是把 sprite 元信息放进另一个 storage buffer，用 `gl_InstanceIndex` + `gl_VertexIndex` 在 shader 里查表索引。

## 利用几何约束进一步压缩

- **轴对齐**：sprite 矩形四角只需要记对角两个点，4 个顶点由 shader 按 bit 位组合出来
- **同形约束**：offset 矩形与 UV 矩形形状一致（贴图上一块矩形完整映射到画布上一块矩形），节约再一半信息
- **整数像素坐标**：贴图尺寸不超万像素，int16 够用

最终 sprite 元信息每条只需 6 个 int16 = 12 字节塞 storage buffer，加上 draw primitive 的 3 float（x, y, mat_index）= 26 字节/sprite。这比 ejoy2d 当年在 CPU 做 2×3 定点数矩阵、四顶点全展开的方案要薄很多，也比朴素 10 float 顶点格式节约 70%+ 带宽。

## CPU 侧：batch 中间层

sokol 等图形 API 不支持多线程，所有指令必须在同一线程提交。解法：引入 batch 中间层——多个线程各自持有 batch，逻辑层只往 batch 里填 `draw_primitive`，渲染线程统一 drain 并翻译成图形指令。`draw_primitive` 里 `sprite id` 的负数位保留给非默认材质（文本等），下一条记录即该材质参数，省下显式 tag 字段。

## 相关

- [[draw-procedural-gpu]]
- [[batching]]
- [[compact-vertex-format]]
- [[vertex-shader-basics]]
- [[soluna-2d-engine]]
- [[cloudwu]]

## Sources

- [[sources/cloudwu-soluna-2d-pipeline]]
