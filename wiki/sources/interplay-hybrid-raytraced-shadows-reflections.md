---
tags: [source, 渲染, 光线追踪, bvh, compute-shader, 阴影, 反射]
date: 2026-04-14
sources: 1
---

# Hybrid raytraced shadows and reflections（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2018 年 7 月在 DXR / Metal raytracing API 刚发布的时候做的一次小实验：**在没有 DXR 硬件的情况下用 compute shader 手写一条完整的 hybrid ray tracer**，为阴影和镜面反射各投射一条 secondary ray，以此探索「混合管线到底贵在哪里、省在哪里」。

## 摘要

Hybrid 结构：primary ray 用常规光栅化 G-Buffer；secondary ray 在 compute shader 里用 CPU 构造的 BVH 做加速。BVH 是朴素的——叶子里只放 prop 的 AABB + 几何指针而非三角形，构造按「最长轴二分」而不是随机轴，也没有实装 SAH。BVH 在 compute shader 里线性化存储，每个左节点存「跳到右兄弟的 offset」，`do-while` 里用 `index += collision ? 1 : nodeOffset` 实现无栈深度优先遍历。叶子命中不等于 prop 命中（射线可能擦角），所以必须遍历全树再对候选 prop 的所有三角形做 Möller–Trumbore ray-triangle 测试。Shadow pass 要 first hit、关 backface culling；reflection pass 要 closest hit、要在三角形上插值 normal/uv、采 texture atlas、做 shading——**reflection 的成本大约是 shadow 的 2 倍**（GTX 970 / 200 props：shadow 1.5ms，reflection 2.4ms）。

一大串性能尝试里唯一显著见效的是**把顶点 position 从 R32G32B32_FLOAT 改成 R8G8B8A8_SNORM**——因为 raytracing shader 是 memory-bandwidth bound，同一个 vertex 会被触碰多次，数据宽度压到 1/4 是实打实的 4× 收益。NSight 验证瓶颈从 `TEX + Long Scoreboard` 明显下降。另外 thread group 从 256 降到 64 有少量 occupancy 收益；shared memory 缓存 BVH 或 potential collision list 都没收益。最后给出了一条通用原则：**编译器按最大分支分配寄存器——大分支即使不常走也会压低 occupancy**，所以叶子命中不立刻做 ray-triangle 测试，而是先收集再另算。还演示了 normal-map 扰动让 reflection 从 2.4ms 涨到 3.9ms 的 divergence 成本。

## 关键要点

- Hybrid = primary raster + secondary ray trace；每类 secondary 独立切换，按预算分配。
- BVH 存成深度优先线性数组 + 右兄弟 offset = 无栈 compute shader 遍历。
- **叶子命中不立刻做 ray-triangle 是性能优化**——避免大分支导致的寄存器过分配。
- 顶点格式是 memory-bandwidth bound 场景的第一优化点：`R8G8B8A8_SNORM` / `R16G16B16A16_SNORM` 比 float32 显著快。
- Reflection ≈ 2× shadow 成本——因为要最近命中 + attribute 插值 + shading。
- Shadow 1/4 分辨率靠 TAA 补回质量——用 depth downsample 阶段循环切换 4 个 hi-res sample 来模拟 jittering。
- Divergent ray（normal map、refraction）对 raytracing 性能影响巨大——每 warp 32 线程走不同路径，cache 命中崩。
- Maxwell 上 occupancy 约 30%，scoreboard 高；文章自认这是一次没完成的性能优化起点。
- 作者主张 **raytracing 不会近期取代光栅化**，而是「complement it nicely」——这个判断和后来 UE5 Lumen / gkNextRenderer 的走向一致。

## 链接到的概念

- [[hybrid-raytraced-shadows-reflections]]
- [[hybrid-raytracing-pipeline]]
- [[deferred-rendering]]
- [[sdf-ray-marched-shadows]]
- [[shadow-mapping-basics]]
- [[visibility-buffer]]
- [[compact-vertex-format]]
- [[gpu-latency-hiding]]
- [[temporal-antialiasing]]
- [[gpu-based-occlusion-culling]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2018/07/04/hybrid-raytraced-shadows-and-reflections/
- 本地：`raw/articles/interplayoflight.wordpress.com/2018-07-04_hybrid-raytraced-shadows-and-reflections.md`
