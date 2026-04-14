---
tags: [profiling, engine-tools, performance, webgl]
date: 2026-04-14
sources: 1
---

# 帧内性能剖析器浮层

帧内剖析器浮层（frame profiler overlay）是一种直接叠加在运行中应用画面上的调试面板，实时展示当前一帧的耗时分解与场景统计，帮助开发者在真实运行环境下快速定位未达目标帧率的根因。PlayCanvas Profiler 是这一思路在 WebGL 引擎上的典型实现：一侧面板显示帧率、启用相机数、着色器数、材质数、三角形数等场景指标，另一侧把一帧耗时拆为 update（组件更新）、physics（物理模拟）和 render（把图形命令提交到 WebGL）三段。

与单独的 CPU 剖析工具相比，帧内浮层的优势在于即用即看：开发者不必中断运行、也不必离线分析，就能一眼看到"这一帧到底是 JavaScript 回调慢、还是物理爆炸、还是 draw call 膨胀"。这对 [[bottleneck-analysis]] 的前期判断尤其有效——先用浮层缩小到一个大类，再用更细粒度的工具深入。

PlayCanvas Profiler 还引入了**启动时间轴**维度：在浮层右侧用水平条带标出从 DOM interactive 到 preload、再到 start 的关键事件；绿色条表示异步资源加载，橙色条表示阻塞式着色器编译。对 Web 游戏而言，首帧前的资产加载和 shader 编译往往是最致命的体验瓶颈，单凭稳态帧率的数据无法看见——时间轴把启动阶段的事件纵向铺开后，"哪根条阻塞了主线程"就一目了然。这与 [[draw-call]] 主导的稳态剖析形成互补。

## Sources

- [[sources/playcanvas-profiler]]
