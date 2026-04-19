---
tags: [source, 渲染, 后处理, 景深, bokeh, the-forge]
date: 2026-04-19
sources: 1
---

# Bokeh Depth Of Field Project（Erfan Ahmadi / The Forge）

[[people/erfan-ahmadi|Erfan Ahmadi]] 2018 年的个人项目报告——花一个月学复杂 postfx 管线，在 [[the-forge-renderer|The Forge]] 渲染框架上实现了三种主流 Bokeh DoF，作为 UnitTest。目标平台覆盖 PC、Android、macOS、iOS、iPad。代码开源。文章是"项目预告 + 技术简述"，详细 deep-dive 作者当时说稍后补写。

## 摘要

把三条 Gather/Scatter-as-Gather 思路并排实现在同一框架里，便于直接比较：

1. **Circular Separable DOF**（Kleber Garcia, Frostbite）—— 复数卷积推导出的可分离圆盘滤波；1/2 分辨率、near/far 分开、多 pass。出货作品包括 FIFA 17、Mass Effect Andromeda、Anthem、NFS Heat。
2. **Practical Gather-based Bokeh DoF**（GPU Zen 一章）—— 48 样本的圆盘采样，不可分离；1/2 分辨率、分 near/far、多 pass。
3. **Single-pass DoF**（Dennis Gustafsson / tuxedo labs）—— 全分辨率一次 pass 完成，采样和带宽都更高，作者自承因为强行 single-pass 性能最差。

作者承诺未来写一篇深度对比，这篇主要是技术清单 + 截图 + 开源 repo 指针。另外他在这项目里"对 scatter-as-gather 的思维方式"大大提升了——对于 DOF 这种每个输出像素都要"向邻居要颜色"的问题，scatter-as-gather 是主要建模方式。

## 关键要点

- 三种 gather 路线都在 1/2 分辨率 + near/far split 上做，唯一例外是 Gustafsson 的 single-pass
- Circular Separable 和 Practical Gather-based 性能接近，是生产级推荐
- Single-pass 是教学友好的对照组，性能最差
- Garcia 论文刻意略过"near/far 合成"细节，作者自己补实现
- Scatter-as-Gather 思维：不搬精灵，而是让输出像素遍历自己应该读的邻居
- 项目指针：<https://github.com/Erfan-Ahmadi/BokehDepthOfField>

## 链接到的概念

- [[circular-separable-dof]]
- [[gather-bokeh-dof]]
- [[scatter-bokeh-dof]]
- [[the-forge-renderer]]
- [[thin-lens-model]]
- [[separable-gaussian-blur]]
- [[people/erfan-ahmadi]]
- [[people/wolfgang-engel]]

## 原文

- 链接：<https://erfan-ahmadi.github.io/blog/Bokeh>
- 本地：`raw/articles/erfan-ahmadi.github.io/2018-05-04_bokeh-depth-of-field-project.md`
