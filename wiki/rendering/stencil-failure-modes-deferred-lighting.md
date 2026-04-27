---
tags: [渲染, stencil, 延迟渲染, 光源体积, 调试]
date: 2026-04-27
sources: 1
---

# 延迟光照 Stencil 体积的失效模式

延迟渲染的 stencil 光源体积（stencil light volume）是一个高度依赖 stencil bit 资源且对运行时条件敏感的技术。[[ben-supnik]] 在 X-Plane 10 的多次尝试中记录了两类独立失效：**bit 溢出（wrap-around）** 和**单 pass 视锥剔除死角**。

## 回顾：双面 stencil 标准算法

1. **Stencil pre-pass**：对每个光源包围体执行无颜色写入的 pass。
   - 背面：depth-fail → stencil increment（with wrap）
   - 正面：depth-fail → stencil decrement（with wrap）
2. **光照 pass**：stencil > 0 的像素才执行光照 shader。

正值意味着该像素处有几何落在包围体内侧，是潜在的受光区域。

## 失效模式一：stencil bit 溢出（wrap-around）

8-bit stencil 缓冲区理论上有 256 档，但在实际引擎中 stencil 字段往往被多个特性共用（portal、stencil outline、反射标记等），留给光照计数器的 bit 可能只剩 3 位（最多计到 7）。

当同一像素被 8 个及以上**未被遮挡的光源包围体**覆盖时，计数器达到 7 + 1 → 绕回 0，stencil test（> 0）失败，该像素**被错误地排除在所有光照之外**——屏幕上呈现为轮廓清晰的黑色空洞。

症状特征：
- 黑洞出现在光源密集、距摄像机近的区域（正是 fill rate 压力最大处）。
- 黑洞边缘锐利，与深度或法线无关，是计数器精确溢出的边界。
- 改变视角或拉大 FOV 后黑洞形状随之改变（包围体投影覆盖数量变化）。

**修复方向**：为光照计数器保留足够的 bit 数（至少 4 位 = 16 档），或对灯光数量的密度做硬限制，或先按距离分层只 stencil 近处灯光（Supnik 早期的备注方案：只 stencil 200 m 以内的灯光）。

## 失效模式二：单 pass 正面深度测试的视锥剔除死角

为了避免二次过包围体顶点的带宽代价，可以尝试退化为单 pass：只渲染**正面**，用 depth test 剔除被前景几何遮挡的光源体积。

问题在于：当**摄像机在光源体积内部**时，体积的正面全部落在摄像机后方，被背面剔除（back-face culling）或 near-clip 掉。`GL_ARB_depth_clamp` 可以处理近/远剪裁面切掉体积的情况，但**视锥体侧平面在摄像机处交叉**——摄像机后方的体积侧面直接被 frustum culling 丢弃，depth clamp 无能为力。

结果：摄像机进入体积后，屏幕覆盖突然消失，光斑硬切掉。而双面 stencil 方案的画是背面，背面即便在摄像机后也不受此问题影响。

## 两种失效的关系

这两个失效点来自同一套延迟光照系统的不同路径，可以并存：

- 双面 stencil + bit 溢出：用了「正确方案」但资源不足。
- 单 pass 替代：尝试省资源但引入新的几何可见性 bug。

两篇 Supnik 博客分别覆盖了这两个方面：[[deferred-light-volume-stencil-depth-clamp-hack]] 处理远剪裁面问题，本页关注 bit 溢出和单 pass 死角。

## 相关

- [[stencil-buffer]] — stencil 的基本操作与位掩码用法
- [[deferred-rendering]] — 延迟渲染整体架构
- [[deferred-light-volume-stencil-depth-clamp-hack]] — 远剪裁面切背面时的 depth clamp 依赖与降级路径
- [[early-z-late-z]]

## Sources

- [[sources/supnik-stencil-failure-modes]]
