---
tags: [游戏开发, unity, 反模式, aposd]
date: 2026-04-05
sources: 2
---

# 游戏开发中的 Classitis

[[classitis]] 在游戏开发中特别流行，因为 Unity 的组件系统天然鼓励「一个 GameObject 挂一堆小组件」的组织方式，很容易滑向病态。

## 经典 Manager 癌

```
PlayerMovementManager.cs
PlayerAnimationManager.cs
PlayerInputHandler.cs
PlayerStateManager.cs
PlayerHealthManager.cs
PlayerAbilityManager.cs
PlayerAudioManager.cs
PlayerVFXManager.cs
PlayerUIManager.cs
```

十个 Manager，全挂在同一个 Player 上。每个只做「一件事」，看起来职责清晰。

**实际使用痛点**：
- 理解「玩家受伤时发生什么」要同时打开五个文件。
- 加「受伤时摄像机震动」应该改哪个 Manager——答案不明确。
- Manager 之间严重依赖，依赖关系散布在十个文件里，没有一处可以整体看清楚。

## 更深的替代

```csharp
public class PlayerController : MonoBehaviour
{
    // 公共接口：真正需要外部知道的
    public void TakeDamage(float amount, DamageInfo info);
    public void ApplyForce(Vector3 force, ForceMode mode);
    public void SetMovementEnabled(bool enabled);
    public void UseAbility(AbilityType type);

    public float CurrentHealth { get; }
    public bool IsAlive { get; }
    public PlayerState State { get; }

    public event Action<float, float> OnHealthChanged;
    public event Action<DamageInfo> OnDeath;
}
```

调用方只写：

```csharp
player.TakeDamage(50f, new DamageInfo { source = DamageSource.Enemy, hitPoint = hitPos });
```

PlayerController 内部协调所有状态变化——血量、状态机、动画、音效、特效、HUD——调用者无需知道。

## 「但 PlayerController 会很大」

可能 500 行、800 行。**但行数是假指标，认知负担才是真指标**。一个 800 行但接口简洁、逻辑内聚的 PlayerController，比十个 80 行但接口复杂、依赖分散的 Manager，更容易理解、修改、测试。

## 事件系统的隐性 Classitis

一种特别常见的变体：用事件解耦各个 Manager，降低直接依赖——但推到极致后，二三十个 Manager 各自发出若干事件、监听若干事件，整个系统变成一张巨大的事件网络图。

想知道「玩家死亡时发生什么」，需要：
1. 找到 `OnPlayerDeath` 事件的所有发出点。
2. 找到所有订阅者——可能散布在十五个文件里。
3. 理解响应的执行顺序（通常不确定）。
4. 分析竞争条件。

每个 Manager 的接口看起来简洁（「只发一个事件」），但**系统整体的接口是隐形且极度复杂的**。更危险的是：脆弱——两个模块响应同一事件且有顺序依赖时，依赖在代码里看不见。Unity 更新改变脚本执行顺序，bug 悄然出现。

## 游戏中 Classitis 的合理变体

并非所有分散都是病态：

- **框架强制的结构**：Unity 的 MonoBehaviour 生命周期约束导致有时需要把逻辑分布到不同 MonoBehaviour（`FixedUpdate` 物理、`LateUpdate` 相机）。
- **测试隔离**：为了可测试性提取浅接口，是有意识权衡。
- **真正独立可替换的系统**：音乐系统和音效系统如果真的没有状态共享，拆开合理。

关键词是**有意识**。如果你创建浅模块，应该清楚为什么、代价是什么。

## 相关

- [[classitis]]
- [[shallow-modules]]
- [[deep-modules]]
- 更广视角的资源系统问题：[[resource-system-design]]

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
