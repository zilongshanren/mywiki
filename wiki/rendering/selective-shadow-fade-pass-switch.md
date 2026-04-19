---
tags: [渲染, 阴影, unreal, 虚拟阴影贴图]
date: 2026-04-19
sources: 1
---

# 选择性阴影淡出：Shadow Pass Switch 与多阴影 pass

**问题**：跳跃 / 滑翔类游戏通常把「真实阴影」和「blob 落点指示」**同时摆在地上**时会出现**双影**。解决办法之一是让角色的阴影**单独**淡出，给 blob 指示让路——但其他角色和物体的阴影**不能**受影响。[[simon-trumpler]] 在《Infinity Nikki》里观察到的正是这种「只淡主角一人」的方案。

## 方案核心：把 shadow map 拆成多个 pass

单一 shadow map pass 里所有投射者捆在一起，想让其中一个独立淡出只能动贴图本身。Simon 的推测是 Infinity Nikki 使用了**三套独立的 shadow pass**：

1. **主 shadow map**：场景里一切物体和 NPC 的阴影，整张图不动。
2. **Nikki 专属 shadow pass**：只有主角的 caster，可以整张整张地淡入/淡出。渲染主阴影时读这张得到主角的阴影，可通过调透明度或干脆跳过而让主角阴影消失。
3. **角色自阴影 pass**：包含 Nikki 和所有 NPC，用于高质量 self-shadowing。这张**不淡出**——所以跳跃时 Nikki 的阴影仍然会落在旁边 NPC 身上，成为识别的关键线索。

官方在 Unreal 开发者访谈里印证了他们「为角色开发了专用的 high-quality self-shadowing」，进一步支持这个拆分假设。

## 在 Unreal 里的等价玩具：Shadow Pass Switch

Unreal 材质图提供一个叫 **Shadow Pass Switch** 的节点：它让同一个材质在「正常渲染」和「shadow 投射」时走不同分支。利用它配合**dither / 屏幕噪声裁切**，就能做出一个 actor 的阴影柔滑淡出：

- 正常 pass：材质完全不透明。
- Shadow pass：材质用 `dither + opacity mask`，按需要 clip 掉一部分 fragment。

低分辨率 shadow map 下这种 dither 还算隐蔽；但在 **Virtual Shadow Maps**（Nikki 类 UE5 项目正在用）下锐度极高，**dither 噪点会清晰可见**——这反而是 Simon 用来「反证」该技术在用的线索。

## 为什么不直接渐变 alpha

Shadow map 是深度贴图，不是颜色贴图——**depth 没有 "half opacity" 这回事**。任何「半阴影」都要在深度比较之外引入额外信号（alpha、stencil、多 pass），这也是「必须多一条 pass」的根本原因。相关讨论可参考 [Stephen Verderame 的 "The Case of the Disappearing Shadow"](https://stephenverderame.github.io/blog/oort-shadows/)，他用单独的 depth buffer + 混合来做同样效果。

## 边角 case：洞穴里不淡

Simon 注意到在洞窟等**室内**场景，Nikki 跳起来时真实阴影并**没有**淡出——因为那里没有太阳 blob 的意义，继续显示 shadow map 阴影反而正确。这暗示游戏里有「何时该把主角 shadow pass 设为淡出」的状态机，不是无条件生效的。洞内可能还启用了 **capsule shadows**（Unreal 的预烘焙角色阴影系统），因为锐度要求低。

## 相关

- [[shadow-mapping-basics]]
- [[blob-shadow-decal-vs-plane]]
- [[shadow-caster-culling-front-back]]
- [[cached-shadowmaps]]
- [[fizzle-lod-fading]] — 同样是「用 dither 实现平滑淡出」的兄弟思路，用在 LOD 切换上

## Sources

- [[sources/simonschreibt-nikki-shadow]]
