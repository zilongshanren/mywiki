---
tags: [shader, vfx, 顶点动画, mesh, explosion, unity, urp]
date: 2026-04-19
sources: 1
---

# 三角形爆炸 Shader

**Mesh Explosion**（或「shatter」「debris」）是一种 vertex shader 驱动的 VFX：把网格的每个三角形沿某个方向向外扩散，造成物体被炸开的视觉。和 CPU 做 mesh slicing 相比，shader 版不修改 mesh 数据，所有位移都在 vertex 阶段完成，代价低但能做出近似效果。[[daniel-ilett|Daniel Ilett]] 在 *Shader Toolbox for URP* 的 Mesh Explosion 是这种效果的可参数化版本，暴露三种 expansion mode 分别对应三种数据来源。

## 核心难点：如何让三角形作为整体移动

关键挑战是**「整个三角形沿同一方向移动」**，而顶点是 shader 的最小执行单元。三角形的三个顶点在 vertex shader 里各自被调用一次，如果每个顶点按自己的信息独立位移，三角形会**变形**而不是**平移**——相邻三角形共享顶点也会被撕开。

要让三个顶点同步移动，必须让它们收到**完全一致的「这个三角形的位置信息」**。shader 里做不到「读取当前三角形」这种语义（除非用 geometry shader 或 mesh shader），所以数据必须**预先烘进顶点属性**——每个顶点存储「我所属三角形的中心」。

## 三种 Expansion Mode

对应三种不同的方向/位置数据来源：

- **Normal 模式**：沿 vertex normal 向外扩。不需要预处理，但缺陷明显——三个顶点法线不同，三角形会被拉扯变大/变形。适合纹理简单或不在乎几何完整性的场景，例如「爆炸成发光颗粒」。
- **Offset 模式**：给一个**空间中的 origin point**，每个顶点沿 `normalize(position - origin)` 扩散。所有顶点共用同一个 origin，所以越靠近 origin 的三角形各顶点方向越分散——三角形还是会变形，但方向一致性比 Normal 模式好。适合「从一点炸开」的爆炸中心。
- **Colors 模式**：每个顶点的 vertex color 里预先烘入「我所属三角形的中心位置」。三个顶点方向完全一致（都指向同一个 `center - origin`），三角形整体平移而不变形。这是唯一能保持几何完整性的模式。

为支持 Colors 模式，pack 附带 **BakeFaceColors.cs** 脚本：遍历 mesh 的 triangle list，算出每个三角形的中心 `(v0 + v1 + v2) / 3`，塞进对应三个顶点的 vertex color 里。原本 vertex color 是 RGBA `[0, 1]`，用来编码 3D 位置需要缩放/偏移——具体编码细节教程没说，但标准做法是把 local-space bounds 映射到 `[0, 1]³`，shader 里反解。

这种**把静态预计算 bake 进 vertex attribute 再在 shader 里读取**的思路是 [[compact-vertex-format|压缩顶点格式]]的常见设计模式——让 shader 不用访问额外的资源就能拿到「三角形级别」的信息。

## 扩散曲线：distance + shrink + gravity + jitter

- **Explosion Distance**：从 0 到任意值驱动爆炸进度。通常从外部脚本按 `Time.time` 或 animator curve 插值。
- **Debris Shrink Speed**：距离越远三角形越小——碎片远离时逐渐消失。实现上是在顶点位移的同时按 `scale = 1 - distance * shrinkSpeed` 缩放三角形（以三角形中心为轴）。
- **Gravity**：y 方向叠加 `-0.5 * g * t²`（或简化为线性 `-g * distance`）让碎片弧线下落。它不是真实物理但视觉上比直线飞出好得多。
- **Random Offset Range**：每个顶点额外乘一个 `hash(position) * range` 打散方向。过大会直接毁掉三角形形状——这是调参里的主要权衡。

## 和其他爆炸方案的对比

| 方案 | 成本 | 保形 | 交互 |
|------|-----|-----|------|
| Mesh Explosion shader | 低（vertex） | Colors 模式可 | 无 |
| Unity Shuriken mesh particle | 中 | 每粒子独立 | 有限 |
| 实时 mesh slicing | 高（CPU） | 完美 | 可 |
| Pre-fractured + Rigidbody | 高（物理） | 完美 | 完全 |

shader 版的适用场景：**一次性、非交互的爆炸视觉**——Boss 被打败、道具消失、传送特效。需要交互（碎片能被玩家撞）就得用 Rigidbody 方案。

## 相关

- [[compact-vertex-format]] —— 把预计算数据塞进 vertex attribute 的通用设计
- [[vertex-shader-basics]]
- [[texture-dissolve]] —— 另一种「物体消失」的 VFX 骨架，可以和爆炸叠加
- [[fizzle-lod-fading]]
- [[daniel-ilett]]

## Sources

- [[sources/danielilett-toolbox-urp-mesh-explosion]]
