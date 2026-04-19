---
tags: [渲染, 阴影, decal, 游戏设计]
date: 2026-04-19
sources: 1
---

# Blob 阴影：贴地平面 vs 投影 decal

跳跃 / 3D 平台类游戏里，角色脚下的「落点指示圆圈」是玩家判断何时落地的关键信号。它在美术上是一块黑色圆形渐变，但在**实现上**有两条截然不同的路——它们在不平地面、水面、高度差上的表现差距非常大。[[simon-trumpler]] 在《Infinity Nikki》的阴影拆解里把这两条路摆在一起，并发现 Nikki 同时用了三块东西才把各种边角 case 都顶住。

## 路线 A：贴地平面（aligned plane）

**做法**：一块带径向渐变贴图的 quad，对齐到角色正下方的地面法线。Super Mario 64 的 blob 就是这种。

- ✅ 在**半透明表面**（水面）上也有效——plane 可以浮在水面上方，水不水它都能被栅格化。
- ❌ **不平地面**容易穿模：地是斜的而 quad 是直的，quad 边缘会插进地里，引擎检测到再对齐时会有弹跳。Mario 64 能清楚看到这一点。
- ❌ **高度差**跳跃：站在平台边缘时，plane 要么吸在平台上、要么吸在下面的地板上，**二选一**，会突然跳。

## 路线 B：投影 decal

**做法**：一块带渐变贴图的盒体，从上往下投影到 depth buffer 写入的任何表面。Yooka-Laylee 用这条路线。

- ✅ **同时**打在多个高度上——平台和地面都能看到一圈阴影。
- ✅ 地面不平也自然贴合。
- ❌ **不打在半透明表面**：水、玻璃不写 depth，decal 没地方落，blob 消失。
- ❌ 站在悬崖边时，decal 可能被**投射到垂直墙面**上，形成超长竖线阴影（Super Mario 3D World 有样本）——常规对策是**按表面法线方向 mask 掉过于斜的**，只保留朝上法线（Simon 的 [[uv-manipulation-nodes|UV 操作]] 风格 UE 教程里演示了这个 mask）。

## Yooka-Laylee 的小技巧

Yooka-Laylee 决定 blob「何时出现」不用 `距离 < threshold` 的 trace：它在角色脚下**几厘米**处恒定放着一块投影，正常情况这块投影**低于地面**所以完全看不见；角色一跳起，投影相对地面就抬起来，blob 自然浮现。巧在**没有条件判断**，这个开关是物理几何本身。

## Infinity Nikki：plane + plane + decal

Simon 的最终拼图：Nikki 同时用了**两个 plane 加一个 decal**：

1. **Decal**（投影）：担当主 blob 阴影，负责处理高度差（平台+地面同时显示）。用法线方向 mask 避免在墙上拉长。
2. **Plane A（蓝圈）**：贴地法线对齐的蓝色落点指示环——属于 UI 级别的导航辅助。
3. **Plane B（水面专用）**：一块永远浮在水面上的 plane，因为水面不写 depth，decal 打不到。这块 plane **不对齐**任何水下地面，于是会和环境几何相交（反过来印证它真的是个 plane）。

## AO decal

同一篇里 Simon 还推测地上那一圈**主角周围淡淡的 AO**也是一块 decal——站在台阶边缘时能看到它「延伸到空气里一米多」。这符合 decal 的 axis-aligned box 行为：box 把一段空间里所有 depth pixel 都算 AO，超出几何就悬空了。

## 项目时要考虑

- 目标机型是否经常在水面 / 透明物上跳？有就必须准备「水面 plane」作为 fallback。
- 项目引擎是否默认把 decal 打到 translucent 上？**Godot 在 forward renderer 里会自动**（见 Infinity Nikki 那篇的评论区讨论）。UE/Unity 默认不会。
- 是否要支持 blob 同时在多高度面可见？否 → plane 就够；是 → 必须 decal。

## 相关

- [[selective-shadow-fade-pass-switch]]
- [[shadow-mapping-basics]]
- [[normal-decal-edge-blending]]
- [[pom-decal-broken-edges]]

## Sources

- [[sources/simonschreibt-nikki-shadow]]
