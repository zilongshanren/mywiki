---
tags: [人物, 作者, 渲染, frame-analysis]
date: 2026-04-19
sources: 3
---

# Adrian Courrèges

法国图形程序员，以"Graphics Study"系列帧分析闻名。他把 AAA 游戏（GTA V、Metal Gear Solid V、DOOM 2016、Deus Ex: HR、Supreme Commander 等）在 RenderDoc / 自制 [[sources/adrian-transparent-pixels|ReShade 分支]]下逐 pass 拆开，对 G-Buffer、SSAO、bloom、DoF 一类工业实现写成面向大众的长文，是这一"帧解剖"写作范式的奠基者之一——[[kostas-anagnostou|Kostas Anagnostou]] 的 [[unreal-frame-breakdown|UE4 帧拆解]]、[[thomas-poulet|Thomas Poulet]] 的 Anno / Ni no Kuni / DCS 分析都明言受他启发。

职业上他在 Tegra X1 时代为 Switch / NVIDIA Shield 做 [[adrian-ue4-optimized-post-effects|UE4 优化]]，将 BokehDOF → [[gather-bokeh-dof|GatherDOF]]、full-res → half-res SSAO、以及 UE4.18 前的[[ue4-reactive-dynamic-resolution|反应式 dynamic resolution]] 作为 dual-license patch 公开贡献到开源社区，《Dragon Quest XI S》《Pikmin 4》等 Switch 版都使用了这些补丁。

## 相关

- [[mgs-v-fox-engine-frame]] — Fox Engine 一帧的完整解剖
- [[gather-bokeh-dof]] — UE4 BokehDOF 的 gather 式替代
- [[ue4-reactive-dynamic-resolution]] — UE4.18 之前的反应式动态分辨率补丁
- [[srgb-premultiplied-alpha-compression]] — 他的"透明像素陷阱"一文是这套"预乘 alpha"实践的经典入门
- [[unreal-frame-breakdown]] — [[kostas-anagnostou]] 的 UE4 帧分析，明言受 Courrèges GTA V 研究启发
- [[thomas-poulet]]

## Sources

- [[sources/adrian-transparent-pixels]]
- [[sources/adrian-mgs-v-graphics-study]]
- [[sources/adrian-ue4-optimized-post-effects]]
- [[sources/adrian-deus-ex-hr-graphics]]
- [[sources/adrian-gta-v-graphics-1]]
- [[sources/adrian-doom-2016-graphics]]
- [[sources/adrian-supcom-graphics]]
- [[sources/adrian-gta-v-graphics-2]]
- [[sources/adrian-gta-v-graphics-3]]
