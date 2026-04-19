---
tags: [source, 渲染, 阴影, decal, infinity-nikki, unreal]
date: 2026-04-19
sources: 1
---

# Infinity Nikki — Shadow Breakdown（simonschreibt.de / Simon Trümpler）

[[simon-trumpler]] 于 2025 年 3 月发表的大长文：原本想写「跳跃时真实阴影淡出给 blob 让路」的短贴，最后发酵成对《Infinity Nikki》里**三套阴影系统共存**的全景拆解。全程 guesswork——所有常用 GPU profiler（RenderDoc / Nsight / GPA）都无法 attach，所以结论都靠视觉逆推，Ben Golus 与 Froyok 等人在过程中给了建议。

## 摘要

Simon 推断 Nikki 同时跑**三个 shadow map pass**：(1) 场景主阴影（所有 NPC、物件），(2) 仅 Nikki 自己、可单独淡入淡出（[[selective-shadow-fade-pass-switch]]，UE 的 Shadow Pass Switch 节点可做简化版，在虚拟阴影贴图下 dither 噪点清晰可辨），(3) 角色自阴影 high-quality pass——这解释了为什么跳起来 Nikki 自己的 shadow map 阴影消失，却还能看见它投在旁边 NPC 身上。blob 落点指示则是「decal + 贴地 plane + 水面 plane」**三件套**，分别负责高度差、蓝色指示环、以及水面这种不写 depth 的特殊表面。地上那一圈柔和 AO 看起来又是独立的 decal，能从台阶边缘「漏到空气里」一米。文章还穿插 Super Mario 64 / Super Mario Odyssey / Super Mario 3D World / Yooka-Laylee 的对比——Mario Odyssey 用**从顶向下投影的 stencil 阴影**绕开 double shadow 问题；Yooka-Laylee 选择「两种阴影都显示」并用恒定下沉的 decal 做开关。洞内 Nikki 的真实阴影不淡出，推测使用了 capsule shadow 系统。

## 关键要点

- 游戏同时用 shadow map、blob、AO decal 三类阴影各司其职
- 让单 actor 阴影淡出需要额外的 shadow pass，不能靠 alpha——depth 没有「半透明」
- Blob 方案的 plane vs decal 权衡：水面、高度差、斜面投影各有坑
- Nikki 的 blob 实质上是 decal + plane + water plane 三件套
- 官方 UE 访谈印证游戏做了 OIT、自定义粒子碰撞、自定义毛发、多层布料碰撞

## 链接到的概念

- [[selective-shadow-fade-pass-switch]]
- [[blob-shadow-decal-vs-plane]]
- [[shadow-mapping-basics]]
- [[shadow-caster-culling-front-back]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/infinity-nikki-shadow/
- 本地：`raw/articles/simonschreibt.de/2025-03-02_simonschreibt.md`
