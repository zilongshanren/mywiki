---
tags: [source, rendering, grass, gpu-driven, indirect-draw, vulkan]
date: 2026-04-14
sources: 1
---

# Grass Shader（Marco Giordano / A programmer's cave）

[[marco-giordano]] 发表于 2020 年 9 月的文章，记录他在自研 Vulkan/DX12 引擎里实现"GPU 驱动、瓦片化、带 LOD 的实时草地"的完整思路与踩坑。

## 摘要

文章按"先有想法、再有实现、再做剔除、再上 LOD"的时间顺序写成，而不是教程结构。作者的关键决定是用**预烘焙的蓝噪声瓦片**做草位分布：每瓦片 10k 点、100 瓦片，离线跑 3 小时一次，之后运行期直接 load。蓝噪声的妙处是"任意前缀仍是好分布"，于是 LOD 就退化成"选前 K 个点"，既不用重采样也不会闪烁。草几何在 vertex shader 里扩展（没有 geometry / tessellation shader），基础着色参考 Roystan 的 Unity 教程，风的湿鞭效来自 Freek Hoekstra 提议的"按 UV.y 偏移采样 distortion map"技巧——叶尖动得更晚更大。剔除在 compute shader 里完成：vote → scan compact，然后跑 draw indirect；主相机 / 活动相机分离方便 debug flythrough。LOD 计算和剔除合进同一个 pass，用 4 路 scan 把 4 档 LOD 的瓦片压进同一个数组再填 4 个 indirect buffer。一个关键陷阱是 draw indirect buffer 的 barrier 要用专门的 indirect transition，否则 GPU 会读到未完成的 dispatch 结果。收益是 VPC 阶段由彻底崩溃变成 3× 提速。作者感谢 [[alan-zucconi|Alan Wolfe]] 的蓝噪声支持、[[kostas-anagnostou|Kostas Anagnostou]] 的 GPU culling 参考。未来计划是 mesh shader 版本，以及低 LOD 时只绘制叶尖。

## 关键要点

- 蓝噪声预烘焙：100 瓦片 × 10k 点，离线一次，运行期做 LOD 时取前 K 个点即可保持分布
- Vertex shader expansion 做几何生成，不用 geometry / tessellation shader
- 风：按 UV.y 偏移 distortion map 采样 → 叶尖先动叶根后动的鞭子效果（Freek Hoekstra 提议）
- GPU culling：compute shader 做 vote + scan compact，主相机/活动相机分离便于 debug
- LOD：距离分桶成 4 档，4 路 scan 压缩后填 4 个 indirect draw buffer
- 陷阱：draw indirect buffer 必须用专门的 indirect transition barrier，不是普通 write-read
- Intel iGPU 上疑似编译器 bug 导致 culling 失效
- 优化收益：从 VPC 爆死到整体 shader 快 3×
- 未来方向：mesh shader 一 pass 搞定所有、低 LOD 只绘制叶尖
- 作者坦承 MSAA 未做，"谁不喜欢一片闪烁的锯齿呢"

## 链接到的概念

- [[gpu-driven-grass-tiles]]
- [[deferred-grass-shader]] —— 同题但走 tessellation + geometry shader + 延迟 alpha cutout 的对比方案
- [[culling]] / [[occlusion-culling]]
- [[draw-procedural-gpu]]
- [[alan-zucconi]]
- [[kostas-anagnostou]]
- [[marco-giordano]]

## 原文

- 链接：https://giordi91.github.io/post/grass/
- 相关：MPC R&D Unity GPU Culling（作者早期博客）
- 本地：`raw/articles/giordi91.github.io/2020-09-25_grass-shader.md`
