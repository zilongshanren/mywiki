---
tags: [source, unreal-engine, udk, unrealscript, gameplay-framework]
date: 2026-04-19
sources: 2
---

# Beginning Your Game Part 1 & 2（Michael Allar / Allar's Blog，2010）

[[michael-allar]] 2010 年 1 月发的 UDK 入门教程两联篇，教读者怎么从空壳 UDK 安装开始，写出一个能跑起自己 GameMode 的最小工程。本条目把 Part 1 和 Part 2 合并成一个 source 摘要，因为它们原本就是"一节课的上下两段"。

## 摘要

Part 1 做两件事：一是在 `DevelopmentSrc/<你的包名>/Classes/` 里创建一个继承自 `UTGame` 的 GameInfo 子类（`class UDKGame extends UTGame;`），二是改 `DefaultEngine.ini` 的 `ModEditPackages=` 让引擎加载这个脚本包、改 `DefaultGame.ini` 的 `DefaultGame=` 把它设为默认 GameMode，再靠 `ExampleMap` 里有没有"物理枪"来验证 GameMode 确实生效了。Part 2 把这个空壳 GameMode 填实：派生 `UTPlayerController` 和 `UTPawn` 得到 `HTPlayerController` / `HTPawn`，然后在 GameMode 的 `defaultproperties` 里用 `DefaultPawnClass=class'UDKGame.HTPawn'` 和 `PlayerControllerClass=class'UDKGame.HTPlayerController'` 把这两个空壳挂上去，顺带用 `DefaultMapPrefixes(0)=(Prefix="HT",GameType="UDKGame.UDKGame")` 和 `Acronym="HT"` 让带 `HT-` 前缀的地图自动挂载这个 GameMode。

教程本身 2010 年写、针对 UDK，具体的 `.ini` 路径、`;ModEditPackages` 注释、`UTDeathmatch` 继承链全都已经过时；但它把 Unreal 玩法层的**结构骨架**——GameMode 负责规则、Pawn 是身体、PlayerController 是大脑，三者都用类派生 + `defaultproperties` 默认值覆写来配置——讲得很清楚。这套骨架从 UDK 一路活到了 UE5。

## 关键要点

- **派生父类要挑最近的**：`GameInfo → UTGame → UTDeathmatch → UTTeamGame → UTCTFGame → UTVehicleCTFGame`，越下面的类已经叠好的功能越多，直接从顶层派生等于自己把 HUD、输入、死亡判定都重写一遍。
- **ini 三层覆盖**：`Base*.ini`（Epic 的引擎默认）→ `Default*.ini`（你自己发布时打包的默认）→ `UT*.ini`（终端用户改出来的配置）。所有自己的改动都只写 `Default*.ini`，`UT*.ini` 是生成的可随时删。
- **`defaultproperties` 是类级默认值容器**：派生类用它覆写父类的默认值（如 `bGivePhysicsGun=false` 覆盖 UTGame 的 true），这就是 UE4/5 CDO 与蓝图默认值机制的前身。
- **GameMode 引用类用 fully-qualified 名**：`class'PackageName.ClassName'`（如 `class'UDKGame.HTPawn'`），不是实例；这保证"所有玩家都用 HTPawn"而不是"大家共用一个 HTPawn 实例"。
- **Pawn / PlayerController 必须拆开**：Pawn 是物理表现、PlayerController 是输入 + 控制逻辑；换载具、AI 接管、重生都依赖这一拆分。这是 [[unreal-pawn-playercontroller-pattern]] 的核心。
- **地图前缀路由 GameMode**：`DefaultMapPrefixes` 数组按前缀（DM / CTF / VCTF / HT）把地图映射到 GameMode 类；UDK 里靠它决定 `DM-Deck` 起 Deathmatch、`CTF-Face` 起 Capture The Flag。UE4/5 的 World Settings `GameModeOverride` 是它的直系后代。

## 为什么其他三篇 M16 教程被跳

同一批还有三篇 *Adding an M16* 教程：Part 1（Modeling）和 Part 2.5（Dummy Rigging）都只是视频入口页，文字版就两行"slug 测试模型"；Part 2（Geometry Rigging）有正文，但全是 3DS Max + ActorX 导出 `.PSK` 的纯操作步骤，2010 UDK 时代限定，早被 FBX / UE5 Skeletal Editor 替代，抽不出泛化洞察，一并跳过。

## 链接到的概念

- [[unreal-pawn-playercontroller-pattern]]
- [[michael-allar]]

## 原文

- Part 1：<https://allarsblog.com/2010/01/15/beginning-your-game-part-1/>
- Part 2：<https://allarsblog.com/2010/01/15/beginning-your-game-part-2/>
- 本地：
  - `raw/articles/allarsblog.com/2010-01-15_beginning-your-game-part-1.md`
  - `raw/articles/allarsblog.com/2010-01-15_beginning-your-game-part-2.md`
