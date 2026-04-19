---
tags: [source, rendering, shader-art, design, composition]
date: 2026-04-19
sources: 1
---

# Mini: Design Choices（Xor / GM Shaders Mini）

[[xor-shader-artist|Xor]] 发表于 2025-05-19 的一篇**shader art 审美自查清单**，宣告「mini 系列」复活、继续穿插长文之间。

## 摘要

Xor 把自己多年做 shader art 的经验压成 5 项维度，按重要度从前到后：**Composition**——焦点位置与构图平衡，居中 + 对称最通用，刻意失衡要「看起来故意」，有机/流动场景可用 Rule of Thirds；**Lighting**——用直方图确认明度覆盖全域，需要调整用 gamma（平方变暗变艳、开方变亮变柔），高光场景上 tonemapping；**Colors**——饱和度、色温、色相、调色板四项都要刻意选，调色板用三通道不同相位 cos（iq 的套路），screen-blend 大尺度色彩渐变能瞬间给作品「大尺度性格」；**Textures**——多尺度细节 fractal 化让作品在远近两档都耐看（借 turbulence / fractal texturing 实现）；**Motion**——最主观也最常被做过头，Xor 主张「多数 shader 作者动画偏快」，推荐多时间尺度叠加、背景慢、glitch 快，测试法是 1.5×/0.5× 两档对比。文章自称「不是规则是 guidelines」，用来在出片前逐项自查。

## 关键要点

- 和 [[creative-coding-process]]（流程）、[[programmer-art-vis-dev]]（游戏内视觉传达）互补，本文聚焦成品审美维度。
- 构图是首要维度；运动是最主观也最常被滥用的维度。
- 调色板用 cos 生成 + 相位差是 shader 圈的常识化惯用法。
- 不同类型作品（背景 / 抽象 / glitch）有不同的速度合理区间。

## 链接到的概念

- [[shader-art-design-principles]]
- [[creative-coding-process]]
- [[programmer-art-vis-dev]]
- [[turbulence-domain-warping]]
- [[fractal-texturing]]
- [[gamma-correction-srgb]]
- [[local-tonemapping]]
- [[chromatic-aberration-post]]

## 原文

- 链接：https://mini.gmshaders.com/p/design-choices
- 本地：`raw/articles/mini.gmshaders.com/2025-05-19_mini-design-choices.md`
