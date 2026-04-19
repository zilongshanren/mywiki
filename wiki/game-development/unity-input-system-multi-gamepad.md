---
tags: [unity, input-system, 游戏开发, multiplayer, ludum-dare]
date: 2026-04-19
sources: 1
---

# Unity 新旧 Input System 与多手柄配对

[[gemserk]] 在 Ludum Dare 44 开发 *Bankin' Bacon* 时，同一个项目里前后用过 Unity 两代 Input 系统，写下了一份很直白的对比笔记。

## 旧 Input System 的痛点

Legacy Input 本质上是一张全局 axis/button 表，通过 `Input.GetAxis("Player0_Fire1")` 这类**字符串键**访问。要支持 4 个玩家，就得在 `ProjectSettings/InputManager.asset` 里手工复制 N 份条目、按 joystick number 区分。团队为了效率直接用文本编辑器批量改这个 asset，而不是点 Unity 编辑器。

问题集中在两处：

1. **跨平台不一致**：同样的 Xbox 360 手柄，Mac 和 Windows 下 axis/button 编号不一样。他们的处理是给 Mac 再复制一份键名后缀 `Mac`，运行时判断 `Application.platform` 选哪一套。作者自嘲"用了你电脑爆炸不负责"。
2. **无运行时重映射**：legacy 不支持玩家自己在游戏中重绑键位，Unity 自带的 Launcher 窗口也不管手柄。

结构上，他们用 `ScriptableObject` 存"玩家 N 的键名前缀"（`UnitControllerAsset`），角色脚本只读这个 asset 并调 `Input.GetAxis`——这其实已经是"数据驱动输入"的雏形，只是底层 API 限制太多。

## 新 Input System 的事件模型

新系统用 Input Actions 配置资产 + 运行时事件回调。核心对象是 `InputAction.CallbackContext`，通过 `PlayerInput` MonoBehaviour 绑定到 UnityEvent 上。

踩到的第一个坑：**Gamepad 会持续回调、键盘只在按下/抬起时回调**。做"持续移动"时两种设备语义不一致，要么都轮询、要么在键盘一侧自己维护 held 状态。

第二个坑：**区分哪一个手柄触发了回调**需要主动干预。官方文档后来才加的 `PlayerInputManager` 当时还不稳，作者不得不手写配对逻辑：

- 创建 N 个空的 `InputUser`（无绑定设备）。
- `InputUser.listenForUnpairedDeviceActivity = N` 打开"裸设备事件监听"。
- 订阅 `InputUser.onUnpairedDeviceUsed`，只要裸手柄有按键动作，就用 `InputUser.PerformPairingWithDevice` 绑给第一个还没配对的 user。
- 订阅 `InputUser.onChange`（`DevicePaired` / `DeviceUnpaired`）维护 playerId → `Gamepad` 的数组。

配对完成后，游戏逻辑直接读 `gamepad.leftStick.ReadValue()` / `gamepad.rightShoulder.wasPressedThisFrame`，绕开 Input Actions 的事件层——作者认为对这种简单双摇杆+肩键的游戏，低层 API 反而更好用。

## 架构对接

他们抽象了 `UnitControllerBaseInput` 基类，让旧输入和新输入成为可替换实现，再用一个 `UnitNewInputSingleton`（ScriptableObject）做"玩家注册中心"：各角色 `RegisterPlayer()` 拿 id，每帧通过 id 从 singleton 取自己那把 `Gamepad`。

## 对新系统的评价

作者的结论不奉承：新系统设计方向更对（设备抽象、跨平台统一、可运行时重映射），但 2019 年时还不适合生产——API 混入了 split-screen 这类"产品级"抽象，Bug 也多；他们希望 Unity 先把低层设备访问打磨干净、再用可选包做高层封装。

这个观察和 Unity 后来几年 Input System 的演进方向基本一致：Low-level `InputSystem.Update` + `PlayerInputManager` 双层设计被保留并持续扩展。

## 相关

- [[unity-complexity-patterns]] — legacy 的字符串键也是"字符串耦合"的典型
- [[data-driven-architecture]] — ScriptableObject 存键位前缀的数据化尝试
- [[gemserk]]

## Sources

- [[sources/gemserk-new-input-system-ld44]]
