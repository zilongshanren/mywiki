---
tags: [source, 渲染, frame-analysis, ni-no-kuni, NPR, 2018]
date: 2026-04-19
sources: 1
---

# Ni No Kuni 2: Frame Analysis（Thomas Poulet / 2018）

[[thomas-poulet]] 写于 2018 年 11 月的 PC DX11 帧分析。标的是 Level-5 自研引擎上的 **《二之国 2：幽灵国度》**室内场景——正是这款游戏标志性的「吉卜力风」Cel-shading + 线稿渲染最密集的地方。

## 摘要

NnK2 用 **light pre-pass** 风格的管线：先做 depth + normal prepass（D24S8、没用 reversed-Z），然后跑一个 compute light map 算屏幕 irradiance，再进入 color pass 做 forward shading。整帧围绕**四张 MRT** 展开，其中两张 MRT 专门为角色的 line art 管线搬运「艺术家编码」的信号（material ID、folding、朝向、distance），经过 edge detect + 8× multisample + LUT 上色后叠回主图。光照主要靠 ambient + 窗户投射，没有 GI、没有动态点光源阴影。post 阶段走 SMAA（包含 temporal 扩展）+ motion blur + DOF + heavy bloom（三级 downsample 模糊）。UI 用多字母表 packed 贴图贴全语言文字。整体体现自研引擎**为风格定制**的取舍：pipeline 结构简单，但每个 pass 都把「这个视觉特征是不是核心」放在优先级最高位。

## 关键要点

- **管线定位**：light pre-pass（Engel 2009），不是 forward+ 也不是 full deferred；[[light-prepass-pipeline]] 单列一页。
- **CSM**：两张 4K 32-bit depth，内景三个阶段 pass（远近 + 角色分别画）。
- **Line art 管线**：艺术家驱动，MRT 承载信号；[[ninokuni-2-line-art]] 单列一页。
- **Light map on compute**：开一个并行通道填满 GPU，顺带跟 light scattering pass 重叠。
- **Light scattering**：室内 god ray，在 240×135 低分下算，用 R11G11B10 复用 depth 在 green 通道做上采样引导。
- **SMAA + motion map**：AA 留给 post（扩展 SMAA 带时序重投影），motion map 在 color pass 里顺手写了。
- **宽 bloom**：三级 downsample blur 叠加，给游戏一种宽松的光辉感；结合 light scattering 是视觉名片。
- **UI**：多字母表 packed atlas（拉丁 + 希腊 + 西里尔 + 日文 + 中文 + 符号），全用 4 通道。

## 链接到的概念

- [[thomas-poulet]]
- [[light-prepass-pipeline]]
- [[ninokuni-2-line-art]]
- [[cel-shader-outline]] / [[cel-shading-pipeline]]
- [[deferred-rendering]] / [[tiled-light-prepass]]
- [[msaa-ssaa]] / [[temporal-antialiasing]]
- [[motion-vectors]]
- [[bloom-threshold-blur-composite]]
- [[shadow-mapping-basics]]

## 原文

- 链接：<https://blog.thomaspoulet.fr/posts/ni-no-kuni-2-frame-analysis/>
- 本地：`raw/articles/blog.thomaspoulet.fr/2018-11-07_ni-no-kuni-2-frame-analysis-thomas-poulet.md`
