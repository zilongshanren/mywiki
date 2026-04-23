---
tags: [计算机体系结构, 缓存, dod]
date: 2026-04-05
sources: 2
---

# AoS vs SoA

两种内存布局，**直接决定 cache 利用率**。

## AoS（Array of Structures）

传统 OOP 风格：

```csharp
struct Entity { Vector3 pos; Vector3 vel; float health; ... }
Entity[] entities;
```

内存：`[pos|vel|health|...][pos|vel|health|...]...`

## SoA（Structure of Arrays）

数据导向风格（DOD / ECS）：

```csharp
Vector3[] positions;
Vector3[] velocities;
float[]   healths;
```

内存：
```
positions:  [pos|pos|pos|...]
velocities: [vel|vel|vel|...]
healths:    [h|h|h|...]
```

## 性能差异

当系统只需遍历**一个字段**时（最常见的情况），SoA 把该字段连续紧凑放置，cache line 满载。

**AoS with Vector3 + padding**：一条 64 字节 cache line 只能装 ~3 个对象，其它字段是浪费——cache 利用率 ~18.75%。
**SoA**：同一条 cache line 装满相关数据——cache 利用率接近 100%。

## Unity DOTS 的性能来源

**不是"代码更快"——是数据布局更好**。10,000 entity 场景下 SoA vs AoS 可以决定 60fps vs 25fps。

## 什么时候用哪个

- **只读少数字段、频繁遍历**：SoA（光照系统、物理系统）。
- **大部分字段一起访问**：AoS（UI、编辑器对象）。
- **混合需求**：按 access pattern 拆分成多个 struct。

## 限制

- 不是银弹：SoA 让"访问多字段"变慢。
- 游戏逻辑层若无法重构为数据并行，DOTS 学习曲线陡峭。

## 相关
- [[locality-principle]]
- [[memory-hierarchy]]
- [[amdahls-law]]
- [[ecs]]
- [[cache-friendliness]]
- [[sse-tricks]] —— SSE 性能为何依赖 SoA 而非水平指令
- [[datacomponent-single-buffer-allocation]] —— DataComponent 改造第 3 步就是 AoS → SoA，让 key 搜索只灌 key 数组

## Sources

- [[sources/caqa-day02]]
- [[sources/csapp-day01]]
