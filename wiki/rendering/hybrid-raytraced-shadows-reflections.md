---
tags: [渲染, 光线追踪, 阴影, 反射, bvh, compute-shader, gpu-driven, 混合管线]
date: 2026-04-14
sources: 1
---

# 混合光追：硬阴影与镜面反射（Compute Shader 实现）

2018 年 DXR 和 Metal raytracing API 刚发布，[[kostas-anagnostou|Kostas Anagnostou]] 在没有 DXR 硬件的前提下，用**纯 compute shader 手写了一条能跑 200 个 prop instance、带 BVH 的 hybrid ray tracer**，以此摸清「混合管线到底贵在哪里、省在哪里」。它不是 production-ready 的技术，而是一次干净的 profiling 实验。

这篇是 [[hybrid-raytracing-pipeline]] 早期最有参考价值的公开工程记录之一。

## 混合结构：primary = 光栅，secondary = ray

所谓 *hybrid* 是明确定义的：

1. **Primary ray 用光栅化**——走常规 deferred G-Buffer pass，从 depth 重建 world position 作为 secondary ray 的起点。
2. **Secondary ray 用 compute shader 追**——shadow、reflection、AO 各一条/若干条射线。
3. **每一类 secondary 可以独立选择**——可以只加 RTAO 不加 RT 反射，也可以反过来，根据预算分配。

这条路线的前提是 *Imagination* 早在 2014 年就用 PowerVR 硬件验证过，不是新思路，但 Anagnostou 把它在消费级 NVidia 上完整重走了一遍。

## BVH 构造：CPU 端按最大轴二分

Anagnostou 用的是最朴素的 BVH 方案——接近 Peter Shirley *Raytracing: The Next Week* 里的思路，但做了一个小修改：

- 不像 Shirley 那样随机挑分割轴——**每一步挑当前 AABB 最长的轴**。因为他的示例场景 Y 轴很短，随机挑到 Y 轴会产生非常扁的 subtree。
- 更好的选择是 **SAH (Surface Area Heuristic)**——按「面积 × 内部多边形数」的代价函数选分割点，在 prop 分布不均匀的真实场景（即 prop 密度、尺寸、polycount 都异构）里会明显更好。他没实现，留为 TODO。
- **BVH 的叶子里只放 prop AABB + 几何指针**——不到三角形粒度。这会让命中叶子之后仍然要对该 prop 的所有 triangle 做 ray-triangle test，是明显的性能瓶颈，但换来的是更浅的树和更简单的构造代码。

## BVH 在 compute shader 里怎么遍历

递归不可用于 shading language，Anagnostou 没走 explicit stack，而用了更紧凑的方案——**线性化 BVH，每个左节点存「跳到右兄弟的 offset」**。BVH 按深度优先顺序存入一个 structured buffer：

```hlsl
struct BVHNode {
    float3 minBounds; int instanceIndex;   // -1 表示内部节点
    float3 maxBounds; int nodeOffset;      // 命中失败时跳到的位置
};
```

shader 遍历是个 `do-while`：

- **命中 AABB**：`index += 1` 继续往左子树走；
- **未命中**：`index += nodeOffset` 跳过整条右侧兄弟分支；
- **到达叶子**：把 `instanceIndex` 追加到「潜在碰撞列表」——**但不能立刻终止**，因为 AABB 命中不保证 prop 命中（典型反例：射线擦过 cube 的角，打到里面的球）。

所以遍历必须**走完整棵树**，最后得到「潜在碰撞 prop 索引」数组（固定上限 5 个）。这个设计对 shadow 和 reflection 两条路径有微妙差别（见下文）。

**在叶子里立刻做 ray-triangle 测试而不是先收集 prop**：作者实测**更慢**。原因是「节点遍历 + 三角形求交」合并后 shader 有大分支，**编译器会为最大分支保守分配寄存器**——即便大分支不常走，每条线程都付出这笔寄存器预算——结果 occupancy 下降、memory latency 藏不住了。这是全文最通用的 GPU 教训之一：**分支大小 = 寄存器预算**。

## Ray-primitive 求交

- **Ray-AABB**：slab method 的标准写法，用 `rayDirInv` 减掉除法。
- **Ray-triangle**：Möller–Trumbore 算法，从 Yuriy O'Donnell 的 *RayTracedShadows* 移植而来。返回射线沿 `t` 的距离和 barycentric 坐标——后者对 reflection pass 至关重要，因为需要在三角形表面插值 uv 和 normal。

## Shadow pass：简单的一面

找到 first ray-triangle hit 即可返回 *occluded*——不需要最近命中。为了速度还关掉了 backface culling——任何面都能遮光。在 quarter-res 屏幕 buffer 里跑，再用 **TAA** 补偿。

> TAA 这里有个小 trick：没有 projection matrix 可以 jitter，所以在深度 buffer 做 1/4 降采样的时候**循环使用 4 个高分辨率 sample 中的一个**来重建 world position——相当于时间域的 supersampling。配合 neighborhood clamping 解 ghosting。

## Reflection pass：明显更贵

