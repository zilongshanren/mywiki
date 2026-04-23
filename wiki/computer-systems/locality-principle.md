---
tags: [计算机体系结构, 缓存]
date: 2026-04-05
sources: 1
---

# 局部性原理（Locality Principle）

程序访问模式的经验规律，**[[memory-hierarchy]] 的理论基础**。

## 两种局部性

- **时间局部性（Temporal Locality）**：最近访问的数据很可能再次被访问。
- **空间局部性（Spatial Locality）**：邻近最近访问地址的数据很可能被访问。

## 我们不依赖，我们利用

> "The memory hierarchy **takes advantage of** the principle of locality."

"利用"而不是"依赖"——我们设计系统去**从程序的局部性行为中获益**。反过来，程序员的任务是让代码具有**更好的局部性**，以便从存储层次中获益。

## 违反局部性的代价

- 随机指针 chasing（链表遍历）：每次跳都是 cache miss。
- 全局查找表不在热路径：cold path。
- AoS 布局的访问：每次取一个字段都带出一整条 cache line 的无关数据。

## 游戏开发中的应用

- **ECS/DOTS**：SoA 把同类型数据连续排列，最大化两种局部性。
- **Job System**：把处理的数据 pack 到连续的 NativeArray。
- **Texture Mipmap**：远景使用低分辨率贴图，局部性极好。
- **Spatial Data Structure**：Octree/BVH 让查询按空间接近性组织。

## 相关
- [[memory-hierarchy]]
- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[memory-latency-human-metaphor]] —— 把层次延迟翻译成人类时间尺度的教学比喻
- [[alloc-order-matches-draw-order]] —— X-Plane 的隐式对齐：构建顺序→分配顺序→遍历顺序

## Sources

- [[sources/caqa-day02]]
