---
tags: [光线追踪, 图形api, dxr, 行业观点, bvh]
date: 2026-04-19
sources: 2
---

# Ray Tracing API 之辩（2018 DXR 提案期）

2018 年 3 月微软公布 DXR（DirectX Ray Tracing）提案时，业内并非一片欢呼。[[people/wolfgang-engel|Wolfgang Engel]] 连写两篇博客公开质疑，核心观点是：**给 ray tracing 单独立一套 API，短期解锁了硬件厂商的差异化销售，长期把 QA 成本转嫁给了游戏开发者和发行商**。

这不是反对 ray tracing 本身——而是反对「**把加速结构和 shader 绑定逻辑黑盒化**」的路线。

## 他的三条论据

### 1. 创作自由被压缩

游戏靠**视觉辨识度**区分彼此。Engel 的比喻是："只需要一个 metal 材质 pixel shader 和一个 skin 材质 pixel shader，所有 GPU 驱动只针对这两个优化"——这种荒唐的标准化提议历史上真的发生过，被开发者顶回去了。ray tracing 同样有极宽的实现谱系（BVH 结构、material sorting、ray sorting、shader divergence 处理），API 只能在最窄公约数上画框。如果黑盒化这些选择，EA / Ubisoft / R* 这样的开发商就丧失了在 ray tracing 上做差异化的工具。

> "We *might* all be able to agree on a BVH structure but there is where it ends."

### 2. 双重「驱动坏了」风险

PC 上发售新游戏本来就要先陪硬件厂商打一轮驱动官司——任何依赖硬件厂商驱动的 API 都会成为发售前夕的**经济风险点**。多加一套 RT API 就是多一个可以在发售当天把销量打下来的故障点。Engel 特别点出：小开发者在这个游戏里几乎没有议价权——大厂可以喊来 NV/AMD/INTEL 修驱动，小团队等着排队。

### 3. 成本不在首次实现，而在长期维护

中间件厂商（就是 Engel 自己的 Confetti 这类）要在生命周期里同时跟进 RT API 的版本演进、各家驱动的行为差异——这笔 QA 账很快超过初期移植成本。

## 他更偏好的替代路线

**扩展已有 API，而不是新增 API**：

- 先给 compute 管线加一个 "ray tracing feature level"，暴露 BVH traversal / intersection 原语
- 硬件厂商的专用 silicon（BVH 硬件、ray sorter）通过 extension 暴露，让愿意优化的开发者自己选
- 不愿意深挖的团队可以在此之上包一层 opt-in 的高层 API——**黑盒是可选项，而不是强制项**

评论区里 Matt Pettineo（MJP）的回复给出了补充：理想是硬件 BVH + 三角形 intersection 单独可用；同时提供一个**管理"大量 divergent shader micro-dispatch"的硬件 sorter**——这东西不仅 ray tracing 需要，GPGPU 很多场合都需要。

另一位评论者指出 Apple 的 **Metal Performance Shaders ray tracing** 走的正是 Engel 偏好的路线：暴露 intersection，交给用户自己组织 traversal。

## 后续发展（2020 年 Engel 自述）

在 *Catching Up* 那篇回顾里，他承认这场辩论「在 advisory board 上引发了讨论」，行业**最终走向更开放的接口**——虽然 DXR 本身没被推翻，但后续硬件厂商更愿意暴露底层原语，Metal 2 / MPS 的 ray tracing 接口明显更开放。他和 Kostas 合作的 hybrid shadow 移植（见 [[hybrid-raytraced-shadows-reflections]]）就是这场辩论的工程副产品：**用 compute shader 在没有 DXR 的前提下证明 hybrid RT 跨平台可行**——既是技术 demo，也是政策姿态。

## 今天回看

- **硬件 BVH 确实值得加速**——没有人反对这一点
- **API 形态之争被 compute-friendly inline ray tracing 部分化解**——D3D12 后来加了 `RayQuery`，让 ray cast 可以在普通 compute/pixel shader 里发起，部分绕开了最黑盒的 DispatchRays + shader table 结构
- **跨平台中间件仍然痛**——UE5 Lumen 这种跨硬件 hybrid RT 在 PS5 / Xbox / PC 上的实现细节差异很大，Engel 当年担心的 QA 账单确实在发生

## 相关

- [[hybrid-raytraced-shadows-reflections]] —— 没有 DXR 也能做 hybrid RT 的工程证明
- [[hybrid-raytracing-pipeline]]
- [[visibility-buffer]]
- [[the-forge-renderer]]
- [[people/wolfgang-engel]]
- [[kostas-anagnostou]]

## Sources

- [[sources/wolfgang-engel-dxr-api-debate]]
- [[sources/wolfgang-engel-ray-tracing-without-api]]
