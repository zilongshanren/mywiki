---
tags: [unreal-engine, game-architecture, gameplay-framework]
date: 2026-04-19
sources: 1
---

# Unreal 的 GameMode / Pawn / PlayerController 三件套

Unreal 玩法层的核心分工在 2010 年的 UDK 里已经定型，到今天的 UE5 仍然是同一套：**GameMode** 写规则、**Pawn** 只是被推动的物理实体、**PlayerController** 才是真正的"大脑"。这种分离不是美学选择，而是多人联网和 AI 托管的必要前提——`PlayerController` 只存在于拥有这个玩家的客户端（和 server），`Pawn` 在全网复制，"灵魂"和"身体"可以随时解绑。

## 三层都是类继承树

[[michael-allar]] 在 UDK 教程里反复强调的一件事是：写自己的玩法类不要从 `GameInfo`（UE4/5 改名叫 `AGameModeBase` / `AGameMode`）这种基类直接继承，而应当先找到最靠近自己需求的 `Game*` 或 `UT*` 中间类再派生。UDK 里 `GameInfo → UTGame → UTDeathmatch → UTTeamGame → UTCTFGame → UTVehicleCTFGame` 这条链，功能是一层一层叠上去的：Deathmatch 只是加了计分规则，TeamGame 加的是分队逻辑，CTF 加旗子，VehicleCTF 再叠载具。任何一层都可以当做新玩法的起点，跳过越多层就意味着要重写越多 engine 期望存在的回调。

这种"按阶梯挑父类"的结构后来原封不动进了 UE4：开发者写 FPS 就从 `ACharacter`（Pawn 的 FPS 特化）而不是 `APawn` 起步，写 MOBA 可能从 `APawn` 直接来。道理完全一样。

## Pawn 是身体，PlayerController 是大脑

- **Pawn**：场景里的物理/视觉表示——玩家角色、NPC、怪物、载具。按 Allar 的原话，Pawn "被推来推去，自己没有脑子"（*pushed around and have no mind of their own*）。
- **PlayerController**：接管输入、摄像机、UI、状态同步。可以 `Possess()` 一个 Pawn 然后 `Unpossess()` 再换一个。
- **GameMode**：规则仲裁者，决定谁赢、什么时候重生、用哪个 Pawn 类、用哪个 PlayerController 类——通过 `DefaultPawnClass` / `PlayerControllerClass` 在 `defaultproperties`（UE4/5 是 C++ 构造函数或蓝图默认值）里配。

这个切法的直接收益：

1. **换载具不换角色**：玩家上车，PlayerController 解除对角色 Pawn 的 Possess，Possess 载具 Pawn；下车反过来。两个 Pawn 互不知道对方存在，PlayerController 是唯一的延续。
2. **AI 和玩家共用 Pawn**：把 `APlayerController` 换成 `AAIController` Possess 同一个 Pawn 类，同一个角色就能在玩家托管和 AI 托管之间切换（cutscene 常用）。
3. **死亡只毁身体**：Pawn 死掉被销毁，PlayerController 活着等重生，然后 Possess 一个新 Pawn。分不开就做不到这点。

## 默认属性块（defaultproperties / CDO）

UDK 的 `defaultproperties { ... }` 在 UE4/5 是 Class Default Object（CDO）+ 蓝图默认值。Allar 的教程里把它定位成"每个类自己的 config 文件"——派生类要改父类的默认行为，就在自己的 defaults 里覆写而不是去动父类本体。`bGivePhysicsGun=true`（UTGame）被 `bGivePhysicsGun=false`（UTDeathmatch）覆盖就是最小可见的例子。这种"默认值用 CDO 承载、派生类改写 CDO"的模式到 UE5 仍然是反射系统的基石，也是 [[umg-user-widget-lifecycle]] 里 `NativePreConstruct` / 蓝图 `PreConstruct` 的语义来源。

## 小结

UDK 时代的 `UTGame.UDKGame` / `UDKGame.HTPawn` / `UDKGame.HTPlayerController` 三件套，在 UE5 里只是改名叫 `AMyGameMode` / `AMyCharacter` / `AMyPlayerController`，没有任何结构性变化。理解这三者的职责边界，比任何一门具体语言（UnrealScript / C++ / Blueprint）都更接近 Unreal 的本体。

## Sources

- [[sources/allar-udk-beginning-your-game]]
