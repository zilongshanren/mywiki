---
tags: [source, unity, input-system, ludum-dare, gamepad]
date: 2026-04-19
sources: 1
---

# Using the new Unity's Input System during Ludum Dare 44 Jam（Gemserk / Ariel）

[[gemserk]] 2019 年 5 月的复盘：在 Ludum Dare 44 的三天 jam 里同时用过 Unity legacy 和新 Input System，记录两套各自的坑。

## 摘要

Jam 前两天为了稳，用 legacy Input。行的通但满是痛点：InputManager 条目只能靠字符串 key 访问，支持 4 个玩家需要复制四份条目并用 joystick 编号区分；Xbox 360 手柄在 Mac 和 Windows 下按键映射不同，团队为每个平台复制一套键名、运行时判断 `Application.platform` 切换。第三天他们实验新 Input System：`InputAction` 资产 + `PlayerInput` 事件回调。实现多手柄局部多人要手写 `InputUser.listenForUnpairedDeviceActivity` + `InputUser.onUnpairedDeviceUsed` 配对逻辑；最终绕开事件层直接读 `Gamepad.leftStick.ReadValue()`。作者结论：新系统方向对但 2019 年不成熟，API 混了太多高层抽象。

## 关键要点

- legacy Input 的 InputManager.asset 可以用文本编辑器批量改，规避点编辑器的低效。
- 跨平台按键映射差异是 legacy 最大的隐形坑。
- 新 Input System 的关键辅助类：`InputUser`、`PlayerInput`、`PlayerInputManager`。
- 手写多手柄配对的核心是"裸设备事件监听" + 将第一个事件设备配给空 user。
- 对简单需求（双摇杆 + 两肩键）直接读 `Gamepad` 低层 API 反而更直观。
- `UnitControllerBaseInput` 抽象 + `UnitNewInputSingleton`（SO）让两套实现可替换。

## 链接到的概念

- [[unity-input-system-multi-gamepad]]
- [[unity-complexity-patterns]]

## 原文

- 链接：<https://blog.gemserk.com/2019/05/11/experimenting-with-new-unity-input-system/>
- 本地：`raw/articles/blog.gemserk.com/2019-05-11_using-the-new-unity-s-input-system-during-ludum-dare-44-jam.md`
