---
tags: [渲染, 神经渲染, 机器学习, 材质, pbr]
date: 2026-04-19
sources: 1
---

# 神经材质（Neural Materials）

**神经材质** 指把复杂 shader graph（BRDF 级联、多层纹理、测量 BTF/BSDF 数据）压缩进一个小神经网络，在实时管线里按坐标 + 视角 + 光照方向做前向推理，以取代离线渲染器里一整套 analytic 层叠着色树。和 [[neural-graphics-primitives|神经图形原语]] 思路一脉相承——**过拟合即压缩**——但材质场景下的输入空间更复杂（$\vec{\omega}_i, \vec{\omega}_o, \text{texcoord}$），输出是方向性 BRDF 值而不是单色标量。

## 为什么这条路最近被严肃对待

- 离线引擎（Weta Manuka、Pixar RenderMan、ILM Lama）里的材质可能叠上百层 BSDF，这在游戏 shader pipeline 里无法直接跑。
- NVIDIA 的专用 tensor core + cooperative matrix 指令让 per-pixel 小 MLP 推理可接受。
- 神经材质把这种复杂度「烘焙」到一个固定成本的网络里——在实时渲染器内部的 BRDF 调用处调用，仿佛在用普通 analytic BRDF。

在 [[sources/selfshadow-pbs-siggraph-2025|SIGGRAPH 2025 PBR 课程]] 上，NVIDIA 的 Andrea Weidlich 做了 *Bridging the Gap Between Offline and Real Time with Neural Materials* 主题演讲，把这条线正式纳入 PBR 主流论坛——意味着 analytical BRDF 和学习式 BRDF 的边界在持续模糊。

## 相关

- [[neural-graphics-primitives]]
- [[physically-based-shading]]
- [[openpbr]]
- [[microfacet-brdf]]

## Sources

- [[sources/selfshadow-pbs-siggraph-2025]]
