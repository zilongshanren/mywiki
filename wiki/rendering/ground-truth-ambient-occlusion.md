---
tags: [rendering, ssao, gtao, ambient-occlusion, temporal]
date: 2026-04-19
sources: 1
---

# Ground Truth Ambient Occlusion (GTAO)

GTAO 是当前最主流的屏幕空间环境光遮蔽方案，相较早期 SSAO 的经验式"crease 变暗"，它估计的是正确的可见性积分（hemisphere 上的 cosine-weighted visibility）。[[steven-wittens]] 在 [[use-gpu-reactive-runtime|Use.GPU]] 0.14 中把 GTAO 作为默认管线纳入，是一个很好的"现代 SSAO 实战"案例。

## 采样结构

每帧对每个像素在半球上取一环绿色方向（一整圈，但采样角快速旋转），通过深度缓冲在这些方向上步进找遮挡边界。除遮蔽强度外还能同时估计 bent normal（未被遮挡方向的平均向量），用于后续 IBL：ambient 光用的不是表面法线，而是"能看到天空的方向"的平均，这正是 SSAO+IBL 能把外观从"2000 年前后的 OpenGL"提到现代 look 的关键。

采样噪声的选择：Wittens 用 interleaved gradient noise (IGN) 取代 blue noise，并在 2x2 quad 内做预过滤以让斑点尽快扩散；IGN 专为 3x3 滤波设计。

## 时间累积与重投影

SSAO 昂贵，通常 half-res 后配合大量模糊隐藏噪声。GTAO 也不例外，但还需要 [[temporal-antialiasing|时间域]] 平滑：

- 用 [[motion-vectors]] 做 temporal reprojection，复用上一帧的 occlusion 与 bent normal
- 摄像机平滑移动时不清空累积
- 累积可与 blur 融合，但 bent normal 需要保持边缘锐利（否则所有边都会被圆角化），因此 Wittens 用基于 depth+normal 的 bilateral filter + 3D motion vectors，reproject 后保持 aliased

Use.GPU 的 render target "buffer history" 是一等语义——以 `history[i]` 槽位暴露 front/back buffer（甚至 n>2）并在每次渲染后自动轮转，这种抽象是 GTAO 的依赖。Wittens 断言"任何现代 GPU API 若重新设计，都应把 buffer history 视作 first-class"。

## Overscan 抑制边缘

屏幕空间 AO 在画面边缘会因为信息不足出现 shadow 突然消失的伪影。解决办法是 overscan：framebuffer 扩张固定像素数，`projectionMatrix` 同步扩张以保证 `[-1..1]` clip-space 与正常一致；边缘像素在最终 resolve 时裁掉，同时这些多出来的像素在后续帧会被 reprojection 拉回来可见区域、进一步降噪。细节：做的过程要保证管线里"显示相关的东西不依赖 projectionMatrix 的 X/Y 范围"，Use.GPU 为此得清理 2.5D 和 3D 线段/点的一些缩放 shader。Wittens 怀疑这是大多数引擎没实现 overscan 的原因。

## 最终 resolve

在累积的 half-res 样本上做 bilateral upsample，参考原始高分辨率的 normal + depth，得到全分辨率 AO。最后与 IBL 耦合时，occlusion 作为一等接口："以各种方式（分析式、SSAO、prebaked）提供都可以"，这是 Wittens 所说"模块化 vs 易用性"之间的权衡：如果一个组合只有一种合理接法，就把它 prefab 成顶层组件的 flag 而非强迫用户手装。

## 相关

- [[motion-vectors]]
- [[temporal-antialiasing]]
- [[hbao-interleaved-sampling]]
- [[render-pass-orchestration]]
- [[use-gpu-reactive-runtime]]

## Sources

- [[sources/acko-occlusion-with-bells-on]]