Reflection 不只要**找到**命中，还要**找到最近的命中**（否则反射顺序错），还要在三角形上插值 normal 和 uv，采 texture atlas，最后做一次 shading。核心循环里多了一个 `if (t < minDist)` 比较，每次 hit 都保留最小 t。

结果**镜面反射是 shadow 的 2× 成本**（2.4ms vs 1.5ms，GTX 970 @ 200 props），这个比例很有参考价值。

## 性能优化：真正起作用的那一项

一大串尝试里，**唯一显著见效的是改数据格式**：

| 尝试 | 效果 |
|---|---|
| Shared memory 存 potential collision list | 几乎无差别（数组太小） |
| Shared memory 缓存 BVH | 反而更差（需要增大 thread group → occupancy 掉） |
| Thread group 从 256 → 64 | 小有收益（occupancy 提升） |
| **顶点 position 格式：R32G32B32_FLOAT → R8G8B8A8_SNORM** | **显著提速，最大收益** |

原因很直白：**raytracing 是 memory-bandwidth bound**。同一个顶点在 BVH 遍历里可能被多次触碰，带宽翻倍带宽翻倍——把数据宽度减到 1/4 就是实打实的 4×。作者的 object-space position 原本就在 `[-1, 1]` 范围内，SNORM8 精度对阴影够用。对范围稍大的场景，`R16G16B16A16_SNORM` 仍然是很好的 trade-off。

NSight 的 profile 直接验证这一点：改格式前 shader 是 **TEX bound**，warp 大量阻塞在 `Long Scoreboard`（等 memory fetch）；改完后 TEX 瓶颈退到次位，SM 利用率显著上升。

## 总结级的工程教训

作者在结尾给出了几条可以直接抄进笔记本的原则：

1. **Raytracing shader 的瓶颈永远先考虑 memory bandwidth**——SoA 布局、lower precision、只读自己真需要的 attribute。
2. **小 thread group 往往比大 thread group 好**——至少在 Maxwell 上，小 group 更容易填满 SM、藏住 latency。
3. **避免大分支**——编译器按最大分支分配寄存器；大分支即使不常走，也会压低全局 occupancy。
4. **避免 divergent path**——一条 warp 里的 32 条线程如果走完全不同的 shader 路径（例如 refraction 下每像素不同的 ray direction），cache 命中率和执行效率都会崩。作者实测：**在地面加一张 normal map**就让 reflection 从 2.4ms 涨到 3.0ms；法线扰动加倍再涨到 3.9ms。这直接解释了为什么软反射和漫反射 raytracing 总是比硬反射贵得多。

## 和 RT API 出现之后的关系

这个 demo 在硬件 BVH 出来之前用 compute shader 手写了完整的**「CPU 建树 → GPU 遍历 → ray-triangle 求交」**全链路。DXR / Metal 的硬件 intersection 主要解决的是**树的构造和遍历效率**，但：

- **数据布局的经验继续有效**——顶点格式、tangent/normal 的存储、mesh LOD 选择都是和硬件 RT 同样相关的问题；
- **混合管线的策略不变**——光栅化做 primary、硬件 RT 只做 secondary 这条主线在 RTX 时代被各家厂商（UE5 Lumen、gkNextRenderer 等）反复验证。作者的这篇实验是这条路线的**早期全景图**。

文中也留下了一些明显的漏洞作为 future work：

- 反射表面本身没有阴影（需要从反射点再发一条 shadow ray，shader 复杂度暴涨）；
- 没有 material / shader LOD——远处不会跳过昂贵的 shader；
- Ray-triangle 的 loop 里**每次都要重算顶点 transform**——没有 vertex cache，作者建议把变换后的顶点落回 global memory 作为 tradeoff 探索。

## 相关
- [[hybrid-raytracing-pipeline]] —— 同一主题的成熟版落地（gkNextRenderer）
- [[deferred-rendering]] —— hybrid 管线里 primary ray 的替代品
- [[shadow-mapping-basics]] —— 传统阴影方案
- [[sdf-ray-marched-shadows]] —— raymarch 阴影的另一种形态
- [[visibility-buffer]] —— hybrid 管线的现代替代 primary
- [[compact-vertex-format]] —— 顶点格式优化
- [[gpu-based-occlusion-culling]] —— 共享的 global buffer + args buffer 数据布局
- [[multidraw-indirect-occlusion-culling]] —— 同一套 data layout
- [[gcn-wave-occupancy]] —— wave / warp occupancy 的一般框架
- [[gpu-latency-hiding]]
- [[temporal-antialiasing]] —— 1/4 res shadow 靠 TAA 补回质量
- [[kostas-anagnostou]]
- [[the-forge-renderer]] —— Confetti 在 2018 年 9 月把这套 hybrid shadow 移植到 The Forge，跨 PC / macOS / iOS / Xbox 运行（含 iPhone 7 Sponza demo）
- [[ray-tracing-api-debate]] —— Wolfgang Engel 对 DXR 黑盒化的公开质疑，hybrid 移植是这场辩论的工程姿态
- [[people/wolfgang-engel]]

## Sources
- [[sources/interplay-hybrid-raytraced-shadows-reflections]]
- [[sources/wolfgang-engel-ray-tracing-without-api]]
