---
tags: [渲染, 剔除, simd, 性能]
date: 2026-04-14
sources: 2
---

# 视锥剔除：从 p/n-vertex 到 SIMD 极限

ryg 分两篇长文整理了他做视锥剔除十几年的经验，对象是 AABB 对视锥。文章的起点是回应 Zeux 的 view frustum culling 系列——Zeux 明确说「我没实现 p/n-vertex，但我确信它不会比我的 clip-space 方法更快」，ryg 则一路把方法演化到 SPU 上每箱子约 24 cycle 的 SIMD 实现，比 Zeux 原版快一倍以上。本页把两篇合并成一条清晰的递进链。

## 方法 1：8 个顶点对 6 个世界空间平面

最朴素的做法：把 AABB 的 8 个角逐个点乘 6 个平面，若 8 个点都在某平面外侧——完整剔除。不用解释，作为 baseline。

## 方法 2：变换到 clip space 再比

把 8 个顶点 `M * v` 送进 clip space，然后用极其简单的 `-w ≤ x ≤ w`、`-w ≤ y ≤ w`、`-w ≤ z ≤ w`（或 OpenGL 的 `0 ≤ z ≤ w`）做 6 次不等式。代价是 8 个顶点变换，好处是平面方程免费（齐次坐标的 6 个面就是坐标轴）。Zeux 的系列从第 5 部分起用的就是这种。

### 2b：非 FMA 平台的公共子表达式

朴素算 8 个顶点 × 4 分量 × 3 乘加 = 96 乘法。但 `mat[0][0] * min.x` 和 `mat[0][0] * max.x` 每个都被 4 个顶点共享，抽出公共子表达式：6 个 min/max × 4 行 = 24 乘法 + 72 加法。非 FMA 平台能看到 4× 的乘法削减；但在有 FMA 的平台上，这个优化反倒因为增加寄存器压力得不偿失——FMA 时代 96 乘加本来就是 96 个 FMA。

### 3：偏齐次变换——扔掉 z

如果 model-view 是仿射、投影矩阵是标准的透视/正交形式，那么 z 分量对平面测试完全是多余的：z 直接对 w 做近/远平面显式比较即可。这把 96 乘加降到 72 乘加（或结合 2b 到 18 乘 + 54 加）。在 SIMD 里，**row-major 储存**的实现能直接受益（Zeux 的列式储存则不行）。

## 方法 4：p/n-vertex——不检测所有顶点

这是 ryg 和「Real-Time Rendering」「Real-Time Collision Detection」都推荐的方向，和 clip-space 路线互补：clip-space 让所有平面测试变简单，p/n-vertex 则让测试的**顶点数量**减少。

核心观察：要判断 AABB 是否整体在某平面外侧，只需要问「8 个 dot(vertex_i, plane) 的**最大值**是否为负」。而 8 个顶点分别是 min/max 的三轴组合，所以最大值等于：

```
d = max(min.x·plane.x, max.x·plane.x)
  + max(min.y·plane.y, max.y·plane.y)
  + max(min.z·plane.z, max.z·plane.z)
  + plane.w
```

三个轴的贡献互相独立，**你用谁和谁配对无所谓**。把 `max` 换成 `min` 就得到「最内侧」顶点，可以同时输出 inside/outside/intersecting 三态。

### 4b：中心-半尺寸表示

把 AABB 改写成 `center = (min+max)/2`、`extent = (max-min)/2`，8 个顶点是 `center ± extent_axis`，dot 展开后用「符号放进绝对值」的技巧：

```
d = dot(center, plane) + extent.x·|plane.x| + extent.y·|plane.y| + extent.z·|plane.z|
  = dot(center, plane) + dot(extent, absPlane)
```

`absPlane` 是 plane 的分量绝对值，**对一组 box 测同一个平面时只算一次**。每个平面每个 box 只要 2 个 3D dot product + 1 个比较，合计 12 个 dot product 测 6 个平面——比 Method 3 的等价 24 个 dot product 整整少一半。

### 4c / 4d：存储格式

如果你直接用 center/extent 格式储存 AABB，4b 原样跑——12 dot product + 6 比较到底。如果仍用 min/max，可以跳过 `0.5` 的乘法：令 `center = min + max`、`extent = max - min`，整个 dot product 被乘 2，代价只是把对比基准 `plane.w` 预乘 2，**内循环一条指令都不多**。

## 方法 5：放弃「完全包含」，求极速

如果你只要 inside/outside 二态（不在乎 intersecting），还能把 2 个 dot product 合成 1 个。关键是**把符号翻转塞进 extent**：

```
signFlip = (sgn(plane.x), sgn(plane.y), sgn(plane.z))
d = dot3(center + extent * signFlip, plane)
```

