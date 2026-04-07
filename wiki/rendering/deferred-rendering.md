---
tags: [渲染, 延迟渲染]
date: 2026-04-05
sources: 1
---

# 延迟渲染（Deferred Rendering）

**先把几何信息写到 G-Buffer，然后做统一光照 pass**。解决 forward rendering 的光源数限制。

## Forward vs Deferred

| | Forward | Deferred |
|---|---|---|
| 光源数 | 4-8 典型 | 10-100+ |
| G-Buffer 带宽 | 无 | 高 |
| MSAA | 易 | 难 |
| 透明处理 | 易 | 必须另开 forward pass |
| 移动端友好 | 更好 | 差（带宽） |

## G-Buffer 典型布局

- RT0: Albedo + AO (RGBA8)
- RT1: Normal (RG16F 或压缩)
- RT2: Roughness + Metallic + Specular (RGBA8)
- Depth buffer 单独

## 优势

- 光源数量与几何解耦——O(N+M) 而非 O(N×M)。
- 每个光源只和**影响像素**交互（light volume / tile）。

## 劣势

- G-Buffer 带宽成本高——**移动端 killer**。
- MSAA 昂贵（每个 sample 要 resolve G-Buffer）。
- 无法处理半透明——必须加一个 forward pass。

## 在 Unreal 历史中的意义

UE3 推广 deferred rendering 成为主流。UE5 的 Lumen 在 deferred 基础上添加动态 GI。详见 [[engine-evolution]]。

## 相关

- [[rendering-pipeline]]
- [[fragment-shader]]
- [[engine-evolution]]

## Sources

- [[sources/gea-day02]]
