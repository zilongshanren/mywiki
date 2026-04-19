---
tags: [游戏开发, unity, aposd]
date: 2026-04-05
sources: 3
---

# Unity 中的复杂性模式

APoSD 的概念在 Unity 游戏开发中的典型体现与对策。

## 游戏项目的复杂性特征

游戏开发是观察「复杂性如何演化」的绝佳场所：

1. **需求变化极快**：策划的设计反复迭代，代码需要面对大量变更。[[change-amplification]] 的代价特别高昂。
2. **跨学科协作**：程序员、策划、美术共同操作代码库（Unity 里策划经常直接操作 ScriptableObject 和 Prefab）。[[cognitive-load]] 必须在不同背景的人之间共享。
3. **实时系统的隐式顺序**：每一帧都有更新顺序、渲染顺序、物理顺序，这些顺序之间存在大量隐式依赖。[[unknown-unknowns]] 特别危险。

## 典型腐化时间线

**第 1 个月**：`BattleManager` 简洁，代码一百来行。依赖清晰。

**第 4 个月**：策划加 Buff/Debuff 系统。时间紧，Buff 效果直接写进各模块——移速 Buff 进 PlayerController，攻击 Buff 进伤害计算，防御 Buff 进受击逻辑。每个地方只加几行。

**第 8 个月**：二十几种 Buff 散布在七个文件里。没人知道全貌。策划说「减速持续时间从 3 秒改 2 秒」——需要全局搜索，因为这个数值被硬编码了三处。

**第 12 个月**：`BattleManager` 有两千行。依赖 UI、被 UI 依赖、被物理系统读、给存档系统序列化。任何改动都可能引入想不到的 bug。

没有一个时刻系统「坏掉」——它就是渐渐地从清晰腐化到无人敢动。

## 常见 Unity 反模式

### Singleton 泛滥

每一个 Singleton 都是 [[cognitive-load]] 的发射源。大型 Unity 项目充满各种 Singleton，每个都在制造 [[unknown-unknowns]] 的土壤。

### Magic Number 散布

```csharp
if (damage > 50) { ... }
enemy.health -= 50;
if (player.level == 5) { unlockAbility("damage_boost"); }
```

策划说「基础伤害从 50 改成 60」——开始全局搜索。典型 [[change-amplification]]。

### GameObject.Find 链

用字符串在场景图里查找对象，是 [[obscurity]] 的经典形态：依赖以字符串形式隐藏，重命名或移动对象就坏。

### Event Bus 网络

看 [[classitis-in-games]] 中对事件系统滥用的详细分析。

## 正面做法

- **深的 PlayerController**：见 [[classitis-in-games]]。
- **RAII 资源管理**：见 [[resource-system-design]]。
- **ECS 的数据化思维**：见 [[ecs]]。
- **高层渲染接口**：见 [[rendering-api-depth]]。

## 相关
- [[complexity]]
- [[classitis-in-games]]
- [[resource-system-design]]
- [[ecs]]
- [[rendering-api-depth]]
- [[unity-input-system-multi-gamepad]] — legacy Input 的字符串键耦合与多平台差异是"字符串散布"复杂性的又一实例

## Sources

- [[sources/aposd-day01]]
- [[sources/aposd-day02]]
- [[sources/aposd-day03]]
