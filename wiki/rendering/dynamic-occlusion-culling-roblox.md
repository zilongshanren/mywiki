---
tags: [渲染, 可见性, 遮挡剔除, 点云, 体素, roblox, 动态场景]
date: 2026-04-27
sources: 1
---

# 动态遮挡剔除：深度重投影与体素化方案

[[angelo-pesce]] 在 Roblox 研究动态遮挡剔除时面临的核心约束是：场景内一切对象均可通过脚本移动，无法预烘焙静态 PVS；同时不允许美术手工放置 occluder 或门洞。这篇"半成品笔记"记录了从 **实时深度重投影** 到 **世界空间体素 occluder** 两条原型路径，以及贯穿全程的"分支—剪枝—搁置"设计探索方法论。

## 两条主线

**实时路径**以某种形式的深度缓冲为核心。最直接的方案是 CryEngine 3 的 coverage buffer（Anton Kaplanyan）：把上一帧的深度降采样后点 splat 重投影到当前帧，再做 dilation 填补小孔，剩余孔洞接受假阳性误判。Pesce 尝试将这一思路扩展：从多个历史视点生成 depth heightfield，用法线检测深度不连续处并切割 quad mesh，从而得到多视点共同支撑的世界空间 occluder 数据库。对于动态物体，与其包围盒相交的视点可被批量失效或逐 texel 失效。

**体素路径**则绕过视点相关性。把深度缓冲直接反投影打点到一个稀疏二进制体素网格中，等价于压缩点云：整数化坐标后，binary voxel 与 sparse point cloud 互为等价表示。Pesce 在 compute shader 里用带 data race 但仍收敛正确的 bit-pack 直接写体素，验证了可行性。

主要遗留问题：世界空间体素的屏幕误差无上界——摄像机贴近时 occluder 间隙会放大。作者提出三个候选解法：(a) 将体素渲染为 splatted quads/椭球，(b) 屏幕空间点云降采样 + 孔洞重建，(c) 近处体素做 surface net 光追求交。"混合"策略最被看好：上一帧深度做初始重投影，体素数据库只负责填孔。

## 与其他技术的关系

- [[occlusion-culling]]、[[hierarchical-z-buffer]]：本文是对这些经典方案在"全动态无美术干预"场景下的延伸思考。
- [[gpu-based-occlusion-culling]]：Anagnostou 方案在 HZB 生成与 GPU 侧 visibility 判定上与本文思路互补，但处理的是有静态成分的场景。
- [[multidraw-indirect-occlusion-culling]]：GPU-driven 剔除的工程化路径，可作为本文"软件光栅 occluder"之后的绘制阶段参考。
- [[gaussian-splatting-web]]：splatted point/voxel 的渲染策略有共通点。
- [[efficient-sparse-voxel-octrees]]：稀疏二进制体素的数据结构背景。

## Sources

- [[sources/c0de517e-dynamic-occlusion-culling]]
