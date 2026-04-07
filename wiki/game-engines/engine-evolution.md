---
tags: [游戏引擎, gea, 历史]
date: 2026-04-05
sources: 1
---

# 引擎演化史

从 **BSP Tree** 到 **Lumen/Nanite** 的技术谱系，展示**技术决定游戏设计**。

## 谱系简史

| 时代 | 代表 | 关键技术 |
|---|---|---|
| 1993-1996 | Doom / Quake | BSP Tree，首个授权引擎（Quake 1996） |
| 1996-2000 | Quake II/III | Lightmap，Portal+PVS |
| 2000-2006 | UE2/UE3 早期 | 可编程 Shader Model 2.0 |
| 2004 | UE3 Material Editor | 可视化 shader 民主化 |
| 2006-2012 | UE3 主导 | Deferred Rendering，normal mapping |
| 2012-2022 | UE4 + Unity 崛起 | 动态 GI 尝试、SSAO、LPV |
| 2022+ | UE5 | Lumen（实时 GI）、Nanite（虚拟几何） |

## 关键转折点

**Quake 1996**：id Software 授权引擎，游戏引擎作为商品诞生。

**UnrealEd**：Unreal Engine 1 的真正革命不是渲染，是关卡编辑器——**工具比运行时性能更重要**。

**Deferred Rendering（UE3, ~2008）**：突破 forward rendering 的光源数限制。

**Material Editor（UE3, 2004）**：Unity 到 2018 才追上（Shader Graph），12 年差距。

**Lumen（UE5, 2021）**：实时动态 GI = Screen Space GI（近）+ World Space SDF GI（远）。

## 技术决定设计

- **BSP Tree 的限制**：第一代 FPS 必须是室内场景。**设计师不是选择了室内美学，是技术逼的**。
- **光源数的限制**：forward rendering 下每场景 4-8 光，deferred 后 10-100+。游戏场景从"几个聚光"变成"几十个点光"。
- **Nanite 的可能性**：让几何密度不再是约束，游戏美术重新定义。

## 性能预算内的最优近似是游戏引擎的本质

每一代技术都在**精度 vs 性能**的权衡曲线上移动：
- SSAO 代替烘焙 AO
- LPV/VXGI 代替完全 GI
- Nanite 的软件光栅化代替传统 hardware rasterization

## 技术债的历史周期

> 每个架构选择都是对未来的借贷。BSP 在 1993 最优，1998 成了债。Forward rendering 2000 最优，2006 成了债。C# 降低 2005 的门槛，2018 需要 DOTS/Burst 偿还 GC/cache 债。

**作为开发者的启示**：你必须意识到借贷发生了、计划偿还时间表、理解利息。问题不是"该不该借"，而是"是否理解代价并有偿还计划"。

## 相关

- [[game-engine]]
- [[unity-vs-unreal]]
- [[rendering-pipeline]]
- [[deferred-rendering]]
- [[tactical-programming]]——技术债的心态对比

## Sources

- [[sources/gea-day02]]
