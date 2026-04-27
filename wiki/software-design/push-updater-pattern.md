---
tags: [software-design, performance, cache, game-engines, pattern]
date: 2026-04-27
sources: 1
---

# Push Updater 模式

Push Updater 是一种消除渲染/游戏引擎中共享数据"间接指针"的设计模式：将"读时跳转"改为"写时广播"，使访问路径变为零跳转的直接读本地副本。

## 动机

渲染循环每帧遍历数万个 draw call，每个 draw call 需要读取 material → texture handle → GPU resource 等多层指针。这些间接访问通常指向内存中的随机位置，导致大量 cache miss，占用宝贵的 CPU 带宽。

当更新（load/unload/hot-swap）远比访问频率低时，让每次读取都沿指针跳转显然是一种不必要的惩罚。

## 模式描述

引入一个 `UpdateManager`（可以是单例或按数据类型分组的管理器）：

- **注册**：每次创建一个"使用某共享数据"的对象时，把该对象存放副本的内存地址注册给 manager
- **销毁**：对象销毁时反注册
- **更新**：共享数据变化时，manager 主动把新值 **写入** 所有已注册位置（"push"），而非等待下次读取时拉取

```
UpdateManager {
    vector<T*> locations;   // 所有存放副本的地址
    void push(T new_value) {
        // 可按 location 地址排序后写入，提升写入局部性
        for (T* loc : locations) *loc = new_value;
    }
}
```

## 性质与权衡

- **访问路径**：热路径变为直接读本地 `T` 副本，零间接寻址
- **更新成本**：O(n) 写操作，n = 副本数；但更新频率远低于读取频率，整体合算
- **写入局部性**：manager 可以将 `locations` 按地址排序再写，进一步降低写入时的 miss
- **内存占用**：每个使用方存一份副本（通常是指针大小或句柄大小），代价可控
- **兼容性**：与引用计数、流式加载、热加载兼容；变化事件统一汇聚到 manager 而非散布在各处

## 隐式实例

可见性剔除的常见实现——把"可见对象指针追加到 visible list"——本质上就是在推送一条"此对象可见"的隐式消息，而非让渲染循环遍历所有对象再查询状态。这是 push 思路在另一个维度的体现。

## 对比 Pull 模式

| | Pull（传统间接指针） | Push Updater |
|---|---|---|
| 读取成本 | 多级 cache miss | 直接读本地副本 |
| 更新成本 | 仅改一处 | 写 n 份副本 |
| 适用场景 | 更新频繁、读取少 | 更新稀少、读取极频繁 |

## Sources

- [[sources/c0de517e-push-updater-pattern]]
