---
tags: [source, rendering, 图像质量, 游戏分析, 渲染哲学]
date: 2026-04-27
sources: 1
---

# Why the Rendering in The Order: 1886 Rocks（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2015 年 2 月的游戏渲染评析，以「渲染从业者正常游玩视角」而非逐帧拆包视角分析《教团：1886》（Ready at Dawn，PS4 独占）的图像质量。

## 摘要

文章的核心论点不在于具体技术的列举，而在于一种渲染哲学：**质量来自对每一处细节的自律，而非功能清单的累积**。作者逐一分析四个维度：图像稳定性（4× MSAA 加上全流程反锯齿协作，消除 specular shimmer）、遮挡（specular light leaking 是最难隐藏的问题，该游戏对此格外警惕）、大气效果（伦敦大雾作为第一视觉主体，每盏灯都参与散射，无可见 voxel 边界或粒子瑕疵）、材质细节（PBR 材质从不"全开"到极端，纹理密度均匀，无突兀的光泽金属堆砌）。额外讨论了 baking 的重要性——不应以 realtime 替换 baked 解法来解决 authoring 问题——以及 Forward+ 引擎在聚焦平台时的优势。

## 关键要点

- "如果一项渲染技术让人能看出来是什么技术，那它已经出问题了"——分离性（separable blur 痕迹）是反质量信号
- screen-space 效果（SSAO、SSR）的缺席反而是图像质量的证明：这些技术现有实现都带有tell-tale artifacts
- specular 遮挡漏光比 diffuse 遮挡漏光难隐藏，因为高光强度太高，SSAO 等无方向性方法难以压制
- bent normals（仅存储弯曲法线，不存双份）是一种低成本的遮挡近似，优先级高
- 大气散射作为场景气氛"角色"而非特效处理，是该游戏视觉区别于同期作品的关键
- Forward+（Tile-based forward lighting）与 PS4 专属优化的组合，比"升级几个单项技术"效果更明显

## 链接到的概念

- [[image-quality-philosophy]]
- [[forward-plus-rendering]]
- [[atmospheric-perspective]]
- [[physically-based-shading]]
- [[deferred-rendering]]

## 原文

- 链接：https://c0de517e.blogspot.com/2015/02/why-rendering-in-order-1886-rocks.html
- 本地：`raw/articles/c0de517e.blogspot.com/2015-02-27_why-the-rendering-in-the-order-1886-rocks.md`
