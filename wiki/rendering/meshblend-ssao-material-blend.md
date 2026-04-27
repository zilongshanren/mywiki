---
tags: [渲染, 材质混合, screen-space, ssao, deferred-rendering, kitbashing]
date: 2026-04-27
sources: 1
---

# MeshBlend 式屏幕空间材质混合（MeshBlend SSAO Material Blend）

**MeshBlend**（Tore Lervik 开发的 Unreal 插件）解决了一个 kitbashing 工作流中的常见痛点：两个独立建模的网格拼接在一起时，接触处材质硬切换，视觉上像粗糙拼贴。MeshBlend 让相交处材质**双向平滑过渡**，且不修改任何几何体。

Angelo Pesce 在未接触插件源码的情况下推导出可能的实现思路，其核心是把 SSAO（Screen Space Ambient Occlusion）的屏幕空间深度采样机制**改用于材质混合而非遮蔽计算**。

## 核心原理推断

观察到的约束：

- 效果与摄像机角度无关（不是简单的屏幕空间 decal）
- 混合双向且以相交线为中心（两侧网格各自渐出）
- 混合半径小且可配置
- 需要 Deferred Rendering
- 启动后有短暂收敛期（暗示时序积累）

排除方案：距离场（内存代价高，实时更新困难）、几何衬裙（仍有视差问题）、decal（单向，有视差）。

可行方案：类 SSAO 的屏幕空间深度采样——对当前像素在半球方向采样周围深度，当采样命中的深度与当前表面深度接近时，说明另一网格就在附近，利用此"命中率"作为**混合权重**，并从命中点获取对方的 G-buffer 材质属性进行插值。

其比 SSAO 更简单的一点：混合半径小，视差误差接近最初代 SSAO 的"角落晕圈"而非长程遮蔽，稳定性更好。

## 实现要点（推断）

- **延迟管线**：在 G-buffer 已填充后、光照前插入混合 pass，可直接读写材质参数（反照率、法线、粗糙度等）
- **时序积累**：可能将混合权重和材质混合结果分开积累，权重可降采样以节省成本
- **深度不连续拒绝**：采样时需过滤深度差过大的样本（背景穿透），与 SSAO 的深度比较逻辑类似
- **全分辨率材质**：混合权重可低分辨率，但最终材质采样需全分辨率以保留纹理细节

## 与 SSAO 的关系

SSAO 的屏幕空间采样通常用于计算半球遮蔽积分，输出一个遮蔽因子。MeshBlend 则转换了"采样命中"的语义：命中不代表遮蔽，而是代表"另一个表面在附近"，进而用于混合材质属性。这是同一基础机制的语义重用，体现了 Pesce 强调的"不自我设限，列出全部可能"的推导哲学。

## 相关

- [[rendering/hbao-interleaved-sampling]] — 类 SSAO 采样技术的具体变体
- [[rendering/ground-truth-ambient-occlusion]] — SSAO 发展脉络
- [[rendering/deferred-rendering]] — 运行此效果的必要条件
- [[rendering/environment-probe-placement]] — 同样依赖探针/采样密度的效果

## Sources

- [[sources/c0de517e-meshblend-ue]]
