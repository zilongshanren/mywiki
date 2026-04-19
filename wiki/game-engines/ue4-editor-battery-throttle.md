---
tags: [unreal-engine, editor, power-management]
date: 2026-04-19
sources: 1
---

# UE4 编辑器在电池模式下的 60 FPS 硬限制

UE4 编辑器（截至 4.24.1）内置了一个"看起来像跑在电池上就限到 60 FPS"的 tick 节流，用来防止笔记本在编辑器里待机时耗电过快。这个限制**只作用于编辑器**，打包后的 standalone runtime 没有这层节流。

判断是否"跑在电池上"走的是 OS 平台 API（Windows 上是 `GetSystemPowerStatus` 类调用）。它并不总是准确：一个典型误报场景是台式机接了 UPS，但 UPS 固件把自己上报成系统内置电池，于是整台机器被当成笔电处理，编辑器被钳在 60 FPS。

绕过办法是把 console variable `r.DontLimitOnBattery` 设成非零值：

```
r.DontLimitOnBattery 1
```

源码里的硬编码位置在 `Engine/Source/Editor/UnrealEd/Private/EditorEngine.cpp`：

```cpp
static const auto CVarDontLimitOnBattery = IConsoleManager::Get()
    .FindTConsoleVariableDataInt(TEXT("r.DontLimitOnBattery"));
const bool bLimitOnBattery = (FPlatformMisc::IsRunningOnBattery()
    && CVarDontLimitOnBattery->GetValueOnGameThread() == 0);
if (bLimitOnBattery)
{
    MaxTickRate = 60.0f;  // 想改成 30 就只能改这里
}
```

如果想限到 30 FPS 而不是彻底关掉，CVar 本身不支持，只能改源码；或者保留 60 限制之外再套一层 `t.maxFPS 30`。

## Sources

- [[sources/allar-ue4-editor-battery-60fps]]
