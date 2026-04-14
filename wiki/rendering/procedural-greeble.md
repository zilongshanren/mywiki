---
tags: [程序化几何, mesh, extrusion, scifi]
date: 2026-04-14
sources: 1
---

# 程序化 Greeble（Procedural Greeble）

**Greeble** 是科幻模型上那种让人联想到星际毁灭者的细碎表面细节——凸起的管线、盒子、板件。它原本源自物理模型制作时代的「把零件胶水粘满船体」，在数字建模里则被抽象成一条更简单的规则：**把 mesh 的每一个面按法线方向推出一段随机长度**。只要面的划分够密，这种纯几何操作就能在渲染里提供「近看有层次」的廉价视觉丰度，代价是额外的顶点和三角形数，不需要贴图也不需要位移 map。

## 算法骨架：推广到 n 边形的 extrusion

最小实现由两个函数组成：面法线和 extrude。法线只需要在面上任选两条边取叉积并 normalize；但如果面不是共面的 polygon（Linden 的教程针对的是 Limit Theory 的 quad mesh 而不仅是三角形），取固定两条边容易偏向首索引所在的平面。更稳妥的做法是**遍历面上所有 `(v1, v1+i, v2+i)` 三角形的叉积取平均**——几何上相当于对所有可能的三角扇取加权法线，再 normalize。这套推广与 [[procedural-mesh-primitives|Limit Theory 的 procedural mesh]] 把面抽象成变长索引列表的设计是配套的。

Extrude 本体分三步：

1. 沿法线平移原 polygon 的每个顶点，得到一圈「上层」新顶点。
2. 在每对（原边，新边）之间拼一个 quad，形成侧壁。
3. 把原 polygon 的索引替换为新顶点——等价于把它沿法线整体抬起，原位置变成底部。

这套流程对三角形是 [[lindenreid-procedural-extrusion|之前那篇 extrusion 教程]] 的特例，quad 或更一般的 polygon 只是把「3」换成 `#poly`。

## 从 uniform 到有层次的 greebling

直接把 extrude 应用到所有面上、给随机 length，已经能得到 greeble 效果。但这种 uniform greebling 视觉上仍然太规律，Linden 给了两条增加变化的手法：

- **随机 gating**：`random:chance(0.33)` 决定这一面是否被推出去，未被选中的面保持原状。稀疏分布让结果更像人造面板，而不是「被压花的砖墙」。
- **顶面收缩**：在 extrude 内部为新 polygon 加一个 `scale` 参数，沿面重心把新顶点向中心 lerp，使推出的盒子顶面比底面小一圈。侧壁因此变成斜面，整体轮廓从「方块」变成「梯形台」，更像管道法兰和螺栓座。

两种修饰都是纯随机、纯局部的——不需要全局知识、不需要额外的拓扑信息，就能把「均匀 extrude」升级成「差异化细节」。这是程序化 [[mesh-warps-and-tessellation|mesh warp]] 的典型设计哲学：先有最朴素的变换骨架，再用几个按面采样的随机分布层叠出丰度。

## 边界与注意

- 输入 mesh 必须是 [[manifold-mesh|manifold]]——否则侧壁无法与邻面对齐，会出现 [[cel-shader-outline|outline shader]] 那样的顶点割裂。
- 算法是一次性写入的（不是 skeletal 动画），greeble 后的 mesh 需要重新算法线和 UV。
- 随机源如果不 seed，每次运行会得到不同结果；要做可复现的美术版本就得固定 seed 或把结果缓存进资产。

## 相关

- [[lindenreid-procedural-extrusion]] —— 三角形版的 extrusion 基础
- [[mesh-warps-and-tessellation]] —— 面级变形与细分的合集
- [[procedural-mesh-primitives]] —— Limit Theory 的 mesh 抽象
- [[unity-procedural-mesh]]

## Sources

- [[sources/lindenreid-procedural-greeble]]
