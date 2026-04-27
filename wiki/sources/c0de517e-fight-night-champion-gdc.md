---
tags: [source, 渲染, 游戏开发, gdc, 实战案例]
date: 2026-04-27
sources: 1
---

# Fight Night Champion Rendering @ GDC（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2011 年 9 月的公告文章，宣布公开 Fight Night Champion GDC 演讲幻灯片的「导演剪辑版」。

## 摘要

本文是一篇**宣告性短文**，不含演讲幻灯片的技术正文。Pesce 在 EA 期间为 Fight Night 系列制作了至少五份演讲材料，其中面向公众的 GDC 版本由其同事 Vicky Ferguson 在他离职后代为登台。这篇博文的意义在于：Pesce 明确说明该演讲「更注重过程而非最终技术细节」——FNC 的最终着色器实现在幻灯片中并未深入展开。文中提及的具体技术成果包括 pre-blurred SSS（次表面散射预模糊）和 bent normals SSAO，这两项技术在 FNC 之后被其他团队独立发现和发表。

原始幻灯片文件为外部链接（Scribd），原始 markdown 中未嵌入幻灯片内容，因此本 source 页无法提取详细技术要点。

## 关键要点

- FNC 渲染工作的核心是**过程驱动**而非特定黑科技：大量实验 → 筛选 → 落地。
- Pre-blurred SSS 和 bent normals SSAO 是 FNC 期间验证的技术，后被他人独立重新发现并发表。
- 演讲实际由 Vicky Ferguson 登台（Pesce 已离开 EA），说明技术积累具备团队可传递性。
- 本博文本身是对「技术文档化与传播」的一次实践，符合 Pesce 一贯的开放分享风格。

## 链接到的概念

- [[rendering-pipeline]]
- [[deferred-rendering]]
- [[frequency-is-not-latency]]

## 原文

- 链接：http://c0de517e.blogspot.com/2011/09/fight-night-champion-gdc.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-09-28_fight-night-champion-rendering-gdc.md`
