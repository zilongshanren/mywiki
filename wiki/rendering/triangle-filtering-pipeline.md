---
tags: [渲染, gpu-driven, 几何, 剔除, compute-shader, executeindirect, async-compute]
date: 2026-04-19
sources: 1
---

# Triangle Filtering Pipeline（Confetti / The Forge 版）

[[people/wolfgang-engel|Wolfgang Engel]] 和 Confetti 团队在 2015–2018 期间把「几何剔除 + [[visibility-buffer|Visibility Buffer]] 填充 + Forward++ 光照」整合成一条**跨 DX12 / Vulkan / Metal 2 / 主机平台**都能跑的 GPU-driven 管线。核心理念：**把三角形当作数据而非绘制单元**——所有剔除决策都在 compute shader 里以 triangle 粒度做，光栅化阶段只接收已经「按摩过」的最小可见集合，再用 `ExecuteIndirect` 一次性提交。

这一条管线是 [[triangle-visibility-buffer]] 系列文章的主干，对高分辨率（4K/5K/8K）+ 带宽受限平台特别有意义。

## 三级剔除串联

### 1. Cluster Culling（CPU）

把 mesh 切成 256 个三角形一组的 cluster，离线或运行时计算：

- **cluster normal cone**：累加每个三角形的负法线方向得到锥心，取"最紧"的三角形平面算锥开角
- **摄像机在锥内** ⇒ 整个 cluster 背对摄像机 ⇒ 整组剔除

效果高度依赖场景几何：法线分布杂乱的场景（例如 *San Miguel*）收益低，Confetti 的 demo 默认关掉了它；硬件 tessellation 生成的密集几何里收益高。

### 2. Triangle Filtering（GPU async compute）

每 256 个三角形派发一个 compute workgroup，对每条三角形依次测试：

- **Degenerate + Back-face**：用 Olano / Greer 的 2D 齐次坐标判据，测 3×3 矩阵 `[v0.xyw; v1.xyw; v2.xyw]` 的行列式——`det ≥ 0` 背面或退化可剔。理论上能去掉 ~50% 几何
- **Near plane clip**：若三顶点 `w` 都为负，整条剔除；有一到两个在近裁面前的特殊处理是把 `w` 取反避免投影到屏幕两侧
- **Frustum**：先把 `xy` 除以 `w*2 + 0.5` 归一化到 `[0,1]`，bbox 完全在 `[0,1]` 外就剔除
- **Small primitive**：把三角形投影后生成子像素 bbox，判断是否覆盖任何采样点（含 MSAA），不覆盖就剔除

所有剔除通过后，三角形的 index 被 append 到该视点的 **filtered index buffer**。

### 3. Draw Call Compaction（compute）

上一步会留下很多"空洞"——一批 256 个三角形可能一个都没活下来。空 draw call 对 command processor 依然要做完整的 state 设置，是浪费。compaction shader 重新扫描并写出紧凑的 indirect argument buffer + 对应的材质索引 buffer，最后由一次 `ExecuteIndirect` 吞下。

## Multi-View 剔除：省的是带宽，不是三角形

Confetti 管线一个关键工程选择：**同一次 triangle filtering compute 里同时对多个视点（主摄像机 + 阴影图 + RSM …）做剔除**。

这样做看起来更亏——一条三角形只要在任何一个视点里可见就得保留，**最终可见集是所有视点的并集**——但实际上：

- 三角形数据（vertex + index）从显存读出来的成本远高于几条视锥判断的计算
- 多视点合并**让每个三角形只 fetch 一次**，总带宽显著下降
- 各视点的 filtered index buffer 分别输出，不相互污染

在 San Miguel 8 M 三角形场景里，主视点过滤后剩 2.32 M，阴影视点剩 1.84 M——各自用各自的 IB，但加载只做了一次。

## Visibility Buffer 填充：32+32 = 64 bit

过滤好的三角形用 `ExecuteIndirect` 光栅到两张 32-bit render target：

- **VB target (R8G8B8A8)** = `[alphaMasked:1][drawID:8][triangleID:23]`
- **Depth**（32-bit）

对比 5 张 G-Buffer（alb/normal/rough/mat/emissive）+ depth 的传统 deferred，1080p 2× MSAA 下 VB 差不多是 G-Buffer 的 1/3 带宽；分辨率越高差距越大。

## Forward++：VB 基础上的 tiled lighting

命名是对 Forward+ 的戏谑升级。Visibility Buffer 已经保证**屏幕空间每个像素最多只有一层 opaque 三角形**，所以 shading pass 可以：

1. 读 VB 的 drawID / triangleID
2. 从 IB/VB 取三顶点，计算 **screen-space 重心 + 偏导**（用 Schied 论文 Appendix A Eq.4 的显式公式，不走硬件 `ddx/ddy`）
3. 在屏幕空间用这些偏导重建任何顶点属性（normal、tangent、uv）并做 **perspective-correct interpolation**
4. 一次 shading 循环里处理完 directional + tile 光源列表（和 Forward+ 的 tiled light list 逻辑一致）

不透明几何从头到尾**只有这一次 shading 运算**；半透物仍回退到传统 Forward+。这份管线实测 L2 cache 命中率对 texture / vertex / index buffer 接近 99%，因为屏幕空间访问模式是 GPU 架构师设计时的"理想形状"。

## 现代意义与改进点

- **几何 API 层面**的演进（UE5 Nanite、D3D12 work graphs、mesh shader）都印证了 Engel 在文章里写的那句话——「三角形剔除是下一代管线的基础设施」
- **已知问题**：读者评论指出 Confetti 的 barycentric 偏导公式在靠近近裁面 / 越过摄像机的三角形上会炸（projection 非线性），修复需要显式 clip 或回退到 3D 长算法
- 未来迭代方向（Engel 自述）：PBR 材质、ray tracing 协同、object-space shading

## 相关

- [[visibility-buffer]] —— 核心概念页
- [[deferred-rendering]] —— 直接对标的替代方案
- [[gpu-driven-grass-tiles]] / [[gpu-based-occlusion-culling]] —— 同一 GPU-driven 思路的 mesh 粒度版本
- [[multidraw-indirect-occlusion-culling]] —— Kostas 的 draw-call 粒度剔除
- [[meshlets-and-mesh-shaders]] —— mesh shader 时代的 cluster 剔除
- [[async-compute]]
- [[bindless-rendering]]
- [[people/wolfgang-engel]]
- [[the-forge-renderer]]

## Sources

- [[sources/wolfgang-engel-triangle-visibility-buffer]]
