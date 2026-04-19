---
tags: [source, unreal-engine, editor, power-management]
date: 2026-04-19
sources: 1
---

# UE4 Editor limited to 60 FPS when not plugged into power（Michael Allar）

[[michael-allar]] 2020 年 1 月的排障记录。一句话总结：**UE4 编辑器会在"看起来跑在电池上"时把自己钳到 60 FPS，UPS 被误报成电池会触发误限速，用 `r.DontLimitOnBattery 1` 关掉**。

## 摘要

UE4 4.24.1 的编辑器内置了电池节流：只要 `FPlatformMisc::IsRunningOnBattery()` 返回 true 就把 `MaxTickRate` 钳到 60。这只对编辑器生效，打包后的 standalone runtime 不受影响。误报场景集中在：笔电（正常）、以及用 UPS 的台式机——某些 UPS 固件把自己报成系统内置电池，导致编辑器被当成笔电处理。解决办法是设置 CVar `r.DontLimitOnBattery 1`。想要"在电池上但限到 30 FPS"这种中间状态，CVar 不支持，只能改 `EditorEngine.cpp` 第 2001 行附近的硬编码，或者在外面再套 `t.maxFPS 30`。

## 关键要点

- 限速点：`Engine/Source/Editor/UnrealEd/Private/EditorEngine.cpp`，用 `r.DontLimitOnBattery` 开关。
- 判断"在电池上"依赖 OS 平台 API，UPS 误报是最常见的坑。
- 打包运行时不受这层限制——不要在打包游戏里找这个问题。

## 链接到的概念

- [[michael-allar]]
- [[ue4-editor-battery-throttle]]

## 原文

- 链接：https://allarsblog.com/2020/01/12/ue4-framerate-limited-60fps-when-on-battery/
- 本地：`raw/articles/allarsblog.com/2020-01-12_ue4-editor-limited-to-60-fps-when-not-plugged-into-power-on.md`
