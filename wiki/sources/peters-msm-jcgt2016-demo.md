---
tags: [source, 渲染, 阴影, 矩, demo, HLSL]
date: 2026-04-14
sources: 1
---

# New Shadow Demo with Documented HLSL Code（Peters，2016-09-25）

[[christoph-peters]] 2016 年 9 月发布的 [[moment-shadow-mapping|MSM]] 演示程序新版（MSMDemoV2），附带带 doxygen 文档的 HLSL 着色器源码。这一发布对应即将投到 *Journal of Computer Graphics Techniques (JCGT)* 的论文扩展版（即 [[sources/peters-improved-msm-jcgt2017|2017 JCGT 论文]]），把过去一年里对 MSM 与其变体的所有「微小但有用的改进」一次性打包。

## 摘要

demo 覆盖四类应用：filtered hard shadows、translucent occluders、soft shadows 与 single scattering，每一类都能在 UI 上切换十几种不同的技术做并排对比。新版本相对前两个 demo 的核心改动是「全部都更快或更稳，但接口不变」，作者建议无条件迁移。

技术要点列表：

1. **Signed depth**：把深度映射到 \([-1, 1]\)（而非 \([0, 1]\)），128-bit 配置下显著降低漏光，64-bit 也使罕见 artifact 更稀有。
2. **稀疏量化变换矩阵**：得益于 signed depth，原来用于减小舍入误差的 4×4 量化矩阵现在可以让一半元素为 0，cost 减半。
3. **最坏情形 bias**：原始 bias 优化平均情形，clamped 深度时偶有破图；新 bias 优化最坏情形，同 cost 下更稳。
4. **Translucent occluders 也支持 EVSM**：纯粹做对照用，并非推荐配置。
5. **Soft shadow 的 blocker search 不再用 biased depth**——加 bias 在这一步是有害的。
6. **自适应 depth bias**：soft shadow 的 bias 现在与 filter 大小成正比，更高效地减少 surface acne。
7. **Single scattering 的自适应过/欠估计插值**：插值因子现在依光照-视角夹角自适应，减少漏光而不损失近似精度。
8. **改进的六矩 shadow mapping**：用 [[cubic-equation-solver-hlsl|新的 cubic solver]] 把六矩 single scattering 做得更快更稳；上面 1–3 的改进同样适用于六矩版本。
9. **Prefix sum 的优化 compute shader**：transmittance-weighted prefix sum 的生成接近带宽极限；resampling 改为单独 pixel shader pass 反而更快。
10. **杂项**：sRGB 全流程、overdarkening 用于减少漏光、trigonometric MSM 仍然太慢、按需生成 mipmap。

## 关键要点

- **不引入新方法，但落地改进**：每一项都是「同 cost 下更稳或更快」的工程精细化。
- **demo 是论文的「可执行附录」**：UI 直接对比 MSM、VSM、ESM、CSM、EVSM、Trigonometric MSM。
- **Doxygen + RenderDoc 友好**：2016-09-29 的更新明确支持 `enable_shader_debugging = 1`、命名 pass，方便外部团队 profile 与移植。
- **2017 JCGT 论文 = 这个 demo 的正式版本**：博客贴出代码，论文给详细解释。
- 同期博客 [[sources/peters-cubic-equation-revisited|"How to solve a cubic equation, revisited"]] 是这次更新的数学子例程之一。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[cubic-equation-solver-hlsl]]
- [[christoph-peters]]
- [[shadow-mapping-basics]]

## 原文

- 链接：<http://momentsingraphics.de/JCGT2016Demo.html>
- 本地：`raw/articles/momentsingraphics.de/2016-09-25_new-shadow-demo-with-documented-hlsl-code.md`
