---
tags: [渲染, 地形, virtual-texture, anno, 缓存]
date: 2026-04-19
sources: 1
---

# Node Texture：Anno 1800 的地形「虚拟纹理」

[[thomas-poulet]] 在 [[sources/thomas-poulet-anno-1800-frame|Anno 1800 帧分析]] 里拆出的地形方案不是纯 virtual-texture / quadtree LOD，也不是经典的 splatmap——而是一种**固定尺寸的 node texture array + 每帧少量 bake 更新** 的混合方式。

## 问题

城建 top-down 游戏的地形要求：

- 覆盖面积巨大（多个岛 + 宽洋）
- 局部分辨率要高（玩家会 zoom 到最近）
- **编辑即时反馈**：放路、划田要立刻看到
- 帧预算不能 spike

纯 splatmap 满足不了分辨率；纯 virtual texture + quadtree 实现复杂且在编辑时切 LOD 会 flicker；Anno 选了更实用的中间路线。

## 两套纹理

1. **全局大图 (8K)**：两张覆盖整个 play area 的 8K 贴图——一张 **tint**（颜色调色）+ 一张 **grit**（沿岸的破碎细节）。它们在全图 zoom out 时生效，提供低频的一致性。8K 但覆盖超大区域，单位分辨率实际很低，作用是**打底色** + **断开重复感**。
2. **Node texture array (763 × 512²)**：每个地形 tile 对应一个 *node*，node 从这张 array 里取一个 slice 拿到自己的高频 diffuse + specular。763 这个数字看起来是**按内存预算 + 更新节奏选定**的池大小（不是按场景做 quadtree 动态分配）。Normal 和 tint 单独走 regular binding，没放进 array——推测是历史绑定决定或者有不同的驻留策略。

## 每帧 bake（烘焙）

array 里的 node 纹理**在运行时刷新**，集中在帧的开头。步骤两段：

1. **Render ground layers**：读一张 `R32_UINT` 的 **material map**（以 bitfield 形式编码哪些 layer 贡献这个 tile），blend 出底色——典型 tile 会混 10 来层，很多 layer 贡献极小（但给 road / 涂画这类编辑留了 headroom）。
2. **Apply decals**：在 baked 底色上贴 decal（路、装饰等）。

最后一步是**在 GPU 上跑一个自定义 compute shader 对 diffuse 做 BC7 压缩**、生成 mip 链，再写回 array slice。这样地形在主 color pass 里就是「采样一张已压缩的 BC7」—— 便宜。

## 工作负载分摊

引擎把 bake 的工作**跨帧分摊**，一次只更新少量 tile。tile dirty 的触发来自相机移动（视野新进入的 tile）+ 用户编辑（放路）。

## 和其他地形方案的对比

- **相比 quadtree VT**：没有多级 LOD 的 hole-filling 逻辑，编辑时不会在 LOD 级间 pop；代价是分辨率固定，不能 zoom 到超近。
- **相比 [[terrain-splatmap-shader-graph|splatmap per draw]]**：每帧不再在主 pass 里做 N 层混合，成本转移到 offline bake 上；一旦 bake 好就是一张普通纹理。
- **相比 [[virtualized-volume-textures|virtualized volume texture]]**：空间结构简化为一维 array + 索引 buffer，而不是 sparse 3D 结构，适合 2.5D 地形。

关键启示：**Virtual Texture 不一定要 quadtree + feedback loop。对顶视角城建游戏，用一个大 slice array + 每帧少量 bake 就够了**——这把 runtime 复杂度几乎完全消除，只要 CPU 调度一个「谁需要刷新」的队列。

## Sources

- [[sources/thomas-poulet-anno-1800-frame]]