SIMD 里更狠——符号就是 IEEE float 的最高位。抽出 `plane` 的符号位（`and 0x80000000`），和 extent 做 XOR：

```
vector4 signFlip = plane & 0x80000000;
return dot3(center + (extent ^ signFlip), plane) > -plane.w;
```

6 个平面一共只要：**6 个 dot product + 6 个 vector add + 6 个 xor + 6 个比较**。ryg 自己的话：「我不知道能不能更快，但这是我目前知道的最快做法」。

## SIMD 实现：SPU 上每 box ≈ 24 cycle

最优写法是**一次测 4 个 box**：存 6 个向量各 4 个 box 的分量（min.x / min.y / min.z / max.x / max.y / max.z），直接跑标量版代码的 lane-wise 展开。如果无法控制储存格式，只能一次测 1 个 box，浪费一部分 lane，但仍可以写出 46 条 SPU 指令（29 even + 17 odd）的紧凑内循环。

4 箱子并行时 ryg 粗算约 95 cycle / 4 箱 ≈ 24 cycle/box，是 Zeux 原版理论下限的一半多一点。代价是不顺带算出 clip-space 坐标——如果你还需要后续的 occlusion 剔除或屏幕空间 bbox，就要换回齐次路线。**注意 ryg 后来承认他的 cycle 对比不够公平**：他的版本直接用 world-space AABB 对 world-space 平面，Zeux 的版本则顺手生成了 world-view-projection 矩阵和 clip-space 顶点。如果你本来就需要这些中间量，齐次路线并不亏。

## 「第二篇」补充的一些工程判断

第二篇是 ryg 对 Charles Bloom 的回复，讨论「什么时候该精确、什么时候该粗糙」。几条值得记的要点：

### 先确认「便宜」到底多便宜

Charles 建议：便宜对象应该用廉价的 sphere vs. cone 粗测，甚至不测。ryg 反对 cone 近似：

- **几何上就不够紧**：对 4:3 视口，视锥的外接圆锥截面面积比外接矩形大约大 64%；16:9 下大 84%。这是非常保守的近似。
- **节省的不是整个 draw 路径**：就算对象「渲染只要 0.0001 ms」，中间仍有 job-list 排序、遮挡剔除、状态过滤、draw-call 提交——总共几千 cycle。若精确测试只比粗糙测试贵 50 cycle，粗糙测试的假阳性率**哪怕只有 5% 都能把省下的 cycle 吃光**，10% 就开始净亏损。
- **GPU cycle 比 CPU cycle 贵**：假阳性会把废物传给 GPU，而 GPU 只有一个。

结论：ryg 建议用 sphere vs. **frustum**（不要 cone），SIMD + FMA 下几次 dot product 根本不值得担心。

### 为层级设不同测试

一个几何层级里，**内节点的假阳性代价 = 多测几个叶子**，**叶节点的假阳性代价 = 提交到 GPU 浪费一次 draw**，二者权衡完全不同。所以：内节点用粗而快的 sphere-frustum，叶节点用精确的 p/n-vertex 甚至 OBB。

### 层级形状

- **binary tree 是差选择**：大 cache line、高分支预测惩罚、SIMD friendly 的代价下，fan-out 要大。
- **aim for flat**：SPU 尤其明显（随机访存极贵）。
- **cost function 驱动切分**：不用穷举，每层 5–8 个候选里挑最小的即可。

### 平面可以删

如果你有 clip-space 2D bbox（Blinn 的 *Calculating Screen Coverage* 讲得很细），它能同时服务 LOD 选择、小到像素级时的彻底丢弃、以及粗糙遮挡测试——**比远平面更有用**。删掉远平面剩 5 个面，再依几何特征删掉顶面或底面剩 4 个面，正好喂 4-way SIMD。

### 评论里 Charles 对球体的辩护

Charles 说「球体一般不比 AABB 大很多，只是看 T 形角色被放大了」：用 object-space bound + 对象自带位置时，球体**只占 1 个 float**（半径），并且**完全不需要 model-to-world 变换**就能剔除，顶层这是巨大的性能收益。ryg 同意球体在顶层和内节点层很有用，但也反驳「球体不差」的说法：角色、柱子、旗杆、树、长武器——**任何有主轴的物体**球体都很松；世界空间 AABB 一旦旋转也很快退化，所以真要精确就得 OBB。Object-space bound 可以回避这个问题，因为美术一般会把主轴和局部坐标系对齐。

## 相关

- [[culling]]
- [[occlusion-culling]]
- [[collision-detection-gjk-epa]] —— 同一族「中心沿轴 / 半径沿轴」原语构成分离轴定理和 GJK
- [[hierarchical-z-buffer]]
- [[tiled-light-culling]]
- [[sse-tricks]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-view-frustum-culling]]
- [[sources/ryg-frustum-culling-notes]]
