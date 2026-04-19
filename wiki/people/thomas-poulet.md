---
tags: [人物, 作者, 渲染, frame-analysis, unreal]
date: 2026-04-19
sources: 5
---

# Thomas Poulet

Thomas Poulet 是一名图形工程师、咨询顾问，也是独立物理游戏的开发者。他在个人博客 [blog.thomaspoulet.fr](https://blog.thomaspoulet.fr/) 上以「商业游戏帧分析」系列著称，沿用 Adrian Courrèges 开创的风格，用 RenderDoc/PIX 抓一帧、对着 shader 反汇编和 GBuffer 布局反推渲染管线——系列中已有 *The Witness*、*Ni No Kuni 2*、*Digital Combat Simulator*、*Anno 1800* 等自研引擎的解剖。

他同时经营一家面向 AAA 的图形咨询公司，并开发一款基于 UE5 的物理驱动游戏。他在博客上公开分享团队的 UE5 工程实践，特别是围绕物理调试工具链（屏幕日志 / Gameplay Debugger / Visual Logger / ImGui / 自研 Ariadne）与 Blueprint 资产验证。

他的文章偏工程视角：比起讲技术本身，更关注「这样做是为了解决什么约束」，帧分析里也常常点出不足（例如 DCS 远距离 CSM 的 10000:1 vertex-to-pixel 浪费、Anno 非 bindless 导致的 ExecuteIndirect 爆炸）。

## 相关
- [[unreal-frame-breakdown]] — Adrian 派的 UE 帧解剖（Kostas Anagnostou）
- [[simonschreibt-anno-1800-shadows]] — 同一游戏的 VFX 观察（Simon Trümpler）
- [[ue-observability-stack]]
- [[ue-asset-validator-blueprint]]
- [[adrian-courreges]] —— frame-analysis 写作范式的前辈，Poulet 的 Anno / Ni no Kuni / DCS 系列延续这条路线

## Sources

- [[sources/thomas-poulet-ninokuni-2-frame]]
- [[sources/thomas-poulet-dcs-frame]]
- [[sources/thomas-poulet-physics-tools-ue5]]
- [[sources/thomas-poulet-anno-1800-frame]]
- [[sources/thomas-poulet-blueprint-validation]]
