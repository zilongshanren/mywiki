---
tags: [人物, 作者, 路径追踪, GPU]
date: 2026-04-19
sources: 1
---

# Jacco Bikker

荷兰 NHTV / BUAS 的研究者与教学者，ompf.org 论坛昵称 *Phantom*，是把 CPU SSE 光线追踪推到游戏可用帧率的标志性人物。先后做出 **Arauna**（CPU 实时光线追踪引擎）、**Outbound**（基于 Arauna 的探索游戏原型）、以及后来的 **Brigade** 系列实时路径追踪引擎。2010 年其 Brigade 早期原型（CPU i7 + GTX260 混合，~40 Mrays/s，8 spp）被 [[sam-lapere|Sam Lapere]] 定性为"第一个在**游戏语境**下不丢人的实时路径追踪演示"，原因是它带动态全局光照，而前面所有 Quake raytraced / Larrabee / Bugatti 演示都还停留在 Whitted ray tracing（硬阴影 + 反射，光照平淡）。这条线延续到后来的 [[lighthouse-2-optix|Lighthouse 2]]。

Bikker 另一层身份是 flipcode 时代的光线追踪教程作者——老派图形程序员对他的认识往往是从那系列教程开始的。

## 相关

- [[brigade-engine]]
- [[lighthouse-2-optix]]
- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]

## Sources

- [[sources/raytracey-bikker-pathtracing-demo]]
