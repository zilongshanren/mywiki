---
tags: [source, rendering, call-of-duty, activision, game-history, forward-shading, deferred-rendering, pbr]
date: 2026-04-27
sources: 1
---

# A Retrospective on Call of Duty Rendering（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2016 年 8 月的文章，以个人视角回顾了 Call of Duty 系列在跨代过渡期间（Ghosts、Advanced Warfare、Black Ops 3）三款作品的渲染技术演进。

## 摘要

Pesce 在 Activision 任职期间亲历了 COD 多个开发周期，本文以局外人+局内人的混合视角梳理了三个研发阶段。

前世代时期，COD 系列坚持了极简的单渲染路径：单次前向渲染、每对象单个解析光源、积极的 mesh 拆分以减少批次、lightmap GI。在大量同期开发者涌向延迟渲染的背景下，这是一种被低估的"正确"选择——精力集中在把一套已知系统发挥到极致，而非跟风堆功能。

**Call of Duty: Ghosts**（2013 年，首款次世代 COD）：受制于同步支持上世代主机，Infinity Ward 选择押注几何细节而非像素计算量，主推硬件位移贴图与 Catmull-Clark 细分曲面。两项技术在 SIGGRAPH 2014 和 GDC 上单独发表，COD 也成为第一批大规模部署 CC 细分的游戏标题。Pesce 指出硬件 tessellator 的设计对细密置换贴图的适应性有根本限制，Wade Brainerd 后来也在此方向持续推进了改进提案。

**Call of Duty: Advanced Warfare**（2014 年，第一款无上世代约束的 COD）：彻底转向完整 PBR 管线——多光源前向着色、[[physically-based-shading|基于物理的着色]]、全新 lightmap 烘焙流水线，以及 Jorge Jimenez 主导的下一代后效管线。Pesce 特别强调，这款游戏的价值不在于 PBR 数学有多正确，而在于 Sledgehammer 对"感知真实性"的执念——把整个渲染链上的亮度比例、材质行为校准到可感知层面，使"对"的技术真正"看起来对"。

**Call of Duty: Black Ops 3**（2015 年）：Treyarch 的激进重构——前向渲染切换为[[deferred-rendering|延迟渲染]]，几乎所有子系统重写，包括独特的 GI 烘焙方案。核心哲学是"统一性"：粒子、体积效果、网格模型、皮肤，所有对象在同一光照系统下渲染，动静态物体无法从画面上区分。Pesce 称 Treyarch 的做法近乎"疯狂"，是他见过的在如此重要的产品周期内做出如此大规模渲染变革的极少数案例之一。

三年三款游戏，三套各不相同的渲染系统，分别由三个不同的内部工作室以完全独立的研发路线打造——这本身就是 COD 技术生态最引人注目的特征。

## 关键要点

- COD 前世代时期的"守旧"实为明智：单路径前向渲染 + lightmap GI，专注精通而非堆砌
- Ghosts 以几何复杂度换渲染计算量，是跨代主机约束下的合理权衡；硬件 tessellator 局限性此时已有体感
- Advanced Warfare 的 PBR 成功案例表明：感知校准（perceptual validation）比数学精度更关键
- BO3 的核心理念是光照统一性，消除动静物体的光照不连续，代价是几乎全盘重写渲染栈
- COD 引擎甚至没有内部名称——这本身反映了团队文化：解决问题优先于维护技术遗产

## 链接到的概念

- [[deferred-rendering]]
- [[physically-based-shading]]
- [[sources/c0de517e-activision-siggraph-2016]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/08/a-retrospective-on-call-of-duty.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-08-28_a-retrospective-on-call-of-duty-rendering.md`
