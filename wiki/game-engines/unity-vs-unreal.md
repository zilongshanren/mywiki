---
tags: [游戏引擎, gea, unity, unreal]
date: 2026-04-05
sources: 2
---

# Unity vs Unreal

两种引擎设计哲学的代表性对立。

## 设计哲学

**Unity**：引擎作为**工具**（tool）。GameObject + Component 最大灵活性。
- 轻量，学习曲线平缓。
- C# managed runtime，快速迭代。
- **移动端主导**。
- 代价：`GetComponent()` 成本、AoS cache 局部性差。

**Unreal**：引擎作为**框架**（framework）。内建系统，Actor + Component + 生命周期 + 反射。
- 完整特性（网络、序列化、生命周期、动画系统）。
- C++ 性能 + 深度反射。
- **AAA 主导**。
- 代价：编译时间长、学习曲线陡、运行时灵活性稍差。

## 移动端 vs AAA 现实

| 场景 | Unity | Unreal |
|---|---|---|
| 中小团队手游 | 压倒性优先 | 不推荐 |
| 高品质 PC/主机 | 可以 | 压倒性优先 |
| 独立游戏 | 常选 | 渐增 |
| 原型快速验证 | 强 | 弱 |

## Unity 的移动端优势是系统性的

- URP SRP Batcher
- 自动 GPU Instancing
- TBDR 定向优化
- Shader Stripper
- 成熟构建管线
- 生态（Firebase、AppLovin 等优先 Unity）

## Unreal 的 AAA 优势

- 可见性进化：Lumen、Nanite
- Material Editor（2004 民主化 shader）—— Unity 到 2018（Shader Graph）才有，**12 年差距**。
- 长期的 AAA 项目案例
- 工具集成度高

## DOTS 的回应

Unity DOTS 试图用 ECS + Burst 恢复性能，逼近 Unreal 的底层效率——但学习曲线因此变陡。Trade-off 没有消失，只是转移。

## 相关

- [[game-engine]]
- [[engine-evolution]]
- [[data-driven-architecture]]
- [[ecs]]
- [[aos-vs-soa]]

## Sources

- [[sources/gea-day01]]
- [[sources/gea-day02]]
