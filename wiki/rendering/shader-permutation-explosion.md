---
tags: [shader, pipeline, PSO, stutterstruggle]
date: 2026-04-19
sources: 1
---

# Shader 排列爆炸（Shader Permutation Explosion）

现代 AAA 引擎的 shader 数量从几百到上万不等，差异来源是 `#define` 排列、LOD 级别、feature flag、材质变体。这是 **#stutterstruggle** 在 PC 游戏里的技术根源，也是 PSO（Pipeline State Object）编译模型的核心痛点。[[emilio-lopez-ros]] 在 *Life and Death* 中把不同团队的 shader 管理哲学做了横向对比。

## 两轴维度

- **责任轴**（谁能写 shader）
  - 只限图形程序员（*DOOM 2016* 路线）→ 数百 shader；
  - 加技术美术 → 数千；
  - 全体艺术家 → 上万（典型 UE 项目）。

- **使用轴**（shader 跑在帧的哪个阶段）
  - **几何 / 材质阶段**——95% 的变体来自这里：不透明、透明、皮肤、毛发、shadow pass、depth prepass、lightmap 变体；
  - **Lighting / post 阶段**——通常 fullscreen pass，数量少变化少。

责任轴越宽、使用轴越偏几何，**组合爆炸**就越严重。

## 两阶段编译模型

PC / 移动平台的 shader 不是一次编译：

1. **开发机阶段**：HLSL / GLSL / node graph → 中间表示（DXIL / SPIR-V / GLSL）——这发生在编译服务器上，产物进版本库；
2. **用户机阶段**：中间表示 → 厂商 ISA（AMD RDNA、NVIDIA SASS）——这发生在**运行时**，是 `#stutterstruggle` 的直接原因。

当用户第一次进场景、第一次触发某个 shader 变体时，驱动才开始把它编到 ISA，那几毫秒到几十毫秒的 hitch 就是 PSO 编译代价。

## 缓解手段

1. **PSO pre-caching**——启动/装载时把常用 PSO 先编译一遍，换入内存开销减少帧中 stall；
2. **shader 合批 / ubershader**——少量大 shader + define branches，用 branch 换 permutation 数量；代价是 VGPR pressure；
3. **预编译到版本库**——[[emilio-lopez-ros]] 提到他工作过的一家公司，让艺术家保存材质时就为所有目标平台编一遍并 check-in；全员省编译时间，代价是批量改 shader 时成本巨大；
4. **艺术家管线写 HLSL 子集**——比如 UE Substrate 或 Unity Shader Graph 的 [[shader-graph-contract]]，把艺术家能碰到的接口严格定义，从源头压缩 permutation；
5. **Mesh shader / Visibility Buffer**——[[meshlets-and-mesh-shaders]] 与 [[visibility-buffer]] 让绝大多数几何用同一个 shader，material shader 只在延迟解析阶段跑。

## 与本 wiki 其他页的位置

- [[shader-combination-strategies]]——XOR 小品系列里讲的是 shader 本身的组合，侧重 toy；本页侧重工程 / 发布侧面。
- [[shader-instruction-cost]]——单 shader 内部的优化手段。
- [[shader-graph-contract]]——前提契约。
- [[draw-call]] / [[srp-batcher-cbuffer]]——渲染层面的批处理策略，与 shader permutation 是两个正交轴。

## Sources

- [[sources/elopezr-graphics-programmer-life]]
