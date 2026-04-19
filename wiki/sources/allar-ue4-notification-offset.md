---
tags: [source, unreal-engine, editor, slate]
date: 2026-04-19
sources: 1
---

# How To Offset UE4 Pop-Up Notifications（Michael Allar）

[[michael-allar]] 2020 年 7 月的极短笔记。一句话总结：**UE4 编辑器右下角的 Slate 通知气泡偏移量是硬编码的，只能改引擎源码**。

## 摘要

UE4 编辑器（Slate 框架）右下角弹出的通知（"已编译 / 已保存 / ..."）的位置是由 `NotificationManager.cpp` 里 `NotificationManagerConstants::NotificationOffset` 硬编码的 `FVector2D(15.0 + 1520.0, 15.0 + 360.0)` 决定的——相对于工作区右下角的偏移。没有 CVar 开关，也没有编辑器设置页，想挪动只能改源码重编。

路径：`Engine/Source/Runtime/Slate/Private/Framework/Notifications/NotificationManager.cpp`。

## 关键要点

- 适用场景：多显示器布局下，通知弹在意外的位置；或者录屏/演示时想挪开不挡画面。
- 没有运行时 API——只能 fork 引擎。

## 链接到的概念

- [[michael-allar]]

## 原文

- 链接：https://allarsblog.com/2020/07/25/how-to-offset-ue4-pop-up-notifications/
- 本地：`raw/articles/allarsblog.com/2020-07-25_how-to-offset-ue4-pop-up-notifications.md`
