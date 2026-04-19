---
tags: [source, unreal-engine, umg, ui, lifecycle]
date: 2026-04-19
sources: 1
---

# UE4 UMG UUserWidget: Which fires first, NativePreConstruct or Blueprint PreConstruct?（Michael Allar）

[[michael-allar]] 2020 年 1 月的短文，澄清 UMG `UUserWidget` 中 C++ 与蓝图初始化事件的触发顺序。一句话总结：**`NativePreConstruct` 最先跑，但它内部直接调用蓝图 `PreConstruct`，所以默认"先 Super 再做事"的写法会让蓝图 `PreConstruct` 跑在 C++ 自定义逻辑之前**。

## 摘要

表面上"NativePreConstruct 先于 Blueprint PreConstruct"是对的——但 `UUserWidget::NativePreConstruct` 的实现就是直接调用 `UUserWidget::PreConstruct`（蓝图入口）。如果在 C++ override 里按习惯先调 `Super::NativePreConstruct()` 再做 `DoStuff()`，那蓝图 `PreConstruct` 就会先于你的 `DoStuff()` 执行；反过来先 `DoStuff()` 再 `Super::` 才能让蓝图拿到 C++ 已经初始化好的状态。

## 关键要点

- 顺序默认：`Super::NativePreConstruct()` 就等同触发蓝图 `PreConstruct`。
- 如果 C++ 里想"初始化完再让蓝图做布局/样式"，就把 `Super::` 放最后。
- 这是 UMG 设计器预览和运行时都会跑的事件，影响 design-time 所见。

## 链接到的概念

- [[michael-allar]]
- [[umg-user-widget-lifecycle]]

## 原文

- 链接：https://allarsblog.com/2020/01/29/ue4-umg-uuserwidget-which-fires-first-native_preconstruct-or-blueprint-preconstruct/
- 本地：`raw/articles/allarsblog.com/2020-01-29_ue4-umg-uuserwidget-which-fires-first-nativepreconstruct-or.md`
