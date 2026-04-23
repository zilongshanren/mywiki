---
tags: [渲染, 反走样]
date: 2026-04-05
sources: 1
---

# SSAA vs MSAA

两种基于超采样的反走样方法。

## SSAA（Super-Sampling Anti-Aliasing）

**全程多倍采样**：
- 以 N× 分辨率渲染（每个像素跑 N 次 fragment shader）
- 最终 downsample 到目标分辨率

优点：**最高质量**——shading、coverage、texture 全都多次采样。
缺点：**昂贵**——fragment shader 成本 ×N。

## MSAA（Multi-Sample Anti-Aliasing）

**只对 coverage 多次采样**：
- 每像素 N 个 coverage 采样点
- Fragment shader 只执行**一次**（在像素中心）
- 根据 coverage 比例混合颜色

优点：显著便宜——shader 成本不 ×N，只有 coverage 和 depth 测试 ×N。
缺点：**不处理 shader 内部走样**（例如 alpha test、高对比贴图）。

## 何时选哪个

| 情况 | 推荐 |
|---|---|
| 桌面高端，画质优先 | SSAA 或 8×MSAA |
| TBDR 移动端 | MSAA（近免费） |
| Deferred Rendering | 都不适合（G-Buffer 难 resolve）→ TAA/FXAA |
| Alpha Test 密集（草、树叶） | Alpha-to-Coverage + MSAA |

## 相关
- [[aliasing]]
- [[rasterization]]
- [[tbdr-vs-imr]]
- [[temporal-antialiasing]] —— 现代 AAA 的事实标准 AA，MSAA 在延迟渲染下被它取代
- [[analytical-antialiasing]] —— 对已知 SDF 形状的「反向做法」：shader 内按距离淡出一像素
- [[aa-techniques-survey-2011]] —— Supnik 2011 把 SSAA/MSAA/CSAA 放进五档 AA 分类的上下文

## Sources

- [[sources/rtr-day04]]
