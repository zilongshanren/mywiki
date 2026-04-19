---
tags: [unreal-engine, umg, ui, lifecycle]
date: 2026-04-19
sources: 1
---

# UMG UUserWidget 生命周期：NativePreConstruct 与蓝图 PreConstruct

在 UE4 的 UMG 框架中，`UUserWidget` 同时暴露 C++ 虚函数 `NativePreConstruct` 和蓝图事件 `PreConstruct`。常见疑问是两者的触发顺序。

实际实现里 `UUserWidget::NativePreConstruct` **直接调用** `UUserWidget::PreConstruct`（也就是触发蓝图侧的 `PreConstruct`）。因此如果你在 C++ 里按"先 Super、再做自己的事"的常规写法：

```cpp
void UThing::NativePreConstruct()
{
    Super::NativePreConstruct();  // 这里就会触发蓝图 PreConstruct
    DoStuff();
}
```

蓝图 `PreConstruct` 会在 C++ 的 `DoStuff()` **之前**执行。如果你希望 C++ 先把成员变量准备好、让蓝图侧的 `PreConstruct` 看到已经初始化过的状态，就要反过来——最后调 `Super::`：

```cpp
void UThing::NativePreConstruct()
{
    DoStuff();
    Super::NativePreConstruct();  // 最后再触发蓝图 PreConstruct
}
```

这个顺序问题在 UMG 设计器预览（design-time preview）里最容易暴露：蓝图 `PreConstruct` 是少数会在编辑器里就跑起来的事件，用来在设计器里看到"参数化后的预览"。如果 C++ 先初始化、蓝图后运行，蓝图可以在预览里基于 C++ 状态做最终布局；反过来则蓝图拿不到 C++ 还没写入的字段。

## Sources

- [[sources/allar-umg-native-preconstruct-order]]
